import { Flex, Tabs } from "@mantine/core";
import { createFileRoute } from "@tanstack/react-router";
import { zodValidator } from "@tanstack/zod-adapter";
import * as z from "zod";

import { PointParallelCoordinates } from "@/components/PointParallelCoordinates";
import { results as schemaResults } from "@/types/results";
import { TabObjectives } from "../../../components/TabObjectives";
import { TabSteps } from "../../../components/TabSteps";
import { TabPointsAndObjectives } from "../../../components/TabPointsAndObjectives";
import { TabOverview } from "../../../components/TabOverview";

const jobSearchSchema = z.object({
  tab: z
    .enum(["overview", "points", "objectives", "points-objectives", "steps"])
    .default("overview"),
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

  async function onTabChange(value: any) {
    if (!value) {
      return;
    }
    await navigate({
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
          <Tabs.Tab value="overview">Overview</Tabs.Tab>
          <Tabs.Tab value="points">Points</Tabs.Tab>
          <Tabs.Tab value="objectives">Objectives</Tabs.Tab>
          <Tabs.Tab value="points-objectives">Points & Objectives</Tabs.Tab>
          <Tabs.Tab value="steps">Steps</Tabs.Tab>
        </Tabs.List>

        {tab === "overview" && <TabOverview />}

        {tab === "points" && (
          <PointParallelCoordinates
            results={results}
            jobs={jobs}
            title="Points in the design space for all jobs"
          />
        )}

        {tab === "objectives" && (
          <TabObjectives
            results={results}
            jobs={jobs}
            title="Objective values for all jobs"
          />
        )}

        {tab === "steps" && <TabSteps results={results} jobs={jobs} />}

        {tab === "points-objectives" && (
          <TabPointsAndObjectives results={results} jobs={jobs} />
        )}
      </Flex>
    </Tabs>
  );
}
