import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import csv
import threading
import queue
import time
import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

class ImageCrawlApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Crawler")
        self.root.geometry("800x600")
        
        # Color Palette (Dark Theme)
        self.bg_color = "#1e1e1e"
        self.fg_color = "#ffffff"
        self.accent_color = "#007acc"
        self.input_bg = "#2d2d2d"
        self.root.configure(bg=self.bg_color)
        
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        self.style.configure("TFrame", background=self.bg_color)
        self.style.configure("TLabel", background=self.bg_color, foreground=self.fg_color, font=("Segoe UI", 10))
        self.style.configure("TButton", background=self.accent_color, foreground="white", borderwidth=0, font=("Segoe UI", 10, "bold"))
        self.style.map("TButton", background=[("active", "#005f9e")])
        self.style.configure("TEntry", fieldbackground=self.input_bg, foreground=self.fg_color, insertcolor="white", borderwidth=1)
        self.style.configure("Header.TLabel", font=("Segoe UI", 16, "bold"), foreground=self.accent_color)
        self.style.configure("Horizontal.TProgressbar", background=self.accent_color, troughcolor=self.input_bg, bordercolor=self.bg_color, lightcolor=self.accent_color, darkcolor=self.accent_color)

        # State Variables
        self.is_running = False
        self.log_queue = queue.Queue()
        
        self.setup_ui()
        self.process_logs()

    def setup_ui(self):
        # Main Container
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        header = ttk.Label(main_frame, text="Image Crawler", style="Header.TLabel")
        header.pack(pady=(0, 20), anchor="w")
        
        # Input Section
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=5)
        
        # URL Input
        ttk.Label(input_frame, text="Target URL:").grid(row=0, column=0, sticky="w", pady=5)
        self.url_var = tk.StringVar()
        self.url_entry = ttk.Entry(input_frame, textvariable=self.url_var, width=50)
        self.url_entry.grid(row=0, column=1, padx=10, sticky="ew")
        
        # Max Pages Input
        ttk.Label(input_frame, text="Max Pages:").grid(row=1, column=0, sticky="w", pady=5)
        self.max_pages_var = tk.IntVar(value=50)
        self.max_pages_entry = ttk.Entry(input_frame, textvariable=self.max_pages_var, width=10)
        self.max_pages_entry.grid(row=1, column=1, padx=10, sticky="w")
        
        input_frame.columnconfigure(1, weight=1)

        # Output Section
        ttk.Label(input_frame, text="Output PDF:").grid(row=2, column=0, sticky="w", pady=5)
        self.output_var = tk.StringVar(value="images.pdf")
        self.output_entry = ttk.Entry(input_frame, textvariable=self.output_var, width=30)
        self.output_entry.grid(row=2, column=1, padx=10, sticky="w")
        
        # Controls
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=20)
        
        self.start_btn = ttk.Button(btn_frame, text="Start Crawling", command=self.start_crawling)
        self.start_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.stop_btn = ttk.Button(btn_frame, text="Stop", command=self.stop_crawling, state="disabled")
        self.stop_btn.pack(side=tk.LEFT)
        
        # Progress Section
        progress_frame = ttk.Frame(main_frame)
        progress_frame.pack(fill=tk.X, pady=10)
        
        self.progress_label = ttk.Label(progress_frame, text="Ready")
        self.progress_label.pack(anchor="w", pady=(0, 5))
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, maximum=100, style="Horizontal.TProgressbar")
        self.progress_bar.pack(fill=tk.X)
        
        # Log Area
        log_frame = ttk.Frame(main_frame)
        log_frame.pack(fill=tk.BOTH, expand=True, pady=(20, 0))
        
        ttk.Label(log_frame, text="Activity Log:").pack(anchor="w", pady=(0, 5))
        self.log_text = tk.Text(log_frame, height=10, bg=self.input_bg, fg=self.fg_color, relief="flat", font=("Consolas", 9))
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar for log
        scrollbar = ttk.Scrollbar(self.log_text, orient="vertical", command=self.log_text.yview)
        # We need to pack the scrollbar properly, using a frame or grid is better but pack works if done right
        # Actually simplest is to pack scrollbar to right of log_text
        # But tk.Text contains custom widgets? No.
        # Let's just use grid for log frame to hold text and scrollbar
        # Re-doing log_frame layout
        self.log_text.pack_forget()
        self.log_text = tk.Text(log_frame, bg=self.input_bg, fg=self.fg_color, relief="flat", font=("Consolas", 9))
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.configure(yscrollcommand=scrollbar.set)

    def log(self, message):
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        self.log_queue.put(f"[{timestamp}] {message}")

    def process_logs(self):
        while not self.log_queue.empty():
            msg = self.log_queue.get()
            self.log_text.insert(tk.END, msg + "\n")
            self.log_text.see(tk.END)
        self.root.after(100, self.process_logs)

    def toggle_inputs(self, enable):
        state = "normal" if enable else "disabled"
        self.url_entry.configure(state=state)
        self.max_pages_entry.configure(state=state)
        self.output_entry.configure(state=state)
        self.start_btn.configure(state=state)
        self.stop_btn.configure(state="normal" if not enable else "disabled")

    def start_crawling(self):
        url = self.url_var.get().strip()
        if not url:
            messagebox.showerror("Error", "Please enter a URL")
            return
            
        try:
            max_pages = self.max_pages_var.get()
        except tk.TclError:
            messagebox.showerror("Error", "Max pages must be a number")
            return

        pdf_file = self.output_var.get().strip()
        if not pdf_file:
            messagebox.showerror("Error", "Please enter a PDF filename")
            return
        if not pdf_file.lower().endswith('.pdf'):
            pdf_file += ".pdf"

        self.is_running = True
        self.toggle_inputs(False)
        self.progress_var.set(0)
        self.log_text.delete(1.0, tk.END)
        self.log(f"Starting crawl for {url}")
        
        # Start Thread
        self.thread = threading.Thread(target=self.crawl_logic, args=(url, max_pages, pdf_file))
        self.thread.daemon = True
        self.thread.start()

    def stop_crawling(self):
        self.is_running = False
        self.log("Stopping crawler...")

    def crawl_logic(self, start_url, max_pages, pdf_filename):
        visited = set()
        queue_urls = [start_url]
        image_rows = [] # List to store [Image URL, Alt Text, Source Page]
        domain = urlparse(start_url).netloc
        pages_processed = 0
        
        # Headers for requests
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # Valid image extensions to filter garbage
        valid_exts = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.svg', '.tiff', '.ico')

        try:
            while queue_urls and self.is_running and pages_processed < max_pages:
                current_url = queue_urls.pop(0)
                
                if current_url in visited:
                    continue
                
                visited.add(current_url)
                self.root.after(0, lambda u=current_url: self.progress_label.configure(text=f"Crawling: {u}"))
                
                try:
                    response = requests.get(current_url, headers=headers, timeout=10)
                    response.raise_for_status()
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # Extract Images
                    images = soup.find_all('img')
                    new_images = 0
                    
                    for img in images:
                        # Check for lazy loading attributes first
                        src = img.get('data-src') or img.get('data-original') or img.get('data-lazy-src') or img.get('src')
                        
                        # Handle srcset
                        if not src and img.get('srcset'):
                            parts = img.get('srcset').split(',')
                            if parts:
                                src = parts[0].strip().split(' ')[0]
                            
                        alt = img.get('alt', '')
                        
                        if src and not src.startswith('data:'):
                            full_img_url = urljoin(current_url, src)
                            
                            # Strict extension check - user requested links MUST end with valid extension
                            path = urlparse(full_img_url).path.lower()
                            if path.endswith(valid_exts): 
                                # Limit Alt text length
                                clean_alt = alt[:50] + "..." if len(alt) > 50 else alt
                                image_rows.append([full_img_url, clean_alt, current_url])
                                new_images += 1
                    
                    self.log(f"Scanned {current_url} - Found {new_images} images")
                    
                    # Find new links
                    links = soup.find_all('a', href=True)
                    for link in links:
                        href = link['href']
                        full_url = urljoin(current_url, href)
                        parsed_url = urlparse(full_url)
                        
                        if parsed_url.netloc == domain and parsed_url.scheme in ['http', 'https']:
                            clean_url = full_url.split('#')[0]
                            if clean_url not in visited and clean_url not in queue_urls:
                                queue_urls.append(clean_url)
                                
                    pages_processed += 1
                    progress = (pages_processed / max_pages) * 100
                    self.root.after(0, lambda p=progress: self.progress_var.set(p))
                    
                except requests.exceptions.RequestException as e:
                    self.log(f"Failed to fetch {current_url}: {e}")
                except Exception as e:
                    self.log(f"Error processing {current_url}: {e}")
                    
                # Sleep slightly to be polite
                time.sleep(0.5)

            # Generate PDF
            self.log("Generating PDF Report...")
            self.create_pdf_report(pdf_filename, image_rows, start_url)
            
        except Exception as e:
            self.log(f"Critical Error: {e}")
        finally:
            self.stop_thread_safe()
            self.log(f"Crawl finished. Processed {pages_processed} pages.")
            self.log(f"Results saved to {pdf_filename}")

    def create_pdf_report(self, filename, data, start_url):
        doc = SimpleDocTemplate(filename, pagesize=landscape(letter))
        elements = []
        styles = getSampleStyleSheet()

        # Title
        title_style = styles['Title']
        title_style.textColor = colors.HexColor("#007acc")
        elements.append(Paragraph(f"Image Crawl Report: {start_url}", title_style))
        elements.append(Paragraph(f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
        elements.append(Spacer(1, 20))
        
        # Table Data
        table_data = [["Image URL", "Alt Text", "Source Page"]]  # Header
        
        # Style for table cells - we need to wrap text so it fits
        normal_style = styles['BodyText']
        normal_style.fontSize = 8
        
        for row in data:
            # Wrap long strings in Paragraphs to allow multi-line cells
            url = row[0]
            # Simple XML escaping for the URL text/href
            url_safe = url.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            
            # Make clickable link with blue color (and potentially word-break it visually if needed, 
            # but Paragraph handles wrapping if there are delimiters. Long URLs without delim might still flow out, 
            # but priority is clickability)
            link_html = f'<a href="{url_safe}" color="#0000ff">{url_safe}</a>'
            
            url_p = Paragraph(link_html, normal_style)
            alt_p = Paragraph(row[1], normal_style)
            source_p = Paragraph(row[2], normal_style)
            table_data.append([url_p, alt_p, source_p])

        # Table Style
        # Define column widths to fit landscape letter page (~792 points width)
        # Margins are usually ~72 points each side. Available ~650.
        col_widths = [300, 150, 200] 
        
        t = Table(table_data, colWidths=col_widths)
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#007acc")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor("#f0f0f0")),
            ('GRID', (0, 0), (-1, -1), 1, colors.white),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        
        elements.append(t)
        doc.build(elements)

    def stop_thread_safe(self):
        self.is_running = False
        self.root.after(0, lambda: self.toggle_inputs(True))
        self.root.after(0, lambda: self.progress_label.configure(text="Ready"))

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageCrawlApp(root)
    root.mainloop()
