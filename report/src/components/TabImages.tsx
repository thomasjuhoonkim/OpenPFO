import type { Job } from "@/types/results";
import { Flex, Tabs, Image, Box, Title } from "@mantine/core";
import { useState } from "react";

const validExtensions = ["png", "jpg", "jpeg", "gif", "svg", "webp"];

export function TabImages({ job }: { job: Job }) {
  const meta = Object.entries(job.meta).filter(
    ([_, value]) =>
      typeof value === "string" &&
      validExtensions.includes(value.split(".").pop() || "")
  );

  const [activeKey, setActiveKey] = useState(meta[0][0]);

  const filename = job.meta[activeKey];

  if (!filename) {
    return (
      <Flex direction="column" align="center" justify="center" h="100%">
        <Title>No image available</Title>
      </Flex>
    );
  }

  const url = `/${job.id}/${filename}`;

  return (
    <Flex direction="column" h="100%" style={{ flexGrow: 1, minHeight: 0 }}>
      <Tabs
        value={activeKey}
        onChange={(value) => value && setActiveKey(value)}
      >
        <Tabs.List>
          {meta.map(([key]) => (
            <Tabs.Tab key={key} value={key}>
              {key}
            </Tabs.Tab>
          ))}
        </Tabs.List>
      </Tabs>

      <Box style={{ flexGrow: 1, minHeight: 0 }}>
        <Image src={url} fit="contain" height="100%" />
      </Box>
    </Flex>
  );
}
