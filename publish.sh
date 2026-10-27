#!/bin/sh
# The ONLY publish route for scheduled runs and retries: gate, push, then IndexNow. Exits non zero on HOLD_REVIEW.
set -e
cd "$(dirname "$0")"
git fetch -q origin
python3 _legal_gate.py --changed origin/main || { echo "HOLD_REVIEW: not published"; exit 1; }
git push origin HEAD:main
