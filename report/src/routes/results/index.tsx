import { Flex } from "@mantine/core";
import { createFileRoute, Link } from "@tanstack/react-router";

export const Route = createFileRoute("/results/")({
  component: RouteComponent,
});

function RouteComponent() {
  return (
    <Flex direction="column" h="100%">
      <Link to="/results/jobs">Jobs</Link>
      <Link to="/results/searches">Searches</Link>
    </Flex>
  );
}
