import { Flex } from "@mantine/core";
import { Link } from "@tanstack/react-router";

export function TabOverview() {
  return (
    <Flex direction="column" h="100%">
      <Link to="/results">Results</Link>
    </Flex>
  );
}
