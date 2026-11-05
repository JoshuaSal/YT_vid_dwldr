import os
import threading
import tkinter as tk
from tkinter import messagebox, ttk
import yt_dlp

# ==========================================
# CONFIGURATION & CONSTANTS
# ==========================================
OUTPUT_DIR = "videos"
DOWNLOAD_FORMAT = "bestvideo[height<=1080]+bestaudio/best[height<=1080]"


class YouTubeDownloaderApp:

  def __init__(self, root):
    self.root = root
    self.root.title("YouTube Downloader")
    self.root.geometry("480x260")
    self.root.resizable(False, False)

    self.setup_styles()
    self.create_widgets()

  # ==========================================
  # UI SETUP
  # ==========================================
  def setup_styles(self):
    self.style = ttk.Style()
    self.style.theme_use("clam")

  def create_widgets(self):
    main_frame = ttk.Frame(self.root, padding="20")
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Title
    ttk.Label(
        main_frame, text="YouTube Video Downloader", font=("Segoe UI", 14, "bold")
    ).pack(pady=(0, 15))

    # URL Input Field
    ttk.Label(
        main_frame, text="Paste YouTube URL:", font=("Segoe UI", 10)
    ).pack(anchor=tk.W, pady=(0, 5))
    
    self.url_entry = ttk.Entry(main_frame, width=55, font=("Segoe UI", 10))
    self.url_entry.pack(fill=tk.X, pady=(0, 15))

    # Download Button
    self.download_btn = ttk.Button(
        main_frame, text="Download Video (1080p Max)", command=self.start_download_thread
    )
    self.download_btn.pack(fill=tk.X, ipady=5, pady=(0, 15))

    # Status Label
    self.status_label = ttk.Label(
        main_frame, text="Status: Ready", font=("Segoe UI", 9, "italic")
    )
    self.status_label.pack(anchor=tk.W)

  # ==========================================
  # EVENT HANDLERS & THREADING
  # ==========================================
  def start_download_thread(self):
    url = self.url_entry.get().strip()
    if not url:
      messagebox.showerror("Error", "Please enter a valid YouTube URL.")
      return

    self.download_btn.config(state=tk.DISABLED)
    self.status_label.config(text="Status: Downloading...")

    # Run download in a background thread to keep GUI responsive
    threading.Thread(target=self.download_video, args=(url,), daemon=True).start()

  # ==========================================
  # CORE DOWNLOAD LOGIC (yt-dlp)
  # ==========================================
  def download_video(self, url):
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    ydl_opts = {
        "format": DOWNLOAD_FORMAT,
        "outtmpl": os.path.join(OUTPUT_DIR, "%(title)s.%(ext)s"),
    }
    try:
      with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

      self.root.after(
          0, lambda: self.download_complete("Success! Video downloaded.")
      )
    except Exception as e:
      error_msg = str(e)
      self.root.after(
          0, lambda: self.download_error(f"Download failed: {error_msg}")
      )

  def download_complete(self, message):
    self.status_label.config(text=f"Status: {message}")
    self.download_btn.config(state=tk.NORMAL)
    messagebox.showinfo("Success", "Your video has been downloaded successfully!")
    self.url_entry.delete(0, tk.END)

  def download_error(self, message):
    self.status_label.config(text="Status: Error encountered")
    self.download_btn.config(state=tk.NORMAL)
    messagebox.showerror("Error", message)


if __name__ == "__main__":
  root = tk.Tk()
  app = YouTubeDownloaderApp(root)
  root.mainloop()