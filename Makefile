test:
	poetry run pytest --cov

format:
	# reformat all files
	poetry run black .
	fd --extension py \
	| xargs poetry run reorder-python-imports --exit-zero-even-if-changed --application-directories=.:src

lint:
	poetry run flake8

typecheck:
	poetry run mypy .
