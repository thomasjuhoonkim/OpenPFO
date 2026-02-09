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
      const failedKey = { from: from.id, to: `failed-${from.id}` };
      const nextKey = { from: from.id, to: to.id };
      const successKey = { from: to.id, to: "success" };
      count.set(failedKey, (count.get(failedKey) || 0) + from.runOk ? 0 : 1);
      count.set(nextKey, (count.get(nextKey) || 0) + from.runOk ? 1 : 0);
      // if (to.id === "cleanup") {
      //   count.set(successKey, (count.get(successKey) || 0) + to.runOk ? 1 : 0);
      // }
    }
  });
  const data = [];
  count.forEach((value, key) => data.push([key.from, key.to, value]));
  console.log(data);

  const series = [
    {
      keys: ["from", "to", "weight"],

      nodes: [
        ...steps.map((step) => ({ id: step, color: "#ffce2f" })),
        // { id: "failed", color: "red" },
        ...steps.map((step) => ({ id: `failed-${step}`, color: "red" })),
        { id: "success", color: "green" },
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
