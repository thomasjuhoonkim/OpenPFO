import { Center, Loader } from "@mantine/core";
import { createFileRoute } from "@tanstack/react-router";

import { Timeline } from "@/components/Timeline/Timeline";
import { results as schemaResults } from "@/types/results";

export const Route = createFileRoute("/timeline")({
  loader: async () => {
    const response = await fetch("/results.json");
    const json = await response.json();
    const results = schemaResults.parse(json);
    return { results };
  },
  component: RouteComponent,
  pendingComponent: PendingComponent,
});

function RouteComponent() {
  const navigate = Route.useNavigate();
  const { results } = Route.useLoaderData();
  return <Timeline results={results} navigate={navigate} />;
}

function PendingComponent() {
  return (
    <Center h="100%" w="100%">
      <Loader />
    </Center>
  );
}
