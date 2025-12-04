import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader';
import Stats from 'stats.js';
import GUI from 'lil-gui'; 

// --------------------------------------------------------
// 1. CONFIGURACIÓN DE ESCENA
// --------------------------------------------------------
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x111111);
scene.fog = new THREE.Fog(0x111111, 10, 60);

const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
camera.position.set(0, 3, 10); // <--- CORRECCIÓN: Cámara un poco más alta y lejos

const renderer = new THREE.WebGLRenderer({ antialias: true, powerPreference: "high-performance" });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
document.body.appendChild(renderer.domElement);

// --------------------------------------------------------
// 2. ILUMINACIÓN
// --------------------------------------------------------
const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
scene.add(ambientLight);

const dirLight = new THREE.DirectionalLight(0xffffff, 2);
dirLight.position.set(5, 10, 7);
dirLight.castShadow = true;
scene.add(dirLight);

const gridHelper = new THREE.GridHelper(100, 100, 0x00ff00, 0x222222);
scene.add(gridHelper);

const planeGeometry = new THREE.PlaneGeometry(100, 100);
const planeMaterial = new THREE.MeshStandardMaterial({ color: 0x222222, roughness: 0.8 });
const plane = new THREE.Mesh(planeGeometry, planeMaterial);
plane.rotation.x = -Math.PI / 2;
plane.receiveShadow = true;
scene.add(plane);

// --------------------------------------------------------
// 3. LOGICA LOD (OPTIMIZACIÓN VISUAL) - FINAL
// --------------------------------------------------------
const loader = new GLTFLoader();
const lod = new THREE.LOD();

// <--- CORRECCIÓN 1: POSICIÓN
// Subimos el modelo en el eje Y (el segundo número).
// Si sigue enterrado, sube 2 a 3 o 4.
lod.position.set(0, 3, 0); 
scene.add(lod);



// <--- CORRECCIÓN 2: ESCALA
// Bajamos de 5 a 1.5 (Ajusta esto si lo quieres más grande/pequeño)
const ESCALA_GLOBAL = 3; 

// A. Cargar Alta Calidad (High Poly)
loader.load('/models/modelo_high.gltf', (gltf) => {
    const model = gltf.scene;
    
    model.scale.set(ESCALA_GLOBAL, ESCALA_GLOBAL, ESCALA_GLOBAL);
    
    model.traverse((child) => {
        if (child.isMesh) {
            child.castShadow = true;
            child.receiveShadow = true;
        }
    });

    // Nivel 0: Visible de 0 a 20 metros
    lod.addLevel(model, 0);
    console.log("High Poly cargado");
}, undefined, (err) => console.error("Error High:", err));

// B. Cargar Baja Calidad (Low Poly)
loader.load('/models/modelo_low.glb', (gltf) => {
    const model = gltf.scene;

    model.scale.set(ESCALA_GLOBAL, ESCALA_GLOBAL, ESCALA_GLOBAL);

    // <--- CORRECCIÓN 3: QUITAMOS EL MODO DEBUG (ROJO)
    // Ahora el modelo se verá con sus colores originales, pero "cuadrado"
    model.traverse((child) => {
        if (child.isMesh) {
            child.castShadow = true;
            // Opcional: Activar receiveShadow también en low poly
            child.receiveShadow = true; 
        }
    });

    // Nivel 20: Visible a más de 20 metros
    lod.addLevel(model, 20);
    console.log("Low Poly cargado (Normal)");
}, undefined, (err) => console.error("Error Low:", err));

// --------------------------------------------------------
// 4. SIMULACIÓN DE SUBSISTEMAS
// --------------------------------------------------------
const simulacion = {
    estado: 'Esperando...',
    gesto: 'Ninguno',
    activarGestoHola: () => {
        simulacion.gesto = 'Mano Abierta';
        simulacion.estado = 'Saludando';
        
        // <--- CORRECCIÓN 4: ANIMACIÓN RELATIVA A LA ESCALA
        if(lod) {
            // Hacemos que crezca un 50% más de su tamaño base
            const escalaSalto = ESCALA_GLOBAL * 1.5;
            lod.scale.set(escalaSalto, escalaSalto, escalaSalto);
            
            // Al volver, regresamos a ESCALA_GLOBAL (no a 1)
            setTimeout(() => lod.scale.set(1, 1, 1), 500); 
        }
    },
    activarDeteccionPeligro: () => {
        simulacion.estado = 'PELIGRO DETECTADO';
        scene.background = new THREE.Color(0x550000); 
        setTimeout(() => scene.background = new THREE.Color(0x111111), 1000);
    },
    modoNoche: false
};

const gui = new GUI({ title: 'Simulador de Inputs' });
gui.add(simulacion, 'estado').listen().disable();
gui.add(simulacion, 'activarGestoHola').name('Simular Gesto: Hola');
gui.add(simulacion, 'activarDeteccionPeligro').name('Simular: Detección');
gui.add(simulacion, 'modoNoche').name('Voz: Modo Noche').onChange((value) => {
    if(value) {
        dirLight.intensity = 0.1;
        ambientLight.intensity = 0.1;
    } else {
        dirLight.intensity = 2;
        ambientLight.intensity = 0.5;
    }
});

// --------------------------------------------------------
// 5. MÉTRICAS Y LOOP
// --------------------------------------------------------
const stats = new Stats();
document.body.appendChild(stats.dom);

const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;

function animate() {
    requestAnimationFrame(animate);
    stats.begin();

    controls.update();
    lod.update(camera); 
    
    // Rotación suave
    lod.rotation.y += 0.005;

    renderer.render(scene, camera);
    stats.end();
}
animate();

window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
});