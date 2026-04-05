import { Anchor, Center, Flex, ScrollArea, Table } from "@mantine/core";
import { Link } from "@tanstack/react-router";
import dayjs from "dayjs";
import { CheckIcon, XIcon } from "lucide-react";
import { DATETIME_FORMAT } from "react-big-schedule";

import type { Results } from "@/types/results";

export function TabOverview({ results }: { results: Results }) {
  const rows = results.workflow.jobs.map((job) => (
    <Table.Tr key={job.id}>
      <Table.Td>
        {job.runOk ? <CheckIcon color="green" /> : <XIcon color="red" />}
      </Table.Td>
      <Table.Td>{job.status}</Table.Td>
      <Table.Td>{job.id}</Table.Td>
      <Table.Td>{job.point.representation}</Table.Td>
      <Table.Td>{dayjs(job.startTime).format(DATETIME_FORMAT)}</Table.Td>
      <Table.Td>{dayjs(job.startTime).format(DATETIME_FORMAT)}</Table.Td>
      <Table.Td>
        <Anchor component={Link} to={`/results/jobs/${job.id}`}>
          Open
        </Anchor>
      </Table.Td>
    </Table.Tr>
  ));

  return (
    <Flex direction="column" h="100%">
      <Center h="100%">
        <Flex gap="sm" p="xl" direction="column">
          <ScrollArea h="75dvh">
            <Table>
              <Table.Thead>
                <Table.Tr>
                  <Table.Th>Run OK</Table.Th>
                  <Table.Th>Status</Table.Th>
                  <Table.Th>ID</Table.Th>
                  <Table.Th>Point Representation</Table.Th>
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
