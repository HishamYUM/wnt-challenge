## Context

A small event ticketing API built with Django and DRF.

Three endpoints:
- `GET /api/events/`  list events
- `GET /api/events/<uuid>/`  event detail
- `POST /api/events/<uuid>/purchase/`  buy tickets

## Setup

```
uv sync
uv run python manage.py migrate
uv run python manage.py seed_data
uv run python manage.py runserver
```

## Your task

Review the codebase, identify what you think should be improved, and fix it.

Rules:
- Do not change the database schema (no adding or removing fields/models)
- Do not add new functionality. The scope stays the same: listing events and simulating ticket purchases
- Keep the existing tech stack (DRF, SQLite)
- Focus on code quality, correctness, and performance
- Write a `DECISIONS.md` file. For each change you made, add one entry in this format:
  ```
  - **What:** one line describing the change
    **Why:** 1 to 2 sentences explaining the reason
  ```

## Submit

Click "Use this template" at the top of this repo to create your own copy, do your work there, and when you're done reply to the email you received with the link to your repo.
