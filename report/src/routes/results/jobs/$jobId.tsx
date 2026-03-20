import { Center, Flex, Group, Tabs, Text, Title } from "@mantine/core";
import { createFileRoute, Link, notFound } from "@tanstack/react-router";
import { zodValidator } from "@tanstack/zod-adapter";
import { find } from "lodash-es";
import { ArrowLeftIcon } from "lucide-react";
import * as z from "zod";

import { PointParallelCoordinates } from "@/components/PointParallelCoordinates";
import { StepTimeline } from "@/components/StepTimeline";
import { results as schemaResults } from "@/types/results";

import { TabGeometry } from "../../../components/TabGeometry";
import { TabImages } from "../../../components/TabImages";
import { TabObjectives } from "../../../components/TabObjectives";

const jobSearchSchema = z.object({
  tab: z
    .enum(["point", "objectives", "steps", "geometry", "images"])
    .default("point"),
});

export const Route = createFileRoute("/results/jobs/$jobId")({
  validateSearch: zodValidator(jobSearchSchema),
  loader: async ({ params }) => {
    const response = await fetch("/results.json");
    const json = await response.json();
    const results = schemaResults.parse(json);
    const job = find(results.workflow.jobs, { id: params.jobId });
    if (!job) {
      notFound();
    }
    return { results, job };
  },
  component: RouteComponent,
});

function RouteComponent() {
  const navigate = Route.useNavigate();
  const { tab } = Route.useSearch();
  const { results, job } = Route.useLoaderData();
  if (!job) {
    return notFound();
  }

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

  return (
    <Tabs h="100%" onChange={onTabChange} defaultValue={tab}>
      <Flex h="100%" direction="column">
        <Tabs.List>
          {/* @ts-expect-error */}
          <Tabs.Tab component={Link} to="/results/jobs" value="back">
            <Group gap="4" align="center">
              <ArrowLeftIcon size={16} color="var(--mantine-color-anchor)" />
              <Text size="sm" color="var(--mantine-color-anchor)">
                Jobs
              </Text>
            </Group>
          </Tabs.Tab>
          <Tabs.Tab value="point">Point</Tabs.Tab>
          <Tabs.Tab value="objectives">Objectives</Tabs.Tab>
          <Tabs.Tab value="steps">Steps</Tabs.Tab>
          <Tabs.Tab value="geometry">Geometry</Tabs.Tab>
          <Tabs.Tab value="images">Images</Tabs.Tab>
        </Tabs.List>

        {tab === "point" && (
          <PointParallelCoordinates
            results={results}
            jobs={[job]}
            title={`Points in the design space for ${job.id}`}
          />
        )}

        {tab === "objectives" && (
          <TabObjectives
            results={results}
            jobs={[job]}
            title={`Objective values for ${job.id}`}
          />
        )}

        {tab === "steps" && (
          <Center>
            <Flex direction="column" p="xl" gap="lg">
              <Title>Steps</Title>
              <StepTimeline job={job} />
            </Flex>
          </Center>
        )}

        {tab === "geometry" && <TabGeometry job={job} />}

        {tab === "images" && <TabImages job={job} />}
      </Flex>
    </Tabs>
  );
}
