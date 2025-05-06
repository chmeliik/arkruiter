define make_venv
	uv sync --group dev
endef

.venv:
	$(call make_venv)

.PHONY: venv
venv:
	$(call make_venv)
	ln -sf .venv venv

.PHONY: check
check: .venv
	.venv/bin/ruff check .
	.venv/bin/ruff format --check --diff .
	source venv/bin/activate && pyright

.PHONY: autofix
autofix: .venv
	.venv/bin/ruff check --fix .
	.venv/bin/ruff format .

.PHONY: test
test: .venv
	.venv/bin/pytest

.PHONY: unittest
unittest: .venv
	.venv/bin/pytest -m 'not network'
