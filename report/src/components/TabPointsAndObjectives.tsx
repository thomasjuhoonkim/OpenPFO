import type { Job, Results } from "@/types/results";
import { Text, Divider, Flex, Group, Switch } from "@mantine/core";
import { useState } from "react";

import { getNormalizedJobs } from "@/util/getNormalizedJobs";
import { PointsAndObjectives } from "@/components/PointsAndObjectives";

export function TabPointsAndObjectives({
  results,
  jobs,
}: {
  results: Results;
  jobs: Job[];
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
        <PointsAndObjectives
          results={results}
          jobs={getNormalizedJobs(results, jobs)}
          parallelTitle="Points in the design space for all jobs"
          radarTitle="Objective values for all successful jobs (Normalized)"
          isNormalized
        />
      ) : (
        <Flex direction="column" h="100%">
          <PointsAndObjectives
            results={results}
            jobs={jobs}
            parallelTitle="Points in the design space for all jobs"
            radarTitle="Objective values for all successful jobs"
          />
        </Flex>
      )}
    </Flex>
  );
}
