import { Flex, Tabs } from "@mantine/core";
import { createFileRoute, notFound } from "@tanstack/react-router";
import { zodValidator } from "@tanstack/zod-adapter";
import { find } from "lodash-es";
import * as z from "zod";

import { PointParallelCoordinates } from "@/components/PointParallelCoordinates";
import { results as schemaResults } from "@/types/results";

import { TabObjectives } from "../../../components/TabObjectives";
import { TabOverview } from "../../../components/TabOverview";
import { TabPointsAndObjectives } from "../../../components/TabPointsAndObjectives";
import { TabSteps } from "../../../components/TabSteps";

const searchSearchSchema = z.object({
  tab: z
    .enum(["overview", "points", "objectives", "points-objectives", "steps"])
    .default("overview"),
});

export const Route = createFileRoute("/results/searches/$searchId")({
  validateSearch: zodValidator(searchSearchSchema),
  loader: async ({ params }) => {
    const response = await fetch("/results.json");
    const json = await response.json();
    const results = schemaResults.parse(json);
    const search = find(results.workflow.searches, { id: params.searchId });
    if (!search) {
      notFound();
    }
    return { results, search };
  },
  component: RouteComponent,
});

function RouteComponent() {
  const navigate = Route.useNavigate();
  const { tab } = Route.useSearch();
  const { results, search } = Route.useLoaderData();
  if (!search) {
    return notFound();
  }

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

  const jobs = results.workflow.jobs.filter((job) =>
    search.jobs.includes(job.id)
  );

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
            title={`Points in the design space for ${search.id}`}
          />
        )}

        {tab === "objectives" && (
          <TabObjectives
            results={results}
            jobs={jobs}
            title={`Objective values for ${search.id}`}
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
