import type { Job, Results } from "@/types/results";

import { getObjectiveRanges } from "./getObjectiveRanges";

function getNormalizedValue(
  value: number,
  min: number,
  max: number,
  invert: boolean
) {
  return invert ? (max - value) / (max - min) : (value - min) / (max - min);
}

export function getNormalizedJobs(results: Results, jobs: Job[]) {
  const { minObjectiveValuesByObjectiveId, maxObjectiveValuesByObjectiveId } =
    getObjectiveRanges(results);

  const jobsWithNormalizedObjectives = jobs.map((job) => ({
    ...job,
    objectives: job.objectives.map((objective) => ({
      ...objective,
      value: objective.value
        ? getNormalizedValue(
            objective.value,
            minObjectiveValuesByObjectiveId[objective.id],
            maxObjectiveValuesByObjectiveId[objective.id],
            objective.type === "minimize"
          )
        : undefined,
    })),
  }));

  return jobsWithNormalizedObjectives;
}
