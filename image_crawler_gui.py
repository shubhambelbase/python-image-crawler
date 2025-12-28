import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, filedialog
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import csv
import threading
import queue
import time
import datetime
import os
from PIL import Image
import io
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image as RLImage
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

# Set CustomTkinter Theme
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class ImageCrawlApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Crawler Pro")
        self.root.geometry("900x700")
        
        # State Variables
        self.is_running = False
        self.log_queue = queue.Queue()
        self.download_folder = "downloaded_images"
        
        self.setup_ui()
        self.process_logs()

    def setup_ui(self):
        # Main Container
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        header = ctk.CTkLabel(self.main_frame, text="Image Crawler Pro", font=("Roboto", 24, "bold"), text_color="#3B8ED0")
        header.pack(pady=(10, 20), anchor="w", padx=20)
        
        # Input Section
        input_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        input_frame.pack(fill=tk.X, padx=20)
        
        # URL Input Row
        self.url_mode_var = ctk.StringVar(value="Single")
        
        # Grid for URL inputs
        input_frame.columnconfigure(1, weight=1)
        
        ctk.CTkLabel(input_frame, text="Target URL:", font=("Roboto", 14)).grid(row=0, column=0, sticky="w", pady=10)
        self.url_var = tk.StringVar()
        self.url_entry = ctk.CTkEntry(input_frame, textvariable=self.url_var, placeholder_text="https://example.com")
        self.url_entry.grid(row=0, column=1, padx=15, sticky="ew")
        
        self.load_btn = ctk.CTkButton(input_frame, text="Load Text File", command=self.load_url_file, width=120)
        self.load_btn.grid(row=0, column=2, padx=5)

        # Max Pages Input
        ctk.CTkLabel(input_frame, text="Max Pages:", font=("Roboto", 14)).grid(row=1, column=0, sticky="w", pady=10)
        self.max_pages_var = tk.IntVar(value=50)
        self.max_pages_entry = ctk.CTkEntry(input_frame, textvariable=self.max_pages_var, width=100)
        self.max_pages_entry.grid(row=1, column=1, padx=15, sticky="w")
        
        # Switches
        options_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        options_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.download_var = ctk.BooleanVar(value=True)
        self.download_switch = ctk.CTkSwitch(options_frame, text="Download Images Locally", variable=self.download_var, font=("Roboto", 12))
        self.download_switch.pack(side=tk.LEFT, padx=(0, 20))
        
        self.filter_var = ctk.BooleanVar(value=True)
        self.filter_switch = ctk.CTkSwitch(options_frame, text="Smart Size Filter (>5KB)", variable=self.filter_var, font=("Roboto", 12))
        self.filter_switch.pack(side=tk.LEFT, padx=(0, 20))

        self.organize_var = ctk.BooleanVar(value=False)
        self.org_switch = ctk.CTkSwitch(options_frame, text="Folder per Domain", variable=self.organize_var, font=("Roboto", 12))
        self.org_switch.pack(side=tk.LEFT)
        
        # input_frame.columnconfigure(1, weight=1) already done above

        # Controls
        btn_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        btn_frame.pack(fill=tk.X, padx=20, pady=20)
        
        self.start_btn = ctk.CTkButton(btn_frame, text="Start Crawling", command=self.start_crawling, font=("Roboto", 14, "bold"), height=40)
        self.start_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.stop_btn = ctk.CTkButton(btn_frame, text="Stop", command=self.stop_crawling, state="disabled", fg_color="#D32F2F", hover_color="#B71C1C", height=40)
        self.stop_btn.pack(side=tk.LEFT)
        
        # Progress Section
        self.progress_label = ctk.CTkLabel(self.main_frame, text="Ready", font=("Roboto", 12))
        self.progress_label.pack(anchor="w", padx=20, pady=(0, 5))
        
        self.progress_bar = ctk.CTkProgressBar(self.main_frame)
        self.progress_bar.pack(fill=tk.X, padx=20, pady=(0, 20))
        self.progress_bar.set(0)
        
        # Log Area
        ctk.CTkLabel(self.main_frame, text="Activity Log:", font=("Roboto", 12, "bold")).pack(anchor="w", padx=20)
        self.log_text = ctk.CTkTextbox(self.main_frame, height=200, font=("Consolas", 12))
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=20, pady=(5, 20))

    def log(self, message):
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        self.log_queue.put(f"[{timestamp}] {message}")

    def process_logs(self):
        while not self.log_queue.empty():
            msg = self.log_queue.get()
            self.log_text.insert(tk.END, msg + "\n")
            self.log_text.see(tk.END)
        self.root.after(100, self.process_logs)

    def load_url_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, 'r') as f:
                urls = [line.strip() for line in f.readlines() if line.strip()]
            
            if urls:
                self.url_var.set(file_path)
                self.log(f"Loaded {len(urls)} URLs from file")
                self.url_mode_var.set("File")
            else:
                self.log("File is empty")

    def toggle_inputs(self, enable):
        state = "normal" if enable else "disabled"
        self.url_entry.configure(state=state)
        self.load_btn.configure(state=state)
        self.max_pages_entry.configure(state=state)
        self.start_btn.configure(state=state)
        self.download_switch.configure(state=state)
        self.filter_switch.configure(state=state)
        self.org_switch.configure(state=state)
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

        self.is_running = True
        self.toggle_inputs(False)
        self.progress_bar.set(0)
        self.log_text.delete(1.0, tk.END)
        # Prepare URL List
        target_urls = []
        if os.path.isfile(url):
            try:
                with open(url, 'r') as f:
                    target_urls = [line.strip() for line in f.readlines() if line.strip().startswith('http')]
            except:
                messagebox.showerror("Error", "Could not read URL file")
                return
        else:
            target_urls = [url]

        if not target_urls:
            messagebox.showerror("Error", "No valid URLs found")
            return
            
        self.log(f"Starting job with {len(target_urls)} targets")
        
        # Create download folder if needed
        if self.download_var.get():
            if not os.path.exists(self.download_folder):
                os.makedirs(self.download_folder)
        
        # Start Thread
        organize_by_domain = self.organize_var.get()
        self.thread = threading.Thread(target=self.crawl_logic_multi, args=(target_urls, max_pages, organize_by_domain))
        self.thread.daemon = True
        self.thread.start()

    def stop_crawling(self):
        if self.is_running:
            self.is_running = False
            self.log("Stopping crawler... (finishing current task)")
            self.stop_btn.configure(state="disabled", text="Stopping...")
            
    def get_unique_filename(self, filename):
        # If file exists, add (1), (2), etc.
        if not os.path.exists(filename):
            return filename
            
        base, ext = os.path.splitext(filename)
        counter = 1
        while True:
            new_filename = f"{base} ({counter}){ext}"
            if not os.path.exists(new_filename):
                return new_filename
            counter += 1

    def crawl_logic_multi(self, urls, max_pages, organize_by_domain):
        try:
            for i, start_url in enumerate(urls):
                if not self.is_running: break
                
                self.log(f"--- Processing Target {i+1}/{len(urls)}: {start_url} ---")
                rows = self.crawl_single_site(start_url, max_pages, organize_by_domain)
                
                # Generate PDF PER SITE
                domain = urlparse(start_url).netloc
                safe_name = domain.replace('www.', '').replace(':', '_')
                safe_name = "".join([c for c in safe_name if c.isalpha() or c.isdigit() or c in ('-', '_', '.')])
                if not safe_name: safe_name = "website_crawl"
                
                pdf_filename = f"{safe_name}.pdf"
                pdf_filename = self.get_unique_filename(pdf_filename)
                
                self.log(f"Generating PDF for {domain}...")
                self.create_pdf_report(pdf_filename, rows, start_url)
                self.log(f"Saved: {pdf_filename}")
            
        except Exception as e:
            self.log(f"Job Error: {e}")
        finally:
            self.stop_thread_safe()
            self.log(f"All Jobs Finished.")

    def crawl_single_site(self, start_url, max_pages, organize_by_domain):
        visited = set()
        queue_urls = [start_url]
        image_rows = [] # [Image URL, Alt Text, Source Page]
        domain = urlparse(start_url).netloc
        # Create subfolder for domain if requested
        safe_domain = "".join([c for c in domain if c.isalpha() or c.isdigit() or c in ('-', '_')])
        domain_folder = os.path.join(self.download_folder, safe_domain) if organize_by_domain else self.download_folder
        
        if organize_by_domain and self.download_var.get():
            if not os.path.exists(domain_folder):
                os.makedirs(domain_folder)

        pages_processed = 0
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        valid_exts = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.svg', '.tiff', '.ico')

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
                
                images = soup.find_all('img')
                new_images = 0
                
                for img in images:
                    # Priority for high-res attributes
                    src = (img.get('data-full-url') or 
                           img.get('data-large-src') or 
                           img.get('data-high-res') or 
                           img.get('data-src') or 
                           img.get('data-original') or 
                           img.get('data-lazy-src') or 
                           img.get('src'))
                    
                    # Handle srcset - try to find the largest image
                    if img.get('srcset'):
                        try:
                            parts = img.get('srcset').split(',')
                            best_part = parts[-1].strip().split(' ')[0]
                            if best_part:
                                src = best_part
                        except:
                            pass
                        
                    alt = img.get('alt', '')
                    
                    if src and not src.startswith('data:'):
                        full_img_url = urljoin(current_url, src)
                        
                        # --- High-Resolution Magic ---
                        # Attempt to guess high-res URL patterns for common sites (Pinterest, diverse wallpapers)
                        # 1. Pinterest: 236x -> originals
                        if 'pinimg.com' in full_img_url:
                            full_img_url = full_img_url.replace('/236x/', '/originals/')
                            full_img_url = full_img_url.replace('/474x/', '/originals/')
                            full_img_url = full_img_url.replace('/736x/', '/originals/')
                        
                        # 2. WordPress / Generic Thumbs: -150x150, -300x200
                        import re
                        high_res_url = re.sub(r'-\d+x\d+(?=\.[a-zA-Z]+$)', '', full_img_url)
                        high_res_url = re.sub(r'-\d+x(?=\.[a-zA-Z]+$)', '', high_res_url)
                        
                        # 3. Common "thumb", "small", "preview" replacement
                        high_res_url = high_res_url.replace('thumb', 'large').replace('small', 'full').replace('preview', 'source')
                        
                        # Check if the "guessed" High-Res URL actually exists
                        final_url = full_img_url
                        if high_res_url != full_img_url:
                            try:
                                head_resp = requests.head(high_res_url, headers=headers, timeout=1.5)
                                if head_resp.status_code == 200:
                                    final_url = high_res_url
                            except:
                                pass
                        
                        full_img_url = final_url
                        # -----------------------------

                        path = urlparse(full_img_url).path.lower()
                        
                        if path.endswith(valid_exts): 
                            # Process Image
                            valid_image = True
                            
                            # Download & Filter Check
                            if self.download_var.get() or self.filter_var.get():
                                try:
                                    img_resp = requests.get(full_img_url, headers=headers, timeout=5)
                                    content_size = len(img_resp.content)
                                    
                                    # Smart Filter: Check if size > 5KB (ignore tiny icons)
                                    if self.filter_var.get() and content_size < 5120:
                                        valid_image = False
                                    
                                    if valid_image and self.download_var.get():
                                        filename = os.path.basename(urlparse(full_img_url).path)
                                        # Sanitize filename
                                        filename = "".join([c for c in filename if c.isalpha() or c.isdigit() or c in (' ', '.', '_')]).rstrip()
                                        if not filename: filename = "image.jpg"
                                        
                                        timestamp = int(time.time() * 1000)
                                        local_filename = f"{timestamp}_{filename}"
                                        
                                        # Use domain folder if organized
                                        save_path = os.path.join(domain_folder, local_filename)
                                        
                                        with open(save_path, 'wb') as f:
                                            f.write(img_resp.content)
                                            
                                except Exception as e:
                                    if self.filter_var.get(): 
                                        valid_image = False
                            
                            if valid_image:
                                clean_alt = alt[:100] + "..." if len(alt) > 100 else alt
                                image_rows.append([full_img_url, clean_alt, current_url])
                                new_images += 1
                
                self.log(f"Scanned {current_url} - Found {new_images} images")
                
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
                progress = (pages_processed / max_pages)
                self.root.after(0, lambda p=progress: self.progress_bar.set(p))
                
            except Exception as e:
                self.log(f"Error: {str(e)[:50]}...")
                
            time.sleep(0.5)

        return image_rows

    # Replaces old crawl_logic
    def crawl_logic_placeholder(self):
        pass

    def create_pdf_report(self, filename, data, start_url):
        doc = SimpleDocTemplate(filename, pagesize=landscape(letter))
        elements = []
        styles = getSampleStyleSheet()

        title_style = styles['Title']
        title_style.textColor = colors.HexColor("#007acc")
        elements.append(Paragraph(f"Image Crawl Report: {start_url}", title_style))
        elements.append(Paragraph(f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
        elements.append(Spacer(1, 20))
        
        # Header: URL, Alt, Source
        table_data = [["Image URL", "Alt Text", "Source Page"]]
        
        normal_style = styles['BodyText']
        normal_style.fontSize = 8
        
        for row in data:
            url, alt, source = row
            
            url_safe = url.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            link_html = f'<a href="{url_safe}" color="#0000ff">{url_safe}</a>'
            
            url_p = Paragraph(link_html, normal_style)
            alt_p = Paragraph(alt, normal_style)
            source_p = Paragraph(source, normal_style)
            
            table_data.append([url_p, alt_p, source_p])

        col_widths = [4.0*inch, 2.5*inch, 2.5*inch]
        
        t = Table(table_data, colWidths=col_widths)
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#007acc")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor("#f0f0f0")),
            ('GRID', (0, 0), (-1, -1), 1, colors.white),
        ]))
        
        elements.append(t)
        doc.build(elements)

    def stop_thread_safe(self):
        self.is_running = False
        self.root.after(0, lambda: self.toggle_inputs(True))
        self.root.after(0, lambda: self.stop_btn.configure(text="Stop"))
        self.root.after(0, lambda: self.progress_label.configure(text="Ready"))

if __name__ == "__main__":
    root = ctk.CTk()
    app = ImageCrawlApp(root)
    root.mainloop()
