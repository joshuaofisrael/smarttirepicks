#!/bin/sh
# The ONLY publish route for scheduled runs and retries: gate, push, then IndexNow. Exits non zero on HOLD_REVIEW.
# Gate passes a file only if it has no flags, has a SAFE moderate clearance for its exact sha256 (MODERATE rules only),
# or has Joshua's approval for its exact sha256 (required for HIGH rules 1, 2, 6, 8).
set -e
cd "$(dirname "$0")"
git fetch -q origin
CHANGED=$(git diff --name-only --diff-filter=ACMR origin/main HEAD -- '*.html' | sed 's#index\.html$##')
python3 _legal_gate.py --changed origin/main || { echo "HOLD_REVIEW: not published"; exit 1; }
git push origin HEAD:main
if [ -n "$CHANGED" ]; then
  URLS=$(for p in $CHANGED; do printf '"https://smarttirepicks.com/%s",' "$p"; done | sed 's/,$//')
  curl -s -o /dev/null -w "IndexNow %{http_code}\n" -H 'Content-Type: application/json' -d "{\"host\":\"smarttirepicks.com\",\"key\":\"df4a0d3d21dcab6c5b5e47393747f2b2\",\"keyLocation\":\"https://smarttirepicks.com/df4a0d3d21dcab6c5b5e47393747f2b2.txt\",\"urlList\":[$URLS]}" https://api.indexnow.org/indexnow || true
fi
