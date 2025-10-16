import React, { useState, Suspense } from 'react';
import { Canvas } from '@react-three/fiber';
import { PerspectiveCamera, OrthographicCamera, OrbitControls, Text } from '@react-three/drei';
import './styles.css'; // Asegúrate de tener un CSS para el posicionamiento de la UI

function SceneContent() {
  return (
    <>
      {/* Objetos a diferentes profundidades */}
      <mesh position={[0, 0, 0]}>
        <boxGeometry />
        <meshStandardMaterial color="mediumpurple" />
      </mesh>
      <mesh position={[2.5, 0, -5]}>
        <sphereGeometry />
        <meshStandardMaterial color="orange" />
      </mesh>
      <mesh position={[-2.5, 0, -10]}>
        <coneGeometry args={[1, 1.5, 32]} />
        <meshStandardMaterial color="aquamarine" />
      </mesh>
      
      {/* Ayudas visuales */}
      <gridHelper args={[50, 50]} />
      <axesHelper args={[5]} />
      <OrbitControls />
      <ambientLight intensity={0.6} />
      <pointLight position={[10, 10, 10]} intensity={1} />
    </>
  );
}

export default function App() {
  const [isOrthographic, setOrthographic] = useState(false);
  const [paramValue, setParamValue] = useState(75); // FOV para Perspectiva, Zoom para Ortográfica

  return (
    <>
      {/* Interfaz de Usuario (HUD) */}
      <div className="hud">
        <button onClick={() => setOrthographic(!isOrthographic)}>
          Cambiar a {isOrthographic ? 'Perspectiva' : 'Ortográfica'}
        </button>
        <div className="slider-container">
          <label>{isOrthographic ? 'Zoom' : 'FOV'}: {paramValue}</label>
          <input
            type="range"
            min={isOrthographic ? 10 : 30}
            max={isOrthographic ? 200 : 120}
            value={paramValue}
            onChange={(e) => setParamValue(parseInt(e.target.value))}
          />
        </div>
      </div>

      <Canvas>
        {isOrthographic ? (
          <OrthographicCamera makeDefault position={[5, 5, 10]} zoom={paramValue} />
        ) : (
          <PerspectiveCamera makeDefault position={[5, 5, 10]} fov={paramValue} />
        )}
        <Suspense fallback={null}>
          <SceneContent />
        </Suspense>
      </Canvas>
    </>
  );
}