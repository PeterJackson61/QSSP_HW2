import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
# from graph_builder import *
from CohenBergstresser1966 import *

graphs_path = './Graphs_Simulation/'
reference_paths = './Ref_Img/'

def update_images(*args):
    selected_material = material_var.get()
    graph_path = os.path.join(graphs_path, f'{selected_material}.png')
    reference_path = os.path.join(reference_paths, f'{selected_material}_Ref.png')

    if os.path.exists(graph_path) and os.path.exists(reference_path):
        # Load and display graph image
        graph_image = Image.open(graph_path)
        graph_image = graph_image.resize((600, 530), Image.Resampling.LANCZOS)
        graph_image = ImageTk.PhotoImage(graph_image)
        graph_label.config(image=graph_image)
        graph_label.image = graph_image

        # Load and display reference image
        reference_image = Image.open(reference_path)
        reference_image = reference_image.resize((600, 530), Image.Resampling.LANCZOS)
        reference_image = ImageTk.PhotoImage(reference_image)
        reference_label.config(image=reference_image)
        reference_label.image = reference_image
    else:
        print(f"Images not found for {selected_material}")

# Create the main application window

app = tk.Tk()
app.title("Band Structure Viewer")
# Dropdown list for material selection # Replace with your material names

material_var = tk.StringVar(value=material_list[0])
material_dropdown = ttk.Combobox(app, textvariable=material_var, values=material_list[0:-1], font=('Arial', 15))
material_dropdown.grid(row=0, column=0, padx=10, pady=10)

material_dropdown.bind("<<ComboboxSelected>>", update_images)
# Button to update images
update_button = tk.Button(app, text="Update Images", command=update_images)
update_button.grid(row=0, column=1, padx=10, pady=10)

# Image placeholders
graph_label = tk.Label(app)
graph_label.grid(row=1, column=0, padx=10, pady=10)

reference_label = tk.Label(app)
reference_label.grid(row=1, column=1, padx=10, pady=10)

# Initial image update
update_images()

# Start the main event loop
app.mainloop()