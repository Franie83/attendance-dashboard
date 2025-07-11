import os
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

def protect_item(path):
    if not os.path.exists(path):
        messagebox.showerror("Error", "Selected path does not exist.")
        return

    try:
        os.system(f'attrib +r "{path}"')
        result = subprocess.run(
            f'icacls "{path}" /deny Everyone:(D)',
            shell=True,
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            messagebox.showinfo("Success", f"✅ Protection applied to:\n{path}")
        else:
            messagebox.showerror("Error", f"❌ Failed to protect:\n{result.stderr}")
    except Exception as e:
        messagebox.showerror("Exception", f"❌ Exception:\n{e}")

def unprotect_item(path):
    if not os.path.exists(path):
        messagebox.showerror("Error", "Selected path does not exist.")
        return

    try:
        os.system(f'attrib -r "{path}"')
        result = subprocess.run(
            f'icacls "{path}" /remove:d Everyone',
            shell=True,
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            messagebox.showinfo("Success", f"✅ Unprotected:\n{path}")
        else:
            messagebox.showerror("Error", f"❌ Failed to unprotect:\n{result.stderr}")
    except Exception as e:
        messagebox.showerror("Exception", f"❌ Exception:\n{e}")

def browse_folder():
    path = filedialog.askdirectory()
    if path:
        path_var.set(path)

def browse_file():
    path = filedialog.askopenfilename()
    if path:
        path_var.set(path)

# GUI Setup
root = tk.Tk()
root.title("🔐 File & Folder Protector (Windows)")
root.geometry("550x260")
root.resizable(False, False)

path_var = tk.StringVar()

tk.Label(root, text="Select a File or Folder to Protect/Unprotect", font=("Arial", 12)).pack(pady=10)

entry = tk.Entry(root, textvariable=path_var, width=70)
entry.pack(pady=5)

select_frame = tk.Frame(root)
select_frame.pack(pady=5)

tk.Button(select_frame, text="📁 Browse Folder", command=browse_folder).grid(row=0, column=0, padx=10)
tk.Button(select_frame, text="📄 Browse File", command=browse_file).grid(row=0, column=1, padx=10)

btn_frame = tk.Frame(root)
btn_frame.pack(pady=20)

tk.Button(btn_frame, text="🔒 Protect", width=20, bg="lightgreen",
          command=lambda: protect_item(path_var.get())).grid(row=0, column=0, padx=10)

tk.Button(btn_frame, text="🔓 Unprotect", width=20, bg="lightblue",
          command=lambda: unprotect_item(path_var.get())).grid(row=0, column=1, padx=10)

root.mainloop()
