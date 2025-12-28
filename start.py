import subprocess
import sys
import time

def start_crawler():
    print("Starting Image Crawler...")
    try:
        # Launch the GUI script
        # Using subprocess.Popen to launch it independent of this script effectively
        subprocess.Popen([sys.executable, "image_crawler_gui.py"])
    except Exception as e:
        print(f"Error starting application: {e}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    start_crawler()
    # Close this starter window quickly
    time.sleep(1)
