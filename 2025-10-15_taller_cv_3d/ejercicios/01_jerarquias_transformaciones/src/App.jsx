import { Canvas } from '@react-three/fiber'
import { OrbitControls } from '@react-three/drei'
import { useControls } from 'leva'
import { useRef } from 'react'

function Scene() {
  const groupRef = useRef()
  const childRef = useRef()
  const grandChildRef = useRef()

  // Controles para transformar el nodo padre
  const { px, py, pz, rx, ry, rz } = useControls('Transformaciones Padre', {
    px: { value: 0, min: -5, max: 5, step: 0.1 },
    py: { value: 0, min: -5, max: 5, step: 0.1 },
    pz: { value: 0, min: -5, max: 5, step: 0.1 },
    rx: { value: 0, min: -Math.PI, max: Math.PI, step: 0.01 },
    ry: { value: 0, min: -Math.PI, max: Math.PI, step: 0.01 },
    rz: { value: 0, min: -Math.PI, max: Math.PI, step: 0.01 },
  })

  // Controles para transformar el nodo hijo
    const { cx, cy, cz, crx, cry, crz } = useControls('Transformaciones Hijo', {
    cx: { value: 2, min: -5, max: 5, step: 0.1 },
    cy: { value: 0, min: -5, max: 5, step: 0.1 },
    cz: { value: 0, min: -5, max: 5, step: 0.1 },
    crx: { value: 0, min: -Math.PI, max: Math.PI, step: 0.01 },
    cry: { value: 0, min: -Math.PI, max: Math.PI, step: 0.01 },
    crz: { value: 0, min: -Math.PI, max: Math.PI, step: 0.01 },
  })

  return (
    <group
      ref={groupRef}
      position={[px, py, pz]}
      rotation={[rx, ry, rz]}
    >
      {/* Padre */}
      <mesh>
        <boxGeometry args={[1, 1, 1]} />
        <meshStandardMaterial color="orange" />
      </mesh>

      {/* Hijo */}
      <group
        ref={childRef}
        position={[cx, cy, cz]}
        rotation={[crx, cry, crz]}
      >
        <mesh>
          <sphereGeometry args={[0.5, 32, 32]} />
          <meshStandardMaterial color="skyblue" />
        </mesh>

        {/* Nieto */}
        <group ref={grandChildRef} position={[1.5, 0, 0]}>
          <mesh>
            <coneGeometry args={[0.4, 1, 16]} />
            <meshStandardMaterial color="hotpink" />
          </mesh>
        </group>
      </group>
    </group>
  )
}

export default function App() {
  return (
    <Canvas
      camera={{ position: [6, 4, 8], fov: 50 }}
      style={{ width: '100vw', height: '100vh', display: 'block' }}
    >
      <ambientLight intensity={0.5} />
      <directionalLight position={[10, 10, 10]} />
      <OrbitControls />
      <gridHelper args={[20, 20]} />
      <axesHelper args={[5]} />
      <Scene />
    </Canvas>
  )
}
