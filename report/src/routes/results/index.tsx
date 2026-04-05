import { Center, Flex } from "@mantine/core";
import { createFileRoute } from "@tanstack/react-router";
import { BoxesIcon, BoxIcon, HouseIcon } from "lucide-react";

import { LinkCard } from "@/components/LinkCard";

export const Route = createFileRoute("/results/")({
  component: RouteComponent,
});

function RouteComponent() {
  return (
    <Flex direction="column" h="100%">
      <Center h="100%">
        <Flex gap="md" p="xl">
          <LinkCard
            title="Home"
            description="Go home"
            href="/"
            icon={<HouseIcon size={120} />}
          />
          <LinkCard
            title="Jobs"
            description="View jobs from an OpenPFO run"
            href="/results/jobs"
            icon={<BoxIcon size={120} />}
          />
          <LinkCard
            title="Searches"
            description="View searches from an OpenPFO run"
            href="/results/searches"
            icon={<BoxesIcon size={120} />}
          />
        </Flex>
      </Center>
    </Flex>
  );
}
