import tkinter as tk
from tkinter import ttk

from databases.vehicle_databases import display_all_vehicles
from databases.priority_weights import generate_weights


parameters = [
    "Mission Role",
    "Terrain",
    "Payload",
    "Maximum Speed",
    "Endurance",
    "Operating Range"
]

priority_options = [
    "Very High",
    "High",
    "Medium",
    "Low",
    "Very Low"
]

priority_order = {}


def submit_priorities():
    for parameter, variable in priority_variables.items():
        priority_order[parameter] = variable.get()

    weights = generate_weights(priority_order)

    result_text.delete("1.0", tk.END)

    result_text.insert(tk.END, "MISSION PRIORITY WEIGHTS\n")
    result_text.insert(tk.END, "=" * 40 + "\n\n")

    for parameter, weight in weights.items():
        result_text.insert(
            tk.END,
            f"{parameter:<20}: {weight:.2f}%\n"
        )


root = tk.Tk()
root.title("STRIDE - Mission Priority Setup")
root.geometry("600x500")

title = ttk.Label(
    root,
    text="STRIDE - Mission Priority Setup",
    font=("Arial", 16, "bold")
)
title.pack(pady=15)

instruction = ttk.Label(
    root,
    text="Select the importance of each mission requirement:"
)
instruction.pack(pady=5)

priority_variables = {}

for parameter in parameters:
    frame = ttk.Frame(root)
    frame.pack(fill="x", padx=30, pady=5)

    label = ttk.Label(frame, text=parameter, width=20)
    label.pack(side="left")

    variable = tk.StringVar(value="Medium")

    dropdown = ttk.Combobox(
        frame,
        textvariable=variable,
        values=priority_options,
        state="readonly",
        width=15
    )
    dropdown.pack(side="left")

    priority_variables[parameter] = variable


submit_button = ttk.Button(
    root,
    text="Generate Weights",
    command=submit_priorities
)
submit_button.pack(pady=20)

result_text = tk.Text(
    root,
    height=10,
    width=55
)
result_text.pack(pady=10)

root.mainloop()