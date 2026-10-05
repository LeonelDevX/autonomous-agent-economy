.PHONY: setup test lint typecheck doctor demo

setup:
	python -m venv .venv && . .venv/bin/activate && pip install -e ".[dev]"

test:
	pytest

lint:
	ruff check .

typecheck:
	mypy src

doctor:
	agent-economy doctor

demo:
	agent-economy demo
