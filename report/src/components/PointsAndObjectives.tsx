// eslint-disable-next-line simple-import-sort/imports
import Highcharts, { type Options } from "highcharts";
import HighchartsReact from "highcharts-react-official";

import "highcharts/themes/adaptive";
import "highcharts/modules/accessibility";
import "highcharts/modules/exporting";
import "highcharts/modules/parallel-coordinates";
import "highcharts/highcharts-more";

import { useCallback, useMemo, useState } from "react";

import type { Job, Results } from "@/types/results";
import { getObjectiveRanges } from "@/util/getObjectiveRanges";
import { Divider, Flex } from "@mantine/core";

export function PointsAndObjectives({
  results,
  jobs,
  parallelTitle,
  radarTitle,
  isNormalized = false,
}: {
  results: Results;
  jobs: Job[];
  parallelTitle: string;
  radarTitle: string;
  isNormalized?: boolean;
}) {
  const [highlightedJobId, setHighlightedJobId] = useState<string | null>(null);

  const handleSeriesMouseOver = useCallback((jobId: string) => {
    setHighlightedJobId(jobId);
  }, []);

  const handleSeriesMouseOut = useCallback(() => {
    setHighlightedJobId(null);
  }, []);

  // ===========================================================================

  const parallelJobs = jobs;

  const parallelWithHighlight = useMemo(
    () =>
      parallelJobs.map((job) => ({
        data: job.point.variables.map((variable) => variable.value),
        color:
          highlightedJobId === job.id
            ? "white"
            : job.runOk
              ? "rgba(255, 206, 47, 0.5)"
              : "rgba(198, 9, 15, 0.5)",
        type: "spline",
        name: job.id,
        marker: false,
        opacity: 1,
        lineWidth: job.id === highlightedJobId ? 3 : 2,
      })),
    [parallelJobs, highlightedJobId]
  );

  const parallelCategories = useMemo(() => {
    return results.config.model.parameters.map((parameter) => parameter.name);
  }, [results]);

  const parallelYAxis = useMemo(() => {
    return results.config.model.parameters.map((parameter) => ({
      min: parameter.min,
      max: parameter.max,
      startOnTick: false,
      endOnTick: false,
    }));
  }, [results]);

  const parallelOptions: Options = useMemo(
    () => ({
      chart: {
        animation: false,
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
        marginTop: 150,
        marginBottom: 100,
        marginRight: 25,
        marginLeft: 0,
      },
      title: {
        text: parallelTitle,
      },
      subtitle: {
        text: "Source: OpenPFO",
      },
      tooltip: {
        followPointer: true,
      },
      xAxis: {
        categories: parallelCategories,
      },
      yAxis: parallelYAxis,
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
            mouseOver(this: Highcharts.Series) {
              this.graph?.toFront();
              this.area?.toFront();
              handleSeriesMouseOver(this.name);
            },
            mouseOut() {
              handleSeriesMouseOut();
            },
          },
        },
      },
      series: parallelWithHighlight,
    }),
    [
      results,
      parallelTitle,
      isNormalized,
      parallelWithHighlight,
      parallelYAxis,
      handleSeriesMouseOver,
      handleSeriesMouseOut,
    ]
  );

  // ===========================================================================

  const radarJobs = jobs.filter((job) => job.runOk);

  const radarWithHighlight = useMemo(
    () =>
      radarJobs.map((job) => ({
        data: job.objectives.map((objective) => objective.value),
        color:
          highlightedJobId === job.id
            ? "white"
            : `rgba(255, 206, 47, ${Math.max(1 / jobs.length, 0.01)})`,
        type: "line",
        marker: false,
        name: job.id,
        lineWidth: job.id === highlightedJobId ? 3 : 2,
      })),
    [radarJobs, highlightedJobId]
  );

  const radarCategories = useMemo(() => {
    return results.config.optimizer.objectives.map(
      (objective) => objective.name
    );
  }, [results]);

  const radarYAxis = useMemo(() => {
    return isNormalized
      ? {
          min: 0,
          max: 1,
          labels: {
            formatter(this: Highcharts.AxisLabelsFormatterContextObject) {
              return `${Number(this.value) * 100}%`;
            },
          },
        }
      : getObjectiveRanges(results).objectiveRanges.map((objective) => ({
          min: objective.min,
          max: objective.max,
        }));
  }, [results, isNormalized]);

  const radarOptions: Options = useMemo(
    () => ({
      chart: {
        animation: false,
        type: "spline",
        polar: true,
        parallelCoordinates: !isNormalized,
      },
      legend: {
        enabled: false,
      },
      title: {
        text: radarTitle,
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
        categories: radarCategories,
        tickmarkPlacement: "on",
      },
      yAxis: radarYAxis,
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
            mouseOver(this: Highcharts.Series) {
              this.graph?.toFront();
              this.area?.toFront();
              handleSeriesMouseOver(this.name);
            },
            mouseOut() {
              handleSeriesMouseOut();
            },
          },
        },
      },
      series: radarWithHighlight,
    }),
    [
      results,
      radarTitle,
      isNormalized,
      radarWithHighlight,
      radarYAxis,
      handleSeriesMouseOver,
      handleSeriesMouseOut,
    ]
  );

  // ===========================================================================

  return (
    <Flex gap={0} h="100%" w="100%">
      <HighchartsReact
        highcharts={Highcharts}
        options={parallelOptions}
        containerProps={{
          style: { height: "100%", width: "100%" },
          className: "highcharts-dark",
        }}
      />
      <Divider orientation="vertical" size="sm" />
      <HighchartsReact
        highcharts={Highcharts}
        options={radarOptions}
        containerProps={{
          style: { height: "100%", width: "100%" },
          className: "highcharts-dark",
        }}
      />
    </Flex>
  );
}
