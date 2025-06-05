# ui.py

import os
import json
import shutil
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import csv

from config import (
    EXTRACTION_FIELDS, FOLDER_INPROGRESS, FOLDER_PROCESSED,
    FOLDER_ERRORS, CSV_OUTPUT_PATH
)

# Global variables
current_image_path = None
current_json_path = None
current_data = {}
current_img = None
img_tk = None
zoom_factor = 1.0

# Create main window
root = tk.Tk()
root.title("Document Verification")
root.geometry("1600x1000")

# Frames for layout (75% image, 25% form)
left_frame = tk.Frame(root, width=1200, height=1000)
left_frame.pack(side="left", fill="both", expand=False)
left_frame.pack_propagate(False)

right_frame = tk.Frame(root, width=400, height=1000)
right_frame.pack(side="right", fill="both", expand=False)
right_frame.pack_propagate(False)

# Canvas for image with scrollbars
canvas_frame = tk.Frame(left_frame)
canvas_frame.pack(fill="both", expand=True)

canvas = tk.Canvas(canvas_frame, bg="gray")
canvas.pack(side="left", fill="both", expand=True)

v_scroll = tk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
v_scroll.pack(side="right", fill="y")

h_scroll = tk.Scrollbar(left_frame, orient="horizontal", command=canvas.xview)
h_scroll.pack(fill="x")

canvas.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)

image_id = None

# Zoom controls
zoom_frame = tk.Frame(left_frame)
zoom_frame.pack(pady=10)

def zoom_in():
    global zoom_factor
    zoom_factor += 0.1
    render_image()

def zoom_out():
    global zoom_factor
    zoom_factor = max(0.2, zoom_factor - 0.1)
    render_image()

zoom_in_btn = ttk.Button(zoom_frame, text="+ Zoom", command=zoom_in)
zoom_in_btn.pack(side="left", padx=5, ipadx=5, ipady=3)

zoom_out_btn = ttk.Button(zoom_frame, text="- Zoom", command=zoom_out)
zoom_out_btn.pack(side="left", padx=5, ipadx=5, ipady=3)

# Form section with LabelFrame (bordered)
form_frame = ttk.LabelFrame(right_frame, text="Extracted Data", padding=10)
form_frame.pack(fill="both", expand=True, padx=10, pady=10)

form_label = ttk.Label(form_frame, text="Verify extracted fields below:", font=("Arial", 14, "bold"))
form_label.pack(pady=5)

entries = {}

for field in EXTRACTION_FIELDS:
    label = ttk.Label(form_frame, text=field, font=("Arial", 12, "bold"))
    label.pack(anchor="w", padx=5, pady=(10, 0))
    entry = ttk.Entry(form_frame, width=35, font=("Arial", 12))
    entry.pack(padx=5, pady=5)
    entries[field] = entry

# Function to render image at current zoom
def render_image():
    global img_tk, image_id

    if current_img:
        width, height = current_img.size
        new_width = int(width * zoom_factor)
        new_height = int(height * zoom_factor)

        resized_img = current_img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        img_tk = ImageTk.PhotoImage(resized_img)

        canvas.delete("all")
        image_id = canvas.create_image(0, 0, anchor="nw", image=img_tk)
        canvas.config(scrollregion=canvas.bbox("all"))

# Load next file to review
def load_next_file():
    global current_image_path, current_json_path, current_data, current_img, zoom_factor

    files = [f for f in os.listdir(FOLDER_INPROGRESS) if f.lower().endswith(".jpg")]
    if not files:
        messagebox.showinfo("Done", "No more files to review.")
        root.quit()
        return

    file_name = files[0]
    base_name = os.path.splitext(file_name)[0]

    image_path = os.path.join(FOLDER_INPROGRESS, file_name)
    json_path = os.path.join(FOLDER_INPROGRESS, f"{base_name}.json")

    if not os.path.exists(json_path):
        shutil.move(image_path, os.path.join(FOLDER_ERRORS, file_name))
        load_next_file()
        return

    current_image_path = image_path
    current_json_path = json_path

    with open(json_path, "r") as jf:
        current_data = json.load(jf)

    current_img = Image.open(image_path)
    zoom_factor = (canvas.winfo_width() - 20) / current_img.size[0]
    if zoom_factor > 1.5:
        zoom_factor = 1.5
    elif zoom_factor < 0.2:
        zoom_factor = 0.2

    render_image()

    for field in EXTRACTION_FIELDS:
        value = current_data.get(field, "")
        entries[field].delete(0, tk.END)
        entries[field].insert(0, value)

# Confirm button action
def confirm_data():
    updated_data = {}
    for field in EXTRACTION_FIELDS:
        updated_data[field] = entries[field].get()

    file_exists = os.path.isfile(CSV_OUTPUT_PATH)
    with open(CSV_OUTPUT_PATH, "a", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=EXTRACTION_FIELDS)
        if not file_exists:
            writer.writeheader()
        writer.writerow(updated_data)

    shutil.move(current_image_path, os.path.join(FOLDER_PROCESSED, os.path.basename(current_image_path)))
    os.remove(current_json_path)

    load_next_file()

# Reject button action
def reject_data():
    shutil.move(current_image_path, os.path.join(FOLDER_ERRORS, os.path.basename(current_image_path)))
    shutil.move(current_json_path, os.path.join(FOLDER_ERRORS, os.path.basename(current_json_path)))

    load_next_file()

# Button frame
button_frame = tk.Frame(form_frame)
button_frame.pack(pady=20)

confirm_button = ttk.Button(button_frame, text="✔ Confirm & Next", command=confirm_data)
confirm_button.pack(side="left", padx=10, ipadx=10, ipady=8)

reject_button = ttk.Button(button_frame, text="✖ Reject & Next", command=reject_data)
reject_button.pack(side="right", padx=10, ipadx=10, ipady=8)

# Start first file
root.after(100, load_next_file)

# Run the application
root.mainloop()
