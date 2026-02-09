import { GizmoHelper, GizmoViewcube, OrbitControls } from "@react-three/drei";
import { Canvas, useLoader } from "@react-three/fiber";
// @ts-expect-error
import { OBJLoader } from "three/examples/jsm/loaders/OBJLoader";
// @ts-expect-error
import { STLLoader } from "three/examples/jsm/loaders/STLLoader";
// @ts-expect-error
import { VTKLoader } from "three/examples/jsm/loaders/VTKLoader";

export function GeometryViewer({ url }: { url: string }) {
  const loader = (() => {
    const extension = url.split(".").pop();
    if (extension === "stl") {
      return STLLoader;
    } else if (extension === "obj") {
      return OBJLoader;
    } else if (extension === "vtk") {
      return VTKLoader;
    }
  })();
  const geometry = useLoader(loader, url);
  return (
    <div style={{ height: "100%", width: "100%" }}>
      <Canvas>
        <mesh geometry={geometry}>
          <meshStandardMaterial color="#ffce2f" />
        </mesh>

        <axesHelper />
        <ambientLight intensity={0.75} />
        <directionalLight position={[10, 10, 10]} intensity={0.75} />
        <OrbitControls enableDamping dampingFactor={0.05} />
        <GizmoHelper alignment="bottom-left" margin={[75, 75]}>
          <GizmoViewcube />
        </GizmoHelper>
      </Canvas>
    </div>
  );
}
