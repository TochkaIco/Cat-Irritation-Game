import os
import platform
import sys
import subprocess
import logging
from logging.handlers import RotatingFileHandler

LOG_FILE = "setup.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        RotatingFileHandler(LOG_FILE, maxBytes=1_000_000, backupCount=3),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

os_name = platform.system() # Identifying the platform
if os_name == "Windows":  # Path to venv
    venv_python = os.path.join(".venv", "Scripts", "python.exe")
else:
    venv_python = os.path.join(".venv", "bin", "python")

def command_exists(cmd):
    return subprocess.run(
        ["where", cmd],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    ).returncode == 0

def windows_setup():
    print("Detected Windows. Checking system dependencies...")

    try:
        print("Installing Git...")
        if not command_exists("git"):
            subprocess.run(["winget", "install", "--id", "Git.Git", "-e", "--source", "winget", "--silent"], check=True)

        print("Ensuring Python is installed...")
        if not command_exists("python"):
            subprocess.run(["winget", "install", "--id", "Python.Python.3.13", "-e", "--source", "winget", "--silent"],
                       check=True)
    except FileNotFoundError:
        logger.error("File not found", exc_info=True)
        raise

    print("Creating virtual environment...")
    subprocess.run([sys.executable, "-m", "venv", ".venv"], check=True)

    print("Installing requirements...")
    subprocess.run([venv_python, "-m", "pip", "install", "--upgrade", "pip"], check=False)
    subprocess.run([venv_python, "-m", "pip", "install", "requests"], check=True)
    if os.path.exists("requirements.txt"):
        subprocess.run([venv_python, "-m", "pip", "install", "-r", "requirements.txt"], check=True)

def linux_setup():
    global os_name
    global venv_python

    if os.path.exists("/usr/bin/pacman"): # Arch
        manager = "pacman"
        update_cmd = ["sudo", "pacman", "-Sy"]
        install_cmd = ["sudo", "pacman", "-S", "--noconfirm", "python", "python-pip", "git"]
    elif os.path.exists("/usr/bin/dnf"): # Fedora
        manager = "dnf"
        update_cmd = ["sudo", "dnf", "check-update"]
        install_cmd = ["sudo", "dnf", "install", "-y", "python3", "python3-pip", "git"]
    elif os.path.exists("/usr/bin/apt"): # Debian / Ubuntu
        manager = "apt"
        update_cmd = ["sudo", "apt", "update"]
        install_cmd = ["sudo", "apt", "install", "-y", "python3-full", "git"]
    else:
        logger.error("Unsupported package manager", exc_info=True)
        raise

    print(f"Detected {manager}. Updating and installing...")

    try:
        subprocess.run(update_cmd, check=False)
        # Run install
        subprocess.run(install_cmd, check=True)
        # Package Install
        os.chdir("..")
        subprocess.run([sys.executable, "-m", "venv", ".venv"]) # Creating and sourcing the venv
        subprocess.run([venv_python, "-m", "pip", "install", "requests"], check=True)
        subprocess.run([venv_python, "-m", "pip", "install", "-r", "requirements.txt"], check=True) # pip installing packages from requirements.txt
        print("Successfully installed git, python, python venv, pip and pip packages.")
    except subprocess.CalledProcessError as e:
        logger.error("Failed to install, error: {e}", exc_info=True)
        raise

try:
    if os_name!="Windows" and os_name!="Linux":
        logger.error(f"Only Windows and Linux systems are supported. Current platform: {os_name}", exc_info=True)

    # Calling the corresponding setup function
    if os_name == "Windows":
        windows_setup()
    elif os_name == "Linux":
        linux_setup()

except Exception as e:
    logger.critical("Fatal crash", exc_info=True)
    raise