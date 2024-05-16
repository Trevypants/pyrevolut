# Function to check if a package is installed and install if necessary
function check_and_install() {
    package_name=$1
    install_command=$2

    if ! dpkg -s "$package_name" &> /dev/null; then
        echo "$package_name not found. Installing..."
        eval $install_command 
        echo "$package_name installed successfully"
    else
        echo "$package_name is already installed"
    fi
}

# ***** MAIN SETUP SCRIPT *****

# 1. Update package lists
apt-get update

# 2. Install snap
check_and_install "snap" "apt-get install -y snapd"

# 3. Install wget
check_and_install "wget" "apt-get install -y wget"

# 5. Install git
check_and_install "git" "apt-get install -y git"

# 6. Install gh
check_and_install "gh" "apt-get install -y gh"

# 7. Install pyenv
check_and_install "pyenv" "curl https://pyenv.run | bash"

# 8. Install pipx
check_and_install "pipx" "apt-get install -y pipx"
pipx ensurepath

# 9. Install poetry
check_and_install "poetry" "pipx install poetry"