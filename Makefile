CONFIG ?= config.txt
VENV = .venv
PYTHON = $(VENV)/bin/python
FLAKE8 = $(VENV)/bin/flake8
MYPY = $(VENV)/bin/mypy

$(VENV)/bin/python:
	python3 -m venv $(VENV)

install: $(VENV)/bin/python
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -r requirements.txt
	$(PYTHON) -m pip install mazegen-*-py3-none-any.whl

run: $(VENV)/bin/python
	$(PYTHON) a_maze_ing.py $(CONFIG)

debug: $(VENV)/bin/python
	$(PYTHON) -m pdb a_maze_ing.py $(CONFIG)

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +

fclean: clean
	rm -rf $(VENV)

lint: $(VENV)/bin/python
	$(FLAKE8) --exclude=$(VENV) .
	$(MYPY) --exclude $(VENV) . --warn-return-any --warn-unused-ignores --ignore-missing-imports \
		--disallow-untyped-defs --check-untyped-defs

lint-strict: $(VENV)/bin/python
	$(FLAKE8) --exclude=$(VENV) .
	$(MYPY) --exclude $(VENV) . --strict

.PHONY: install run debug clean fclean lint lint-strict