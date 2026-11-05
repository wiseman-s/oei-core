.PHONY: install lint format type test cov gate clean docker docs

install:
	python -m pip install -e ".[dev]"
	pre-commit install

lint:
	ruff check .

format:
	ruff format src tests

type:
	mypy src

test:
	pytest

cov:
	pytest --cov-report=html

gate: lint type test
	ruff format --check src tests

docker:
	docker build -t oei-core:local .

docs:
	mkdocs serve

clean:
	rm -rf build dist *.egg-info .pytest_cache .mypy_cache .ruff_cache htmlcov .coverage site