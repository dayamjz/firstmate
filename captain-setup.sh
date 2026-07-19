#!/usr/bin/env bash
# captain-setup.sh — fork-local bootstrap for dayamjz's firstmate home.
#
# firstmate keeps its working state (projects/, data/, state/) machine-local and
# gitignored by design, so a fresh clone of this fork starts empty. This script
# provisions that state for dayamjz's fleet, idempotently:
#
#   1. clones dayamjz/travel-recommender into projects/ (if absent)
#   2. seeds data/projects.md with its registry entry (if absent)
#   3. seeds data/captain.md with starter preferences (if absent)
#
# Usage (on a fresh machine):
#   gh repo clone dayamjz/firstmate && cd firstmate && ./captain-setup.sh && claude
#
# Registry line format is parsed by bin/fm-project-mode.sh:
#   - <name> [<mode>] - <desc> (added <date>)
# mode no-mistakes = full pipeline -> PR -> captain merge (the safe default).
set -eu

FM_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECTS="$FM_ROOT/projects"
DATA="$FM_ROOT/data"
TODAY="$(date +%Y-%m-%d)"

mkdir -p "$PROJECTS" "$DATA"

# 1. Project clone
if [ -d "$PROJECTS/travel-recommender/.git" ]; then
  echo "ok: projects/travel-recommender already cloned"
else
  echo "cloning dayamjz/travel-recommender into projects/ ..."
  git clone https://github.com/dayamjz/travel-recommender "$PROJECTS/travel-recommender"
fi

# 2. Project registry (skip if the captain already has one — never clobber)
if [ -f "$DATA/projects.md" ]; then
  if grep -q "^- travel-recommender" "$DATA/projects.md"; then
    echo "ok: travel-recommender already registered in data/projects.md"
  else
    printf -- "- travel-recommender [no-mistakes] - Travel recommendations cron system: home + away modes, Slack delivery; build/QA commands in its AGENTS.md (added %s)\n" "$TODAY" >> "$DATA/projects.md"
    echo "ok: appended travel-recommender to existing data/projects.md"
  fi
else
  cat > "$DATA/projects.md" <<EOF
# Fleet projects

- travel-recommender [no-mistakes] - Travel recommendations cron system: home + away modes, Slack delivery; build/QA commands in its AGENTS.md (added $TODAY)
EOF
  echo "ok: wrote data/projects.md"
fi

# 3. Captain preferences (starter — edit freely; gitignored, machine-local)
if [ -f "$DATA/captain.md" ]; then
  echo "ok: data/captain.md already exists (left untouched)"
else
  cat > "$DATA/captain.md" <<'EOF'
# Captain preferences (dayamjz)

- Address me plainly; lead with outcomes, not mechanics.
- travel-recommender: always verify with `npx tsc --noEmit && npm run validate` and a
  `--dry-run` of any touched job before opening a PR (see its AGENTS.md).
- Never merge without my explicit approval (default posture; no yolo).
- Secrets live in GitHub Actions repo secrets / local .env only — never committed.
EOF
  echo "ok: wrote data/captain.md"
fi

echo
echo "Done. Launch your harness from this directory (e.g. 'claude') to start the first mate."
