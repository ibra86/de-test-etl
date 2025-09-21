# Minimal Makefile for Docker Compose project

DC := docker compose
TEST_PATH ?= tests
PYTEST_OPTS ?=

.PHONY: build up up-d down logs reset-db etl test test-cov

build:
	$(DC) build

up:
	$(DC) up --build

up-d:
	$(DC) up -d --build

down:
	$(DC) down

logs:
	$(DC) logs -f

reset-db:
	$(DC) down -v

etl:
	$(DC) run --rm etl python -m etl.main

test:
	$(DC) run --rm etl sh -lc "python -m pip install -q --no-cache-dir --root-user-action=ignore pytest && python -m pytest -q $(PYTEST_OPTS) $(TEST_PATH)"

.PHONY: test-cov
test-cov:
	$(DC) run --rm etl sh -lc "python -m pip install -q --no-cache-dir --root-user-action=ignore pytest pytest-cov && python -m pytest --cov=. --cov-report=term-missing $(PYTEST_OPTS) $(TEST_PATH)"
