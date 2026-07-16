import customtkinter as ctk
from tkinter import filedialog, messagebox
import yt_dlp
import threading
import os

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

def paste_url():
    try:
        url_entry.delete(0, "end")
        url_entry.insert(0, app.clipboard_get())
    except:
        messagebox.showerror("Error", "Clipboard is empty")

def browse():
    folder = filedialog.askdirectory()
    if folder:
        path_entry.delete(0, "end")
        path_entry.insert(0, folder)

def download():
    url = url_entry.get().strip()
    path = path_entry.get().strip()

    if not url or not path:
        messagebox.showerror("Error", "URL and download folder are required")
        return

    status_label.configure(text="Downloading...", text_color="yellow")

    ydl_opts = {
        "format": "bv*+ba/b",
        "merge_output_format": "mp4",
        "outtmpl": os.path.join(path, "%(title)s.%(ext)s"),
        "noplaylist": True,
        "quiet": True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        status_label.configure(text="Download completed successfully", text_color="green")

    except Exception as e:
        status_label.configure(text="Download failed", text_color="red")
        messagebox.showerror("Download failed", str(e))

def start_download():
    threading.Thread(target=download).start()

# ---------- GUI ----------
app = ctk.CTk()
app.title("Professional Video Downloader(by AmirReza Mahdavi)")
app.geometry("600x360")
app.resizable(False, False)

ctk.CTkLabel(app, text="Pinterest Video Downloader", font=("Segoe UI", 22, "bold")).pack(pady=15)

ctk.CTkLabel(app, text="Pinterest Video URL").pack()
url_frame = ctk.CTkFrame(app)
url_frame.pack(pady=8)

url_entry = ctk.CTkEntry(url_frame, width=420)
url_entry.pack(side="left", padx=8)

ctk.CTkButton(url_frame, text="Paste", width=80, command=paste_url).pack(side="left")

ctk.CTkLabel(app, text="Download Folder").pack()
path_frame = ctk.CTkFrame(app)
path_frame.pack(pady=8)

path_entry = ctk.CTkEntry(path_frame, width=340)
path_entry.pack(side="left", padx=8)

ctk.CTkButton(path_frame, text="Browse", width=80, command=browse).pack(side="left")

ctk.CTkButton(app, text="Download", width=260, height=45, command=start_download).pack(pady=25)

status_label = ctk.CTkLabel(app, text="")
status_label.pack()

app.mainloop()
