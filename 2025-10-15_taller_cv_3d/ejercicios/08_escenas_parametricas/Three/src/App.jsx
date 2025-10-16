import React from "react";
import { Canvas } from "@react-three/fiber";
import { OrbitControls } from "@react-three/drei";
import { Leva, useControls } from "leva";
import Scene from "./Scene";
import { objects } from "./objects";

export default function App() {
  const { globalColor, globalScale, lightIntensity } = useControls({
    globalColor: { value: "#ffffff" },
    globalScale: { value: 1, min: 0.5, max: 2, step: 0.1 },
    lightIntensity: { value: 0.8, min: 0, max: 2, step: 0.1 },
  });

  const modifiedObjects = objects.map(obj => ({
    ...obj,
    color: globalColor || obj.color,
    scale: obj.scale.map(s => s * globalScale),
  }));

  return (
    <>
      <Leva collapsed />
      <Canvas
        camera={{ position: [5, 4, 6], fov: 45 }}
        style={{ width: "100vw", height: "100vh" }}
      >
        <ambientLight intensity={lightIntensity} />
        <directionalLight position={[5, 5, 5]} intensity={lightIntensity} />
        <Scene data={modifiedObjects} />
        <OrbitControls />
      </Canvas>
    </>
  );
}

