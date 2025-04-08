import os
import unicodedata
import re
import datetime
from collections import defaultdict  
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText

# GUI Settings and definitions ------------------------------------------
root = Tk()
root.title("Renamer")


mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0,row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# --- App-wide UI state ---
use_custom_name = BooleanVar()
include_subdirs = BooleanVar()
append_date = BooleanVar()
append_day = BooleanVar()
base_dir = StringVar()
name_base = StringVar()


def toggle_name_entry():
    if use_custom_name.get():
        name.config(state='normal')
    else:
        name.config(state='disabled')


def toggle_day_checkbox():
    if append_date.get():
        check_day.config(state='normal')
    else:
        check_day.config(state='disabled')


def select_folder():
    folder = filedialog.askdirectory()
    if folder:
        base_dir.set(folder)

def generate_renamed_pairs():
    folder = base_dir.get()
    if not folder or not os.path.isdir(folder):
        messagebox.showerror("Invalid folder", "Select a valid folder before continuing.")
        return []
    
def preview_naming():
    pairs = generate_renamed_pairs()
    if not pairs:
        return
    preview_box.config(state='normal')
    preview_box.delete("1.0", END)
   
    # Insert each rename pair.
    for old, new in pairs:
        preview_box.insert(END, f"{os.path.basename(old)}  →  {os.path.basename(new)}\n")
        preview_box.config(state='disabled')

def apply_renaming():
    pairs = generate_renamed_pairs()
    if not pairs:
        return

    proceed = messagebox.askyesno("Confirm Rename", "Are you sure you want to rename the files?")
    if not proceed:
        return

    renamed_count = 0
    skipped_count = 0
    error_count = 0

    for old_path, new_path in pairs:
        if os.path.exists(new_path):
            skipped_count += 1
            continue

        try:
            os.rename(old_path, new_path)
            renamed_count += 1
        except PermissionError:
            error_count += 1
        except Exception:
            error_count += 1

    messagebox.showinfo("Done", f"Renamed: {renamed_count}\nSkipped: {skipped_count}\nErrors: {error_count}")

# End of GUI base settings --------------------------------------------


#base directory selection
btn_select_folder = ttk.Button(mainframe, text="Select Folder", command=select_folder)
btn_select_folder.grid(row=0, column=0, sticky=(W, E), padx=(5, 5), pady=(10, 0))
folder_display = ttk.Entry(mainframe, textvariable=base_dir, state='readonly', width=40)
folder_display.grid(row=1, column=0, sticky=(W, E), padx=(5, 5), pady=(10, 8))





#toggles subdir crawl and indexing
check_subdirs = ttk.Checkbutton(mainframe, text="Include Subfolders",
        variable=include_subdirs)
check_subdirs.grid(row=2, column=0, sticky=W, pady=(5, 0))

subdir_warn = ttk.Label(mainframe, text="NOTE: Including subfolders will append folder and subfolder names to the renamed file names, regardless of custom name usage, to prevent identical duplicate names.",
                        wraplength=300)
subdir_warn.grid(row=8, column=0, pady=(5, 15))


# Custom Name entry 
check_custom_name = ttk.Checkbutton(mainframe,text="Use custom File Names", variable=use_custom_name)
check_custom_name.config(command=toggle_name_entry)
check_custom_name.grid(row=4, column=0, sticky=W, pady=(10, 0))
name = ttk.Entry(mainframe, textvariable=name_base)
name.grid(row=5, column=0, columnspan=2, sticky=(W, E), pady=(0, 10))
toggle_name_entry()


# Uses Custom name instead of Folder name. Normalizes characters for OS comp.
if use_custom_name.get(): 
    raw_input = name_base.get().strip()
    normalized = unicodedata.normalize("NFKD", raw_input)
    without_accents = ''.join(c for c in normalized if not unicodedata.combining(c))
    clean_name = re.sub(r'[^\w\-]', '_', without_accents).strip('_')
    
    name_base.set(clean_name)  # this updates the StringVar safely 




#toggles date append
check_date = ttk.Checkbutton(mainframe, text="Append date to file names", variable=append_date)
check_date.config(command=toggle_day_checkbox)
check_date.grid(row=6, column=0, sticky=(W, E))
check_day = ttk.Checkbutton(mainframe, text="Include day in date", variable=append_day, state='disabled')
check_day.grid(row=7, column=0, sticky=W, pady=(0, 15))
toggle_day_checkbox()





def generate_renamed_pairs():
    folder = base_dir.get()
    if not folder or not os.path.isdir(folder):
        messagebox.showerror("Invalid folder", "Select a valid folder before continuing.")
        return []  # Return an empty list if no valid folder is selected.
    
    # Reset your image list.
    img_files = []
    if include_subdirs.get():
        for root, _, filenames in os.walk(folder):
            for f in filenames:
                if f.lower().endswith((".jpg", ".gif", ".png", ".webm")):
                    full_path = os.path.join(root, f)
                    img_files.append(full_path)
    else:
        for f in os.listdir(folder):
            if f.lower().endswith((".jpg", ".gif", ".png", ".webm")):
                full_path = os.path.join(folder, f)
                img_files.append(full_path)
    
    # Group files by subfolder.
    folder_files = defaultdict(list)
    for path in img_files:
        subfolder = os.path.dirname(path)
        folder_files[subfolder].append(path)
    
    # Now build renamed_pairs.
    renamed_pairs = []
    for folder, filelist in folder_files.items():
        subdir_name = os.path.basename(folder)
        for i, path in enumerate(sorted(filelist, key=os.path.getmtime)):
            timestamp = os.path.getmtime(path)
            dt = datetime.datetime.fromtimestamp(timestamp)

            if append_date.get():
                if append_day.get():
                    date_part = dt.strftime("%B_%d_%Y")
                else:
                    date_part = dt.strftime("%B_%Y")
            else:
                date_part = ""

            ext = os.path.splitext(path)[1]
            parts = []

            # Base name: custom or fallback to subdir.
            parts.append(name_base.get() if use_custom_name.get() else subdir_name)

            # Optional: subdir suffix only if both toggles are active.
            if use_custom_name.get() and include_subdirs.get():
                parts.append(subdir_name)

            # Optional: append date.
            if date_part:
                parts.append(date_part)

            # Append index and extension.
            parts.append(f"{i+1:03}{ext}")

            new_name = '_'.join(parts)
            new_path = os.path.join(folder, new_name)
            renamed_pairs.append((path, new_path))
    
    return renamed_pairs

# Create a scrollable text box for the preview output.
preview_box = ScrolledText(mainframe, width=40, height=4)
preview_box.grid(row=11, column=0, columnspan=1, sticky=(W, E), padx=5, pady=5)
# make the box read-only
preview_box.config(state='disabled')


#runs a print of projected changes to the msg box
preview_btn = ttk.Button(root, text="Preview Naming", command=preview_naming)
preview_btn.grid(row=9, column=0, sticky=(W, E))

#applies renaming
Rename_btn = ttk.Button(root, text="Rename", command=apply_renaming)
Rename_btn.grid(row=10, column=0, sticky=(W, E))


root.mainloop()