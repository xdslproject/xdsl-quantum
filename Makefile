MAKEFLAGS += --warn-undefined-variables
SHELL := bash

# allow overriding the name of the venv directory
VENV_DIR ?= .venv

# use activated venv if any
export UV_PROJECT_ENVIRONMENT=$(if $(VIRTUAL_ENV),$(VIRTUAL_ENV),$(VENV_DIR))

# allow overriding which extras are installed
VENV_EXTRAS ?= --all-extras
VENV_GROUPS ?= --all-groups

# set default lit options
LIT_OPTIONS ?= -v --order=smart
PYTEST_OPTIONS ?= -vv

.PHONY: uv-installed
uv-installed:
	@command -v uv &> /dev/null ||\
		(echo "UV doesn't seem to be installed, try the following instructions:" &&\
		echo "https://docs.astral.sh/uv/getting-started/installation/" && false)

# set up the venv with all dependencies for development
.PHONY: ${VENV_DIR}/
${VENV_DIR}/: uv-installed
	uv sync ${VENV_EXTRAS} ${VENV_GROUPS}

.PHONY: venv
venv: ${VENV_DIR}/ ## make sure `make venv` also works correctly

.PHONY: precommit-install
precommit-install: uv-installed ## set up all precommit hooks
	uv run prek install

.PHONY: precommit
precommit: uv-installed ## run all precommit hooks and apply them
	uv run prek run --all-files

.PHONY: pyright
pyright: uv-installed
	uv run pyright $(shell git diff --staged --name-only  -- '*.py')

.PHONY: tests
tests: pytest filecheck

.PHONY: pytest
pytest: uv-installed
	uv run pytest -W error --cov $(PYTEST_OPTIONS)

.PHONY: filecheck
filecheck: uv-installed
	uv run lit $(LIT_OPTIONS) tests/filecheck

.PHONY: docs
docs: uv-installed
	uv run mkdocs serve
	uv run mkdocs build

.PHONY: clean-caches
clean-caches:
	rm -rf .mypy_cache/ .pytest_cache/ .ruff_cache/ .coverage
	find . -not -path "./.venv/*" | \
		grep -E "(/__pycache__$$|\.pyc$$|\.pyo$$)" | \
		xargs rm -rf

.PHONY: clean
clean: clean-caches
	rm -rf ${VENV_DIR}
