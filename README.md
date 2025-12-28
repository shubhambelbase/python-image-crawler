# Image Crawler Pro

![Python](https://img.shields.io/badge/Python-3.7%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![Vibe](https://img.shields.io/badge/Vibe-100%25-ff0066?style=for-the-badge)

A powerful, sleek, and dark-themed web image crawler built with Python and CustomTkinter. 
Extracts image links, downloads high-quality images, and generates a professional PDF report.

**100% vibe coded**

## ✨ Features

* **🎨 Ultra Modern UI**: Built with `CustomTkinter` for a premium dark-mode experience.
* **🕷️ Deep Crawling**: Recursively finds every image on the site.
* **📂 Multi-Source & Bulk**: 
    * Load specific URLs from a text file.
    * Organize downloaded images into separate folders per domain.
* **💾 Auto-Downloader**: Automatically downloads valid images to a local folder.
* **🧠 Smart High-Res Logic**: Automatically finds the HD version of thumbnails (Pinterest, Wallpaper sites).
* **⚡ Threaded & Fast**: Non-blocking IO for smooth performance.

## 🚀 Installation

### 🪟 Windows

[![Download ZIP](https://img.shields.io/badge/Download_Project_ZIP-ff0066?style=for-the-badge&logo=github)](https://github.com/shubhambelbase/python-image-crawler/archive/refs/heads/main.zip)

1. **Download and Extract** the ZIP (click the button above).
2. **Install Dependencies**: 
   * Double-click `Install_Dependencies.bat`.
3. **Start the App**: 
   * Double-click `Start_App.bat`.

---

### 🐧 Linux / 🍎 macOS

For Unix-based systems, it is recommended to use a virtual environment to ensure the GUI runs smoothly.

#### **1. Install System Prerequisites**
Before running the app, ensure you have the Python Tkinter library installed on your system:

* **macOS (Homebrew):** `brew install python-tk`
* **Linux (Debian/Ubuntu):** `sudo apt install python3-tk python3-pip`

#### **2. Setup & Installation**
Open your terminal and run the following commands:

```bash
# Clone the repository
git clone [https://github.com/shubhambelbase/python-image-crawler.git](https://github.com/shubhambelbase/python-image-crawler.git)
cd python-image-crawler

# Create a virtual environment
python3 -m venv venv

# Activate the environment
# For macOS/Linux:
source venv/bin/activate

# Install requirements
pip install -r requirements.txt
