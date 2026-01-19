from enum import Enum


class JobStatus(Enum):
    INITIALIZED = "initialized"
    READY = "ready"
    RUNNING = "running"
    FAILED = "failed"
    COMPLETE = "complete"
