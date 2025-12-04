import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

// --- 1. CONFIGURACIÓN BÁSICA (ESCENA, CÁMARA, RENDER) ---
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x202020); // Fondo gris oscuro

// Cámara
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
camera.position.set(0, 5, 10); // Posición inicial

// Renderizador
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.shadowMap.enabled = true; // Activar sombras
document.body.appendChild(renderer.domElement);

// Controles (OrbitControls)
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true; // Suavizado al mover


// --- 2. ILUMINACIÓN (Dos luces requeridas) ---
// Luz Ambiental (ilumina todo suavemente)
const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
scene.add(ambientLight);

// Luz Direccional (como el sol, genera sombras)
const dirLight = new THREE.DirectionalLight(0xffffff, 1);
dirLight.position.set(5, 10, 7);
dirLight.castShadow = true;
scene.add(dirLight);


// --- 3. TEXTURAS ---
const textureLoader = new THREE.TextureLoader();

// CARGA TUS TEXTURAS AQUÍ
// Asegúrate de que los nombres coincidan con los archivos en la carpeta 'textures'
const textureFloor = textureLoader.load('./textures/piso.jpg'); 
const textureObject = textureLoader.load('./textures/caja.jpg');


// --- 4. OBJETOS (Formas Geométricas) ---

// A. El Piso
const planeGeometry = new THREE.PlaneGeometry(20, 20);
const planeMaterial = new THREE.MeshStandardMaterial({ 
    map: textureFloor, 
    side: THREE.DoubleSide 
});
const plane = new THREE.Mesh(planeGeometry, planeMaterial);
plane.rotation.x = -Math.PI / 2; // Acostar el plano
plane.receiveShadow = true;
scene.add(plane);

// B. Cubo (Con textura)
const cubeGeo = new THREE.BoxGeometry(2, 2, 2);
const cubeMat = new THREE.MeshStandardMaterial({ map: textureObject });
const cube = new THREE.Mesh(cubeGeo, cubeMat);
cube.position.set(-3, 1, 0);
cube.castShadow = true;
scene.add(cube);

// C. Esfera (Color solido + Brillante)
const sphereGeo = new THREE.SphereGeometry(1.5, 32, 32);
const sphereMat = new THREE.MeshStandardMaterial({ color: 0xff5733, roughness: 0.1, metalness: 0.5 });
const sphere = new THREE.Mesh(sphereGeo, sphereMat);
sphere.position.set(3, 1.5, 0);
sphere.castShadow = true;
scene.add(sphere);

// D. Torus (Dona - Objeto decorativo extra)
const torusGeo = new THREE.TorusGeometry(1, 0.4, 16, 100);
const torusMat = new THREE.MeshStandardMaterial({ color: 0x3388ff });
const torus = new THREE.Mesh(torusGeo, torusMat);
torus.position.set(0, 2, -4);
torus.castShadow = true;
scene.add(torus);


// --- 5. LOGICA DE CAMBIO DE CÁMARA (Perspectivas) ---
let isDefaultView = true;
const btnCamera = document.getElementById('btn-camera');

btnCamera.addEventListener('click', () => {
    if (isDefaultView) {
        // Vista 2: Desde arriba (Top View)
        camera.position.set(0, 15, 0);
        camera.lookAt(0, 0, 0);
    } else {
        // Vista 1: Original (Perspectiva frontal)
        camera.position.set(0, 5, 10);
        camera.lookAt(0, 0, 0);
    }
    isDefaultView = !isDefaultView;
    controls.update(); // Importante actualizar controles tras cambiar cámara manual
});


// --- 6. ANIMACIÓN (Loop de Renderizado) ---
function animate() {
    requestAnimationFrame(animate);

    // Animación de formas
    // 1. Rotar el cubo
    cube.rotation.x += 0.01;
    cube.rotation.y += 0.01;

    // 2. Hacer rebotar la esfera (usando Math.sin y el tiempo)
    const time = Date.now() * 0.002;
    sphere.position.y = 1.5 + Math.sin(time) * 0.5;

    // 3. Rotar el torus
    torus.rotation.y -= 0.02;

    controls.update(); // Necesario para el 'damping'
    renderer.render(scene, camera);
}

// Manejo de redimensionamiento de ventana
window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
});

animate();