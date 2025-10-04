// main.js

import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';

// 1. Escena
const scene = new THREE.Scene();

const clock = new THREE.Clock();

// --- CÁMARAS ---
// 1. Cámara en Perspectiva 
const perspectiveCamera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
perspectiveCamera.position.z = 4.5;
perspectiveCamera.position.y = 0.5;
perspectiveCamera.position.x = -2;
const initialCameraPosition = perspectiveCamera.position.clone();

// 2. Cámara Ortográfica
// 2. Nueva Cámara Ortográfica
const aspect = window.innerWidth / window.innerHeight;
const frustumSize = 25; // Controla el "zoom" de la cámara ortográfica
const orthographicCamera = new THREE.OrthographicCamera(
    frustumSize * aspect / -2, // left
    frustumSize * aspect / 2,  // right
    frustumSize / 2,           // top
    frustumSize / -2,          // bottom
    0.1,                       // near
    1000                       // far
);
orthographicCamera.position.set(20, 20, 20); // Posición para una vista isométrica
orthographicCamera.lookAt(0, 0, 0); // La cámara siempre mira al centro

// 3. Variable para saber qué cámara está activa
let activeCamera = perspectiveCamera;

// 3. Renderizador
const renderer = new THREE.WebGLRenderer();
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(window.devicePixelRatio); 
document.body.appendChild(renderer.domElement);

// Controles de órbita (para mover la cámara con el mouse)
const controls = new OrbitControls(perspectiveCamera, renderer.domElement);

// Lógica

// TEXTURAS

const textureLoader = new THREE.TextureLoader();


// Textura procedural

// main.js

/**
 * Crea una textura procedural de bandas.
 * @param {string} direction - 'vertical' u 'horizontal'.
 * @param {string[]} colors - Un array con los colores de las bandas.
 * @param {number} size - El tamaño en píxeles de la textura (ej. 256).
 * @returns {THREE.CanvasTexture} La textura lista para usar.
 */
function createStripeTexture(direction = 'vertical', colors = ['#ffffff', '#000000'], size = 256) {
    const canvas = document.createElement('canvas');
    canvas.width = size;
    canvas.height = size;
    const context = canvas.getContext('2d');
    const stripeCount = colors.length;
    const stripeSize = size / stripeCount;

    for (let i = 0; i < stripeCount; i++) {
        context.fillStyle = colors[i];
        if (direction === 'vertical') {
            context.fillRect(i * stripeSize, 0, stripeSize, size);
        } else { // horizontal
            context.fillRect(0, i * stripeSize, size, stripeSize);
        }
    }
    const texture = new THREE.CanvasTexture(canvas);
    return texture;
}

/**
 * Crea una textura procedural de damero usando Canvas.
 * @param {number} cells - El número de celdas por lado (ej. 8 para 8x8).
 * @param {string} color1 - El primer color del damero.
 * @param {string} color2 - El segundo color del damero.
 * @param {number} size - El tamaño en píxeles de la textura (ej. 512 para 512x512).
 * @returns {THREE.CanvasTexture} La textura lista para usar.
 */
function createCheckerboardTexture(cells = 8, color1 = '#757575', color2 = '#545454', size = 512) {
    const canvas = document.createElement('canvas');
    canvas.width = size;
    canvas.height = size;
    const context = canvas.getContext('2d');
    const cellSize = size / cells;

    for (let i = 0; i < cells; i++) {
        for (let j = 0; j < cells; j++) {
            context.fillStyle = (i + j) % 2 === 0 ? color1 : color2;
            context.fillRect(i * cellSize, j * cellSize, cellSize, cellSize);
        }
    }
    const texture = new THREE.CanvasTexture(canvas);
    // Hacemos que la textura se repita
    texture.wrapS = THREE.RepeatWrapping;
    texture.wrapT = THREE.RepeatWrapping;
    return texture;
}

// Textura de la cabaña
const woodColorTexture = textureLoader.load('/textures/dark_planks_2k/textures/dark_planks_diff_2k.jpg');
// const woodRoughnessTexture = textureLoader.load('/textures/dark_planks_rough_2k.jpg');
// const woodNormalTexture = textureLoader.load('/textures/dark_planks_nor_gl_2k.jpg');

const cabinWoodMaterial = new THREE.MeshStandardMaterial({
    //color: 0xff0000, // Rojo brillante para que sea muy obvio si funciona
    map: woodColorTexture,
    metalness: 0.0, // Asegúrate de que no sea metálico para que el color sea claro
    roughness: 1.0  // Asegúrate de que sea totalmente rugoso para que el color no se distorsione
});

// Carga previa de las dos texturas de cielo
const daySkyTexture = textureLoader.load('/textures/sky.jpg');
const sunsetSkyTexture = textureLoader.load('/textures/sunset.jpg');

// --- SKYDOME (CIELO ENVOLVENTE) ---

// 1. Carga la textura panorámica del cielo
const skyMaterial = new THREE.MeshBasicMaterial({
    map: daySkyTexture, // Empezamos con el cielo de día
    side: THREE.BackSide
});
// 2. Crea la geometría (una esfera gigante)
// El radio debe ser lo suficientemente grande para que nunca te choques con él
const skyGeometry = new THREE.SphereGeometry(500, 60, 40); 

// 4. Crea la malla del Skydome y añádela a la escena
const skyDome = new THREE.Mesh(skyGeometry, skyMaterial);
scene.add(skyDome);

// --- SUELO CON TEXTURA PROCEDURAL ---

// 1. Llama a la función para generar la textura
const floorTexture = createCheckerboardTexture(10, '#4a5d23', '#3a4a13'); // Tonos de verde bosque
floorTexture.repeat.set(20, 20); // Repite el patrón 20x20 veces a lo largo del plano

// 2. Crea el material usando la textura
const floorMaterial = new THREE.MeshStandardMaterial({
    map: floorTexture,
    roughness: 0.8,
    metalness: 0.2,
});

// 3. Crea la geometría del suelo (un plano)
const floorGeometry = new THREE.PlaneGeometry(100, 100); // Un plano grande de 100x100 unidades

// 4. Crea la malla del suelo y aplícale el material
const floor = new THREE.Mesh(floorGeometry, floorMaterial);
floor.rotation.x = -Math.PI / 2; // Rótalo para que quede plano en el suelo
floor.position.y = -3; // Ponlo ligeramente por debajo del nivel 0
floor.receiveShadow = true; // Haz que el suelo reciba sombras
scene.add(floor);

// --- OBJETO CON SEGUNDA TEXTURA PROCEDURAL ---

// 1. Define los colores para las bandas (¡usa los de tu paleta de color!)
const stripeColors = ['#4a5d23', '#C5C6C7', '#1e2a3a']; 

// 2. Llama a la función para generar la textura
const stripeTexture = createStripeTexture('vertical', stripeColors, 256);

// 3. Crea el material usando la nueva textura
const proceduralStripeMaterial = new THREE.MeshStandardMaterial({
    map: stripeTexture,
    roughness: 0.4,
    metalness: 0.7, // Hazlo un poco metálico para que refleje la luz
});

// 4. Crea un objeto para mostrar el material (un cilindro como un tótem)
const totemGeometry = new THREE.CylinderGeometry(0.5, 0.5, 4, 30); // Radio sup, radio inf, altura, segmentos
const proceduralTotem = new THREE.Mesh(totemGeometry, proceduralStripeMaterial);

// 5. Colócalo en algún lugar visible de tu escena
proceduralTotem.position.set(0, 0, -5); 
proceduralTotem.castShadow = true;
scene.add(proceduralTotem);

//Nature loop
const loader = new GLTFLoader();

loader.load(
    '/glb_models/Nature.glb', 
    (gltf) => {
        const organicModel = gltf.scene;
        // --- Ajustes de escala, posición y rotación ---
        organicModel.scale.set(2, 2, 2); 
        organicModel.position.set(0, -0.5, 2.5); 
        scene.add(organicModel); 
    },
    undefined, 
    (error) => {
        console.error('An error happened', error);
    }
);

//Campfire loop

loader.load(
    '/glb_models/Camp fire.glb',
    (gltf) => {
        const utilitarianModel = gltf.scene;
        // --- Ajustes de escala, posición y rotación ---
        utilitarianModel.scale.set(0.002, 0.002, 0.002); // Hazlo más pequeño
        utilitarianModel.position.set(100, -0.6, 10); // Muévelo a la izquierda
        scene.add(utilitarianModel); // ¡Importante! Añádelo a la escena
    },
    undefined, // Función de progreso (opcional)
    (error) => {
        console.error('An error happened', error);
    }
);

//Cabin loop
loader.load(
    '/glb_models/Log cabin.glb', // Ruta al modelo en la carpeta 'public'
    (gltf) => {
        const architecturalModel = gltf.scene;
      //   architecturalModel.traverse((child) => {
      //   // Si el hijo es una malla (un objeto visible con geometría y material)
      //   if (child.isMesh) {
      //       child.material = cabinWoodMaterial; 
      //   }
      // });
        // --- Ajustes de escala, posición y rotación ---
        architecturalModel.scale.set(0.08, 0.08, 0.08); // Hazlo más pequeño
        architecturalModel.position.set(-0.5, -0.5, 2.2); // Muévelo a la izquierda
        architecturalModel.rotation.y = 7;  
        scene.add(architecturalModel); // ¡Importante! Añádelo a la escena
    },
    undefined, // Función de progreso (opcional)
    (error) => {
        console.error('An error happened', error);
    }
);

loader.load(
    '/glb_models/Camp fire.glb', // Ruta al modelo en la carpeta 'public'
    (gltf) => {
        const organicModel = gltf.scene;
        // --- Ajustes de escala, posición y rotación ---
        organicModel.scale.set(0.002, 0.002, 0.002); // Hazlo más pequeño
        organicModel.position.set(0, -0.6, 3.5); // Muévelo a la izquierda
        scene.add(organicModel); // ¡Importante! Añádelo a la escena
    },
    undefined, // Función de progreso (opcional)
    (error) => {
        console.error('An error happened', error);
    }
);

// ILUMINACION
// 1. Luz Ambiental 
const ambientLight = new THREE.AmbientLight(0x404040, 5); // Un gris suave, con poca intensidad
scene.add(ambientLight);

// 2. Key Light (Sol)
const keyLight = new THREE.DirectionalLight(0xe8ebb7, 3); // Luz blanca, muy intensa
keyLight.position.set(10, 15, 10); // Viene desde arriba, a la derecha y adelante
keyLight.castShadow = true; 
scene.add(keyLight);

// 3. Fill Light (Luz de Relleno)
const fillLight = new THREE.DirectionalLight(0xadd8e6, 0.01); // Luz azulada y suave
fillLight.position.set(-10, 5, 10); // Viene desde la izquierda, más abajo que la Key Light
scene.add(fillLight);

// 4. Rim Light (Luz de Contorno)
const rimLight = new THREE.DirectionalLight(0xffffff, 2.0); // Luz blanca para el borde
rimLight.position.set(0, 10, -15); // Viene desde atrás de la escena
scene.add(rimLight);

// Activa las sombras en el renderizador
renderer.shadowMap.enabled = true;

// Define la resolución de las sombras para la Key Light
keyLight.shadow.mapSize.width = 2048;
keyLight.shadow.mapSize.height = 2048;

// --- PRESETS DE ILUMINACIÓN ---

function setDayPreset() {
    keyLight.color.setHex(0xedcf58); // Sol amarillo
    keyLight.intensity = 3.5;
    fillLight.color.setHex(0x71dece); // Relleno azul claro
    fillLight.intensity = 0.7;
    ambientLight.intensity = 0.5;
    skyMaterial.map = daySkyTexture;
    console.log("Preset de Día activado.");
}

function setSunsetPreset() {
    keyLight.color.setHex(0xde9937); // Sol naranja
    keyLight.intensity = 4.0;
    fillLight.color.setHex(0x4682b4); // Relleno azul acero
    fillLight.intensity = 0.6;
    ambientLight.intensity = 0.2;
    skyMaterial.map = sunsetSkyTexture;
    console.log("Preset de Atardecer activado.");
}

window.addEventListener('keydown', (event) => {
    if (event.key === '1') {
        setDayPreset();
    }
    if (event.key === '2') {
        setSunsetPreset();
    }
});

// --- BUCLE DE ANIMACIÓN ---
function animate() {
    const elapsedTime = clock.getElapsedTime();
    requestAnimationFrame(animate);

    if (proceduralTotem) { // Verificamos que el modelo ya haya cargado
    proceduralTotem.rotation.y = elapsedTime * 0.3; // Rota usando el tiempo
    }

    keyLight.position.x = Math.sin(elapsedTime * 0.4) * 15;
    keyLight.position.z = Math.cos(elapsedTime * 0.4) * 15;

    // --- NUEVA ANIMACIÓN DE CÁMARA SUTIL ---
    const subtleRadius = 2.0; // Qué tan amplio será el círculo. ¡Ajusta este valor!
    const subtleSpeed = 0.2;  // Qué tan rápido se moverá. ¡Ajusta este valor!

    if (activeCamera === perspectiveCamera) {
        // Calculamos un pequeño desplazamiento circular
        const cameraOffsetX = Math.cos(elapsedTime * subtleSpeed) * subtleRadius;
        const cameraOffsetZ = Math.sin(elapsedTime * subtleSpeed) * subtleRadius;

        // Lo sumamos a la posición inicial
        perspectiveCamera.position.x = initialCameraPosition.x + cameraOffsetX;
        perspectiveCamera.position.z = initialCameraPosition.z + cameraOffsetZ;
        
        // Mantenemos la altura constante (o puedes animarla también si quieres)
        // perspectiveCamera.position.y = initialCameraPosition.y;

        // Aseguramos que siempre mire al mismo punto
        perspectiveCamera.lookAt(0, 2, 0); 
    }

    //controls.update(); // Actualiza los controles de la cámara
    renderer.render(scene, activeCamera);
}

// --- MANEJO DEL CAMBIO DE TAMAÑO DE LA VENTANA ---
window.addEventListener('resize', () => {
    activeCamera.aspect = window.innerWidth / window.innerHeight;
    activeCamera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
});

// --- EVENT LISTENER PARA CAMBIAR DE CÁMARA ---
window.addEventListener('keydown', (event) => {
    if (event.key.toLowerCase() === 'c') {
        if (activeCamera === perspectiveCamera) {
            activeCamera = orthographicCamera;
            console.log("Cámara cambiada a: Ortográfica");
        } else {
            activeCamera = perspectiveCamera;
            console.log("Cámara cambiada a: Perspectiva");
        }
        // ¡Crucial! Actualiza los controles para que apunten a la nueva cámara activa
        controls.object = activeCamera;
    }
});

// Iniciar la animación
animate();