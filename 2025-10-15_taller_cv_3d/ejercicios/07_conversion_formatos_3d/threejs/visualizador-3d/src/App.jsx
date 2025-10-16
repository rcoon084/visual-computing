import React, { Suspense, useState, useMemo } from 'react';
import { Canvas, useLoader } from '@react-three/fiber';
import { OrbitControls, useGLTF, Html, Bounds } from '@react-three/drei';
import { OBJLoader } from 'three/examples/jsm/loaders/OBJLoader';
import { MTLLoader } from 'three/examples/jsm/loaders/MTLLoader';
import { STLLoader } from 'three/examples/jsm/loaders/STLLoader';
import * as THREE from 'three';
import './App.css';

// Componente que muestra un texto de "Cargando..."
function Loader() {
  return <Html center style={{ color: 'white', fontSize: '24px', whiteSpace: 'nowrap' }}>Cargando modelo...</Html>;
}

// Componente especializado para cargar GLB/GLTF
const ModelGltf = ({ url }) => <primitive object={useGLTF(url).scene} />;

// Componente especializado para cargar OBJ con su material
const ModelObj = ({ mtlUrl, objUrl }) => {
  const materials = useLoader(MTLLoader, mtlUrl);
  const obj = useLoader(OBJLoader, objUrl, (loader) => {
    materials.preload();
    loader.setMaterials(materials);
  });
  return <primitive object={obj} />;
};

// Componente especializado para cargar STL (el más simple)
const ModelStl = ({ url }) => {
  const geom = useLoader(STLLoader, url);
  return (
    <mesh geometry={geom} rotation={[-Math.PI / 2, 0, 0]}>
      <meshPhongMaterial color="mediumpurple" specular="#111111" shininess={200} />
    </mesh>
  );
};

// Componente principal de la aplicación
export default function App() {
  const [format, setFormat] = useState('glb'); // 'glb' será el formato por defecto

  const Model = useMemo(() => {
    switch (format) {
      case 'obj':
        return <ModelObj mtlUrl="/models/11.10.2025_moo_deng.mtl" objUrl="/models/11.10.2025_moo_deng.obj" />;
      case 'stl':
        return <ModelStl url="/models/modelo.stl" />;
      case 'glb':
      default:
        return <ModelGltf url="/models/modelo.glb" />;
    }
  }, [format]);

  return (
    <>
      <div className="hud">
        <h3>🖼️ Selector de Formato 3D</h3>
        <p>Compara cómo se visualiza cada formato.</p>
        <div className="controls">
          <button onClick={() => setFormat('glb')} className={format === 'glb' ? 'active' : ''}>GLB (Para Web)</button>
          <button onClick={() => setFormat('obj')} className={format === 'obj' ? 'active' : ''}>OBJ (Universal)</button>
          <button onClick={() => setFormat('stl')} className={format === 'stl' ? 'active' : ''}>STL (Impresión 3D)</button>
        </div>
        <div className="info">
          {format === 'glb' && '✅ Incluye texturas y materiales en un solo archivo. Eficiente.'}
          {format === 'obj' && '⚠️ Requiere un archivo .mtl y texturas externas. Menos eficiente.'}
          {format === 'stl' && '❌ Solo geometría. No soporta colores ni materiales.'}
        </div>
      </div>

      <Canvas camera={{ position: [0, 1, 5], fov: 60 }} shadows>
        <ambientLight intensity={0.8} />
        <directionalLight position={[10, 10, 5]} intensity={1.5} castShadow />
        <color attach="background" args={['#1e1e28']} />

        <Suspense fallback={<Loader />}>
          <Bounds fit clip observe margin={1.2}>
            {Model}
          </Bounds>
        </Suspense>

        <OrbitControls makeDefault />
        <gridHelper args={[20, 20, '#444', '#222']} position={[0, -0.01, 0]}/>
      </Canvas>
    </>
  );
}