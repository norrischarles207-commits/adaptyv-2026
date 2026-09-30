#!/usr/bin/env bash
# Run a command, tee its combined stdout+stderr to a log file, and exit with the
# COMMAND's real status -- not tee's.
#
# WHY: the v3c two-arm launch was typed as
#     modal run ... | tee v3c-core.log && modal run ... --run-tag phase1-v3c-q408
# In a pipeline the shell's exit status is the LAST stage (tee), not modal, so
# `&&` fired on tee's success and Arm B launched even though Arm A had died on
# the disabled workspace. See challenges/egfr/methods.md (2026-09-30, Correction 2).
#
# `set -o pipefail` makes the pipeline's status the first failing stage, so a
# chained launch sees modal's real exit code.
#
# Usage:
#   modal/run_logged.sh <logfile> -- <command> [args...]
# Chained safely:
#   modal/run_logged.sh a.log -- modal run ... --run-tag arm-a \
#     && modal/run_logged.sh b.log -- modal run ... --run-tag arm-b
set -euo pipefail

if [ "$#" -lt 2 ]; then
  echo "usage: $0 <logfile> -- <command> [args...]" >&2
  exit 2
fi
log="$1"; shift
if [ "${1:-}" = "--" ]; then shift; fi

# pipefail (set above) makes this exit with "$@"'s status when it fails, even
# though tee succeeds; set -e then propagates that non-zero status.
"$@" 2>&1 | tee "$log"
