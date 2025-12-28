# Image Crawler Pro

![Python](https://img.shields.io/badge/Python-3.7%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![Vibe](https://img.shields.io/badge/Vibe-100%25-ff0066?style=for-the-badge)

A powerful, sleek, and dark-themed web image crawler built with Python and CustomTkinter. 
Extracts image links, downloads high-quality images, and generates a professional PDF report with visual thumbnails.

**100% vibe coded**

## ✨ Features

*   **🎨 Ultra Modern UI**: Built with `CustomTkinter` for a premium dark-mode experience.
*   **🕷️ Deep Crawling**: Recursively finds every image on the site.
*   **💾 Auto-Downloader**: Automatically downloads valid images to a local folder.
*   **� Visual PDF Reports**: Generates a PDF that includes **actual thumbnails** of the images found.
*   **🧠 Smart Filtering**: 
    *   **Size Filter**: Ignored tiny images/icons (< 5KB).
    *   **Extension Filter**: Only keeps real image formats.
*   **⚡ Threaded & Fast**: Non-blocking IO for smooth performance.

## 🚀 Installation

### 🪟 Windows

1.  **Clone or Download** this repository.
2.  **Install Dependencies**: 
    *   Double-click `Install_Dependencies.bat`.
    *   This script automatically checks for Python and installs required libraries (`customtkinter`, `reportlab`, `Pillow`, etc).
3.  **Start the App**: 
    *   Double-click `Start_App.bat`.

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

1.  **Target URL**: Enter the website address (e.g., `https://example.com`).
2.  **Switches**:
    *   **Download Images**: Toggle on to save files locally to `downloaded_images/`.
    *   **Smart Size Filter**: Toggle on to ignore tiny junk images.
3.  **Start Crawling**: Click the button.
4.  **Results**: 
    *   Images saved in `downloaded_images/`
    *   Professional PDF report generated as `images.pdf` (or your chosen name).

## 📦 Requirements

*   Python 3.7+
*   Internet Connection

---
*Vibe Coded by Shubham*
