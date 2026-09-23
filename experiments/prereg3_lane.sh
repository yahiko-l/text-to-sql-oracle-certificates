#!/usr/bin/env bash
# Run several Preregistration 3 jobs one after another on the same cards, so that one screen
# session and one waiter cover a lane. A failing job does not stop the lane; the exit code is
# the number of failed jobs and every job's exit code is printed at the end.
#
#   experiments/prereg3_lane.sh <tag>:<stage>[:<seed>] ...
set -uo pipefail
fails=0; report=()
for job in "$@"; do
  IFS=: read -r tag stage seed <<< "$job"
  echo "=== LANE JOB $job  $(date -u +%FT%TZ)"
  bash experiments/prereg3_run.sh "$tag" "$stage" ${seed:-}
  code=$?
  echo "=== LANE JOB $job exit=$code  $(date -u +%FT%TZ)"
  report+=("$job exit=$code")
  [ "$code" -eq 0 ] || fails=$((fails+1))
done
printf '%s\n' "LANE SUMMARY:" "${report[@]}"
exit $fails
