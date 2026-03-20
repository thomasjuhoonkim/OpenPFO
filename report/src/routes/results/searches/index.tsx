import {
  Anchor,
  Center,
  Flex,
  Group,
  ScrollArea,
  Table,
  Text,
} from "@mantine/core";
import { createFileRoute, Link } from "@tanstack/react-router";
import dayjs from "dayjs";
import { ArrowLeftIcon } from "lucide-react";
import { DATETIME_FORMAT } from "react-big-schedule";

import { results as schemaResults } from "@/types/results";

export const Route = createFileRoute("/results/searches/")({
  loader: async () => {
    const response = await fetch("/results.json");
    const json = await response.json();
    const results = schemaResults.parse(json);
    return { results };
  },
  component: RouteComponent,
});

function RouteComponent() {
  const { results } = Route.useLoaderData();

  const rows = results.workflow.searches.map((search) => (
    <Table.Tr key={search.id}>
      <Table.Td>{search.id}</Table.Td>
      <Table.Td>{dayjs(search.startTime).format(DATETIME_FORMAT)}</Table.Td>
      <Table.Td>{dayjs(search.startTime).format(DATETIME_FORMAT)}</Table.Td>
      <Table.Td>
        <Anchor component={Link} to={`/results/searches/${search.id}`}>
          Open
        </Anchor>
      </Table.Td>
    </Table.Tr>
  ));

  return (
    <Flex direction="column" h="100%">
      <Center h="100%">
        <Flex gap="sm" p="xl" direction="column">
          <Anchor component={Link} to="/results">
            <Group gap="4" align="center">
              <ArrowLeftIcon size={16} />
              <Text>Results</Text>
            </Group>
          </Anchor>

          <ScrollArea h="75dvh">
            <Table>
              <Table.Thead>
                <Table.Tr>
                  <Table.Th>ID</Table.Th>
                  <Table.Th>Start Time</Table.Th>
                  <Table.Th>End Time</Table.Th>
                  <Table.Th />
                </Table.Tr>
              </Table.Thead>
              <Table.Tbody>{rows}</Table.Tbody>
            </Table>
          </ScrollArea>
        </Flex>
      </Center>
    </Flex>
  );
}
