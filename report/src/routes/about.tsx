import { Flex } from "@mantine/core";
import { createFileRoute, Link } from "@tanstack/react-router";

export const Route = createFileRoute("/about")({
  component: RouteComponent,
});

function RouteComponent() {
  return (
    <Flex direction="column" h="100%">
      <Link to="/">Home</Link>
    </Flex>
  );
}
