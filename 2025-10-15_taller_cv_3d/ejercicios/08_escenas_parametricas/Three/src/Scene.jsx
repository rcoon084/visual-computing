import React from "react";
import { Box, Sphere, Cone, Cylinder } from "@react-three/drei";

const Primitive = ({ type, position, scale, color }) => {
  switch (type) {
    case "box":
      return <Box args={[1, 1, 1]} position={position} scale={scale}><meshStandardMaterial color={color} /></Box>;
    case "sphere":
      return <Sphere args={[0.5, 32, 32]} position={position} scale={scale}><meshStandardMaterial color={color} /></Sphere>;
    case "cone":
      return <Cone args={[0.5, 1, 32]} position={position} scale={scale}><meshStandardMaterial color={color} /></Cone>;
    case "cylinder":
      return <Cylinder args={[0.5, 0.5, 1, 32]} position={position} scale={scale}><meshStandardMaterial color={color} /></Cylinder>;
    default:
      return null;
  }
};

const Scene = ({ data }) => {
  return (
    <>
      {data.map((obj, i) => (
        <Primitive key={i} {...obj} />
      ))}
    </>
  );
};

export default Scene;
