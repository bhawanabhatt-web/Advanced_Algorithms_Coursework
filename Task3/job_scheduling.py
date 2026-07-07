from __future__ import annotations
import bisect
from dataclasses import dataclass
__all__ = ["Job", "SchedulingResult", "weighted_job_scheduling"]

@dataclass(frozen=True)
class Job:
    start: int
    end: int
    profit: int

    def __post_init__(self) -> None:
        if self.end <= self.start:
            raise ValueError(f"Job end ({self.end}) must be after start ({self.start}).")
        if self.profit < 0:
            raise ValueError(f"Job profit must be non-negative, got {self.profit}.")

@dataclass
class SchedulingResult:
    max_profit: int
    selected_jobs: list[Job]

def weighted_job_scheduling(jobs: list[Job]) -> SchedulingResult:
    
    if not jobs:
        return SchedulingResult(max_profit=0, selected_jobs=[])

    sorted_jobs = sorted(jobs, key=lambda job: job.end)
    end_times = [job.end for job in sorted_jobs]
    n = len(sorted_jobs)

    # dp[i] = best achievable profit using the first i jobs (1-indexed).
    dp = [0] * (n + 1)
    include_job = [False] * (n + 1)

    for i in range(1, n + 1):
        current_job = sorted_jobs[i - 1]
        latest_compatible = _latest_non_conflicting_index(end_times, current_job.start, i - 1)

        profit_if_included = current_job.profit
        if latest_compatible != -1:
            profit_if_included += dp[latest_compatible + 1]

        profit_if_excluded = dp[i - 1]

        if profit_if_included > profit_if_excluded:
            dp[i] = profit_if_included
            include_job[i] = True
        else:
            dp[i] = profit_if_excluded

    selected_jobs = _reconstruct_selection(sorted_jobs, end_times, include_job)
    return SchedulingResult(max_profit=dp[n], selected_jobs=selected_jobs)

def _latest_non_conflicting_index(end_times: list[int], start_time: int, upper_bound: int) -> int:
    return bisect.bisect_right(end_times, start_time, 0, upper_bound) - 1


def _reconstruct_selection(
    sorted_jobs: list[Job], end_times: list[int], include_job: list[bool]
) -> list[Job]:

    selected: list[Job] = []
    i = len(sorted_jobs)
    while i > 0:
        if include_job[i]:
            job = sorted_jobs[i - 1]
            selected.append(job)
            i = _latest_non_conflicting_index(end_times, job.start, i - 1) + 1
        else:
            i -= 1
    selected.reverse()
    return selected