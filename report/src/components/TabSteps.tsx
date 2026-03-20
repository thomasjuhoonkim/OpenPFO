import { Flex } from "@mantine/core";

import { StepSankey } from "@/components/StepSankey";
import type { Job, Results } from "@/types/results";

export function TabSteps({
  results,
  jobs,
  title,
}: {
  results: Results;
  jobs: Job[];
  title: string;
}) {
  return (
    <Flex direction="column" h="100%">
      <StepSankey results={results} jobs={jobs} title={title} />
    </Flex>
  );
}
