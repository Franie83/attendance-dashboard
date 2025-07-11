import os
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox

def protect_folder(folder_path):
    try:
        os.system(f'attrib +r "{folder_path}"')
        result = subprocess.run(
            f'icacls "{folder_path}" /deny Everyone:(D)',
            shell=True,
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            messagebox.showinfo("Success", f"✅ Folder is now protected: {folder_path}")
        else:
            messagebox.showerror("Error", f"❌ Failed to protect folder:\n{result.stderr}")
    except Exception as e:
        messagebox.showerror("Exception", f"❌ Exception occurred:\n{e}")

def unprotect_folder(folder_path):
    try:
        os.system(f'attrib -r "{folder_path}"')
        result = subprocess.run(
            f'icacls "{folder_path}" /remove:d Everyone',
            shell=True,
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            messagebox.showinfo("Success", f"✅ Folder is now unprotected: {folder_path}")
        else:
            messagebox.showerror("Error", f"❌ Failed to unprotect folder:\n{result.stderr}")
    except Exception as e:
        messagebox.showerror("Exception", f"❌ Exception occurred:\n{e}")

def browse_folder():
    path = filedialog.askdirectory()
    if path:
        folder_path.set(path)

# GUI Setup
root = tk.Tk()
root.title("Folder Protection Tool")
root.geometry("500x200")
root.resizable(False, False)

folder_path = tk.StringVar()

# Widgets
tk.Label(root, text="Select Folder to Protect/Unprotect:", font=("Arial", 12)).pack(pady=10)
tk.Entry(root, textvariable=folder_path, width=60).pack()
tk.Button(root, text="Browse", command=browse_folder).pack(pady=5)

btn_frame = tk.Frame(root)
btn_frame.pack(pady=15)

tk.Button(btn_frame, text="🔒 Protect Folder", width=20, bg="lightgreen",
          command=lambda: protect_folder(folder_path.get())).grid(row=0, column=0, padx=10)

tk.Button(btn_frame, text="🔓 Unprotect Folder", width=20, bg="lightblue",
          command=lambda: unprotect_folder(folder_path.get())).grid(row=0, column=1, padx=10)

root.mainloop()
