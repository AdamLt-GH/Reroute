# Reroute

Reroute is a small scheduling app for rebuilding a weekly plan when something
unexpected happens.

Users can add fixed events, flexible tasks, availability and task dependencies.
The app finds free time, splits tasks into sessions and creates a proposed
schedule. Adding an unexpected event generates a revised proposal.

## Main features

- user registration and cookie based login
- fixed events with travel time
- flexible tasks with deadlines and session lengths
- weekly availability and task dependencies
- simple schedule generation and acceptance
- basic recalculation after an unexpected event

## Run with Docker

Docker is the shortest way to start the app:

```bash
docker compose up --build
```

Open `http://localhost:3000`. PostgreSQL data is kept in the
`postgres-data` volume.

## Run locally

Start PostgreSQL:

```bash
docker compose up postgres -d
```

Set up the API:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -e "apps/api[dev]"
alembic -c apps/api/alembic.ini upgrade head
uvicorn app.main:app --app-dir apps/api --reload
```

In another terminal, start the frontend:

```bash
npm install
npm run dev:web
```

The frontend runs on `http://localhost:5173` and the API runs on
`http://localhost:8000`.

## Checks

```bash
./scripts/check-api.sh
npm run lint:web
npm run typecheck:web
npm run test:web
npm run build:web
```

The scheduling algorithm is in
`apps/api/app/scheduling/solver.py`. It is intentionally a straightforward
Python implementation rather than a full optimisation system.
