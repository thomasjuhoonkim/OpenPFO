import { Center, Flex, Tabs, Title } from "@mantine/core";
import { createFileRoute, notFound } from "@tanstack/react-router";
import { zodValidator } from "@tanstack/zod-adapter";
import { find } from "lodash-es";
import * as z from "zod";

import { GeometryViewer } from "@/components/GeometryViewer";
import { ObjectivesParallelCoordinates } from "@/components/ObjectivesParallelCoordinates";
import { PointParallelCoordinates } from "@/components/PointParallelCoordinates";
import { StepTimeline } from "@/components/StepTimeline";
import { results as schemaResults } from "@/types/results";

const jobSearchSchema = z.object({
  tab: z.enum(["point", "objectives", "geometry", "steps"]).default("point"),
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

  const stl = `/${job.id}/${job.id}.stl`;

  return (
    <Tabs h="100%" onChange={onTabChange} defaultValue={tab}>
      <Flex h="100%" direction="column">
        <Tabs.List>
          <Tabs.Tab value="point">Point</Tabs.Tab>
          <Tabs.Tab value="objectives">Objectives</Tabs.Tab>
          <Tabs.Tab value="geometry">Geometry</Tabs.Tab>
          <Tabs.Tab value="steps">Steps</Tabs.Tab>
        </Tabs.List>

        <Tabs.Panel value="point" h="100%">
          <PointParallelCoordinates
            results={results}
            jobs={[job]}
            title={`Points in the design space for ${job.id}`}
          />
        </Tabs.Panel>
        <Tabs.Panel value="objectives" h="100%">
          <ObjectivesParallelCoordinates
            results={results}
            jobs={[job]}
            title={`Objective values for ${job.id}`}
          />
        </Tabs.Panel>
        <Tabs.Panel value="geometry" h="100%">
          <GeometryViewer url={stl} />
        </Tabs.Panel>
        <Tabs.Panel value="steps">
          <Center>
            <Flex direction="column" p="xl" gap="lg">
              <Title>Steps</Title>
              <StepTimeline job={job} />
            </Flex>
          </Center>
        </Tabs.Panel>
      </Flex>
    </Tabs>
  );
}
