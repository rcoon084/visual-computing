// App.jsx
import React, { useState, Suspense } from 'react';
import { Canvas } from '@react-three/fiber';
import { PerspectiveCamera, OrthographicCamera, OrbitControls, Grid } from '@react-three/drei';
import './App.css'; // ¡No olvides importar los estilos!

/**
 * Componente que contiene los objetos 3D de nuestra escena.
 * Es buena práctica separarlo para mantener el código limpio.
 */
function SceneContent() {
  return (
    <>
      {/* 1. LUCES: Sin ellas, todo sería negro. */}
      <ambientLight intensity={0.5} />
      <directionalLight position={[10, 10, 5]} intensity={1.5} />

      {/* 2. OBJETOS: Colocados a distintas profundidades (eje Z). */}
      {/* Cubo en el origen */}
      <mesh position={[0, 1, 0]}>
        <boxGeometry args={[2, 2, 2]} />
        <meshStandardMaterial color="#8e44ad" />
      </mesh>

      {/* Esfera más alejada */}
      <mesh position={[0, 1, -6]}>
        <sphereGeometry args={[1, 32, 32]} />
        <meshStandardMaterial color="#e67e22" />
      </mesh>

      {/* Cilindro aún más alejado */}
      <mesh position={[0, 1, -12]}>
        <cylinderGeometry args={[1, 1, 2, 32]} />
        <meshStandardMaterial color="#2980b9" />
      </mesh>

      {/* 3. AYUDAS VISUALES Y CONTROLES */}
      <OrbitControls />
      <Grid infiniteGrid cellSize={1} sectionSize={5} fadeDistance={100} />
    </>
  );
}

/**
 * Componente principal que maneja la lógica de la cámara y la UI.
 */
export default function App() {
  // Estado para controlar qué tipo de cámara usamos
  const [isOrthographic, setOrthographic] = useState(false);
  
  // Estado para el valor del slider (FOV o Zoom)
  const [paramValue, setParamValue] = useState(75);

  // Función para alternar el estado de la cámara
  const toggleCamera = () => {
    const newMode = !isOrthographic;
    setOrthographic(newMode);
    // Asignamos un valor por defecto razonable al cambiar de modo
    setParamValue(newMode ? 50 : 75); 
  };

  return (
    <>
      {/* --- INTERFAZ DE USUARIO (HUD) --- */}
      <div className="hud">
        <button onClick={toggleCamera}>
          Cambiar a Cámara {isOrthographic ? 'Perspectiva' : 'Ortográfica'}
        </button>
        <div className="slider-container">
          <label>
            {isOrthographic ? `Zoom: ${paramValue}` : `Campo de Visión (FOV): ${paramValue}°`}
          </label>
          <input
            type="range"
            min={isOrthographic ? 10 : 30}
            max={isOrthographic ? 200 : 120}
            step="1"
            value={paramValue}
            onChange={(e) => setParamValue(Number(e.target.value))}
          />
        </div>
      </div>

      {/* --- LIENZO 3D --- */}
      <Canvas>
        {/* Lógica condicional: renderiza una cámara u otra según el estado */}
        {isOrthographic ? (
          <OrthographicCamera makeDefault position={[10, 10, 10]} zoom={paramValue} near={0.1} far={1000} />
        ) : (
          <PerspectiveCamera makeDefault position={[10, 10, 10]} fov={paramValue} near={0.1} far={1000} />
        )}
        
        <Suspense fallback={null}>
          <SceneContent />
        </Suspense>
      </Canvas>
    </>
  );
}