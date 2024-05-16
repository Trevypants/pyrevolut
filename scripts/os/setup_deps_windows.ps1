# Function to check if a package is installed and install if necessary
function Check-And-Install {
    param (
        [string]$PackageName,
        [string]$InstallCommand
    )

    if (!(Get-Command $PackageName -ErrorAction SilentlyContinue)) {
        Write-Host "$PackageName not found. Installing..."
        if (!($InstallCommand | Invoke-Expression)) {
            Write-Host "Error: Failed to install $PackageName"
            Exit 1
        }
        Write-Host "$PackageName installed successfully"
    } else {
        Write-Host "$PackageName is already installed"
    }
}


# ***** MAIN SETUP SCRIPT ***** 

# 1. Install Chocolatey if not already present
Check-And-Install "choco" "[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))"

# 2. Install Scoop
Check-And-Install "scoop" 'iex "& {$(irm get.scoop.sh)} -RunAsAdmin"'

# 3. Install wget
Check-And-Install "wget" "choco install wget"

# 4. Install git
Check-And-Install "git" "choco install git"

# 5. Install gh
Check-And-Install "gh" "choco install gh"

# 6. Install pyenv
Check-And-Install "pyenv" "Invoke-WebRequest -UseBasicParsing -Uri 'https://raw.githubusercontent.com/pyenv-win/pyenv-win/master/pyenv-win/install-pyenv-win.ps1' -OutFile './install-pyenv-win.ps1'; &'./install-pyenv-win.ps1'"

# 7. Install pipx
Check-And-Install "pipx" "scoop install pipx"
pipx ensurepath

# 8. Install poetry
Check-And-Install "poetry" "pipx install poetry"
