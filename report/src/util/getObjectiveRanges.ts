import type { Results } from "@/types/results";

export function getObjectiveRanges(results: Results) {
  const configObjectives = results.config.optimizer.objectives;

  const objectiveValuesByObjectiveId: Record<string, number[]> = {};
  results.workflow.jobs.forEach((job) => {
    job.objectives.forEach((objective) => {
      if (!(objective.id in objectiveValuesByObjectiveId)) {
        objectiveValuesByObjectiveId[objective.id] = [];
      }
      if (objective.value) {
        objectiveValuesByObjectiveId[objective.id].push(objective.value);
      }
    });
  });

  const maxObjectiveValuesByObjectiveId: Record<string, number> = {};
  configObjectives.forEach((objective) => {
    maxObjectiveValuesByObjectiveId[objective.id] = Math.max(
      ...objectiveValuesByObjectiveId[objective.id]
    );
  });
  const minObjectiveValuesByObjectiveId: Record<string, number> = {};
  configObjectives.forEach((objective) => {
    minObjectiveValuesByObjectiveId[objective.id] = Math.min(
      ...objectiveValuesByObjectiveId[objective.id]
    );
  });

  const objectiveRanges = configObjectives.map((objective) => {
    return {
      ...objective,
      min: minObjectiveValuesByObjectiveId[objective.id],
      max: maxObjectiveValuesByObjectiveId[objective.id],
    };
  });

  return {
    objectiveRanges,
    maxObjectiveValuesByObjectiveId,
    minObjectiveValuesByObjectiveId,
  };
}
