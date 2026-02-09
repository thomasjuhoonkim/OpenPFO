// eslint-disable-next-line simple-import-sort/imports
import Highcharts, { type Options } from "highcharts";
import HighchartsReact from "highcharts-react-official";

import "highcharts/themes/adaptive";
import "highcharts/modules/accessibility";
import "highcharts/modules/exporting";
import "highcharts/modules/parallel-coordinates";

import { useMemo } from "react";

import type { Job, Results } from "@/types/results";

export function PointParallelCoordinates({
  results,
  jobs,
  title,
}: {
  results: Results;
  jobs: Job[];
  title: string;
}) {
  const series = jobs.map((job) => ({
    data: job.point.variables.map((variable) => variable.value),
    color: job.runOk ? "rgba(255, 206, 47, 0.5)" : "rgba(198, 9, 15, 0.5)",
    name: `${job.id}${job.runOk ? "" : " (failed)"}`,
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
        categories: results.config.model.parameters.map(
          (parameter) => parameter.name
        ),
      },
      yAxis: results.config.model.parameters.map((parameter) => ({
        min: parameter.min,
        max: parameter.max,
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
