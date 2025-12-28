# Image Crawler

![Python](https://img.shields.io/badge/Python-3.7%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![Vibe](https://img.shields.io/badge/Vibe-100%25-ff0066?style=for-the-badge)

A powerful, sleek, and dark-themed web image crawler built with Python. 
Extracts image links from any website and generates a professional PDF report with clickable links.

**100% vibe coded**

## ✨ Features

*   **🎨 Dark Modern UI**: A clean, responsive interface designed for visual comfort and style.
*   **🕷️ Deep Crawling**: Recursively crawls pages to find every single reachable image.
*   **🧠 Smart Filtering**: Automatically filters out icons, tracking pixels, and non-image junk.
*   **📄 PDF Reporting**: Generates a professional PDF report with clickable links to all images found.
*   **⚡ Threaded Performance**: Runs smoothly in the background without freezing the UI.

## 🚀 Installation

### 🪟 Windows

1.  **Clone or Download** this repository.
2.  **Install Dependencies**: 
    *   Double-click `Install_Dependencies.bat`.
    *   This script automatically checks for Python and installs required libraries (`requests`, `beautifulsoup4`, `reportlab`).
3.  **Start the App**: 
    *   Double-click `Start_App.bat`.

### 🐧 Linux / 🍎 macOS

1.  **Clone or Download** this repository.
2.  Open your terminal and navigate to the folder.
3.  **Install Dependencies**:
    ```bash
    pip3 install -r requirements.txt
    ```
    *(Note: You might need to use a virtual environment)*
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```
4.  **Start the App**:
    ```bash
    python3 image_crawler_gui.py
    ```

## 📖 Usage

1.  **Target URL**: Enter the website address you want to scrape (e.g., `https://example.com`).
2.  **Max Pages**: Set how many pages you want to crawl (default: 50).
3.  **Output PDF**: Name your output report (e.g., `my_images.pdf`).
4.  **Start Crawling**: Click the button and watch it go.
5.  **Enjoy**: Sit back and enjoy the vibes while the crawler builds your report.

## 📦 Requirements

*   Python 3.7+
*   Internet Connection

---
*Vibe Coded by Shubham*
