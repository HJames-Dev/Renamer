import os
import unicodedata
import re
import datetime
from collections import defaultdict  

input_path = input("Enter the full path to the folder you want to rename files in:\n(Leave blank to use current folder)\n> ").strip()

if input_path:
    base_dir = os.path.abspath(os.path.expanduser(input_path))
else:
    base_dir = os.getcwd()  # current working directory

if not os.path.isdir(base_dir):
    print(f"❌ Error: '{base_dir}' is not a valid directory.")
    exit(1)

include_subdirs = input("Include subfolders? [y/n]: ").strip().lower() in ("y", "yes")

img_files = []  

if include_subdirs:
    for root, _, filenames in os.walk(base_dir):
        for f in filenames:
            if f.lower().endswith((".jpg", ".gif", ".png", ".webm")):
                full_path = os.path.join(root, f)
                img_files.append(full_path)
else:
    for f in os.listdir(base_dir):
        if f.lower().endswith((".jpg", ".gif", ".png", ".webm")):
            full_path = os.path.join(base_dir, f)
            img_files.append(full_path)

# Group files by subfolder
from collections import defaultdict  #  (already shown above)
folder_files = defaultdict(list)  

for path in img_files:  
    subfolder = os.path.dirname(path)  
    folder_files[subfolder].append(path)  

use_custom_name = input("Use custom base name? (y/n): ").lower().startswith('y')

# Uses Custom name instead of Folder name. Normalizes characters for OS comp.
if use_custom_name: 
    raw_input = input("Base name for renamed files: ").strip() 
    normalized = unicodedata.normalize("NFKD", raw_input)
    without_accents = ''.join(c for c in normalized if not unicodedata.combining(c))
    name_base = re.sub(r'[^\w\-]', '_', without_accents).strip('_')


# Selects if Date is to be appended to file names.
append_date = input("Append date to filenames? (y/n): ").lower().startswith('y')
append_day = False
if append_date:
    append_day = input("Include day in date? (y/n): ").lower().startswith('y')

renamed_pairs = []

# Loop per folder and rename with per-folder indexing
for folder, filelist in folder_files.items():  
    subdir_name = os.path.basename(folder)  
    
    for i, path in enumerate(sorted(filelist, key=os.path.getmtime)):  
        timestamp = os.path.getmtime(path)
        dt = datetime.datetime.fromtimestamp(timestamp)
        
        if append_date:
            if append_day:
                date_part = dt.strftime("%B_%d_%Y")  # e.g., April_07_2025
            else:
                date_part = dt.strftime("%B_%Y")  # e.g., April_2025
        else:
            date_part = ""

        year = dt.year
        ext = os.path.splitext(path)[1]

        parts = []

# Base name: custom or fallback to subdir
        parts.append(name_base if use_custom_name else subdir_name)

# Optional: subdir suffix only if both toggles are active
        if use_custom_name and include_subdirs:
            parts.append(subdir_name)

# Optional: append date if user enabled it
        if date_part:
            parts.append(date_part)

# Append index and extension
        parts.append(f"{i+1:03}{ext}")

# Join everything into final filename
        new_name = '_'.join(parts)

        new_path = os.path.join(folder, new_name)  
        renamed_pairs.append((path, new_path))

# Preview renaming
for old, new in renamed_pairs:
    print(f"{os.path.basename(old)} → {os.path.basename(new)}")


renamed_count = 0
error_count = 0
skipped_count = 0


proceed = input("Proceed with renaming? [y/N]: ").strip().lower() in ("y", "yes")

# Renaming loop and exception handling
if proceed:
    for old, new in renamed_pairs:
        if os.path.exists(new):
            print(f"Skipped: {os.path.basename(new)} already exists.")
            skipped_count += 1
            continue
       
        try:
            os.rename(old, new)
            print(f"Renamed: {os.path.basename(old)} → {os.path.basename(new)}")
            renamed_count += 1
        except PermissionError:
            print(f"Permission denied: {os.path.basename(old)}")
            error_count += 1
        except Exception as e:
            print(f"Error renaming {os.path.basename(old)} → {os.path.basename(new)}: {e}")
            error_count += 1

    print(f"\nSummary: {renamed_count} renamed, {skipped_count} skipped (already exists), {error_count} errors.\n")
else:
    print("No files were renamed.")


input("Press Enter to close...")