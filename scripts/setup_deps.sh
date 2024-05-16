#!/bin/bash

# Function to execute an installation script
function execute_install_script() {
    script_path=$1
    use_sudo=$2  # Flag to determine if 'sudo' should be used

    if [ -f "$script_path" ]; then
        echo "Executing installation script: $script_path"
        if $use_sudo; then
            sudo bash "$script_path"
        else
            bash "$script_path"
        fi
    else
        echo "Error: Installation script not found at $script_path"
        exit 1
    fi
}

# Detect the operating system and check for sudo
OS=$(uname -s)

if command -v sudo &> /dev/null; then  
    has_sudo=true
else
    has_sudo=false
fi

case "$OS" in
    "Darwin") 
        execute_install_script "scripts/os/setup_deps_macos.sh" false
        ;;
    "Linux")
        execute_install_script "scripts/os/setup_deps_linux.sh" $has_sudo
        ;;
    "MINGW64"* | "CYGWIN"* | "MSYS"*)  # Covers different Windows environments
        powershell.exe -File "scripts/os/setup_deps_windows.ps1" -ExecutionPolicy Bypass -Scope Process -Force
        ;;
    *)
        echo "Unsupported operating system: $OS"
        exit 1
        ;;
esac