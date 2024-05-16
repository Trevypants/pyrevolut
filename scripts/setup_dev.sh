#!/bin/bash

# 1. Read the required Python version from your project's .python-version file
if [ -f ".python-version" ]; then
    PYTHON_VERSION=$(cat .python-version)
else 
    echo "Error: .python-version file not found"
    exit 1
fi

# 2. Check if pyenv is installed -- if not, install it
if ! command -v "pyenv" &> /dev/null; then
    echo "pyenv not found. Running setup_deps.sh to install dependencies..."
    bash scripts/setup_deps.sh
fi

# 3. Install the required Python version using pyenv
echo "Installing Python $PYTHON_VERSION using pyenv..."
pyenv install -s $PYTHON_VERSION # -s flag to skip prompts

# 4. Set the local Python version to the one you just installed
echo "Setting local repo Python version to $PYTHON_VERSION..."
pyenv local $PYTHON_VERSION

# 5. Install dependencies via poetry
echo "Installing dependencies via Poetry..."
poetry install

# 6. Set up pre-commit hooks
echo "Setting up pre-commit hooks..."
poetry run pre-commit install --hook-type commit-msg
wget -O .git/hooks/prepare-commit-msg https://raw.githubusercontent.com/commitizen-tools/commitizen/master/hooks/prepare-commit-msg.py
chmod +x .git/hooks/prepare-commit-msg

# 7. Set up post-commit hooks
echo "Setting up post-commit hooks..."
wget -O .git/hooks/post-commit https://raw.githubusercontent.com/commitizen-tools/commitizen/master/hooks/post-commit.py
chmod +x .git/hooks/post-commit