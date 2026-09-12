.PHONY: install run debug clean lint

VENV = venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip
CONFIG = config.txt

install:
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

run:
	$(PYTHON) a_maze_ing.py $(CONFIG)

debug:
	$(PYTHON) -m pdb a_maze_ing.py $(CONFIG)

clean:
	rm -rf $(VENV)
	find . -type -name "__pycache__"
	find . -type -name ".mypy_cache"

lint:
	$(VENV)/bin/flake8 .
	$(VENV)/bin/mypy . --warn-return-any --warn-unused-ignores --ignore-missing-import --disallow-untyped-defs --check-untyped-defs

lint-strict:
	$(VENV)/bin/mypy . --strict
