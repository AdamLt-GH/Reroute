#!/usr/bin/env bash

set -euo pipefail

# run from the repository root so every path stays predictable
cd "$(dirname "$0")/.."

.venv/bin/ruff format --check apps/api
.venv/bin/ruff check apps/api
.venv/bin/mypy apps/api/app
.venv/bin/pytest apps/api/tests
