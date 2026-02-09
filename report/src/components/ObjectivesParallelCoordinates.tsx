// eslint-disable-next-line simple-import-sort/imports
import Highcharts, { type Options } from "highcharts";
import HighchartsReact from "highcharts-react-official";

import "highcharts/themes/adaptive";
import "highcharts/modules/accessibility";
import "highcharts/modules/exporting";
import "highcharts/modules/parallel-coordinates";

import { useMemo } from "react";

import type { Job, Results } from "@/types/results";

export function ObjectivesParallelCoordinates({
  results,
  jobs,
  title,
}: {
  results: Results;
  jobs: Job[];
  title: string;
}) {
  const series = jobs.map((job) => ({
    data: job.objectives.map((objective) => objective.value),
    color: job.runOk ? "rgba(255, 206, 47, 0.5)" : "rgba(198, 9, 15, 0.5)",
    name: job.id,
    marker: false,
  }));

  const options: Options = useMemo(
    () => ({
      chart: {
        type: "spline",
        parallelCoordinates: true,
        parallelAxes: {
          lineWidth: 2,
          labels: {
            x: 12,
          },
        },
        zooming: {
          type: "y",
        },
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
      xAxis: {
        categories: results.config.optimizer.objectives.map(
          (objective) =>
            `${objective.name} (${objective.type === "minimize" ? "Lower is better" : "High is better"})`
        ),
      },
      yAxis: results.config.optimizer.objectives.map((objective) => ({
        reversed: objective.type === "minimize",
      })),
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
