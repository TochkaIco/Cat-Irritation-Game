import platform
import distro
import subprocess

def windows_setup():
    pass

def linux_setup():
    global distro_name

    match distro_name:
        case "Debian-Ubuntu":
            print(f"Entering Debian/Ubuntu installation steps...")
            try:
                subprocess.run(["sudo", "apt", "update"])
                subprocess.run(["sudo", "apt", "install", "-y", "python3-full","git"]) # Package Install
                subprocess.run(["cd", ".."])
                subprocess.run(["python", "-m", "venv", ".venv"]) # Creating and sourcing the venv
                subprocess.run(["source", ".venv/bin/activate"])
                subprocess.run(["pip", "install", "-r", "requirements.txt"]) # pip installing packages from requirenments.txt
                print("Successfully installed git, python, python venv, pip and pip packages.")
            except subprocess.CalledProcessError:
                raise RuntimeError("Failed to install. Do you have admin/sudo privileges?")

os_name = platform.system() # Identifying the platform
if os_name!="Windows" and os_name!="Linux":
    raise RuntimeError(f"Only Windows and Linux systems are supported. Current platform: {os_name}")

# Calling the corresponding setup function
if os_name == "Windows":
    windows_setup()
elif os_name == "Linux":
    distro_name = distro.name()
    if "Debian" in distro_name or "Ubuntu" in distro_name: # Verifying Linux distro type
        distro_name = "Debian-Ubuntu"
    elif "Fedora" in distro_name:
        distro_name = "Fedora"
    elif "Arch" in distro_name:
        distro_name = "Arch"
    else:
        raise RuntimeError(f"Unsupported Linux distro: {distro_name}")
    linux_setup()
