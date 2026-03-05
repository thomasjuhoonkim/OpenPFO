import { ObjectivesRadar } from "@/components/ObjectivesRadar";

import type { Job, Results } from "@/types/results";
import { Text, Divider, Flex, Group, Switch } from "@mantine/core";
import { useState } from "react";

import { getNormalizedJobs } from "@/util/getNormalizedJobs";

export function TabObjectives({
  results,
  jobs,
  title,
}: {
  results: Results;
  jobs: Job[];
  title: string;
}) {
  const [isNormalized, setIsNormalized] = useState(false);

  return (
    <Flex direction="column" h="100%">
      <Flex direction="column">
        <Group p="sm" gap="xs">
          <Text size="sm">Normalize Objectives</Text>
          <Switch
            checked={isNormalized}
            onChange={(event) => setIsNormalized(event.currentTarget.checked)}
          />
        </Group>
        <Divider size="sm" />
      </Flex>

      {isNormalized ? (
        <ObjectivesRadar
          results={results}
          jobs={getNormalizedJobs(results, jobs)}
          title={`${title} (Normalized)`}
          isNormalized
        />
      ) : (
        <Flex direction="column" h="100%">
          <ObjectivesRadar results={results} jobs={jobs} title={title} />
        </Flex>
      )}
    </Flex>
  );
}
