import * as z from "zod";

const parameter = z.object({
  id: z.string(),
  name: z.string(),
  min: z.number(),
  max: z.number(),
});

const objective = z.object({
  id: z.string(),
  name: z.string(),
  type: z.enum(["maximize", "minimize"]),
  value: z.number().nullish(),
});

const config = z.object({
  compute: z.object({
    hpc: z.boolean(),
    processors_per_job: z.number(),
    max_job_workers: z.number(),
  }),
  model: z.object({
    parameters: z.array(parameter),
  }),
  optimizer: z.object({
    objectives: z.array(objective),
  }),
});

const stepId = z.enum([
  "prepare",
  "geometry",
  "mesh",
  "solve",
  "objectives",
  "cleanup",
]);
export type StepId = z.infer<typeof stepId>;

const step = z.object({
  id: stepId,
  runOk: z.boolean(),
  startTime: z.string(),
  endTime: z.string(),
  // executionTimeSeconds: z.number(), probably don't need this
});
export type Step = z.infer<typeof step>;

const variable = z.object({
  id: z.string(),
  name: z.string(),
  value: z.number(),
});

const point = z.object({
  representation: z.string(),
  variables: z.array(variable),
});

const job = z.object({
  id: z.string(),
  searchId: z.string(),
  status: z.enum(["ready", "running", "failed", "complete"]),
  runOk: z.boolean(),
  steps: z.array(step),
  startTime: z.string(),
  endTime: z.string(),
  jobDirectory: z.string(),
  point,
  objectives: z.array(objective),
  meta: z.record(z.string(), z.any()),
});
export type Job = z.infer<typeof job>;

const search = z.object({
  id: z.string(),
  jobs: z.array(z.string()),
  points: z.array(point),
  startTime: z.string(),
  endTime: z.string(),
});
export type Search = z.infer<typeof search>;

const workflow = z.object({
  jobs: z.array(job),
  searches: z.array(search),
});

const solution = z.object({
  point,
  objectives: z.array(objective),
});

export const results = z.object({
  config,
  workflow,
  solutions: z.array(solution),
  endTime: z.string(),
  startTime: z.string(),
  command: z.string(),
});
export type Results = z.infer<typeof results>;
