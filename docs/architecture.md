# Architecture

Reroute has three main parts:

- a React frontend for planning inputs and schedule results
- a FastAPI backend for authentication, storage and schedule generation
- PostgreSQL for users, tasks, events and generated schedules

The solver uses plain Python objects and does not import FastAPI or SQLAlchemy.
The API maps saved records into those objects, runs the solver synchronously and
saves the result as a proposed schedule.

This keeps the project easy to run and makes the scheduling rules testable
without starting the web app or database.
