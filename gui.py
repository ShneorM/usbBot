import os
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import asyncio
from pcToTelegram import upload_files

def start_upload():
    directory = entry.get()
    if not os.path.isdir(directory):
        messagebox.showerror("Error", "Invalid directory path")
        return

    progress_label = ttk.Label(frame, text="")
    progress_label.grid(row=3, column=0, columnspan=2, pady=5)

    progress_var = tk.DoubleVar()
    progress_bar = ttk.Progressbar(frame, variable=progress_var, maximum=100)
    progress_bar.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)

    
    root.update_idletasks()
    asyncio.run(upload_files(directory, progress_var, progress_label, root))
    
    progress_var.set(0)
    progress_bar.grid_remove()
    progress_label.grid_remove()

def browse_directory():
    directory = filedialog.askdirectory()
    if directory:
        entry.delete(0, tk.END)
        entry.insert(0, directory)

root = tk.Tk()
root.title("Upload Folder to Telegram Bot")

frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

label = ttk.Label(frame, text="Enter directory path:")
label.grid(row=0, column=0, sticky=tk.W, pady=5)

entry = ttk.Entry(frame, width=50)
entry.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=5)

browse_button = ttk.Button(frame, text="Browse", command=browse_directory)
browse_button.grid(row=1, column=1, sticky=tk.W, pady=5, padx=5)

upload_button = ttk.Button(frame, text="Upload", command=start_upload)
upload_button.grid(row=2, column=0, columnspan=2, pady=10)

for child in frame.winfo_children():
    child.grid_configure(padx=5, pady=5)

root.mainloop()
