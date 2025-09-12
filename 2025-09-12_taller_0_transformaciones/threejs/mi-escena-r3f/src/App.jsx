import { useRef } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls } from '@react-three/drei';
import './App.css'; // Asegúrate de tener este archivo o crea uno vacío.

/**
 * Componente que contiene el objeto 3D y su lógica de animación.
 */
function AnimatedObject() {
  const meshRef = useRef();

  useFrame((state, delta) => {
    // 'state.clock.getElapsedTime()' da el tiempo total transcurrido.
    const t = state.clock.getElapsedTime();

    // 1. ROTACIÓN: Rotar sobre su propio eje.
    if (meshRef.current) {
      meshRef.current.rotation.y += delta * 0.5;
      meshRef.current.rotation.x += delta * 0.2;
    }

    // 2. TRASLACIÓN: Moverse en una trayectoria circular.
    if (meshRef.current) {
      meshRef.current.position.x = Math.cos(t) * 2;
      meshRef.current.position.z = Math.sin(t) * 2;
    }

    // 3. ESCALADO: Escalar suavemente con una función temporal.
    if (meshRef.current) {
      const scale = 1 + 0.5 * Math.sin(t * 2);
      meshRef.current.scale.set(scale, scale, scale);
    }
  });

  return (
    <mesh ref={meshRef}>
      {/* Geometría: La forma del objeto (un cubo). */}
      <boxGeometry args={[1, 1, 1]} />
      {/* Material*/}
      <meshStandardMaterial color="mediumpurple" />
    </mesh>
  );
}

/**
 * Componente principal que configura la escena y renderiza el Canvas.
 */
export default function App() {
  return (
    <Canvas camera={{ position: [0, 2, 5], fov: 70 }}>
      <ambientLight intensity={1.5} />
      <directionalLight position={[3, 5, 2]} intensity={2} />

      <AnimatedObject />

      <OrbitControls />
      
      <gridHelper />
      <axesHelper args={[2]} />
    </Canvas>
  );
}