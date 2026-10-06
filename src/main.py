import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import traceback
from PIL import Image, ImageTk

# Add src to sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from databases.vehicle_manager import get_active_catalog, add_vehicle, load_custom_vehicles
from databases.priority_weights import generate_weights
from databases.scoring_engine import rank_vehicles
from mission.mission_parser import parse_mission_narrative

# Standardized Taxonomies
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

# Categorized Mission Roles for Engineer's Product Feel
role_categories = {
    "ISR & Target Acquisition": [
        ("Surveillance", "Border / perimeter optical watch & forward sensor monitoring"),
        ("Reconnaissance", "Route exploration, terrain scouting & enemy position tracking"),
        ("CBRN Reconnaissance", "Chemical, biological, radiological & nuclear sensor detection")
    ],
    "Combat & Direct Action": [
        ("Combat / Tactical Support", "Remote weapon station (RCWS), suppressing fire & force protection"),
        ("Precision Strike / Anti-Armor", "ATGM anti-tank guided missile & loitering munition platform"),
        ("Urban Assault / Confined Space Recon", "Counter-terror room breaching, stairs & CQB tactical reconnaissance")
    ],
    "Engineering & Field Logistics": [
        ("Logistics / Transport / Casualty Evacuation", "Ammunition resupply, heavy payload hauling & CASEVAC"),
        ("High-Altitude Logistics / Extreme Cold", "Himalayan LAC/LOC sub-zero snow transport up to 5,000m ASL"),
        ("Mine Detection / Clearance", "Ground-penetrating radar, flail/plow counter-mine breaching"),
        ("EOD / IED Disposal", "Robotic manipulator arm, explosive disruptor & bomb neutralizer")
    ]
}

mission_roles = [r[0] for cat in role_categories.values() for r in cat]

terrain_options = [
    "Paved Road / Urban",
    "Plain / Grassland",
    "Desert / Sand",
    "Mud / Soft Ground",
    "Rugged / Mountainous / Rocky",
    "Snow / Ice",
    "Extreme Obstacles / Stairs / Confined Spaces",
    "Amphibious / Riverine / Fording"
]

control_links = [
    "Any / Standard Tactical Link",
    "RF LOS (Direct Ground Radio Line-of-Sight - 0 to 20 km)",
    "COFDM NLOS Mesh (Anti-Jamming / Hills, Valleys & Urban)",
    "SATCOM / BLOS Drone Relay (Beyond Line-of-Sight Deep Ingress)",
    "Autonomous Waypoint / GNSS-Denied (GPS-Jammed / Radio Silence)"
]

stealth_options = [
    "Standard Military Profile (Engine / Battery)",
    "Silent Electric Only (Strict Acoustic/Thermal Suppression)"
]

# =============================================================================
# INDIAN DEFENCE TACTICAL THEME PALETTE
# =============================================================================
BG = "#090D12"                # Deep Strategic Dark
CARD = "#121924"              # Matte Navy Slate Card
CARD_LIGHT = "#182232"        # Hover / Sub-Card
CARD_BORDER = "#223043"       # Tactical Slate Frame Border
INPUT_BG = "#0D131C"          # Field Input Background

# Tiranga & Defence Accents
ACCENT = "#FF9933"            # Tiranga Kesari / Tactical Saffron
ACCENT_LIGHT = "#FFB266"      # Bright Saffron Highlight
ACCENT_DARK = "#D97706"       # Deep Saffron Border / Shadow
CHAKRA_NAVY = "#2563EB"       # Ashoka Navy Blue
SUCCESS = "#10B981"           # Tactical Olive / Emerald Green
WARNING = "#F59E0B"           # Operational Warning Amber
DANGER = "#EF4444"            # Critical Disqualification Red

TEXT = "#F8FAFC"              # Pure Titanium White
TEXT_MUTED = "#94A3B8"        # Tactical Muted Silver
TEXT_DIM = "#64748B"          # Muted Metadata


# Main Window Setup
root = tk.Tk()
root.title("STRIDE — Indian Defence UGV Mission Intelligence & Decision Support Engine")
root.geometry("1340x880")
root.minsize(1120, 750)
root.configure(background=BG)

style = ttk.Style()
style.theme_use("clam")
style.configure("Main.TFrame", background=BG)
style.configure(
    "STRIDE.TCombobox",
    fieldbackground=INPUT_BG,
    background=CARD,
    foreground=TEXT,
    arrowcolor=ACCENT,
    bordercolor=CARD_BORDER,
    lightcolor=CARD_BORDER,
    darkcolor=CARD_BORDER,
    font=("Segoe UI", 9)
)
style.map(
    "STRIDE.TCombobox",
    fieldbackground=[("readonly", INPUT_BG)],
    foreground=[("readonly", TEXT)]
)

# Global Image Cache
current_vehicle_photo = None
current_results_data = None


# =============================================================================
# TRICOLOR ACCENT HEADER
# =============================================================================
top_tricolor = tk.Frame(root, height=4, bg=BG)
top_tricolor.pack(fill="x")
tk.Frame(top_tricolor, bg="#FF9933", height=4).pack(side="left", fill="both", expand=True)
tk.Frame(top_tricolor, bg="#FFFFFF", height=4).pack(side="left", fill="both", expand=True)
tk.Frame(top_tricolor, bg="#138808", height=4).pack(side="left", fill="both", expand=True)

header_bar = tk.Frame(root, bg=CARD, highlightbackground=CARD_BORDER, highlightthickness=1, padx=25, pady=12)
header_bar.pack(fill="x")

header_left = tk.Frame(header_bar, bg=CARD)
header_left.pack(side="left")

title_box = tk.Frame(header_left, bg=CARD)
title_box.pack(anchor="w")

tk.Label(
    title_box,
    text="STRIDE",
    bg=CARD,
    fg=ACCENT,
    font=("Segoe UI", 18, "bold")
).pack(side="left")

tk.Label(
    title_box,
    text="🇮🇳 ATMANIRBHAR DEFENCE C4ISR",
    bg=INPUT_BG,
    fg=ACCENT_LIGHT,
    font=("Segoe UI", 8, "bold"),
    padx=8,
    pady=2,
    relief="flat",
    highlightbackground=CARD_BORDER,
    highlightthickness=1
).pack(side="left", padx=12)

catalog_init = get_active_catalog()
tk.Label(
    title_box,
    text=f"{len(catalog_init)} Indian Platforms Cataloged",
    bg=CARD,
    fg=SUCCESS,
    font=("Segoe UI", 9, "bold")
).pack(side="left")

tk.Label(
    header_left,
    text="Smart Terrain & Robotic Intelligence for Defense Engineering • Tactical Decision & Mission Support System",
    bg=CARD,
    fg=TEXT_MUTED,
    font=("Segoe UI", 9)
).pack(anchor="w", pady=(3, 0))

header_right = tk.Frame(header_bar, bg=CARD)
header_right.pack(side="right")


# =============================================================================
# VIEW CONTROLLER (INPUT VIEW vs RESULTS VIEW)
# =============================================================================
view_container = tk.Frame(root, bg=BG)
view_container.pack(fill="both", expand=True)

input_view_frame = tk.Frame(view_container, bg=BG)
results_view_frame = tk.Frame(view_container, bg=BG)

input_view_frame.pack(fill="both", expand=True)


def switch_to_input_view():
    results_view_frame.pack_forget()
    input_view_frame.pack(fill="both", expand=True)
    status_label.config(text=f"● Ready for mission analysis ({len(get_active_catalog())} Indian UGVs active)")


def switch_to_results_view():
    input_view_frame.pack_forget()
    results_view_frame.pack(fill="both", expand=True)


# =============================================================================
# INPUT VIEW: SCROLLABLE CANVAS
# =============================================================================
input_canvas = tk.Canvas(input_view_frame, bg=BG, highlightthickness=0)
input_canvas.pack(side="left", fill="both", expand=True)

input_scrollbar = ttk.Scrollbar(input_view_frame, orient="vertical", command=input_canvas.yview)
input_scrollbar.pack(side="right", fill="y")
input_canvas.configure(yscrollcommand=input_scrollbar.set)

input_content = tk.Frame(input_canvas, bg=BG)
input_window_id = input_canvas.create_window((0, 0), window=input_content, anchor="nw")


def resize_input_canvas(event):
    input_canvas.itemconfig(input_window_id, width=event.width)


def update_input_scroll(event=None):
    input_canvas.configure(scrollregion=input_canvas.bbox("all"))


input_content.bind("<Configure>", update_input_scroll)
input_canvas.bind("<Configure>", resize_input_canvas)


# Mousewheel binding
def on_mousewheel(event):
    if input_view_frame.winfo_ismapped():
        input_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    elif results_view_frame.winfo_ismapped() and results_canvas:
        results_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")


root.bind_all("<MouseWheel>", on_mousewheel)


# =============================================================================
# INPUT VIEW: SECTION 1 - TACTICAL MULTI-ROLE CAPABILITY MATRIX (ENGINEER'S DECK)
# =============================================================================
role_matrix_card = tk.Frame(input_content, bg=CARD, highlightbackground=CARD_BORDER, highlightthickness=1, padx=25, pady=18)
role_matrix_card.pack(fill="x", padx=30, pady=(20, 10))

role_matrix_header = tk.Frame(role_matrix_card, bg=CARD)
role_matrix_header.pack(fill="x", pady=(0, 12))

tk.Label(
    role_matrix_header,
    text="1. TACTICAL MISSION ROLES & OPERATIONAL PROFILE",
    bg=CARD,
    fg=TEXT,
    font=("Segoe UI", 12, "bold")
).pack(side="left")

role_count_badge = tk.Label(
    role_matrix_header,
    text="1 Active Role Selected",
    bg=INPUT_BG,
    fg=ACCENT,
    font=("Segoe UI", 9, "bold"),
    padx=10,
    pady=3,
    relief="flat",
    highlightbackground=CARD_BORDER,
    highlightthickness=1
)
role_count_badge.pack(side="right")

tk.Label(
    role_matrix_card,
    text="Select single or concurrent mission capabilities. The engine evaluates multi-role flexibility and tactical specialization.",
    bg=CARD,
    fg=TEXT_MUTED,
    font=("Segoe UI", 9)
).pack(anchor="w", pady=(0, 14))

# Role checkboxes state
role_variables = {}


def on_role_toggle():
    selected = [r for r, v in role_variables.items() if v.get()]
    if not selected:
        role_count_badge.config(text="⚠ 0 Roles Selected (Please select at least 1)", fg=DANGER)
    elif len(selected) == 1:
        role_count_badge.config(text=f"Primary: {selected[0]}", fg=SUCCESS)
    else:
        role_count_badge.config(text=f"{len(selected)} Concurrent Roles Active", fg=ACCENT)


role_columns_frame = tk.Frame(role_matrix_card, bg=CARD)
role_columns_frame.pack(fill="x")

for col_idx, (cat_name, cat_roles) in enumerate(role_categories.items()):
    cat_box = tk.Frame(role_columns_frame, bg=INPUT_BG, highlightbackground=CARD_BORDER, highlightthickness=1, padx=12, pady=10)
    cat_box.pack(side="left", fill="both", expand=True, padx=(0 if col_idx == 0 else 10, 0))

    tk.Label(
        cat_box,
        text=cat_name.upper(),
        bg=INPUT_BG,
        fg=ACCENT_LIGHT,
        font=("Segoe UI", 9, "bold")
    ).pack(anchor="w", pady=(0, 8))

    for r_name, r_desc in cat_roles:
        var = tk.BooleanVar(value=(r_name == "Surveillance"))
        role_variables[r_name] = var

        r_row = tk.Frame(cat_box, bg=INPUT_BG)
        r_row.pack(fill="x", pady=3)

        cb = tk.Checkbutton(
            r_row,
            text=r_name,
            variable=var,
            command=on_role_toggle,
            bg=INPUT_BG,
            fg=TEXT,
            selectcolor=CARD,
            activebackground=INPUT_BG,
            activeforeground=ACCENT,
            font=("Segoe UI", 9, "bold")
        )
        cb.pack(anchor="w")

        tk.Label(
            r_row,
            text=r_desc,
            bg=INPUT_BG,
            fg=TEXT_DIM,
            font=("Segoe UI", 8),
            wraplength=320,
            justify="left"
        ).pack(anchor="w", padx=(22, 0))


# =============================================================================
# INPUT VIEW: SECTION 2 - OPERATIONAL MOBILITY & PHYSICAL REQUIREMENTS
# =============================================================================
mobility_card = tk.Frame(input_content, bg=CARD, highlightbackground=CARD_BORDER, highlightthickness=1, padx=25, pady=18)
mobility_card.pack(fill="x", padx=30, pady=10)

tk.Label(
    mobility_card,
    text="2. OPERATIONAL ENVIRONMENT & MOBILITY REQUIREMENTS",
    bg=CARD,
    fg=TEXT,
    font=("Segoe UI", 12, "bold")
).pack(anchor="w")

tk.Label(
    mobility_card,
    text="Specify environmental terrain, physical payload, transit range, and time limits along with priority weights.",
    bg=CARD,
    fg=TEXT_MUTED,
    font=("Segoe UI", 9)
).pack(anchor="w", pady=(2, 14))

# Table layout for parameters
params_table = tk.Frame(mobility_card, bg=CARD)
params_table.pack(fill="x")

for c_idx, title in enumerate(["TACTICAL PARAMETER", "REQUIRED SPECIFICATION / VALUE", "MISSION PRIORITY WEIGHT"]):
    tk.Label(
        params_table,
        text=title,
        bg=CARD,
        fg=TEXT_MUTED,
        font=("Segoe UI", 8, "bold")
    ).grid(row=0, column=c_idx, sticky="w", padx=10, pady=(0, 8))

priority_variables = {}


def add_priority_combo(parent, row, col, param_name, default="Medium"):
    var = tk.StringVar(value=default)
    cb = ttk.Combobox(
        parent,
        textvariable=var,
        values=priority_options,
        state="readonly",
        width=16,
        style="STRIDE.TCombobox"
    )
    cb.grid(row=row, column=col, sticky="w", padx=10, pady=4)
    priority_variables[param_name] = var
    return var


# Row 1: Mission Role Priority
tk.Label(params_table, text="Role Weighting (Relative Weight):", bg=CARD, fg=TEXT, font=("Segoe UI", 9)).grid(row=1, column=0, sticky="w", padx=10, pady=4)
tk.Label(params_table, text="Applies to selected active mission roles above", bg=CARD, fg=TEXT_DIM, font=("Segoe UI", 8)).grid(row=1, column=1, sticky="w", padx=10, pady=4)
add_priority_combo(params_table, 1, 2, "Mission Role", "High")

# Row 2: Operational Terrain
tk.Label(params_table, text="Operational Terrain:", bg=CARD, fg=TEXT, font=("Segoe UI", 9, "bold")).grid(row=2, column=0, sticky="w", padx=10, pady=4)
terrain_var = tk.StringVar(value=terrain_options[1])
terrain_combo = ttk.Combobox(params_table, textvariable=terrain_var, values=terrain_options, state="readonly", width=34, style="STRIDE.TCombobox")
terrain_combo.grid(row=2, column=1, sticky="w", padx=10, pady=4)
add_priority_combo(params_table, 2, 2, "Terrain", "High")

# Row 3: Payload Capacity
tk.Label(params_table, text="Payload Capacity (kg):", bg=CARD, fg=TEXT, font=("Segoe UI", 9, "bold")).grid(row=3, column=0, sticky="w", padx=10, pady=4)
payload_entry = tk.Entry(params_table, width=36, bg=INPUT_BG, fg=TEXT, insertbackground=TEXT, relief="flat", highlightbackground=CARD_BORDER, highlightcolor=ACCENT, highlightthickness=1, font=("Segoe UI", 9))
payload_entry.insert(0, "50.0")
payload_entry.grid(row=3, column=1, sticky="w", padx=10, pady=4)
add_priority_combo(params_table, 3, 2, "Payload", "Medium")

# Row 4: Mission Transit Distance
tk.Label(params_table, text="Mission Transit Distance (km):", bg=CARD, fg=TEXT, font=("Segoe UI", 9, "bold")).grid(row=4, column=0, sticky="w", padx=10, pady=4)
range_entry = tk.Entry(params_table, width=36, bg=INPUT_BG, fg=TEXT, insertbackground=TEXT, relief="flat", highlightbackground=CARD_BORDER, highlightcolor=ACCENT, highlightthickness=1, font=("Segoe UI", 9))
range_entry.insert(0, "15.0")
range_entry.grid(row=4, column=1, sticky="w", padx=10, pady=4)
add_priority_combo(params_table, 4, 2, "Operating Range", "High")

# Row 5: Minimum Mission Time
tk.Label(params_table, text="Minimum Mission Duration (hours):", bg=CARD, fg=TEXT, font=("Segoe UI", 9)).grid(row=5, column=0, sticky="w", padx=10, pady=4)
min_time_entry = tk.Entry(params_table, width=36, bg=INPUT_BG, fg=TEXT, insertbackground=TEXT, relief="flat", highlightbackground=CARD_BORDER, highlightcolor=ACCENT, highlightthickness=1, font=("Segoe UI", 9))
min_time_entry.insert(0, "1.0")
min_time_entry.grid(row=5, column=1, sticky="w", padx=10, pady=4)
add_priority_combo(params_table, 5, 2, "Minimum Mission Time", "Low")

# Row 6: Maximum Mission Time
tk.Label(params_table, text="Maximum Mission Deadline (hours):", bg=CARD, fg=TEXT, font=("Segoe UI", 9, "bold")).grid(row=6, column=0, sticky="w", padx=10, pady=4)
max_time_entry = tk.Entry(params_table, width=36, bg=INPUT_BG, fg=TEXT, insertbackground=TEXT, relief="flat", highlightbackground=CARD_BORDER, highlightcolor=ACCENT, highlightthickness=1, font=("Segoe UI", 9))
max_time_entry.insert(0, "4.0")
max_time_entry.grid(row=6, column=1, sticky="w", padx=10, pady=4)
add_priority_combo(params_table, 6, 2, "Maximum Mission Time", "Medium")


# =============================================================================
# INPUT VIEW: SECTION 3 - COMMAND & TELEMETRY LINK + TACTICAL ENVELOPES
# =============================================================================
tactical_card = tk.Frame(input_content, bg=CARD, highlightbackground=CARD_BORDER, highlightthickness=1, padx=25, pady=18)
tactical_card.pack(fill="x", padx=30, pady=10)

tk.Label(
    tactical_card,
    text="3. COMMAND & TELEMETRY DATA LINK & TACTICAL ENVELOPES",
    bg=CARD,
    fg=TEXT,
    font=("Segoe UI", 12, "bold")
).pack(anchor="w")

tk.Label(
    tactical_card,
    text="Configure RF electronic warfare resilience, line-of-sight occlusion protocol, Himalayan altitude rating, and acoustic stealth.",
    bg=CARD,
    fg=TEXT_MUTED,
    font=("Segoe UI", 9)
).pack(anchor="w", pady=(2, 14))

tac_grid = tk.Frame(tactical_card, bg=CARD)
tac_grid.pack(fill="x")

# Row 1: Command & Telemetry Link
tk.Label(tac_grid, text="Command & Telemetry Data Link:", bg=CARD, fg=TEXT, font=("Segoe UI", 9, "bold")).grid(row=0, column=0, sticky="w", padx=(0, 15), pady=6)
link_var = tk.StringVar(value=control_links[0])
link_combo = ttk.Combobox(tac_grid, textvariable=link_var, values=control_links, state="readonly", width=42, style="STRIDE.TCombobox")
link_combo.grid(row=0, column=1, sticky="w", pady=6)

tk.Label(
    tac_grid,
    text="ℹ C2 wireless protocol based on terrain occlusion & electronic warfare threat",
    bg=CARD,
    fg=TEXT_DIM,
    font=("Segoe UI", 8)
).grid(row=0, column=2, sticky="w", padx=(15, 0), pady=6)

# Row 2: Standoff Range
tk.Label(tac_grid, text="Operator Standoff Range (km):", bg=CARD, fg=TEXT, font=("Segoe UI", 9, "bold")).grid(row=1, column=0, sticky="w", padx=(0, 15), pady=6)
standoff_entry = tk.Entry(tac_grid, width=20, bg=INPUT_BG, fg=TEXT, insertbackground=TEXT, relief="flat", highlightbackground=CARD_BORDER, highlightcolor=ACCENT, highlightthickness=1, font=("Segoe UI", 9))
standoff_entry.insert(0, "10.0")
standoff_entry.grid(row=1, column=1, sticky="w", pady=6)

tk.Label(
    tac_grid,
    text="[Direct Indian Ground RF max: ~25 km without aerial/satellite relay]",
    bg=CARD,
    fg=ACCENT,
    font=("Segoe UI", 8)
).grid(row=1, column=2, sticky="w", padx=(15, 0), pady=6)

# Row 3: Altitude & Temperature
tk.Label(tac_grid, text="Operational Altitude (m ASL):", bg=CARD, fg=TEXT, font=("Segoe UI", 9)).grid(row=2, column=0, sticky="w", padx=(0, 15), pady=6)
alt_entry = tk.Entry(tac_grid, width=20, bg=INPUT_BG, fg=TEXT, insertbackground=TEXT, relief="flat", highlightbackground=CARD_BORDER, highlightcolor=ACCENT, highlightthickness=1, font=("Segoe UI", 9))
alt_entry.insert(0, "1500")
alt_entry.grid(row=2, column=1, sticky="w", pady=6)

tk.Label(
    tac_grid,
    text="[Ladakh / LAC High-Altitude: 3,000m to 5,200m ASL]",
    bg=CARD,
    fg=TEXT_DIM,
    font=("Segoe UI", 8)
).grid(row=2, column=2, sticky="w", padx=(15, 0), pady=6)

# Row 4: Temperature
tk.Label(tac_grid, text="Operating Temperature (°C):", bg=CARD, fg=TEXT, font=("Segoe UI", 9)).grid(row=3, column=0, sticky="w", padx=(0, 15), pady=6)
temp_entry = tk.Entry(tac_grid, width=20, bg=INPUT_BG, fg=TEXT, insertbackground=TEXT, relief="flat", highlightbackground=CARD_BORDER, highlightcolor=ACCENT, highlightthickness=1, font=("Segoe UI", 9))
temp_entry.insert(0, "20.0")
temp_entry.grid(row=3, column=1, sticky="w", pady=6)

tk.Label(
    tac_grid,
    text="[Himalayan Winter: -30°C | Thar Desert Summer: +52°C]",
    bg=CARD,
    fg=TEXT_DIM,
    font=("Segoe UI", 8)
).grid(row=3, column=2, sticky="w", padx=(15, 0), pady=6)

# Row 5: Stealth Profile
tk.Label(tac_grid, text="Acoustic & Thermal Stealth Profile:", bg=CARD, fg=TEXT, font=("Segoe UI", 9, "bold")).grid(row=4, column=0, sticky="w", padx=(0, 15), pady=6)
stealth_var = tk.StringVar(value=stealth_options[0])
stealth_combo = ttk.Combobox(tac_grid, textvariable=stealth_var, values=stealth_options, state="readonly", width=42, style="STRIDE.TCombobox")
stealth_combo.grid(row=4, column=1, sticky="w", pady=6)

tk.Label(
    tac_grid,
    text="[Heavy payloads >100kg over long distance typically require Hybrid/Diesel power]",
    bg=CARD,
    fg=WARNING,
    font=("Segoe UI", 8)
).grid(row=4, column=2, sticky="w", padx=(15, 0), pady=6)


# =============================================================================
# INPUT VIEW: PRIMARY ACTION BUTTON
# =============================================================================
action_bar = tk.Frame(input_content, bg=BG)
action_bar.pack(fill="x", padx=30, pady=(15, 30))

analyze_btn = tk.Button(
    action_bar,
    text="⚡  RUN TACTICAL MISSION EVALUATION  &  RECOMMENDATION",
    command=lambda: run_analysis_pipeline(),
    bg=ACCENT,
    fg="#0B0F14",
    activebackground=ACCENT_LIGHT,
    activeforeground="#0B0F14",
    relief="flat",
    cursor="hand2",
    font=("Segoe UI", 12, "bold"),
    padx=25,
    pady=14
)
analyze_btn.pack(side="left")

status_label = tk.Label(
    action_bar,
    text=f"● Ready for mission analysis ({len(catalog_init)} Indian UGVs active)",
    bg=BG,
    fg=TEXT_MUTED,
    font=("Segoe UI", 9)
)
status_label.pack(side="left", padx=20)


# =============================================================================
# RESULTS VIEW: DEDICATED FRESH DOSSIER SCREEN (ITEM 1 & 2)
# =============================================================================
results_top_nav = tk.Frame(results_view_frame, bg=CARD, highlightbackground=CARD_BORDER, highlightthickness=1, padx=25, pady=12)
results_top_nav.pack(fill="x")

back_btn = tk.Button(
    results_top_nav,
    text="⬅  Back to Mission Configuration",
    command=switch_to_input_view,
    bg=INPUT_BG,
    fg=ACCENT,
    activebackground=CARD_LIGHT,
    activeforeground=ACCENT_LIGHT,
    relief="flat",
    cursor="hand2",
    font=("Segoe UI", 10, "bold"),
    padx=16,
    pady=6,
    highlightbackground=ACCENT_DARK,
    highlightthickness=1
)
back_btn.pack(side="left")

results_mode_badge = tk.Label(
    results_top_nav,
    text="● ANALYSIS COMPLETE",
    bg=INPUT_BG,
    fg=SUCCESS,
    font=("Segoe UI", 9, "bold"),
    padx=12,
    pady=5,
    relief="flat",
    highlightbackground=CARD_BORDER,
    highlightthickness=1
)
results_mode_badge.pack(side="left", padx=15)

mission_summary_pill = tk.Label(
    results_top_nav,
    text="",
    bg=INPUT_BG,
    fg=TEXT_MUTED,
    font=("Segoe UI", 9),
    padx=12,
    pady=5,
    relief="flat",
    highlightbackground=CARD_BORDER,
    highlightthickness=1
)
mission_summary_pill.pack(side="right")


# Results Scrollable Container
results_canvas = tk.Canvas(results_view_frame, bg=BG, highlightthickness=0)
results_canvas.pack(side="left", fill="both", expand=True)

results_scrollbar = ttk.Scrollbar(results_view_frame, orient="vertical", command=results_canvas.yview)
results_scrollbar.pack(side="right", fill="y")
results_canvas.configure(yscrollcommand=results_scrollbar.set)

results_content = tk.Frame(results_canvas, bg=BG)
results_window_id = results_canvas.create_window((0, 0), window=results_content, anchor="nw")


def resize_results_canvas(event):
    results_canvas.itemconfig(results_window_id, width=event.width)


def update_results_scroll(event=None):
    results_canvas.configure(scrollregion=results_canvas.bbox("all"))


results_content.bind("<Configure>", update_results_scroll)
results_canvas.bind("<Configure>", resize_results_canvas)


# Split Layout in Results Content
dossier_split = tk.Frame(results_content, bg=BG)
dossier_split.pack(fill="x", padx=30, pady=20)

# LEFT COLUMN: VEHICLE SHOWCASE & HIGH-DEFINITION PHOTOGRAPH (ITEM 1)
showcase_col = tk.Frame(dossier_split, bg=CARD, highlightbackground=CARD_BORDER, highlightthickness=1, width=470)
showcase_col.pack(side="left", fill="both", expand=False)
showcase_col.pack_propagate(False)

# Left Column Accent Header
sc_header = tk.Frame(showcase_col, bg=CARD, padx=15, pady=12)
sc_header.pack(fill="x")

tk.Label(
    sc_header,
    text="TOP RECOMMENDED PLATFORM",
    bg=CARD,
    fg=ACCENT,
    font=("Segoe UI", 9, "bold")
).pack(anchor="w")

showcase_veh_name = tk.Label(
    sc_header,
    text="Platform Name",
    bg=CARD,
    fg=TEXT,
    font=("Segoe UI", 16, "bold"),
    wraplength=430,
    justify="left"
)
showcase_veh_name.pack(anchor="w")

showcase_veh_sub = tk.Label(
    sc_header,
    text="Manufacturer • ID • Status",
    bg=CARD,
    fg=TEXT_MUTED,
    font=("Segoe UI", 9)
)
showcase_veh_sub.pack(anchor="w", pady=(2, 0))

# Large Crystal-Clear Image Box (440x260px)
image_container = tk.Frame(showcase_col, bg=INPUT_BG, highlightbackground=CARD_BORDER, highlightthickness=1, width=440, height=260)
image_container.pack(padx=15, pady=(0, 10))
image_container.pack_propagate(False)

showcase_image_label = tk.Label(image_container, bg=INPUT_BG, text="Loading Platform Image...", fg=TEXT_MUTED, font=("Segoe UI", 10))
showcase_image_label.pack(fill="both", expand=True)

# Technical Specification Grid
specs_box = tk.Frame(showcase_col, bg=CARD, padx=15, pady=10)
specs_box.pack(fill="both", expand=True)

tk.Label(specs_box, text="KEY PLATFORM SPECIFICATIONS", bg=CARD, fg=TEXT, font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=(0, 6))

specs_grid = tk.Frame(specs_box, bg=CARD)
specs_grid.pack(fill="x")

spec_labels = {}
spec_fields = [
    ("Mobility Type", "mobility"),
    ("Payload Capacity", "payload"),
    ("Maximum Speed", "speed"),
    ("Operating Range", "range"),
    ("Continuous Endurance", "endurance"),
    ("Max Control Standoff", "standoff"),
    ("Primary Control Link", "link"),
    ("Climate & Altitude", "climate")
]

for idx, (title, key) in enumerate(spec_fields):
    row = idx // 2
    col = (idx % 2) * 2
    tk.Label(specs_grid, text=f"{title}:", bg=CARD, fg=TEXT_MUTED, font=("Segoe UI", 8)).grid(row=row, column=col, sticky="w", pady=2)
    val_lbl = tk.Label(specs_grid, text="--", bg=CARD, fg=TEXT, font=("Segoe UI", 8, "bold"))
    val_lbl.grid(row=row, column=col+1, sticky="w", padx=(4, 12), pady=2)
    spec_labels[key] = val_lbl


# RIGHT COLUMN: TACTICAL DECISION & RECOMMENDATION DOSSIER (ITEM 2)
dossier_col = tk.Frame(dossier_split, bg=BG)
dossier_col.pack(side="left", fill="both", expand=True, padx=(20, 0))

# Top Score Card
score_card = tk.Frame(dossier_col, bg=CARD, highlightbackground=CARD_BORDER, highlightthickness=1, padx=20, pady=15)
score_card.pack(fill="x", pady=(0, 12))

score_row = tk.Frame(score_card, bg=CARD)
score_row.pack(fill="x")

score_val_lbl = tk.Label(score_row, text="88.5%", bg=CARD, fg=SUCCESS, font=("Segoe UI", 24, "bold"))
score_val_lbl.pack(side="left")

score_meta_box = tk.Frame(score_row, bg=CARD)
score_meta_box.pack(side="left", padx=15)

score_title_lbl = tk.Label(score_meta_box, text="OVERALL MISSION SUITABILITY SCORE", bg=CARD, fg=TEXT, font=("Segoe UI", 10, "bold"))
score_title_lbl.pack(anchor="w")

compliance_lbl = tk.Label(score_meta_box, text="100% Mandatory Constraints Satisfied", bg=CARD, fg=TEXT_MUTED, font=("Segoe UI", 9))
compliance_lbl.pack(anchor="w")

rationale_summary_lbl = tk.Label(
    score_card,
    text="Decision Rationale Summary",
    bg=INPUT_BG,
    fg=TEXT,
    font=("Segoe UI", 9),
    wraplength=650,
    justify="left",
    padx=12,
    pady=8,
    highlightbackground=CARD_BORDER,
    highlightthickness=1
)
rationale_summary_lbl.pack(fill="x", pady=(10, 0))


# Strengths Card
strengths_card = tk.Frame(dossier_col, bg=CARD, highlightbackground=CARD_BORDER, highlightthickness=1, padx=20, pady=12)
strengths_card.pack(fill="x", pady=(0, 12))

tk.Label(strengths_card, text="TACTICAL CAPABILITIES & VALIDATED STRENGTHS", bg=CARD, fg=SUCCESS, font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(0, 6))
strengths_box = tk.Frame(strengths_card, bg=CARD)
strengths_box.pack(fill="x")

# Compromises / Trade-Offs Card
compromises_card = tk.Frame(dossier_col, bg=CARD, highlightbackground=CARD_BORDER, highlightthickness=1, padx=20, pady=12)
compromises_card.pack(fill="x", pady=(0, 12))

compromises_title_lbl = tk.Label(compromises_card, text="OPERATIONAL NOTICES & TACTICAL WORKAROUNDS", bg=CARD, fg=WARNING, font=("Segoe UI", 10, "bold"))
compromises_title_lbl.pack(anchor="w", pady=(0, 6))
compromises_box = tk.Frame(compromises_card, bg=CARD)
compromises_box.pack(fill="x")

# Terrain Route Feasibility Card
route_card = tk.Frame(dossier_col, bg=CARD, highlightbackground=CARD_BORDER, highlightthickness=1, padx=20, pady=12)
route_card.pack(fill="x")

tk.Label(route_card, text="TERRAIN MOBILITY & TRANSIT FEASIBILITY BRIEFING", bg=CARD, fg=ACCENT, font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(0, 6))
route_info_lbl = tk.Label(route_card, text="", bg=CARD, fg=TEXT_MUTED, font=("Segoe UI", 9), justify="left")
route_info_lbl.pack(anchor="w")


# =============================================================================
# RESULTS VIEW: COMPARATIVE RANKING TABLE & ALTERNATIVES (ITEM 2)
# =============================================================================
comparative_card = tk.Frame(results_content, bg=CARD, highlightbackground=CARD_BORDER, highlightthickness=1, padx=25, pady=18)
comparative_card.pack(fill="x", padx=30, pady=(0, 30))

comp_header_row = tk.Frame(comparative_card, bg=CARD)
comp_header_row.pack(fill="x", pady=(0, 12))

comp_table_title = tk.Label(
    comp_header_row,
    text="COMPARATIVE PLATFORM RANKING & SENSITIVITY AUDIT",
    bg=CARD,
    fg=TEXT,
    font=("Segoe UI", 11, "bold")
)
comp_table_title.pack(side="left")

tk.Label(
    comp_header_row,
    text="💡 Click any row to inspect platform specs & photo in the left showcase",
    bg=CARD,
    fg=ACCENT_LIGHT,
    font=("Segoe UI", 8)
).pack(side="right")

table_container = tk.Frame(comparative_card, bg=INPUT_BG, highlightbackground=CARD_BORDER, highlightthickness=1)
table_container.pack(fill="x")

table_text = tk.Text(
    table_container,
    bg=INPUT_BG,
    fg=TEXT,
    relief="flat",
    font=("Consolas", 9),
    height=8,
    padx=15,
    pady=10,
    cursor="hand2"
)
table_text.pack(fill="x")

table_text.tag_configure("th", foreground=ACCENT, font=("Consolas", 9, "bold"))
table_text.tag_configure("rk", foreground=TEXT_MUTED, font=("Consolas", 9, "bold"))
table_text.tag_configure("name", foreground=TEXT, font=("Consolas", 9, "bold"))
table_text.tag_configure("score_good", foreground=SUCCESS, font=("Consolas", 9, "bold"))
table_text.tag_configure("score_warn", foreground=WARNING, font=("Consolas", 9, "bold"))
table_text.tag_configure("meta", foreground=TEXT_MUTED, font=("Consolas", 9))
table_text.tag_configure("sep", foreground=CARD_BORDER)


def on_table_click(event):
    global current_results_data
    if not current_results_data:
        return
    try:
        index = table_text.index(f"@{event.x},{event.y}")
        line_num = int(index.split(".")[0])
        row_idx = line_num - 3
        if 0 <= row_idx < len(current_results_data):
            selected_item = current_results_data[row_idx]
            display_platform_showcase(
                selected_item["details"],
                selected_item["final_score"],
                selected_item.get("is_compromise", False)
            )
    except Exception:
        pass


table_text.bind("<ButtonRelease-1>", on_table_click)


# Robustness Sensitivity Brief
sens_box = tk.Frame(comparative_card, bg=CARD)
sens_box.pack(fill="x", pady=(10, 0))

sens_lbl = tk.Label(sens_box, text="", bg=CARD, fg=TEXT_MUTED, font=("Segoe UI", 9), justify="left")
sens_lbl.pack(anchor="w")


# =============================================================================
# HELPER FUNCTIONS: DISPLAY PLATFORM SHOWCASE (ITEM 1)
# =============================================================================
def display_platform_showcase(vehicle_dict, score_val, is_compromise=False):
    """Updates the left showcase with large high-definition image and specs."""
    global current_vehicle_photo
    v_name = vehicle_dict.get("vehicle_name", "Unknown Vehicle")
    v_id = vehicle_dict.get("vehicle_id", "N/A")
    manuf = vehicle_dict.get("manufacturer", "Indian Defense")
    status = vehicle_dict.get("status", "Demonstrator")

    showcase_veh_name.config(text=v_name)
    showcase_veh_sub.config(text=f"{manuf}  •  {v_id}  •  {status}")

    # Load & display large photo (440x260px)
    image_rel = vehicle_dict.get("image_path", "")
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    full_path = os.path.join(repo_root, image_rel) if image_rel else ""

    loaded = None
    if full_path and os.path.exists(full_path):
        try:
            im = Image.open(full_path)
            # High-res thumbnail scaling with aspect ratio preserved
            im.thumbnail((440, 255), Image.Resampling.LANCZOS)
            loaded = ImageTk.PhotoImage(im)
        except Exception as e:
            print(f"Error rendering image: {e}")

    if loaded:
        current_vehicle_photo = loaded
        showcase_image_label.config(image=current_vehicle_photo, text="", bg=INPUT_BG)
    else:
        current_vehicle_photo = None
        showcase_image_label.config(image="", text=f"📷 Photo Preview\n{v_name}\n({image_rel})", bg=INPUT_BG, fg=TEXT_MUTED)

    # Populate Spec Grid
    spec_labels["mobility"].config(text=str(vehicle_dict.get("mobility_type", "N/A")))
    p_val = vehicle_dict.get("payload_capacity_kg", "N/A")
    spec_labels["payload"].config(text=f"{p_val} kg" if p_val is not None else "Mission-Specific")
    spec_labels["speed"].config(text=f"{vehicle_dict.get('max_speed_kmh', 0.0)} km/h")
    spec_labels["range"].config(text=f"{vehicle_dict.get('operating_range_km', 0.0)} km")
    spec_labels["endurance"].config(text=f"{vehicle_dict.get('endurance_hours', 0.0)} h")
    spec_labels["standoff"].config(text=f"{vehicle_dict.get('max_control_range_km', 0.0)} km")

    links = vehicle_dict.get("control_link_types", ["Standard RF"])
    spec_labels["link"].config(text=links[0] if links else "RF LOS")

    clim = vehicle_dict.get("climate_altitude", {})
    t_min = clim.get("min_operating_temp_c", -20)
    t_max = clim.get("max_operating_temp_c", 50)
    alt = clim.get("max_altitude_m_asl", 4000)
    spec_labels["climate"].config(text=f"{t_min:.0f}° to {t_max:.0f}°C | {alt}m")


# =============================================================================
# CORE PIPELINE EXECUTION (RUN ANALYSIS)
# =============================================================================
def run_analysis_pipeline():
    try:
        raw_payload = payload_entry.get().strip()
        raw_range = range_entry.get().strip()
        raw_min_time = min_time_entry.get().strip()
        raw_max_time = max_time_entry.get().strip()

        if not all([raw_payload, raw_range, raw_min_time, raw_max_time]):
            messagebox.showerror("Input Error", "Please fill in all numerical fields.")
            return

        payload = float(raw_payload)
        operating_range = float(raw_range)
        minimum_time = float(raw_min_time)
        maximum_time = float(raw_max_time)

        if payload <= 0 or operating_range <= 0 or minimum_time <= 0 or maximum_time <= 0:
            messagebox.showerror("Invalid Data", "Numerical values must be strictly greater than 0.")
            return

        if minimum_time > maximum_time:
            messagebox.showerror("Invalid Mission Time", "Minimum duration cannot exceed maximum deadline.")
            return

    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid numeric values.")
        return

    # Extract Active Roles (Engineer's Multi-Role Deck)
    selected_roles = [r for r, var in role_variables.items() if var.get()]
    if not selected_roles:
        messagebox.showerror("Role Selection Required", "Please select at least one tactical mission role from Section 1.")
        return

    requirements = {
        "Mission Role": selected_roles[0],
        "Mission Roles": selected_roles,
        "Terrain": terrain_var.get(),
        "Payload": payload,
        "Operating Range": operating_range,
        "Minimum Mission Time": minimum_time,
        "Maximum Mission Time": maximum_time
    }

    # Tactical Parameters
    try:
        standoff_val = float(standoff_entry.get().strip() or "0.0")
        if standoff_val > 0:
            requirements["Standoff Distance"] = standoff_val
    except ValueError:
        pass

    try:
        alt_val = float(alt_entry.get().strip() or "0.0")
        if alt_val > 0:
            requirements["Operational Altitude"] = alt_val
    except ValueError:
        pass

    try:
        temp_val = float(temp_entry.get().strip() or "25.0")
        requirements["Operating Temperature"] = temp_val
    except ValueError:
        pass

    if stealth_var.get() == "Silent Electric Only (Strict Acoustic/Thermal Suppression)":
        requirements["Stealth Requirement"] = "Silent Electric Only"

    if link_var.get() != control_links[0]:
        requirements["Control Link Type"] = link_var.get()

    priority_selections = {
        param: var.get() for param, var in priority_variables.items()
    }

    try:
        weights = generate_weights(priority_selections)
        catalog = get_active_catalog()
        results = rank_vehicles(catalog, requirements, weights)

        global current_results_data
        feasible_list = results.get("feasible", [])
        compromise_list = results.get("compromise", [])
        current_results_data = feasible_list if feasible_list else compromise_list
        derived = results.get("derived", {})

        # Clear existing dynamic result cards
        for widget in strengths_box.winfo_children():
            widget.destroy()
        for widget in compromises_box.winfo_children():
            widget.destroy()
        table_text.delete("1.0", tk.END)

        # Update Mission Summary Pill
        roles_str = ", ".join(selected_roles) if len(selected_roles) <= 2 else f"{selected_roles[0]} + {len(selected_roles)-1} more"
        mission_summary_pill.config(
            text=f"📍 {requirements['Terrain']}  |  📦 {payload:.0f} kg  |  🎯 {operating_range:.1f} km  |  ⏱ {minimum_time:.1f}-{maximum_time:.1f}h  |  Roles: {roles_str}"
        )

        # Render Qualified Candidate vs Adaptive Compromise
        if feasible_list:
            best = feasible_list[0]
            v_details = best.get("details", {})
            expl = best.get("explanation", {})

            results_mode_badge.config(
                text=f"● QUALIFIED PLATFORMS IDENTIFIED ({len(feasible_list)} of {len(catalog)} Passed Gatekeeper)",
                fg=SUCCESS
            )

            score_val_lbl.config(text=f"{best['final_score']:.1f}%", fg=SUCCESS)
            score_title_lbl.config(text="OVERALL MISSION SUITABILITY SCORE (QUALIFIED)")
            compliance_lbl.config(text=f"100% Mandatory Constraints Satisfied  •  Rank #1 of {len(feasible_list)} Qualified", fg=SUCCESS)
            rationale_summary_lbl.config(text=f"• {expl.get('summary', 'Achieved top multi-criteria compatibility.')}")

            # Populate Strengths
            strengths = expl.get("strengths", ["All physical and operational constraints confirmed."])
            for s in strengths:
                tk.Label(strengths_box, text=f"  ✓  {s}", bg=CARD, fg=SUCCESS, font=("Segoe UI", 9), anchor="w").pack(fill="x", pady=1)

            # Compromises / Warnings
            weaknesses = expl.get("weaknesses", [])
            if weaknesses:
                compromises_title_lbl.config(text="OPERATIONAL NOTICES & DESIGN MARGINS", fg=WARNING)
                for w in weaknesses:
                    tk.Label(compromises_box, text=f"  ⚠  {w}", bg=CARD, fg=WARNING, font=("Segoe UI", 9), anchor="w").pack(fill="x", pady=1)
            else:
                compromises_title_lbl.config(text="OPERATIONAL NOTICES & DESIGN MARGINS", fg=TEXT_MUTED)
                tk.Label(compromises_box, text="  ✓  Zero tactical trade-offs required. Full design margins verified.", bg=CARD, fg=TEXT_MUTED, font=("Segoe UI", 9), anchor="w").pack(fill="x")

            # Route Info
            route_info = best.get("route_info", {})
            if route_info:
                eff_d = route_info.get("effective_distance_km", operating_range)
                eff_spd = route_info.get("effective_speed_kmh", v_details.get("max_speed_kmh", 0))
                t_dur = route_info.get("transit_duration_hours", 0)
                trav_idx = route_info.get("traversability_index", 1.0)
                route_info_lbl.config(
                    text=f"• Detour-Adjusted Route: {eff_d:.1f} km  |  Traversability Index: {trav_idx:.2f}\n• Effective Off-Road Speed: {eff_spd:.1f} km/h  |  Est. Transit Duration: {t_dur:.2f} hours (Deadline: {maximum_time:.1f}h)"
                )

            # Update Showcase
            display_platform_showcase(v_details, best["final_score"], False)

            # Populate Comparative Table
            comp_table_title.config(text=f"QUALIFIED PLATFORMS COMPARISON ({len(feasible_list)} Passed Gatekeeper)")
            table_text.insert(tk.END, f"{'RK':<4}{'PLATFORM NAME':<26}{'OVERALL':<12}{'SPEED':<12}{'PAYLOAD':<12}{'MOBILITY':<16}\n", "th")
            table_text.insert(tk.END, "-" * 82 + "\n", "sep")

            for idx, item in enumerate(feasible_list, start=1):
                v_name = item["vehicle_name"]
                score_str = f"{item['final_score']:>6.1f}%    "
                spd_str = f"{item['details'].get('max_speed_kmh', 0.0):.1f} km/h"
                p_str = f"{item['details'].get('payload_capacity_kg', 'N/A')} kg"
                mob_str = item["details"].get("mobility_type", "N/A")
                table_text.insert(tk.END, f"{idx:<4}", "rk")
                table_text.insert(tk.END, f"{v_name:<26}", "name")
                table_text.insert(tk.END, score_str, "score_good")
                table_text.insert(tk.END, f"{spd_str:<12}", "meta")
                table_text.insert(tk.END, f"{p_str:<12}", "meta")
                table_text.insert(tk.END, f"{mob_str:<16}\n", "meta")

            sens = results.get("sensitivity", {})
            sens_lbl.config(text=f"• Decision Robustness: {sens.get('summary', 'Robust recommendation under weight perturbations.')}")

        elif compromise_list:
            # ADAPTIVE TRADE-OFF MODE
            best = compromise_list[0]
            v_details = best.get("details", {})
            expl = best.get("explanation", {})

            results_mode_badge.config(
                text="⚠️ ADAPTIVE TRADE-OFF ACTIVATED (BEST-FIT OPERATIONAL COMPROMISES)",
                fg=WARNING
            )

            score_val_lbl.config(text=f"{best['final_score']:.1f}%", fg=WARNING)
            score_title_lbl.config(text="OPERATIONAL TRADE-OFF SUITABILITY SCORE")
            compliance_lbl.config(text=f"Compliance: {best.get('compliance_text', '')}  •  Top Near-Miss Alternative", fg=WARNING)
            rationale_summary_lbl.config(text=f"• {expl.get('summary', 'Achieved top partial compliance among available defense platforms.')}")

            # Strengths
            strengths = expl.get("strengths", [])
            for s in strengths:
                tk.Label(strengths_box, text=f"  ✓  {s}", bg=CARD, fg=SUCCESS, font=("Segoe UI", 9), anchor="w").pack(fill="x", pady=1)

            # Compromises Required
            compromises = expl.get("compromises", [])
            compromises_title_lbl.config(text="REQUIRED OPERATIONAL CONCESSIONS & TACTICAL WORKAROUNDS", fg=WARNING)
            for c in compromises:
                tk.Label(compromises_box, text=f"  ⚠  {c}", bg=CARD, fg=WARNING, font=("Segoe UI", 9), anchor="w").pack(fill="x", pady=1)

            # Route Info
            route_info = best.get("route_info", {})
            if route_info:
                eff_d = route_info.get("effective_distance_km", operating_range)
                eff_spd = route_info.get("effective_speed_kmh", v_details.get("max_speed_kmh", 0))
                t_dur = route_info.get("transit_duration_hours", 0)
                route_info_lbl.config(
                    text=f"• Detour-Adjusted Route: {eff_d:.1f} km  |  Effective Speed: {eff_spd:.1f} km/h\n• Estimated Transit: {t_dur:.2f} hours (Mission Window: {minimum_time:.1f}h - {maximum_time:.1f}h)"
                )

            # Update Showcase
            display_platform_showcase(v_details, best["final_score"], True)

            # Populate Table
            comp_table_title.config(text="TOP COMPROMISE ALTERNATIVES (Ranked by Multi-Criteria Proximity)")
            table_text.insert(tk.END, f"{'RK':<4}{'PLATFORM NAME':<26}{'MATCH':<12}{'COMPLIANCE':<16}{'PRIMARY COMPROMISE REQUIRED':<36}\n", "th")
            table_text.insert(tk.END, "-" * 94 + "\n", "sep")

            for idx, item in enumerate(compromise_list[:5], start=1):
                v_name = item["vehicle_name"]
                score_str = f"{item['final_score']:>6.1f}%    "
                comp_str = item.get("compliance_text", "")
                shortfall = item.get("primary_shortfall", "")
                table_text.insert(tk.END, f"{idx:<4}", "rk")
                table_text.insert(tk.END, f"{v_name:<26}", "name")
                table_text.insert(tk.END, score_str, "score_warn")
                table_text.insert(tk.END, f"{comp_str:<16}", "meta")
                table_text.insert(tk.END, f"{shortfall:<36}\n", "score_warn")

            sens_lbl.config(
                text="• Zero 100% compliant platforms exist for this specific combination of extreme constraints. Alternatives ranked by physical proximity."
            )

        # Switch to Results Screen
        switch_to_results_view()
        results_canvas.yview_moveto(0)

    except Exception as e:
        error_msg = traceback.format_exc()
        messagebox.showerror("Execution Error", f"An error occurred during mission analysis:\n\n{error_msg}")


# =============================================================================
# MODAL DIALOG 1: ADD NEW VEHICLE (PRESERVED & ENHANCED)
# =============================================================================
def open_add_vehicle_dialog():
    dialog = tk.Toplevel(root)
    dialog.title("STRIDE — Add New Indian Defence UGV Platform")
    dialog.geometry("820x760")
    dialog.minsize(750, 600)
    dialog.configure(bg=BG)
    dialog.transient(root)
    dialog.grab_set()

    d_canvas = tk.Canvas(dialog, bg=BG, highlightthickness=0)
    d_canvas.pack(side="left", fill="both", expand=True)
    d_scroll = ttk.Scrollbar(dialog, orient="vertical", command=d_canvas.yview)
    d_scroll.pack(side="right", fill="y")
    d_canvas.configure(yscrollcommand=d_scroll.set)

    d_frame = tk.Frame(d_canvas, bg=BG, padx=25, pady=20)
    d_win = d_canvas.create_window((0, 0), window=d_frame, anchor="nw")

    d_frame.bind("<Configure>", lambda e: d_canvas.configure(scrollregion=d_canvas.bbox("all")))
    d_canvas.bind("<Configure>", lambda e: d_canvas.itemconfig(d_win, width=e.width))

    tk.Label(d_frame, text="DEFENCE PLATFORM ONBOARDING PORTAL", bg=BG, fg=ACCENT, font=("Segoe UI", 15, "bold")).pack(anchor="w")
    tk.Label(d_frame, text="Register an indigenous or OEM UGV with canonical specifications, telemetry envelopes, and photographic asset.", bg=BG, fg=TEXT_MUTED, font=("Segoe UI", 9)).pack(anchor="w", pady=(2, 15))

    form = tk.Frame(d_frame, bg=CARD, highlightbackground=CARD_BORDER, highlightthickness=1, padx=20, pady=15)
    form.pack(fill="x")

    def make_entry(parent, label_text, row, col=0, width=28):
        tk.Label(parent, text=label_text, bg=CARD, fg=TEXT, font=("Segoe UI", 9, "bold")).grid(row=row, column=col, sticky="w", pady=(8, 2))
        entry = tk.Entry(parent, width=width, bg=INPUT_BG, fg=TEXT, insertbackground=TEXT, relief="flat", highlightbackground=CARD_BORDER, highlightcolor=ACCENT, highlightthickness=1, font=("Segoe UI", 9))
        entry.grid(row=row+1, column=col, sticky="w", pady=(0, 6), padx=(0, 15))
        return entry

    vname_entry = make_entry(form, "Platform / Vehicle Name *", 0, 0)
    manuf_entry = make_entry(form, "Manufacturer / Developer *", 0, 1)

    tk.Label(form, text="Mobility Type *", bg=CARD, fg=TEXT, font=("Segoe UI", 9, "bold")).grid(row=2, column=0, sticky="w", pady=(4, 2))
    mob_var = tk.StringVar(value="Tracked")
    ttk.Combobox(form, textvariable=mob_var, values=["Tracked", "Wheeled 4x4", "Wheeled 6x6", "Wheeled 8x8", "Quadruped"], state="readonly", width=25, style="STRIDE.TCombobox").grid(row=3, column=0, sticky="w", pady=(0, 8), padx=(0, 15))

    tk.Label(form, text="Operational Status", bg=CARD, fg=TEXT, font=("Segoe UI", 9, "bold")).grid(row=2, column=1, sticky="w", pady=(4, 2))
    status_var = tk.StringVar(value="Field Trials / Evaluated")
    ttk.Combobox(form, textvariable=status_var, values=["In Service", "Field Trials / Evaluated", "Developed / Demonstrated", "Technology Demonstrator"], state="readonly", width=25, style="STRIDE.TCombobox").grid(row=3, column=1, sticky="w", pady=(0, 8))

    # Supported Roles
    tk.Label(form, text="Supported Mission Roles *", bg=CARD, fg=ACCENT, font=("Segoe UI", 10, "bold")).grid(row=4, column=0, columnspan=2, sticky="w", pady=(10, 4))
    r_frame = tk.Frame(form, bg=CARD)
    r_frame.grid(row=5, column=0, columnspan=2, sticky="w")
    role_checks = {}
    for idx, r in enumerate(mission_roles):
        var = tk.BooleanVar(value=(idx == 0))
        cb = tk.Checkbutton(r_frame, text=r, variable=var, bg=CARD, fg=TEXT, selectcolor=INPUT_BG, activebackground=CARD, activeforeground=ACCENT, font=("Segoe UI", 8))
        cb.grid(row=idx//2, column=idx%2, sticky="w", padx=(0, 20), pady=2)
        role_checks[r] = var

    # Performance
    tk.Label(form, text="Physical Performance Metrics", bg=CARD, fg=ACCENT, font=("Segoe UI", 10, "bold")).grid(row=6, column=0, columnspan=2, sticky="w", pady=(10, 4))
    payload_input = make_entry(form, "Payload Capacity (kg)", 7, 0)
    speed_input = make_entry(form, "Max Speed (km/h)", 7, 1)
    range_input = make_entry(form, "Operating Range (km)", 9, 0)
    endurance_input = make_entry(form, "Continuous Endurance (hours)", 9, 1)
    standoff_input = make_entry(form, "Operator Standoff Range (km)", 11, 0)
    alt_input = make_entry(form, "Max Operating Altitude (m ASL)", 11, 1)
    alt_input.insert(0, "4000")

    # Image
    tk.Label(form, text="Image Asset Path:", bg=CARD, fg=TEXT, font=("Segoe UI", 9, "bold")).grid(row=13, column=0, sticky="w", pady=(6, 2))
    img_entry = make_entry(form, "", 14, 0, width=40)
    img_entry.insert(0, "assets/images/tasl_tracked_ugv.jpg")

    def browse_image():
        filename = filedialog.askopenfilename(
            parent=dialog,
            title="Select Vehicle Image",
            filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.webp"), ("All Files", "*.*")]
        )
        if filename:
            img_entry.delete(0, tk.END)
            img_entry.insert(0, filename)

    tk.Button(form, text="Browse...", command=browse_image, bg=CARD_LIGHT, fg=TEXT, font=("Segoe UI", 8), padx=10, relief="flat", cursor="hand2").grid(row=14, column=1, sticky="w", padx=10)

    def submit_vehicle():
        roles_chosen = [r for r, v in role_checks.items() if v.get()]
        raw = {
            "vehicle_name": vname_entry.get(),
            "manufacturer": manuf_entry.get(),
            "mobility_type": mob_var.get(),
            "status": status_var.get(),
            "mission_roles": roles_chosen,
            "terrain_capabilities": terrain_options[:4],
            "payload_capacity_kg": payload_input.get().strip(),
            "max_speed_kmh": speed_input.get().strip(),
            "operating_range_km": range_input.get().strip(),
            "endurance_hours": endurance_input.get().strip(),
            "max_control_range_km": standoff_input.get().strip(),
            "control_link_types": ["RF LOS (Radio Frequency Line of Sight)"],
            "max_altitude_m_asl": alt_input.get().strip(),
            "image_path": img_entry.get()
        }

        success, msg, v_rec = add_vehicle(raw)
        if success:
            messagebox.showinfo("Success", msg, parent=dialog)
            status_label.config(text=f"● Platform registered! Total {len(get_active_catalog())} Indian UGVs active")
            dialog.destroy()
        else:
            messagebox.showerror("Validation Error", msg, parent=dialog)

    b_frame = tk.Frame(d_frame, bg=BG)
    b_frame.pack(fill="x", pady=15)
    tk.Button(b_frame, text="REGISTER IN DATABASE", command=submit_vehicle, bg=SUCCESS, fg="#090D12", font=("Segoe UI", 10, "bold"), padx=20, pady=8, relief="flat", cursor="hand2").pack(side="left")
    tk.Button(b_frame, text="CANCEL", command=dialog.destroy, bg=CARD, fg=TEXT, font=("Segoe UI", 10), padx=15, pady=8, relief="flat", cursor="hand2").pack(side="left", padx=10)


# =============================================================================
# MODAL DIALOG 2: DESCRIBE MISSION (NATURAL LANGUAGE PARSER)
# =============================================================================
def open_nlp_mission_dialog():
    dialog = tk.Toplevel(root)
    dialog.title("STRIDE — Describe Mission in Natural Language")
    dialog.geometry("720x620")
    dialog.minsize(620, 500)
    dialog.configure(bg=BG)
    dialog.transient(root)
    dialog.grab_set()

    tk.Label(dialog, text="SMART MISSION NARRATIVE PARSER", bg=BG, fg=ACCENT, font=("Segoe UI", 15, "bold")).pack(anchor="w", padx=25, pady=(20, 2))
    tk.Label(dialog, text="Describe your operational scenario in free-form English. STRIDE will extract mission roles, terrain, and envelopes.", bg=BG, fg=TEXT_MUTED, font=("Segoe UI", 9)).pack(anchor="w", padx=25, pady=(0, 12))

    # Presets
    presets_frame = tk.Frame(dialog, bg=CARD, padx=15, pady=10, highlightbackground=CARD_BORDER, highlightthickness=1)
    presets_frame.pack(fill="x", padx=25, pady=(0, 10))
    tk.Label(presets_frame, text="Select a tactical scenario preset:", bg=CARD, fg=TEXT, font=("Segoe UI", 9, "bold")).pack(anchor="w")

    preset_texts = {
        "Galwan LAC High-Altitude Patrol": "Conduct high altitude reconnaissance and surveillance patrol in Ladakh at 15000 ft in sub-zero snow terrain, carrying 50 kg sensor payload with silent electric stealth and 10 km standoff within 3 hours.",
        "Pokhran Desert Logistics Resupply": "Heavy logistics transport resupply mission across the Thar Desert sand dunes carrying 500 kg ammunition payload over a 15 km distance within a 3 hour deadline.",
        "Urban C-IED Room Breaching": "Enter a confined urban building and neutralize explosive devices using manipulator arm within 45 minutes and 500m standoff."
    }

    def load_preset(text):
        nlp_text.delete("1.0", tk.END)
        nlp_text.insert(tk.END, text)

    btn_row = tk.Frame(presets_frame, bg=CARD)
    btn_row.pack(fill="x", pady=6)
    for title, p_text in preset_texts.items():
        tk.Button(btn_row, text=title, command=lambda t=p_text: load_preset(t), bg=CARD_LIGHT, fg=TEXT, font=("Segoe UI", 8), relief="flat", cursor="hand2").pack(side="left", padx=4)

    nlp_text = tk.Text(dialog, bg=INPUT_BG, fg=TEXT, insertbackground=TEXT, relief="flat", highlightbackground=CARD_BORDER, highlightcolor=ACCENT, highlightthickness=1, font=("Consolas", 10), padx=15, pady=12, height=6)
    nlp_text.pack(fill="x", padx=25, pady=10)
    nlp_text.insert(tk.END, preset_texts["Galwan LAC High-Altitude Patrol"])

    log_box = tk.Text(dialog, bg=INPUT_BG, fg=TEXT_MUTED, relief="flat", font=("Consolas", 8), height=6, padx=10, pady=8)
    log_box.pack(fill="both", expand=True, padx=25, pady=(0, 10))

    def parse_and_apply():
        content = nlp_text.get("1.0", tk.END).strip()
        if not content:
            messagebox.showerror("Error", "Please enter a mission description.", parent=dialog)
            return

        parsed = parse_mission_narrative(content)
        log_box.delete("1.0", tk.END)
        log_box.insert(tk.END, f"=== PARSED MISSION PARAMETERS ===\n")
        for k, v in parsed.items():
            log_box.insert(tk.END, f"  • {k}: {v}\n")

        # Apply to main UI
        if parsed.get("Mission Roles"):
            for r, var in role_variables.items():
                var.set(r in parsed["Mission Roles"])
            on_role_toggle()

        if parsed.get("Terrain"):
            terrain_var.set(parsed["Terrain"])

        if parsed.get("Payload"):
            payload_entry.delete(0, tk.END)
            payload_entry.insert(0, str(parsed["Payload"]))

        if parsed.get("Operating Range"):
            range_entry.delete(0, tk.END)
            range_entry.insert(0, str(parsed["Operating Range"]))

        if parsed.get("Maximum Mission Time"):
            max_time_entry.delete(0, tk.END)
            max_time_entry.insert(0, str(parsed["Maximum Mission Time"]))

        if parsed.get("Standoff Distance"):
            standoff_entry.delete(0, tk.END)
            standoff_entry.insert(0, str(parsed["Standoff Distance"]))

        if parsed.get("Operational Altitude"):
            alt_entry.delete(0, tk.END)
            alt_entry.insert(0, str(int(parsed["Operational Altitude"])))

        if parsed.get("Stealth Requirement") == "Silent Electric Only":
            stealth_var.set(stealth_options[1])

        messagebox.showinfo("Parsed Successfully", "Mission parameters extracted and applied to STRIDE form!", parent=dialog)
        dialog.destroy()

    btn_f = tk.Frame(dialog, bg=BG)
    btn_f.pack(fill="x", padx=25, pady=(0, 15))
    tk.Button(btn_f, text="EXTRACT PARAMETERS & APPLY", command=parse_and_apply, bg=ACCENT, fg="#090D12", font=("Segoe UI", 10, "bold"), padx=20, pady=8, relief="flat", cursor="hand2").pack(side="left")
    tk.Button(btn_f, text="CANCEL", command=dialog.destroy, bg=CARD, fg=TEXT, font=("Segoe UI", 10), padx=15, pady=8, relief="flat", cursor="hand2").pack(side="left", padx=10)


def reset_to_defaults():
    for r, var in role_variables.items():
        var.set(r == "Surveillance")
    on_role_toggle()
    terrain_var.set(terrain_options[1])
    payload_entry.delete(0, tk.END)
    payload_entry.insert(0, "50.0")
    range_entry.delete(0, tk.END)
    range_entry.insert(0, "15.0")
    min_time_entry.delete(0, tk.END)
    min_time_entry.insert(0, "1.0")
    max_time_entry.delete(0, tk.END)
    max_time_entry.insert(0, "4.0")
    standoff_entry.delete(0, tk.END)
    standoff_entry.insert(0, "10.0")
    alt_entry.delete(0, tk.END)
    alt_entry.insert(0, "1500")
    temp_entry.delete(0, tk.END)
    temp_entry.insert(0, "20.0")
    stealth_var.set(stealth_options[0])
    link_var.set(control_links[0])
    for p, var in priority_variables.items():
        var.set("Medium")
    switch_to_input_view()
    status_label.config(text=f"● Form reset to defaults ({len(get_active_catalog())} Indian UGVs active)")


# Header buttons setup
tk.Button(
    header_right,
    text="➕ Add New Vehicle",
    command=open_add_vehicle_dialog,
    bg=INPUT_BG,
    fg=TEXT,
    activebackground=CARD_LIGHT,
    activeforeground=TEXT,
    relief="flat",
    cursor="hand2",
    font=("Segoe UI", 9, "bold"),
    padx=12,
    pady=6,
    highlightbackground=CARD_BORDER,
    highlightthickness=1
).pack(side="right", padx=5)

tk.Button(
    header_right,
    text="💬 Describe Mission (NLP)",
    command=open_nlp_mission_dialog,
    bg=INPUT_BG,
    fg=ACCENT,
    activebackground=CARD_LIGHT,
    activeforeground=ACCENT_LIGHT,
    relief="flat",
    cursor="hand2",
    font=("Segoe UI", 9, "bold"),
    padx=12,
    pady=6,
    highlightbackground=ACCENT_DARK,
    highlightthickness=1
).pack(side="right", padx=5)

tk.Button(
    header_right,
    text="🔄 Reset Defaults",
    command=reset_to_defaults,
    bg=INPUT_BG,
    fg=TEXT_MUTED,
    activebackground=CARD_LIGHT,
    activeforeground=TEXT,
    relief="flat",
    cursor="hand2",
    font=("Segoe UI", 9),
    padx=10,
    pady=6,
    highlightbackground=CARD_BORDER,
    highlightthickness=1
).pack(side="right", padx=5)


if __name__ == "__main__":
    root.mainloop()