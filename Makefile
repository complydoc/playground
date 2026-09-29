.PHONY: setup start trace ui cli python test baseline all

setup: ## Install complydoc and the LangChain packages the examples use
	uv sync

start: ## Two LangChain loaders compared and five LangChain splitters on their text: then `make ui`
	rm -rf .complydoc
	uv run python python/04_compare_loaders.py > /dev/null
	uv run complydoc chunks documents --extractor pypdf --no-ocr --preset common --name chunks -q

trace: ## The pipeline, observed twice: as written and with masking
	uv run python pipeline.py
	uv run python pipeline.py --mask

ui: ## Open every run in .complydoc in the browser
	uv run complydoc ui

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
