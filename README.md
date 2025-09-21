# ETL Pipeline Demo

![CI](https://github.com/ibra86/de-test-etl/actions/workflows/ci.yml/badge.svg)


A lightweight **ETL (Extract–Transform–Load) pipeline** built as a demonstration of modern **Data Engineering practices**.  
It ingests raw JSON data, transforms it into a relational schema, and loads the results into a PostgreSQL database.  

The project is fully containerized with **Docker Compose**, uses **Alembic** for schema migrations, and includes **tests** to ensure reliability.

---

## Features

- **Dockerized stack**: PostgreSQL, Alembic migrations, ETL service  
- **ETL workflow**:
  - Extract: read raw JSON input
  - Transform: normalize into structured tables
  - Load: insert into PostgreSQL with upserts  
- **Schema migrations** managed with Alembic  
- **Testing** using `pytest`  
- **Reproducible builds** with `Makefile` shortcuts  
- **Dependency management** with [uv](https://github.com/astral-sh/uv)

---

## Project Structure

```
.
├── data/                 # Raw input data (JSON)
├── db/                   # Database models & Alembic migrations
├── etl/                  # ETL logic (extract, transform, load)
├── tests/                # Pytest-based tests
├── docker-compose.yml    # Container orchestration
├── Dockerfile            # Build ETL image
├── Makefile              # Developer shortcuts
├── pyproject.toml        # Project config
├── uv.lock               # uv lockfile
└── README.md             # Project documentation
```

---

## Quickstart

### 1. Build and start the stack
```bash
make up-d
```

### 2. Run database migrations
```bash
make migrate
```

### 3. Run the ETL pipeline
```bash
make etl
```

### 4. Run tests
```bash
make test
```

---

## Testing

Run all tests:

```bash
make test
```

Run tests with coverage:

```bash
make test-cov
```

---

## Local Development (without Docker)

This project uses [uv](https://github.com/astral-sh/uv) for dependency management.  
You need to install `uv` first (e.g., via `pip install uv` or your package manager).

Install dependencies:

```bash
uv sync
```

Run ETL locally:

```bash
uv run python -m etl.main
```

Run tests:

```bash
uv run pytest -q
```

---

## Build & Install (Hatchling)

This project uses [Hatchling](https://hatch.pypa.io/latest/hatchling/) as the build backend, specified in `pyproject.toml`.

### Build the package
```
uv build
```

This produces distribution artifacts in `dist/`:
- `de_test_etl-0.1.0.tar.gz` (source distribution)
- `de_test_etl-0.1.0-py3-none-any.whl` (wheel)

### Install the package locally
```
uv pip install dist/de_test_etl-0.1.0-py3-none-any.whl
```

Or in editable mode:
```
uv pip install -e .
```

---

## License

MIT License
