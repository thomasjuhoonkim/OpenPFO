from enum import Enum


class JobStatus(Enum):
    READY = "ready"
    RUNNING = "running"
    FAILED = "failed"
    COMPLETE = "complete"
