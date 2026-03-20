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
  isNormalized = false,
}: {
  results: Results;
  jobs: Job[];
  title: string;
  isNormalized?: boolean;
}) {
  const transparency = jobs.length === 1 ? 1 : 0.5;
  const series = jobs.map((job) => ({
    data: job.objectives.map((objective) => objective.value),
    color: job.runOk
      ? `rgba(255, 206, 47, ${transparency})`
      : `rgba(198, 9, 15, ${transparency})`,
    name: job.id,
    marker: false,
  }));

  const objectiveCategories = useMemo(
    () =>
      results.config.optimizer.objectives.map((objective) =>
        isNormalized
          ? objective.name
          : `${objective.name} (${
              objective.type === "minimize"
                ? "Lower is better"
                : "High is better"
            })`
      ),
    [results, isNormalized]
  );

  const yAxis = useMemo(() => {
    if (isNormalized) {
      return results.config.optimizer.objectives.map(() => ({
        min: 0,
        max: 1,
        labels: {
          formatter(this: Highcharts.AxisLabelsFormatterContextObject) {
            return `${Number(this.value) * 100}%`;
          },
        },
      }));
    }

    return results.config.optimizer.objectives.map((objective) => ({
      reversed: objective.type === "minimize",
    }));
  }, [results, isNormalized]);

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
        categories: objectiveCategories,
      },
      yAxis,
      series,
    }),
    [title, objectiveCategories, yAxis, series]
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
