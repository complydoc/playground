.PHONY: setup cli python test baseline all

setup: ## Install complydoc and the loaders the examples use
	uv sync

cli: ## Run every command line example
	for script in cli/*.sh; do echo "== $$script"; sh "$$script" || exit 1; done

python: ## Run every Python example
	for script in python/*.py; do echo "== $$script"; uv run python "$$script" || exit 1; done

test: ## Run the document tests
	uv run pytest -q

baseline: ## Rewrite the baseline report the CI diff compares against
	uv run complydoc audit documents --no-ocr --no-extracted-text \
		--out baseline --name report -q

all: cli python test
