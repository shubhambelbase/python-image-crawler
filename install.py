import sys
import subprocess
import time
import os
import platform

def check_python():
    print(f"Checking Python installation...")
    print(f"Current Python: {sys.version}")
    # Obviously if this script is running, Python is installed.
    # However, we can check for minimum version.
    if sys.version_info < (3, 7):
        print("Error: Python 3.7 or newer is required.")
        print("Please download and install it from https://www.python.org/downloads/")
        input("Press Enter to exit...")
        sys.exit(1)
    print("Python version is compatible.")

def install_requirements():
    print("\nChecking and installing requirements...")
    req_file = "requirements.txt"
    if not os.path.exists(req_file):
        print(f"Error: {req_file} not found!")
        input("Press Enter to exit...")
        sys.exit(1)

    try:
        # Upgrade pip first
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
        # Install requirements
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", req_file])
        print("\nSUCCESS: All requirements installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"\nERROR: Failed to install requirements. Error code: {e.returncode}")
        print("Try running this script as Administrator.")
        input("Press Enter to exit...")
        sys.exit(1)

if __name__ == "__main__":
    print("=== Image Crawler Installer ===")
    check_python()
    install_requirements()
    print("\nInstallation complete! You can now run 'start.py'.")
    print("Closing in 5 seconds...")
    time.sleep(5)
