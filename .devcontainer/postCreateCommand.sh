#!/bin/zsh

# create venv in project, for use as default python interpreter. This also configures vscode extensions to use the poetry venv
poetry config virtualenvs.in-project true --local

# install dependencies
poetry install --no-interaction --no-ansi --quiet

# activate venv
source $(poetry env info --path)/bin/activate
