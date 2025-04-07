# Renamer CLI

A Python-based command-line tool for batch-renaming images with custom naming patterns.  
Supports subdirectories, custom base names, optional date tags, and sort-safe indexing.

---

## Features

- Rename `.jpg`, `.png`, `.gif`, `.webm` files
- Recursive folder scanning (optional)
- Custom base name input
- Optional date or month tagging
- Accent-safe, filesystem-friendly names
- Dry-run preview before renaming
- CLI-native; `.exe` ready via PyInstaller

---

## Usage

```bash
python3 renamer_cli.py
Follow prompts:

Select folder (absolute path or press Enter for current)

Choose to include subfolders

Choose a base name (optional)

Toggle date and day inclusion

Preview rename plan before applying

🧪 Example
text
Copy
Edit
Input folder: /home/user/Pictures/Vacation/
Base name: TokyoTrip
Include subfolders: yes
Include date: yes
Include day: no

Result:
TokyoTrip_Shibuya_March_2025_001.jpg
TokyoTrip_Shibuya_March_2025_002.jpg
...
📦 Packaging
To create a .exe for Windows users:

bash
Copy
Edit
pyinstaller --onefile renamer_cli.py
✅ Requirements
Python 3.6+

Standard Library only (no external dependencies)
