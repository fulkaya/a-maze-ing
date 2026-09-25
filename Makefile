CONFIG ?= config.txt
VENV = .venv
PYTHON = $(VENV)/bin/python

$(VENV)/bin/python:
	python3 -m venv $(VENV)

install: $(VENV)/bin/python
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -r requirements.txt

run: $(VENV)/bin/python
	$(PYTHON) a_maze_ing.py $(CONFIG)

debug: $(VENV)/bin/python
	$(PYTHON) -m pdb a_maze_ing.py $(CONFIG)

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +

lint:
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports \
		--disallow-untyped-defs --check-untyped-defs

lint-strict:
	flake8 .
	mypy . --strict

.PHONY: install run debug clean lint lint-strict