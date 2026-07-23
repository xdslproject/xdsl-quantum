MAKEFLAGS += --no-builtin-rules
MAKEFLAGS += --no-builtin-variables

# allow overriding the name of the venv directory
VENV_DIR ?= .venv

# use activated venv if any
export UV_PROJECT_ENVIRONMENT=$(if $(VIRTUAL_ENV),$(VIRTUAL_ENV),$(VENV_DIR))

# allow overriding which extras are installed
VENV_EXTRAS ?= --all-extras
VENV_GROUPS ?= --all-groups

# default lit options
LIT_OPTIONS ?= -v --order=smart
PYTEST_OPTIONS ?= -vv

define print_help
	@C="\033[$${1}32m"; R='\033[0m'; \
	 printf "%b" "Usage: make $${C}<target>$${R}\n\n"; \
	 printf "Available targets:\n"; \
	 grep -E '^[a-zA-Z_-]+:.*?##' $(MAKEFILE_LIST) | \
	   sort | \
	   awk "BEGIN {FS = \":.*?## \"}; {printf \"  $${C}%-$(2)s$${R} %s\n\", \$$1, \$$2}"
endef

HELP_COLOR := 1;32 # bright green
HELP_COLUMN_WIDTH := 25

.DEFAULT_GOAL := help

.PHONY: help
help: ## show this help message
	$(call print_help,$(HELP_COLOR),$(HELP_COLUMN_WIDTH))

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

.PHONY: pytest
pytest: uv-installed ## run pytest tests
	uv run pytest -W error $(PYTEST_OPTIONS)

.PHONY: filecheck
filecheck: uv-installed ## run filecheck tests
	uv run lit $(LIT_OPTIONS) tests/filecheck

.PHONY: pyright
pyright: uv-installed ## run pyright
	uv run pyright $(shell git diff --staged --name-only  -- '*.py')

.PHONY: tests-functional
tests: pytest filecheck ## run functional tests

.PHONY: tests
tests: tests-functional pyright ## run all tests

.PHONY: docs
docs: uv-installed ## Build and serve documentation
	uv run mkdocs serve
	uv run mkdocs build

.PHONY: sync
sync:
	uvx sync-template sync ## sync repository to xdsl-template

.PHONY: clean-caches
clean-caches: ## Delete various cashes
	rm -rf .mypy_cache/ .pytest_cache/ .ruff_cache/ .coverage
	find . -not -path "./.venv/*" | \
		grep -E "(/__pycache__$$|\.pyc$$|\.pyo$$)" | \
		xargs rm -rf

.PHONY: clean
clean: clean-caches ## Clean caches and venv
	rm -rf ${VENV_DIR}
