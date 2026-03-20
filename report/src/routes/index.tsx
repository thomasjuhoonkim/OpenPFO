import { Center, Flex } from "@mantine/core";
import { createFileRoute } from "@tanstack/react-router";
import { DatabaseIcon, GanttChartIcon, GithubIcon } from "lucide-react";

import { LinkCard } from "@/components/LinkCard";

export const Route = createFileRoute("/")({
  component: App,
});

function App() {
  return (
    <Flex direction="column" h="100%">
      <Center h="100%">
        <Flex gap="md" p="xl">
          <LinkCard
            title="Timeline"
            description="View the run timeline"
            href="/timeline"
            icon={<GanttChartIcon size={120} />}
          />
          <LinkCard
            title="Results"
            description="View results from an OpenPFO run"
            href="/results"
            icon={<DatabaseIcon size={120} />}
          />
          <LinkCard
            title="GitHub"
            description="OpenPFO GitHub"
            href="https://github.com/thomasjuhoonkim/OpenPFO"
            target="_blank"
            icon={<GithubIcon size={120} />}
          />
        </Flex>
      </Center>
    </Flex>
  );
}
