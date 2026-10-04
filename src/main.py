import tkinter as tk
from tkinter import ttk, messagebox
import traceback

from databases.vehicle_databases import vehicle_database
from databases.priority_weights import generate_weights
from databases.scoring_engine import rank_vehicles

parameters = [
    "Mission Role",
    "Terrain",
    "Payload",
    "Operating Range",
    "Minimum Mission Time",
    "Maximum Mission Time"
]

priority_options = [
    "Very High",
    "High",
    "Medium",
    "Low",
    "Very Low"
]

mission_roles = [
    "Reconnaissance",
    "Surveillance",
    "Combat / Tactical Support",
    "EOD / IED Disposal",
    "Mine Detection / Clearance",
    "CBRN Reconnaissance",
    "Logistics / Transport / Casualty Evacuation"
]

terrain_options = [
    "Paved Road / Urban",
    "Plain / Grassland",
    "Desert / Sand",
    "Mud / Soft Ground",
    "Rugged / Mountainous / Rocky",
    "Snow / Ice",
    "Extreme Obstacles / Stairs / Confined Spaces"
]

def clear_results():
    result_text.delete("1.0", tk.END)
    status_label.config(text="● Ready for mission analysis")

def calculate_results():
    try:
        raw_payload = payload_entry.get().strip()
        raw_range = range_entry.get().strip()
        raw_min_time = minimum_time_entry.get().strip()
        raw_max_time = maximum_time_entry.get().strip()

        if not all([raw_payload, raw_range, raw_min_time, raw_max_time]):
            messagebox.showerror("Input Error", "Please fill in all numerical fields.")
            return

        payload = float(raw_payload)
        operating_range = float(raw_range)
        minimum_time = float(raw_min_time)
        maximum_time = float(raw_max_time)

        if payload <= 0 or operating_range <= 0 or minimum_time <= 0 or maximum_time <= 0:
            messagebox.showerror("Invalid Data", "Values must be strictly greater than 0.")
            return

        if minimum_time > maximum_time:
            messagebox.showerror(
                "Invalid Mission Time",
                "Minimum mission time cannot exceed maximum mission time."
            )
            return

    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid numbers.")
        return

    requirements = {
        "Mission Role": role_variable.get(),
        "Terrain": terrain_variable.get(),
        "Payload": payload,
        "Operating Range": operating_range,
        "Minimum Mission Time": minimum_time,
        "Maximum Mission Time": maximum_time
    }

    priority_selections = {
        param: var.get() for param, var in priority_variables.items()
    }

    try:
        weights = generate_weights(priority_selections)
        results = rank_vehicles(vehicle_database, requirements, weights)

        feasible_list = results.get("feasible", [])
        infeasible_list = results.get("infeasible", [])
        derived = results.get("derived", {})

        clear_results()

        result_text.insert(tk.END, "STRIDE VEHICLE ANALYSIS\n", "title")
        result_text.insert(tk.END, "Indian Defence UGV Mission Compatibility & Selection Engine\n\n", "subtitle")

        # Operational Mission Context
        result_text.insert(tk.END, "MISSION PROFILE & DERIVED CONSTRAINTS\n", "heading")
        result_text.insert(tk.END, "-" * 68 + "\n", "separator")
        result_text.insert(tk.END, f"• Role: {requirements['Mission Role']}   |   Terrain: {requirements['Terrain']}\n", "meta_text")
        result_text.insert(tk.END, f"• Payload: {payload:.1f} kg   |   Mission Distance: {operating_range:.1f} km\n", "meta_text")
        result_text.insert(tk.END, f"• Time Window: {minimum_time:.1f}h - {maximum_time:.1f}h   |   Min Required Speed: {derived.get('required_speed', 0.0):.1f} km/h\n\n", "meta_text")

        if feasible_list:
            best_vehicle = feasible_list[0]
            expl = best_vehicle.get("explanation", {})

            result_text.insert(tk.END, "=" * 68 + "\n", "separator")
            result_text.insert(tk.END, "★ RECOMMENDED VEHICLE\n\n", "recommendation_title")
            result_text.insert(tk.END, f"{best_vehicle['vehicle_name']}   ({best_vehicle.get('vehicle_id', 'N/A')})\n", "recommendation_vehicle")
            result_text.insert(tk.END, f"Overall Suitability Score: {best_vehicle['final_score']:.2f}%\n", "recommendation_score")
            result_text.insert(tk.END, f"Manufacturer: {best_vehicle['details'].get('manufacturer', 'Unknown')}   |   Mobility: {best_vehicle['details'].get('mobility_type', 'N/A')}\n\n", "meta_text")

            result_text.insert(tk.END, "WHY RECOMMENDED:\n", "heading_small")
            result_text.insert(tk.END, f"• {expl.get('summary', 'Achieved top multi-criteria compatibility.')}\n", "recommendation_note")

            if expl.get("strengths"):
                result_text.insert(tk.END, "\nKEY STRENGTHS:\n", "heading_small")
                for s in expl["strengths"]:
                    result_text.insert(tk.END, f"  ✓  {s}\n", "bullet_green")

            if expl.get("weaknesses"):
                result_text.insert(tk.END, "\nOPERATIONAL NOTICES / UNCERTAINTIES:\n", "heading_small")
                for w in expl["weaknesses"]:
                    result_text.insert(tk.END, f"  ⚠  {w}\n", "bullet_yellow")

            result_text.insert(tk.END, "\n" + "=" * 68 + "\n\n", "separator")

            # Feasible Ranking Table
            result_text.insert(tk.END, "QUALIFIED VEHICLE RANKING (STAGE 2 MCDM)\n", "heading")
            result_text.insert(tk.END, "-" * 68 + "\n", "separator")
            result_text.insert(tk.END, f"{'RK':<4}{'VEHICLE':<24}{'OVERALL':<12}{'SPEED':<12}{'MOBILITY':<16}\n", "table_header")
            result_text.insert(tk.END, "-" * 68 + "\n", "separator")

            for index, vehicle in enumerate(feasible_list, start=1):
                score = vehicle["final_score"]
                v_name = vehicle["vehicle_name"]
                v_speed = f"{vehicle['details'].get('max_speed_kmh', 0.0):.1f} km/h"
                v_mob = vehicle['details'].get('mobility_type', 'N/A')
                result_text.insert(tk.END, f"{index:<4}", "rank")
                result_text.insert(tk.END, f"{v_name:<24}", "vehicle")
                result_text.insert(tk.END, f"{score:>6.2f}%    ", "score")
                result_text.insert(tk.END, f"{v_speed:<12}", "meta_text")
                result_text.insert(tk.END, f"{v_mob:<16}\n", "meta_text")

            # Phase 7: Decision Robustness & Sensitivity Briefing
            sens = results.get("sensitivity", {})
            if sens:
                result_text.insert(tk.END, "\nDECISION ROBUSTNESS & SENSITIVITY:\n", "heading_small")
                result_text.insert(tk.END, f"• {sens.get('summary', '')}\n", "meta_text")
                for sp in sens.get("sensitive_parameters", []):
                    result_text.insert(tk.END, f"  ↳ {sp}\n", "bullet_yellow")

        else:
            result_text.insert(tk.END, "⚠️ NO QUALIFIED CANDIDATES FOUND\n", "infeasible_title")
            result_text.insert(tk.END, "No vehicle in the database satisfies all mandatory mission constraints.\n\n", "bullet_red")

        # Infeasible Candidates Diagnostic
        if infeasible_list:
            result_text.insert(tk.END, "\n" + "-" * 68 + "\n", "separator")
            result_text.insert(tk.END, f"DISQUALIFIED CANDIDATES ({len(infeasible_list)} vehicles failed Stage 1 Gatekeeper):\n", "heading_small")
            for inf in infeasible_list:
                reasons = inf.get("explanation", {}).get("failed_constraints", ["Failed constraints"])
                result_text.insert(tk.END, f"  ✕  {inf['vehicle_name']}: ", "bullet_red")
                result_text.insert(tk.END, f"{'; '.join(reasons)}\n", "infeasible_text")

        status_label.config(
            text=f"● Analysis complete. {len(feasible_list)} qualified, {len(infeasible_list)} disqualified"
        )
        
        root.update_idletasks()
        outer_canvas.configure(scrollregion=outer_canvas.bbox("all"))
        outer_canvas.yview_moveto(0.0)

    except Exception as e:
        error_msg = traceback.format_exc()
        messagebox.showerror("Execution Error", f"An error occurred during analysis:\n\n{error_msg}")

root = tk.Tk()
root.title("STRIDE — Defense Vehicle Selection System")
root.geometry("900x850")
root.minsize(750, 600)

BG = "#111827"
CARD = "#1F2937"
CARD_LIGHT = "#273449"
TEXT = "#F3F4F6"
TEXT_SECONDARY = "#9CA3AF"
ACCENT = "#38BDF8"
ACCENT_DARK = "#0284C7"
SUCCESS = "#34D399"
BORDER = "#374151"
INPUT_BG = "#111827"

root.configure(background=BG)

style = ttk.Style()
style.theme_use("clam")
style.configure("Main.TFrame", background=BG)
style.configure("Title.TLabel", background=BG, foreground=TEXT, font=("Segoe UI", 25, "bold"))
style.configure("Subtitle.TLabel", background=BG, foreground=TEXT_SECONDARY, font=("Segoe UI", 10))
style.configure(
    "STRIDE.TCombobox",
    fieldbackground=INPUT_BG,
    background=INPUT_BG,
    foreground=TEXT,
    arrowcolor=ACCENT,
    bordercolor=BORDER,
    lightcolor=BORDER,
    darkcolor=BORDER
)
style.map(
    "STRIDE.TCombobox",
    fieldbackground=[("readonly", INPUT_BG)],
    foreground=[("readonly", TEXT)]
)

outer_container = tk.Frame(root, bg=BG)
outer_container.pack(fill="both", expand=True)

outer_canvas = tk.Canvas(outer_container, bg=BG, highlightthickness=0)
outer_canvas.pack(side="left", fill="both", expand=True)

outer_scrollbar = ttk.Scrollbar(outer_container, orient="vertical", command=outer_canvas.yview)
outer_scrollbar.pack(side="right", fill="y")
outer_canvas.configure(yscrollcommand=outer_scrollbar.set)

page_frame = tk.Frame(outer_canvas, bg=BG)
page_window = outer_canvas.create_window((0, 0), window=page_frame, anchor="nw")

def update_scroll_region(event=None):
    outer_canvas.configure(scrollregion=outer_canvas.bbox("all"))

def resize_page(event):
    outer_canvas.itemconfig(page_window, width=event.width)

page_frame.bind("<Configure>", update_scroll_region)
outer_canvas.bind("<Configure>", resize_page)

def mousewheel_scroll(event):
    outer_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

outer_canvas.bind_all("<MouseWheel>", mousewheel_scroll)

# Header
header = ttk.Frame(page_frame, style="Main.TFrame")
header.pack(fill="x", padx=35, pady=(25, 18))

title_frame = ttk.Frame(header, style="Main.TFrame")
title_frame.pack(fill="x")
ttk.Label(title_frame, text="STRIDE", style="Title.TLabel").pack(side="left")
ttk.Label(title_frame, text="DEFENSE VEHICLE ANALYSIS", style="Subtitle.TLabel").pack(side="left", padx=15, pady=(10, 0))
ttk.Label(header, text="Smart Terrain & Robotic Intelligence For Defense Engineering", style="Subtitle.TLabel").pack(anchor="w", pady=(2, 0))

# Requirements Form
requirements_frame = tk.Frame(page_frame, bg=CARD, highlightbackground=BORDER, highlightthickness=1)
requirements_frame.pack(fill="x", padx=35, pady=8)

tk.Label(
    requirements_frame,
    text="MISSION CONFIGURATION",
    bg=CARD,
    fg=TEXT,
    font=("Segoe UI", 12, "bold")
).grid(row=0, column=0, columnspan=3, sticky="w", padx=20, pady=(18, 4))

tk.Label(
    requirements_frame,
    text="Define mission requirements and their relative importance.",
    bg=CARD,
    fg=TEXT_SECONDARY,
    font=("Segoe UI", 9)
).grid(row=1, column=0, columnspan=3, sticky="w", padx=20, pady=(0, 15))

for column, text in enumerate(["REQUIREMENT", "REQUIRED VALUE", "PRIORITY"]):
    tk.Label(
        requirements_frame,
        text=text,
        bg=CARD,
        fg=TEXT_SECONDARY,
        font=("Segoe UI", 8, "bold")
    ).grid(row=2, column=column, sticky="w", padx=20, pady=(0, 8))

priority_variables = {}

def create_priority(row, parameter):
    variable = tk.StringVar(value="Medium")
    combo = ttk.Combobox(
        requirements_frame,
        textvariable=variable,
        values=priority_options,
        state="readonly",
        width=18,
        style="STRIDE.TCombobox"
    )
    combo.grid(row=row, column=2, sticky="w", padx=20, pady=7)
    priority_variables[parameter] = variable

# 1. Mission Role
tk.Label(requirements_frame, text="Mission Role", bg=CARD, fg=TEXT, font=("Segoe UI", 10)).grid(row=3, column=0, sticky="w", padx=20, pady=7)
role_variable = tk.StringVar(value=mission_roles[0])
ttk.Combobox(
    requirements_frame,
    textvariable=role_variable,
    values=mission_roles,
    state="readonly",
    width=30,
    style="STRIDE.TCombobox"
).grid(row=3, column=1, sticky="w", padx=20, pady=7)
create_priority(3, "Mission Role")

# 2. Terrain
tk.Label(requirements_frame, text="Terrain", bg=CARD, fg=TEXT, font=("Segoe UI", 10)).grid(row=4, column=0, sticky="w", padx=20, pady=7)
terrain_variable = tk.StringVar(value=terrain_options[0])
ttk.Combobox(
    requirements_frame,
    textvariable=terrain_variable,
    values=terrain_options,
    state="readonly",
    width=30,
    style="STRIDE.TCombobox"
).grid(row=4, column=1, sticky="w", padx=20, pady=7)
create_priority(4, "Terrain")

# 3. Payload
tk.Label(requirements_frame, text="Payload (kg)", bg=CARD, fg=TEXT, font=("Segoe UI", 10)).grid(row=5, column=0, sticky="w", padx=20, pady=7)
payload_entry = tk.Entry(
    requirements_frame,
    width=33,
    bg=INPUT_BG,
    fg=TEXT,
    insertbackground=TEXT,
    relief="flat",
    highlightbackground=BORDER,
    highlightcolor=ACCENT,
    highlightthickness=1,
    font=("Segoe UI", 10)
)
payload_entry.grid(row=5, column=1, sticky="w", padx=20, pady=7)
create_priority(5, "Payload")

# 4. Mission Distance
tk.Label(requirements_frame, text="Mission Distance (km)", bg=CARD, fg=TEXT, font=("Segoe UI", 10)).grid(row=6, column=0, sticky="w", padx=20, pady=7)
range_entry = tk.Entry(
    requirements_frame,
    width=33,
    bg=INPUT_BG,
    fg=TEXT,
    insertbackground=TEXT,
    relief="flat",
    highlightbackground=BORDER,
    highlightcolor=ACCENT,
    highlightthickness=1,
    font=("Segoe UI", 10)
)
range_entry.grid(row=6, column=1, sticky="w", padx=20, pady=7)
create_priority(6, "Operating Range")

# 5. Minimum Mission Time
tk.Label(requirements_frame, text="Minimum Mission Time (hours)", bg=CARD, fg=TEXT, font=("Segoe UI", 10)).grid(row=7, column=0, sticky="w", padx=20, pady=7)
minimum_time_entry = tk.Entry(
    requirements_frame,
    width=33,
    bg=INPUT_BG,
    fg=TEXT,
    insertbackground=TEXT,
    relief="flat",
    highlightbackground=BORDER,
    highlightcolor=ACCENT,
    highlightthickness=1,
    font=("Segoe UI", 10)
)
minimum_time_entry.grid(row=7, column=1, sticky="w", padx=20, pady=7)
create_priority(7, "Minimum Mission Time")

# 6. Maximum Mission Time
tk.Label(requirements_frame, text="Maximum Mission Time (hours)", bg=CARD, fg=TEXT, font=("Segoe UI", 10)).grid(row=8, column=0, sticky="w", padx=20, pady=7)
maximum_time_entry = tk.Entry(
    requirements_frame,
    width=33,
    bg=INPUT_BG,
    fg=TEXT,
    insertbackground=TEXT,
    relief="flat",
    highlightbackground=BORDER,
    highlightcolor=ACCENT,
    highlightthickness=1,
    font=("Segoe UI", 10)
)
maximum_time_entry.grid(row=8, column=1, sticky="w", padx=20, pady=7)
create_priority(8, "Maximum Mission Time")

# Action Buttons
action_frame = tk.Frame(page_frame, bg=BG)
action_frame.pack(fill="x", padx=35, pady=18)

tk.Button(
    action_frame,
    text="ANALYZE VEHICLES",
    command=calculate_results,
    bg=ACCENT_DARK,
    fg="white",
    activebackground=ACCENT,
    activeforeground="white",
    relief="flat",
    cursor="hand2",
    font=("Segoe UI", 11, "bold"),
    padx=25,
    pady=10
).pack(side="left")

tk.Button(
    action_frame,
    text="CLEAR RESULTS",
    command=clear_results,
    bg=CARD_LIGHT,
    fg=TEXT,
    activebackground=BORDER,
    activeforeground=TEXT,
    relief="flat",
    cursor="hand2",
    font=("Segoe UI", 10),
    padx=20,
    pady=10
).pack(side="left", padx=10)

# Results Display Frame
result_frame = tk.Frame(page_frame, bg=CARD, highlightbackground=BORDER, highlightthickness=1)
result_frame.pack(fill="both", expand=True, padx=35, pady=(0, 15))

tk.Label(
    result_frame,
    text="ANALYSIS RESULTS",
    bg=CARD,
    fg=TEXT,
    font=("Segoe UI", 12, "bold")
).pack(anchor="w", padx=20, pady=(15, 2))

tk.Label(
    result_frame,
    text="Compatibility ranking generated from the configured mission.",
    bg=CARD,
    fg=TEXT_SECONDARY,
    font=("Segoe UI", 9)
).pack(anchor="w", padx=20, pady=(0, 10))

result_container = tk.Frame(result_frame, bg=INPUT_BG)
result_container.pack(fill="both", expand=True, padx=15, pady=(0, 15))

result_text = tk.Text(
    result_container,
    bg=INPUT_BG,
    fg=TEXT,
    insertbackground=TEXT,
    selectbackground=ACCENT_DARK,
    relief="flat",
    wrap="none",
    font=("Consolas", 10),
    padx=15,
    pady=15,
    height=18
)
result_text.pack(side="left", fill="both", expand=True)

result_scrollbar = ttk.Scrollbar(result_container, orient="vertical", command=result_text.yview)
result_scrollbar.pack(side="right", fill="y")
result_text.configure(yscrollcommand=result_scrollbar.set)

result_text.tag_configure("title", foreground=ACCENT, font=("Segoe UI", 15, "bold"))
result_text.tag_configure("subtitle", foreground=TEXT_SECONDARY, font=("Segoe UI", 9))
result_text.tag_configure("heading", foreground=TEXT, font=("Segoe UI", 11, "bold"))
result_text.tag_configure("heading_small", foreground=TEXT, font=("Segoe UI", 10, "bold"))
result_text.tag_configure("meta_text", foreground=TEXT_SECONDARY, font=("Consolas", 9))
result_text.tag_configure("table_header", foreground=ACCENT, font=("Consolas", 10, "bold"))
result_text.tag_configure("rank", foreground=TEXT_SECONDARY, font=("Consolas", 10, "bold"))
result_text.tag_configure("vehicle", foreground=TEXT, font=("Consolas", 10, "bold"))
result_text.tag_configure("score", foreground=SUCCESS, font=("Consolas", 10, "bold"))
result_text.tag_configure("separator", foreground=BORDER)
result_text.tag_configure("recommendation_title", foreground=SUCCESS, font=("Segoe UI", 12, "bold"))
result_text.tag_configure("recommendation_vehicle", foreground=TEXT, font=("Segoe UI", 16, "bold"))
result_text.tag_configure("recommendation_score", foreground=SUCCESS, font=("Segoe UI", 12, "bold"))
result_text.tag_configure("recommendation_note", foreground=TEXT, font=("Segoe UI", 9))
result_text.tag_configure("bullet_green", foreground=SUCCESS, font=("Segoe UI", 9))
result_text.tag_configure("bullet_yellow", foreground="#FBBF24", font=("Segoe UI", 9))
result_text.tag_configure("bullet_red", foreground="#F87171", font=("Segoe UI", 9))
result_text.tag_configure("infeasible_title", foreground="#F87171", font=("Segoe UI", 11, "bold"))
result_text.tag_configure("infeasible_text", foreground=TEXT_SECONDARY, font=("Segoe UI", 9))

status_frame = tk.Frame(page_frame, bg=BG)
status_frame.pack(fill="x", padx=35, pady=(0, 12))

status_label = tk.Label(status_frame, text="● Ready for mission analysis", bg=BG, fg=TEXT_SECONDARY, font=("Segoe UI", 9))
status_label.pack(side="left")

tk.Label(status_frame, text="STRIDE Prototype v1.0", bg=BG, fg=TEXT_SECONDARY, font=("Segoe UI", 9)).pack(side="right")

root.mainloop()