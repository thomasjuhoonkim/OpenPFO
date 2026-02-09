import {
  Anchor,
  AppShell,
  Badge,
  Flex,
  Group,
  MantineProvider,
  Text,
} from "@mantine/core";
import { createRootRoute, Link, Outlet } from "@tanstack/react-router";
import type { PropsWithChildren } from "react";

import { theme } from "@/theme";
import { results as schemaResults } from "@/types/results";

import styles from "./root.module.css";

export const Route = createRootRoute({
  loader: async () => {
    const response = await fetch("/results.json");
    const json = await response.json();
    const results = schemaResults.parse(json);
    return { results };
  },
  component: () => (
    <MantineProvider theme={theme} forceColorScheme="dark">
      <Layout>
        <Outlet />
      </Layout>
    </MantineProvider>
  ),
});

function Layout({ children }: PropsWithChildren) {
  const { results } = Route.useLoaderData();
  return (
    <AppShell padding="0" header={{ height: 60 }} h="100vh">
      <AppShell.Header style={{ borderWidth: 2 }}>
        <Flex align="center" justify="space-between" h="100%" p="md">
          <Group>
            <Text className={styles.logo} component={Link} to="/" size="lg">
              OpenPFO Report
            </Text>
            {results.endTime ? (
              <Badge color="green">Finished</Badge>
            ) : (
              <Badge color="indigo">Running</Badge>
            )}
          </Group>

          <Group>
            <Anchor
              className={styles.logo}
              component={Link}
              to="/timeline"
              size="lg"
            >
              Timeline
            </Anchor>
            <Anchor
              className={styles.logo}
              component={Link}
              to="/results"
              size="lg"
            >
              Results
            </Anchor>
            <Anchor
              className={styles.logo}
              component={Link}
              to="/about"
              size="lg"
            >
              About
            </Anchor>
          </Group>

          {/* <Group>
            <ColorSchemeToggle />
          </Group> */}
        </Flex>
      </AppShell.Header>

      <AppShell.Main px="0" h="100%">
        {children}
      </AppShell.Main>
    </AppShell>
  );
}
