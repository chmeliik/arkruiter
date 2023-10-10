venv:
	if command -v virtualenv; then virtualenv venv; else python -m venv venv; fi
	venv/bin/pip install pdm
	venv/bin/pdm install -G dev

.PHONY: update-venv
update-venv: venv
	venv/bin/pdm self update
	venv/bin/pdm sync -G dev

.PHONY: update-deps
update-deps: venv
	venv/bin/pdm update -G dev

.PHONY: check
check: venv
	venv/bin/black --check --diff .
	venv/bin/ruff check .
	venv/bin/pyright

.PHONY: autofix
autofix: venv
	venv/bin/black .
	venv/bin/ruff check --fix .

.PHONY: test
test: venv
	venv/bin/pytest

.PHONY: unittest
unittest: venv
	venv/bin/pytest -m 'not network'
