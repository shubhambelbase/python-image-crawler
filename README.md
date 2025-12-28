# Image Crawler Pro

![Python](https://img.shields.io/badge/Python-3.7%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![Vibe](https://img.shields.io/badge/Vibe-100%25-ff0066?style=for-the-badge)
[![Download ZIP](https://img.shields.io/badge/Download-Source_Code-ff0066?style=for-the-badge&logo=github)](https://github.com/shubhambelbase/python-image-crawler/blob/main/ImageCrawler.zip)

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

1.  **Download and Extract** the ZIP (using the button above).
2.  **Install Dependencies**: 
    * Double-click `Install_Dependencies.bat`.
3.  **Start the App**: 
    * Double-click `Start_App.bat`.

### 🐧 Linux / 🍎 macOS

1.  **Clone or Download** this repository.
2.  Open your terminal and navigate to the folder.
3.  **Install Dependencies**:
    ```bash
    pip3 install -r requirements.txt
    ```
4.  **Start the App**:
    ```bash
    python3 image_crawler_gui.py
    ```

## 📖 Usage

### Single URL
1.  Enter the URL (e.g., `https://example.com`) and click **Start**.

### Bulk Mode
1.  Create a text file (`targets.txt`) with one URL per line.
2.  Click **Load Text File** in the app.
3.  Click **Start Crawling**. 

### Options
* **Download Images**: Save files locally.
* **Smart Size Filter**: Ignore junk <5KB.
* **Folder per Domain**: Keeps your downloads organized if crawling multiple sites.

## 📦 Requirements

* Python 3.7+
* Internet Connection

---
*Vibe Coded by Shubham*

