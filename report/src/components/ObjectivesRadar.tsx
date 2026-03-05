// eslint-disable-next-line simple-import-sort/imports
import Highcharts, { type Options } from "highcharts";
import HighchartsReact from "highcharts-react-official";

import "highcharts/themes/adaptive";
import "highcharts/modules/accessibility";
import "highcharts/modules/exporting";
import "highcharts/highcharts-more";

import { useMemo } from "react";

import type { Job, Results } from "@/types/results";
import { getObjectiveRanges } from "@/util/getObjectiveRanges";

export function ObjectivesRadar({
  results,
  jobs,
  title,
  isNormalized = false,
}: {
  results: Results;
  jobs: Job[];
  title: string;
  isNormalized?: boolean;
}) {
  const series = jobs
    .filter((job) => job.runOk)
    .map((job) => ({
      data: job.objectives.map((objective) => objective.value),
      color: "rgba(255, 206, 47, 0.01)",
      type: "line",
      name: job.id,
      marker: false,
    }));

  const options: Options = useMemo(
    () => ({
      chart: {
        type: "spline",
        className: "radar-chart",
        polar: true,
        parallelCoordinates: !isNormalized,
      },
      legend: {
        enabled: true,
        navigation: {
          enabled: true,
        },
        maxHeight: 100,
      },
      title: {
        text: title,
      },
      subtitle: {
        text: "Source: OpenPFO",
      },
      pane: {
        startAngle: 0,
        endAngle: 360,
      },
      tooltip: {
        followPointer: true,
      },
      xAxis: {
        categories: results.config.optimizer.objectives.map(
          (objective) => objective.name
        ),
        tickmarkPlacement: "on",
      },
      yAxis: isNormalized
        ? {
            min: 0,
            max: 1,
          }
        : getObjectiveRanges(results).objectiveRanges.map((objective) => ({
            min: objective.min,
            max: objective.max,
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
            mouseOver: function () {
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
