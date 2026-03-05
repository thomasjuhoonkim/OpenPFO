import { StepSankey } from "@/components/StepSankey";
import type { Job, Results } from "@/types/results";
import { Flex } from "@mantine/core";

export function TabSteps({ results, jobs }: { results: Results; jobs: Job[] }) {
  return (
    <Flex direction="column" h="100%">
      <StepSankey
        results={results}
        jobs={jobs}
        title="All jobs by step status throughout job execution"
      />
    </Flex>
  );
}
