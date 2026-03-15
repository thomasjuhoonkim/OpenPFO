import { Flex, Title } from "@mantine/core";

import { GeometryViewer } from "@/components/GeometryViewer";
import type { Job } from "@/types/results";

const validExtensions = ["stl", "obj", "vtk"];

export function TabGeometry({ job }: { job: Job }) {
  if (!job.meta.geometry) {
    return (
      <Flex direction="column" align="center" justify="center" h="100%">
        <Title>No geometry available</Title>
      </Flex>
    );
  }

  if (!validExtensions.includes(job.meta.geometry.split(".").pop())) {
    return (
      <Flex direction="column" align="center" justify="center" h="100%">
        <Title>Invalid geometry file</Title>
      </Flex>
    );
  }

  const url = `/${job.id}/${job.meta.geometry}`;

  return <GeometryViewer url={url} />;
}
