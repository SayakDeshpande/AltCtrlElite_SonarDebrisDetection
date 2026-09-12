# SIH26057 database layer

This directory contains only the PostgreSQL/SQLAlchemy database layer for the
SIH26057 sonar-debris project. It does not include FastAPI routes, YOLO code,
file upload handling, or a frontend integration.

## Schema

The initial migration creates:

- `analysis_status` PostgreSQL enum: `queued`, `processing`, `completed`, and
  `failed`.
- `analyses`: one uploaded sonar image and its processing run.
- `detections`: one detected object/anomaly belonging to an analysis.

The migration also creates the `pgcrypto` extension so PostgreSQL can generate
UUID values with `gen_random_uuid()`.

## Setup

1. Create and activate a Python virtual environment.
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Copy `.env.example` to `.env`, then set `DATABASE_URL` with the credentials
   for the `sih26057` PostgreSQL database.
4. Export `DATABASE_URL` in your shell or IDE environment before using
   Alembic. The `.env` file is a reference template and is not loaded
   automatically.

## Apply the migration later

From the `backend` directory, after intentionally configuring PostgreSQL:

```bash
alembic upgrade head
```

No migration has been run by this scaffold. Running the command above is the
first operation that will create or alter database objects.

## Constraints

- Detection confidence is constrained to 0 through 100.
- Latitude is constrained to -90 through 90 when supplied.
- Longitude is constrained to -180 through 180 when supplied.
- Bounding-box x/y coordinates are non-negative.
- Bounding-box width and height must be greater than zero.
- Each detection belongs to one analysis through `analysis_id`; deleting an
  analysis cascades to its detections.
