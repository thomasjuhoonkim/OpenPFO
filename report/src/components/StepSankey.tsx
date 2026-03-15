// eslint-disable-next-line simple-import-sort/imports
import Highcharts, { type Options } from "highcharts";
import HighchartsReact from "highcharts-react-official";

import "highcharts/themes/adaptive";
import "highcharts/modules/accessibility";
import "highcharts/modules/exporting";
import "highcharts/modules/sankey";

import { useMemo } from "react";

import type { Job, Results, StepId } from "@/types/results";

export function StepSankey({
  results,
  jobs,
  title,
}: {
  results: Results;
  jobs: Job[];
  title: string;
}) {
  const steps: StepId[] = [
    "prepare",
    "geometry",
    "mesh",
    "solve",
    "objectives",
    "cleanup",
  ];
  const count = new Map();
  jobs.forEach((job) => {
    for (let i = 0; i < job.steps.length - 1; i++) {
      const from = job.steps[i];
      const to = job.steps[i + 1];
      const failedStepKey = { from: from.id, to: `failed-${from.id}` };
      const nextStepKey = { from: from.id, to: to.id };
      const failedCleanupKey = { from: `failed-${from.id}`, to: to.id };
      count.set(
        failedStepKey,
        (count.get(failedStepKey) || 0) + from.runOk ? 0 : 1
      );
      count.set(
        nextStepKey,
        (count.get(nextStepKey) || 0) + from.runOk ? 1 : 0
      );
      if (!job.runOk && to.id === "cleanup") {
        count.set(
          failedCleanupKey,
          (count.get(failedCleanupKey) || 0) + to.runOk ? 1 : 0
        );
      }
    }
  });

  const data: [string, string, number][] = [];
  count.forEach((value, key) => data.push([key.from, key.to, value]));
  data.sort((a, b) => a[0].localeCompare(b[0]));
  data.sort((a, b) => a[1].localeCompare(b[1]));

  const series = [
    {
      keys: ["from", "to", "weight"],

      nodes: [
        ...steps.map((step, i) => ({
          id: step,
          color: "#ffce2f",
          column: i,
        })),
        // { id: "failed", color: "red" },
        ...steps.map((step, i) => ({
          id: `failed-${step}`,
          color: "red",
          column: i + 1,
        })),
        { id: "success", color: "green", column: steps.length },
      ],

      data,

      type: "sankey",
    },
  ];

  const options: Options = useMemo(
    () => ({
      chart: {
        zooming: {
          type: "xy",
        },
        panning: {
          enabled: true,
          type: "xy",
        },
        panKey: "shift",
        margin: 200,
      },
      title: {
        text: title,
      },
      subtitle: {
        text: "Source: OpenPFO",
      },
      tooltip: {
        followPointer: true,
      },
      series,
    }),
    [results, jobs]
  );

  return (
    <HighchartsReact
      highcharts={Highcharts}
      options={options}
      containerProps={{
        style: { height: "100%" },
        className: "highcharts-dark",
      }}
    />
  );
}
