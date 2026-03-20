import { Divider, Flex, Group, Switch, Text } from "@mantine/core";
import { useState } from "react";

import { ObjectivesRadar } from "@/components/ObjectivesRadar";
import type { Job, Results } from "@/types/results";
import { getNormalizedJobs } from "@/util/getNormalizedJobs";

import { ObjectivesParallelCoordinates } from "./ObjectivesParallelCoordinates";

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

      {results.config.optimizer.objectives.length <= 2 ? (
        isNormalized ? (
          <ObjectivesParallelCoordinates
            results={results}
            jobs={getNormalizedJobs(results, jobs)}
            title={`${title} (Normalized)`}
            isNormalized
          />
        ) : (
          <Flex direction="column" h="100%">
            <ObjectivesParallelCoordinates
              results={results}
              jobs={jobs}
              title={title}
            />
          </Flex>
        )
      ) : isNormalized ? (
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
