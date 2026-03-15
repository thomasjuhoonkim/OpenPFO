import { Flex } from "@mantine/core";
import { createFileRoute, Link } from "@tanstack/react-router";

export const Route = createFileRoute("/")({
  component: App,
});

function App() {
  return (
    <Flex direction="column" h="100%">
      <Link to="/results">Results</Link>
      <Link to="/timeline">Timeline</Link>
      <Link to="/about">About</Link>
    </Flex>
  );
}
