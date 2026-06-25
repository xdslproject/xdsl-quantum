MAKEFLAGS += --warn-undefined-variables
SHELL := bash

# allow overriding which dependency groups are installed
VENV_GROUPS ?= --group dev --group docs

# set default lit options
LIT_OPTIONS ?= -v --order=smart


.PHONY: install
install: .venv/ pre-commit

.venv/:
	uv sync ${VENV_GROUPS}

.PHONY: pre-commit
pre-commit: .venv/
	uv run prek install

.PHONY: check
check: .venv/
	uv run prek run --all-files

.PHONY: pyright
pyright: .venv/
	uv run pyright $(shell git diff --staged --name-only  -- '*.py')

.PHONY: tests
tests: pytest filecheck

.PHONY: pytest
pytest: .venv/
	uv run pytest -W error --cov

.PHONY: filecheck
filecheck: .venv/
	uv run lit $(LIT_OPTIONS) tests/filecheck

.PHONY: docs
docs: .venv/
	uv run mkdocs serve
	uv run mkdocs build

.PHONY: sync
sync:
	uvx sync-template sync

.PHONY: clean-caches
clean-caches:
	rm -rf .mypy_cache/ .pytest_cache/ .ruff_cache/ .coverage
	find . -not -path "./.venv/*" | \
		grep -E "(/__pycache__$$|\.pyc$$|\.pyo$$)" | \
		xargs rm -rf

.PHONY: clean
clean: clean-caches
	rm -rf ${VENV_DIR}
