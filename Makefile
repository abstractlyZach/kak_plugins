all: format test lint typecheck

test:
	poetry run pytest --cov -m "not os"

format:
	# reformat all files
	poetry run black .
	poetry run isort .

lint:
	poetry run flake8

typecheck:
	poetry run mypy .
