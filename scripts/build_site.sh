#!/usr/bin/env bash
# Use the same Pages-compatible renderer locally and in CI.
set -euo pipefail
source_dir="$(cd "$(dirname "$0")/.." && pwd)"
output_dir="${1:-$source_dir/_site}"
mkdir -p "$output_dir"
output_dir="$(cd "$output_dir" && pwd)"
if [[ "$source_dir" == "$output_dir" ]]; then
  echo "Build output must differ from the source directory." >&2
  exit 1
fi
image='ghcr.io/actions/jekyll-build-pages@sha256:a4ebed99056cd2a2c867cfce074d0cc92070855516b131ff099db3b3f961dfa9'
docker run --rm --platform linux/amd64 \
  --user "$(id -u):$(id -g)" \
  -e JEKYLL_ENV=production \
  -v "$source_dir:/src:ro" -v "$output_dir:/out" \
  --entrypoint sh "$image" -c \
  'cd /src && ruby scripts/test_note_contract.rb && ruby scripts/validate_notes.rb && ruby scripts/validate_note_images.rb && jekyll build --source /src --destination /out'
