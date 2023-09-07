.PHONY: venv
venv:
	if command -v virtualenv; then virtualenv venv; else python -m venv venv; fi
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

unittest:
	venv/bin/pytest -m 'not network'
