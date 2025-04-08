from tkinter import *
from tkinter import ttk
from tkinter import filedialog




root = Tk()
root.title("Renamer")
#root.geometry("600x800")

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

#toggles date append
check_date = ttk.Checkbutton(mainframe, text="Append date to file names", variable=append_date)
check_date.config(command=toggle_day_checkbox)
check_date.grid(row=6, column=0, sticky=(W, E))
check_day = ttk.Checkbutton(mainframe, text="Include day in date", variable=append_day, state='disabled')
check_day.grid(row=7, column=0, sticky=W, pady=(0, 15))
toggle_day_checkbox()

#runs a print of projected changes
preview_btn = ttk.Button(root, text="Preview Naming")
preview_btn.grid(row=9, column=0, sticky=(W, E))

#applies renaming
Rename_btn = ttk.Button(root, text="Rename")
Rename_btn.grid(row=10, column=0, sticky=(W, E))




root.mainloop()