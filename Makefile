.PHONY: clean lint requirements jupyter venv

#################################################################################
# GLOBALS                                                                       #
#################################################################################
PROJECT_NAME = iefp
VENV_DIR = env
NOTEBOOK_DIR = notebooks

PYTHON_INTERPRETER = $(VENV_DIR)/bin/python3
PIP = $(VENV_DIR)/bin/pip

#################################################################################
# COMMANDS                                                                      #
#################################################################################
all: clean requirements

## Delete all compiled Python files
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete

jupyter:
	@echo "Running jupyter notebook in background..."
	@$(VENV_DIR)/bin/jupyter notebook --notebook-dir=$(NOTEBOOK_DIR)

lint:
	@$(PYTHON_INTERPRETER) -m flake8 --max-line-length=90 ./src

## Install Python Dependencies
requirements: venv
	$(PIP) install -U pip setuptools wheel
ifneq ($(wildcard ./setup.py),)
	$(PIP) install -e .
endif
ifneq ($(wildcard ./requirements.txt),)
	$(PIP) install -r requirements.txt
endif
	@echo "Installing jupyter kernel..."
	@$(PYTHON_INTERPRETER) -m ipykernel install --sys-prefix --name=$(PROJECT_NAME)

## Install virtual environment
venv:
ifeq ($(wildcard $(VENV_DIR)/*),)
	@echo "Did not find $(VENV_DIR), creating..."
	mkdir -p $(VENV_DIR)
	python3 -m venv $(VENV_DIR)
endif
