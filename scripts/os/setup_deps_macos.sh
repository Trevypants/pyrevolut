#!/bin/bash

# Function to check if a package is installed and install if necessary
function check_and_install() {
    package_name=$1
    install_command=$2

    if ! command -v "$package_name" &> /dev/null; then
        echo "$package_name not found. Installing..."
        if ! $install_command; then
            echo "Error: Failed to install $package_name"
            exit 1
        fi
        echo "$package_name installed successfully"
    else
        echo "$package_name is already installed"
    fi
}


# ***** MAIN SETUP SCRIPT *****

# 1. Install Homebrew if not already present
check_and_install "brew" "/bin/bash -c \"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""

# 2. Install wget
check_and_install "wget" "brew install wget"

# 3. Install git
check_and_install "git" "brew install git"

# 4. Install gh
check_and_install "gh" "brew install gh"

# 5. Install pyenv
check_and_install "pyenv" "brew install pyenv"

# 6. Install pipx
check_and_install "pipx" "brew install pipx"
pipx ensurepath

# 7. Install poetry
check_and_install "poetry" "pipx install poetry"