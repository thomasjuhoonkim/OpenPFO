import { Flex, Group, Tabs, Text } from "@mantine/core";
import { createFileRoute, Link } from "@tanstack/react-router";
import { zodValidator } from "@tanstack/zod-adapter";
import { ArrowLeftIcon } from "lucide-react";
import * as z from "zod";

import { PointParallelCoordinates } from "@/components/PointParallelCoordinates";
import { results as schemaResults } from "@/types/results";

import { TabObjectives } from "../../../components/TabObjectives";
import { TabOverview } from "../../../components/TabOverview";
import { TabPointsAndObjectives } from "../../../components/TabPointsAndObjectives";
import { TabSteps } from "../../../components/TabSteps";

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
          {/* @ts-expect-error */}
          <Tabs.Tab component={Link} to="/results" value="back">
            <Group gap="4" align="center">
              <ArrowLeftIcon size={16} color="var(--mantine-color-anchor)" />
              <Text size="sm" color="var(--mantine-color-anchor)">
                Results
              </Text>
            </Group>
          </Tabs.Tab>
          <Tabs.Tab value="overview">Overview</Tabs.Tab>
          <Tabs.Tab value="points">Points</Tabs.Tab>
          <Tabs.Tab value="objectives">Objectives</Tabs.Tab>
          <Tabs.Tab value="points-objectives">Points & Objectives</Tabs.Tab>
          <Tabs.Tab value="steps">Steps</Tabs.Tab>
        </Tabs.List>

        {tab === "overview" && <TabOverview results={results} />}

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

        {tab === "steps" && (
          <TabSteps
            results={results}
            jobs={jobs}
            title="All jobs by step status throughout job execution"
          />
        )}

        {tab === "points-objectives" && (
          <TabPointsAndObjectives results={results} jobs={jobs} />
        )}
      </Flex>
    </Tabs>
  );
}
