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
    color: job.runOk ? "rgba(255, 206, 47, 0.33)" : "rgba(198, 9, 15, 0.33)",
    name: `${job.id}${job.runOk ? "" : " (failed)"}`,
    marker: false,
  }));

  const options: Options = useMemo(
    () => ({
      chart: {
        type: "spline",
        className: "parallel-coordinates-chart",
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
        marginTop: 150,
        marginBottom: 75,
        marginRight: 25,
        marginLeft: 0,
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
        startOnTick: false,
        endOnTick: false,
      })),
      plotOptions: {
        series: {
          states: {
            inactive: {
              enabled: false,
            },
            hover: {
              halo: {
                size: 0,
              },
            },
          },
          events: {
            mouseOver() {
              this.graph?.toFront();
              this.area?.toFront();
            },
          },
        },
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
