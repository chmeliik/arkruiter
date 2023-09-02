.PHONY: venv
venv:
	virtualenv venv
	venv/bin/pip install pdm
	venv/bin/pdm install -G dev

check:
	venv/bin/black --check --diff .
	venv/bin/ruff check .
	venv/bin/pyright

autofix:
	venv/bin/black .
	# isort-only
	venv/bin/ruff check --fix .

test:
	venv/bin/pytest
