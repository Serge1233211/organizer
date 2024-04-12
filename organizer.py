import os
import shutil
import json
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

# Reserved names for Windows file extensions
reserved_names = ['CON', 'PRN', 'AUX', 'NUL', 'COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8', 'COM9', 'LPT1', 'LPT2', 'LPT3', 'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9']

def load_folder_mappings():
    try:
        with open('file_types.json', 'r') as f:
            folder_mappings = json.load(f)
    except FileNotFoundError:
        folder_mappings = {
            "Documents": ["xlsx", "doc", "docx", "pdf", "txt"],
            "Images": ["jpg", "jpeg", "png", "gif"],
            "Audio": ["mp3", "wav", "flac"],
            "Video": ["mp4", "avi", "mov"],
            "Miscellaneous": []
        }
    return folder_mappings

def save_folder_mappings(folder_mappings):
    with open('file_types.json', 'w') as f:
        json.dump(folder_mappings, f, indent=4)

def choose_directory():
    path = filedialog.askdirectory()
    if path:
        organize_files(path)
    else:
        messagebox.showerror("Error", "No directory selected.")

def organize_files(path):
    folder_mappings = load_folder_mappings()
    items = os.listdir(path)
    for item in items:
        item_path = os.path.join(path, item)
        if os.path.isfile(item_path):
            filename, extension = os.path.splitext(item)
            extension = extension[1:].lower()
            if extension.upper() in reserved_names or extension == '':
                extension = 'Miscellaneous'
            folder_name = next((folder for folder, extensions in folder_mappings.items() if extension in extensions), "Miscellaneous")
            new_path = os.path.join(path, folder_name, item)  # Removed the extension folder
            if item_path != new_path:
                if not os.path.exists(os.path.join(path, folder_name)):
                    os.makedirs(os.path.join(path, folder_name))
                shutil.move(item_path, new_path)
            else:
                print(f"File '{item}' already organized in '{folder_name}' folder.")
        else:
            print(f"Skipping non-file item: '{item}'")

        # Add unknown extensions to the Miscellaneous category
        if extension not in folder_mappings["Miscellaneous"]:
            folder_mappings["Miscellaneous"].append(extension)

    save_folder_mappings(folder_mappings)
    print("File organization completed!")

# Create the GUI window
window = tk.Tk()
window.title("File Organizer")
choose_button = tk.Button(window, text='Choose Directory', command=choose_directory)
choose_button.pack(pady=20)
window.mainloop()
