import { Text, Timeline } from "@mantine/core";
import dayjs from "dayjs";
import { upperFirst } from "lodash-es";
import {
  BoxIcon,
  BrushCleaningIcon,
  DatabaseIcon,
  PyramidIcon,
  SettingsIcon,
  SigmaIcon,
} from "lucide-react";

import type { Job, StepId } from "@/types/results";

function getStepIcon(stepId: StepId) {
  switch (stepId) {
    case "prepare":
      return <SettingsIcon />;
    case "geometry":
      return <BoxIcon />;
    case "mesh":
      return <PyramidIcon />;
    case "solve":
      return <SigmaIcon />;
    case "objectives":
      return <DatabaseIcon />;
    case "cleanup":
      return <BrushCleaningIcon />;
  }
}

export function StepTimeline({ job }: { job: Job }) {
  return (
    <Timeline active={job.steps.length} bulletSize={44}>
      {job.steps.map((step) => {
        const FORMAT = "YYYY MMM D, hh:mm:ss.SSS A";
        const startTime = dayjs(step.startTime);
        const endTime = dayjs(step.endTime);
        const differenceInSeconds = endTime.diff(startTime, "s", true);
        return (
          <Timeline.Item
            title={upperFirst(step.id)}
            bullet={getStepIcon(step.id)}
            color={step.runOk ? undefined : "red"}
            lineVariant={step.runOk ? "solid" : "dotted"}
          >
            <Text size="xs" mt={4}>
              Start time: {startTime.format(FORMAT)}
            </Text>
            <Text size="xs" mt={4}>
              End time: {endTime.format(FORMAT)}
            </Text>
            <Text size="xs" mt={4}>
              Duration: {differenceInSeconds} seconds
            </Text>
          </Timeline.Item>
        );
      })}
    </Timeline>
  );
}
