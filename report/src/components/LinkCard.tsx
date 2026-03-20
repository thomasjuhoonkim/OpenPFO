import { Card, Center, Divider, Text } from "@mantine/core";
import { Link } from "@tanstack/react-router";
import type { ReactNode } from "react";

export function LinkCard({
  icon,
  title,
  description,
  href,
  target,
}: {
  icon: ReactNode;
  title: string;
  description: string;
  href: string;
  target?: string;
}) {
  return (
    <Card component={Link} to={href} withBorder p="0" w={200} target={target}>
      <Card.Section p="xl" pb="md">
        <Center>{icon}</Center>
      </Card.Section>
      <Divider />
      <Card.Section p="xl" pt="md">
        <Text fw={500}>{title}</Text>
        <Text size="sm" c="dimmed">
          {description}
        </Text>
      </Card.Section>
    </Card>
  );
}
