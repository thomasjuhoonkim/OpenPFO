import { Flex, Tabs } from "@mantine/core";
import { createFileRoute } from "@tanstack/react-router";
import { zodValidator } from "@tanstack/zod-adapter";
import * as z from "zod";

import { ObjectivesParallelCoordinates } from "@/components/ObjectivesParallelCoordinates";
import { PointParallelCoordinates } from "@/components/PointParallelCoordinates";
import { StepSankey } from "@/components/StepSankey";
import { results as schemaResults } from "@/types/results";

const jobSearchSchema = z.object({
  tab: z.enum(["points", "objectives", "steps"]).default("points"),
});

export const Route = createFileRoute("/results/jobs/")({
  validateSearch: zodValidator(jobSearchSchema),
  loader: async () => {
    const response = await fetch("/results.json");
    const json = await response.json();
    const results = schemaResults.parse(json);
    return { results };
  },
  component: RouteComponent,
});

function RouteComponent() {
  const navigate = Route.useNavigate();
  const { tab } = Route.useSearch();
  const { results } = Route.useLoaderData();

  function onTabChange(value: any) {
    if (!value) {
      return;
    }
    navigate({
      search: (prev) => ({
        ...prev,
        tab: value,
      }),
    });
  }

  const jobs = results.workflow.jobs;

  return (
    <Tabs h="100%" onChange={onTabChange} defaultValue={tab}>
      <Flex h="100%" direction="column">
        <Tabs.List>
          <Tabs.Tab value="points">Points</Tabs.Tab>
          <Tabs.Tab value="objectives">Objectives</Tabs.Tab>
          <Tabs.Tab value="steps">Steps</Tabs.Tab>
        </Tabs.List>

        <Tabs.Panel value="points" h="100%">
          <PointParallelCoordinates
            results={results}
            jobs={jobs}
            title="Points in the design space for all jobs"
          />
        </Tabs.Panel>
        <Tabs.Panel value="objectives" h="100%">
          <ObjectivesParallelCoordinates
            results={results}
            jobs={jobs}
            title="Objective values for all jobs"
          />
        </Tabs.Panel>
        <Tabs.Panel value="steps" h="100%">
          <StepSankey
            results={results}
            jobs={jobs}
            title="All jobs by step status throughout job execution"
          />
        </Tabs.Panel>
      </Flex>
    </Tabs>
  );
}
