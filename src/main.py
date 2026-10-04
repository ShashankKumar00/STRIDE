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

mission_roles = [
    "Surveillance",
    "Reconnaissance",
    "Mine Detection / Clearance",
    "CBRN Reconnaissance",
    "Combat / Tactical Support",
    "Logistics / Transport / Casualty Evacuation",
    "EOD / IED Disposal",
    "High-Altitude Logistics / Extreme Cold",
    "Precision Strike / Anti-Armor",
    "Urban Assault / Confined Space Recon"
]

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
    "Any / Standard",
    "RF LOS (Radio Frequency Line of Sight)",
    "COFDM NLOS (Non-Line of Sight Mesh)",
    "Fiber-Optic (Jam-Proof / EW-Immune)",
    "SATCOM / BLOS Drone Relay",
    "Autonomous Waypoint / GNSS-Denied SLAM"
]

stealth_options = [
    "Standard (Any Propulsion)",
    "Silent Electric Only (Strict Acoustic/Thermal Masking)"
]


# Root Window Initialization
root = tk.Tk()
root.title("STRIDE — Defense Vehicle Selection System")
root.geometry("980x920")
root.minsize(800, 650)

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
style.configure("Title.TLabel", background=BG, foreground=TEXT, font=("Segoe UI", 24, "bold"))
style.configure("Subtitle.TLabel", background=BG, foreground=TEXT_SECONDARY, font=("Segoe UI", 9))
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

# Cache for rendered PhotoImage to prevent garbage collection
current_vehicle_photo = None


def clear_results():
    global current_vehicle_photo
    result_text.delete("1.0", tk.END)
    image_label.config(image="", text="No platform selected", bg=CARD)
    image_meta_label.config(text="")
    current_vehicle_photo = None
    catalog = get_active_catalog()
    status_label.config(text=f"● Ready for mission analysis ({len(catalog)} Indian UGVs active)")


def update_vehicle_image(image_path: str, vehicle_name: str, manufacturer: str):
    """Loads, resizes, and displays the vehicle's photo in the recommendation pane."""
    global current_vehicle_photo
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    
    candidates = []
    if image_path:
        candidates.append(os.path.join(repo_root, image_path))
        candidates.append(image_path)
    
    loaded_img = None
    for cand in candidates:
        if os.path.exists(cand) and os.path.isfile(cand):
            try:
                raw_img = Image.open(cand)
                # Resize with aspect ratio preserved (320x190 box)
                raw_img.thumbnail((320, 190), Image.Resampling.LANCZOS)
                loaded_img = ImageTk.PhotoImage(raw_img)
                break
            except Exception as e:
                print(f"Error loading image {cand}: {e}")

    if loaded_img:
        current_vehicle_photo = loaded_img
        image_label.config(image=current_vehicle_photo, text="", bg=INPUT_BG)
        image_meta_label.config(text=f"{vehicle_name}\n({manufacturer})")
    else:
        current_vehicle_photo = None
        image_label.config(image="", text=f"📷 Photo Preview\n{vehicle_name}", bg=CARD_LIGHT, fg=TEXT_SECONDARY)
        image_meta_label.config(text=f"{vehicle_name} ({manufacturer})")


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
            messagebox.showerror("Invalid Data", "Numerical values must be strictly greater than 0.")
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

    # Multi-role extraction
    selected_roles = [role for role, var in role_checkbox_vars.items() if var.get()]
    if not selected_roles:
        selected_roles = [primary_role_variable.get()]

    requirements = {
        "Mission Role": primary_role_variable.get(),
        "Mission Roles": selected_roles,
        "Terrain": terrain_variable.get(),
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
        alt_val = float(altitude_entry.get().strip() or "0.0")
        if alt_val > 0:
            requirements["Operational Altitude"] = alt_val
    except ValueError:
        pass

    try:
        temp_val = float(temp_entry.get().strip() or "25.0")
        requirements["Operating Temperature"] = temp_val
    except ValueError:
        pass

    if stealth_variable.get() == "Silent Electric Only (Strict Acoustic/Thermal Masking)":
        requirements["Stealth Requirement"] = "Silent Electric Only"

    priority_selections = {
        param: var.get() for param, var in priority_variables.items()
    }

    try:
        weights = generate_weights(priority_selections)
        catalog = get_active_catalog()
        results = rank_vehicles(catalog, requirements, weights)

        feasible_list = results.get("feasible", [])
        infeasible_list = results.get("infeasible", [])
        derived = results.get("derived", {})

        clear_results()

        result_text.insert(tk.END, "STRIDE VEHICLE ANALYSIS\n", "title")
        result_text.insert(tk.END, "Indian Defence UGV Mission Compatibility & Selection Engine\n\n", "subtitle")

        # Operational Mission Context
        result_text.insert(tk.END, "MISSION PROFILE & DERIVED CONSTRAINTS\n", "heading")
        result_text.insert(tk.END, "-" * 68 + "\n", "separator")
        result_text.insert(tk.END, f"• Target Roles:    {', '.join(selected_roles)}\n", "meta_text")
        result_text.insert(tk.END, f"• Terrain:         {requirements['Terrain']}\n", "meta_text")
        result_text.insert(tk.END, f"• Mission Payload: {payload:.1f} kg   |   Mission Distance: {operating_range:.1f} km\n", "meta_text")
        result_text.insert(tk.END, f"• Time Window:     {minimum_time:.1f}h - {maximum_time:.1f}h   |   Min Required Speed: {derived.get('required_speed', 0.0):.1f} km/h\n", "meta_text")
        
        if "Standoff Distance" in requirements:
            result_text.insert(tk.END, f"• Standoff Req:    {requirements['Standoff Distance']:.1f} km\n", "meta_text")
        if "Operational Altitude" in requirements:
            result_text.insert(tk.END, f"• Operational Alt: {requirements['Operational Altitude']:.0f} m ASL\n", "meta_text")
        if requirements.get("Stealth Requirement"):
            result_text.insert(tk.END, f"• Stealth Mode:    Silent Electric Only\n", "meta_text")
        result_text.insert(tk.END, "\n", "meta_text")

        if feasible_list:
            best_vehicle = feasible_list[0]
            expl = best_vehicle.get("explanation", {})
            v_details = best_vehicle.get("details", {})

            # Update Photo Preview
            update_vehicle_image(
                v_details.get("image_path", ""),
                best_vehicle["vehicle_name"],
                v_details.get("manufacturer", "Indian Defense")
            )

            result_text.insert(tk.END, "=" * 68 + "\n", "separator")
            result_text.insert(tk.END, "★ RECOMMENDED VEHICLE\n\n", "recommendation_title")
            result_text.insert(tk.END, f"{best_vehicle['vehicle_name']}   ({best_vehicle.get('vehicle_id', 'N/A')})\n", "recommendation_vehicle")
            result_text.insert(tk.END, f"Overall Suitability Score: {best_vehicle['final_score']:.2f}%\n", "recommendation_score")
            result_text.insert(tk.END, f"Manufacturer: {v_details.get('manufacturer', 'Unknown')}   |   Mobility: {v_details.get('mobility_type', 'N/A')}\n\n", "meta_text")

            result_text.insert(tk.END, "WHY RECOMMENDED (DECISION RATIONALE):\n", "heading_small")
            result_text.insert(tk.END, f"• {expl.get('summary', 'Achieved top multi-criteria compatibility.')}\n", "recommendation_note")

            if expl.get("strengths"):
                result_text.insert(tk.END, "\nKEY TACTICAL STRENGTHS:\n", "heading_small")
                for s in expl["strengths"]:
                    result_text.insert(tk.END, f"  ✓  {s}\n", "bullet_green")

            if expl.get("weaknesses"):
                result_text.insert(tk.END, "\nOPERATIONAL NOTICES / TRADE-OFFS:\n", "heading_small")
                for w in expl["weaknesses"]:
                    result_text.insert(tk.END, f"  ⚠  {w}\n", "bullet_yellow")

            # Terrain Route Feasibility Briefing
            route_info = best_vehicle.get("route_info", {})
            if route_info:
                result_text.insert(tk.END, "\nTERRAIN & ROUTE FEASIBILITY:\n", "heading_small")
                eff_d = route_info.get("effective_distance_km", operating_range)
                df = route_info.get("detour_factor", 1.0)
                eff_spd = route_info.get("effective_speed_kmh", v_details.get('max_speed_kmh', 0))
                t_dur = route_info.get("transit_duration_hours", 0)
                trav_idx = route_info.get("traversability_index", 1.0)
                result_text.insert(tk.END, f"  • Detour-Adjusted Route: {eff_d:.1f} km (Detour Factor: {df:.2f}x)\n", "meta_text")
                result_text.insert(tk.END, f"  • Off-Road Traversability: {trav_idx:.2f}   |   Effective Speed: {eff_spd:.1f} km/h\n", "meta_text")
                result_text.insert(tk.END, f"  • Estimated Transit Time: {t_dur:.2f} h   |   Deadline: {maximum_time:.1f} h\n", "meta_text")

            result_text.insert(tk.END, "\n" + "=" * 68 + "\n\n", "separator")

            # Feasible Ranking Table
            result_text.insert(tk.END, f"QUALIFIED VEHICLE RANKING ({len(feasible_list)} Platforms Passed Gatekeeper)\n", "heading")
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

            # Decision Robustness & Sensitivity Briefing
            sens = results.get("sensitivity", {})
            if sens:
                result_text.insert(tk.END, "\nDECISION ROBUSTNESS & SENSITIVITY:\n", "heading_small")
                result_text.insert(tk.END, f"• {sens.get('summary', '')}\n", "meta_text")
                for sp in sens.get("sensitive_parameters", []):
                    result_text.insert(tk.END, f"  ↳ {sp}\n", "bullet_yellow")

        else:
            result_text.insert(tk.END, "⚠️ NO QUALIFIED CANDIDATES FOUND\n", "infeasible_title")
            result_text.insert(tk.END, "No vehicle in the database satisfies all mandatory physical and tactical constraints.\n\n", "bullet_red")

        # Infeasible Candidates Diagnostic
        if infeasible_list:
            result_text.insert(tk.END, "\n" + "-" * 68 + "\n", "separator")
            result_text.insert(tk.END, f"DISQUALIFIED CANDIDATES ({len(infeasible_list)} vehicles failed Stage 1 Gatekeeper):\n", "heading_small")
            for inf in infeasible_list:
                reasons = inf.get("explanation", {}).get("failed_constraints", ["Failed constraints"])
                result_text.insert(tk.END, f"  ✕  {inf['vehicle_name']}: ", "bullet_red")
                result_text.insert(tk.END, f"{'; '.join(reasons)}\n", "infeasible_text")

        status_label.config(
            text=f"● Analysis complete. {len(feasible_list)} qualified, {len(infeasible_list)} disqualified (Total: {len(catalog)})"
        )
        
        root.update_idletasks()
        outer_canvas.configure(scrollregion=outer_canvas.bbox("all"))

    except Exception as e:
        error_msg = traceback.format_exc()
        messagebox.showerror("Execution Error", f"An error occurred during analysis:\n\n{error_msg}")


# -------------------------------------------------------------
# MODAL DIALOG 1: NEW VEHICLE ADDITION (PLATFORM ONBOARDING)
# -------------------------------------------------------------
def open_new_vehicle_dialog():
    dialog = tk.Toplevel(root)
    dialog.title("STRIDE — Platform Onboarding Portal (Add New UGV)")
    dialog.geometry("760x780")
    dialog.minsize(680, 600)
    dialog.configure(bg=BG)
    dialog.transient(root)
    dialog.grab_set()

    d_canvas = tk.Canvas(dialog, bg=BG, highlightthickness=0)
    d_canvas.pack(side="left", fill="both", expand=True)

    d_scrollbar = ttk.Scrollbar(dialog, orient="vertical", command=d_canvas.yview)
    d_scrollbar.pack(side="right", fill="y")
    d_canvas.configure(yscrollcommand=d_scrollbar.set)

    d_frame = tk.Frame(d_canvas, bg=BG, padx=25, pady=20)
    d_window = d_canvas.create_window((0, 0), window=d_frame, anchor="nw")

    def d_update_scroll(event=None):
        d_canvas.configure(scrollregion=d_canvas.bbox("all"))

    def d_resize(event):
        d_canvas.itemconfig(d_window, width=event.width)

    d_frame.bind("<Configure>", d_update_scroll)
    d_canvas.bind("<Configure>", d_resize)

    # Header
    tk.Label(
        d_frame,
        text="DEFENCE PLATFORM ONBOARDING",
        bg=BG,
        fg=ACCENT,
        font=("Segoe UI", 16, "bold")
    ).pack(anchor="w")
    tk.Label(
        d_frame,
        text="Register a new Indian defence UGV platform with full canonical specifications and imagery.",
        bg=BG,
        fg=TEXT_SECONDARY,
        font=("Segoe UI", 9)
    ).pack(anchor="w", pady=(2, 15))

    # Form Container
    form = tk.Frame(d_frame, bg=CARD, highlightbackground=BORDER, highlightthickness=1, padx=20, pady=15)
    form.pack(fill="x")

    def make_entry(parent, label_text, row, col=0, width=28):
        tk.Label(parent, text=label_text, bg=CARD, fg=TEXT, font=("Segoe UI", 9, "bold")).grid(row=row, column=col, sticky="w", pady=(8, 2))
        entry = tk.Entry(
            parent,
            width=width,
            bg=INPUT_BG,
            fg=TEXT,
            insertbackground=TEXT,
            relief="flat",
            highlightbackground=BORDER,
            highlightcolor=ACCENT,
            highlightthickness=1,
            font=("Segoe UI", 9)
        )
        entry.grid(row=row+1, column=col, sticky="w", pady=(0, 6), padx=(0, 15))
        return entry

    # 1. Identity
    tk.Label(form, text="1. PLATFORM IDENTITY", bg=CARD, fg=ACCENT, font=("Segoe UI", 10, "bold")).grid(row=0, column=0, columnspan=2, sticky="w", pady=(4, 6))
    vname_entry = make_entry(form, "Platform / Vehicle Name *", 1, 0)
    manuf_entry = make_entry(form, "Manufacturer / Developer *", 1, 1)

    tk.Label(form, text="Mobility Type *", bg=CARD, fg=TEXT, font=("Segoe UI", 9, "bold")).grid(row=3, column=0, sticky="w", pady=(4, 2))
    mob_var = tk.StringVar(value="Tracked")
    mob_combo = ttk.Combobox(form, textvariable=mob_var, values=["Tracked", "Wheeled 4x4", "Wheeled 6x6", "Wheeled 8x8", "Quadruped (Robot Dog)"], state="readonly", width=25, style="STRIDE.TCombobox")
    mob_combo.grid(row=4, column=0, sticky="w", pady=(0, 8), padx=(0, 15))

    tk.Label(form, text="Operational Status", bg=CARD, fg=TEXT, font=("Segoe UI", 9, "bold")).grid(row=3, column=1, sticky="w", pady=(4, 2))
    status_var = tk.StringVar(value="Developed / Demonstrated")
    status_combo = ttk.Combobox(form, textvariable=status_var, values=["Developed / Demonstrated", "Field Trials / Evaluated", "In Service", "Under Procurement / Induction", "In Production", "Technology Demonstrator"], state="readonly", width=25, style="STRIDE.TCombobox")
    status_combo.grid(row=4, column=1, sticky="w", pady=(0, 8))

    # 2. Roles (Multi-Select Checkboxes)
    tk.Label(form, text="2. SUPPORTED MISSION ROLES * (Select all that apply)", bg=CARD, fg=ACCENT, font=("Segoe UI", 10, "bold")).grid(row=5, column=0, columnspan=2, sticky="w", pady=(12, 6))
    role_checks = {}
    r_frame = tk.Frame(form, bg=CARD)
    r_frame.grid(row=6, column=0, columnspan=2, sticky="w")
    for idx, role in enumerate(mission_roles):
        var = tk.BooleanVar(value=(idx == 0))
        cb = tk.Checkbutton(r_frame, text=role, variable=var, bg=CARD, fg=TEXT, selectcolor=INPUT_BG, activebackground=CARD, activeforeground=ACCENT, font=("Segoe UI", 8))
        cb.grid(row=idx//2, column=idx%2, sticky="w", padx=(0, 20), pady=2)
        role_checks[role] = var

    # 3. Terrains (Multi-Select Checkboxes)
    tk.Label(form, text="3. OPERATIONAL TERRAIN CAPABILITIES * (Select all that apply)", bg=CARD, fg=ACCENT, font=("Segoe UI", 10, "bold")).grid(row=7, column=0, columnspan=2, sticky="w", pady=(12, 6))
    terrain_checks = {}
    t_frame = tk.Frame(form, bg=CARD)
    t_frame.grid(row=8, column=0, columnspan=2, sticky="w")
    for idx, t in enumerate(terrain_options):
        var = tk.BooleanVar(value=(idx < 2))
        cb = tk.Checkbutton(t_frame, text=t, variable=var, bg=CARD, fg=TEXT, selectcolor=INPUT_BG, activebackground=CARD, activeforeground=ACCENT, font=("Segoe UI", 8))
        cb.grid(row=idx//2, column=idx%2, sticky="w", padx=(0, 20), pady=2)
        terrain_checks[t] = var

    # 4. Performance Metrics
    tk.Label(form, text="4. PERFORMANCE METRICS (Leave empty if unknown)", bg=CARD, fg=ACCENT, font=("Segoe UI", 10, "bold")).grid(row=9, column=0, columnspan=2, sticky="w", pady=(12, 6))
    payload_input = make_entry(form, "Payload Capacity (kg)", 10, 0)
    speed_input = make_entry(form, "Max Speed (km/h)", 10, 1)
    range_input = make_entry(form, "Operating Range (km)", 12, 0)
    endurance_input = make_entry(form, "Continuous Endurance (hours)", 12, 1)

    # 5. Standoff, Climate & Stealth
    tk.Label(form, text="5. TACTICAL STANDOFF, CLIMATE & STEALTH", bg=CARD, fg=ACCENT, font=("Segoe UI", 10, "bold")).grid(row=14, column=0, columnspan=2, sticky="w", pady=(12, 6))
    standoff_input = make_entry(form, "Operator Standoff Range (km)", 15, 0)
    alt_input = make_entry(form, "Max Operating Altitude (m ASL)", 15, 1)
    alt_input.insert(0, "4000")

    tk.Label(form, text="Propulsion & Acoustic Stealth", bg=CARD, fg=TEXT, font=("Segoe UI", 9, "bold")).grid(row=17, column=0, sticky="w", pady=(4, 2))
    prop_var = tk.StringVar(value="All-Electric (Silent)")
    prop_combo = ttk.Combobox(form, textvariable=prop_var, values=["All-Electric (Silent)", "Hybrid-Electric", "Diesel / IC Engine"], state="readonly", width=25, style="STRIDE.TCombobox")
    prop_combo.grid(row=18, column=0, sticky="w", pady=(0, 8), padx=(0, 15))

    tk.Label(form, text="Primary Control Link", bg=CARD, fg=TEXT, font=("Segoe UI", 9, "bold")).grid(row=17, column=1, sticky="w", pady=(4, 2))
    link_var = tk.StringVar(value="COFDM NLOS (Non-Line of Sight Mesh)")
    link_combo = ttk.Combobox(form, textvariable=link_var, values=control_links[1:], state="readonly", width=25, style="STRIDE.TCombobox")
    link_combo.grid(row=18, column=1, sticky="w", pady=(0, 8))

    # 6. Image & Source
    tk.Label(form, text="6. IMAGE ASSET & CITATION", bg=CARD, fg=ACCENT, font=("Segoe UI", 10, "bold")).grid(row=19, column=0, columnspan=2, sticky="w", pady=(12, 6))
    source_input = make_entry(form, "Source / Reference Citation", 20, 0, width=58)
    source_input.insert(0, "OEM Datasheet / Defense Exhibition")

    img_frame = tk.Frame(form, bg=CARD)
    img_frame.grid(row=22, column=0, columnspan=2, sticky="w", pady=(4, 10))
    tk.Label(img_frame, text="Vehicle Image Path:", bg=CARD, fg=TEXT, font=("Segoe UI", 9, "bold")).pack(side="left")
    img_path_entry = tk.Entry(img_frame, width=38, bg=INPUT_BG, fg=TEXT, insertbackground=TEXT, relief="flat", highlightbackground=BORDER, highlightcolor=ACCENT, highlightthickness=1, font=("Segoe UI", 9))
    img_path_entry.insert(0, "assets/images/kalyani_ecars_4x4.jpg")
    img_path_entry.pack(side="left", padx=8)

    def browse_image():
        filename = filedialog.askopenfilename(
            parent=dialog,
            title="Select Vehicle Image",
            filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.webp"), ("All Files", "*.*")]
        )
        if filename:
            img_path_entry.delete(0, tk.END)
            img_path_entry.insert(0, filename)

    tk.Button(img_frame, text="Browse...", command=browse_image, bg=CARD_LIGHT, fg=TEXT, font=("Segoe UI", 8), padx=10, relief="flat", cursor="hand2").pack(side="left")

    def submit_vehicle():
        roles_chosen = [r for r, v in role_checks.items() if v.get()]
        terrains_chosen = [t for t, v in terrain_checks.items() if v.get()]

        raw = {
            "vehicle_name": vname_entry.get(),
            "manufacturer": manuf_entry.get(),
            "mobility_type": mob_var.get(),
            "status": status_var.get(),
            "mission_roles": roles_chosen,
            "terrain_capabilities": terrains_chosen,
            "payload_capacity_kg": payload_input.get().strip(),
            "max_speed_kmh": speed_input.get().strip(),
            "operating_range_km": range_input.get().strip(),
            "endurance_hours": endurance_input.get().strip(),
            "max_control_range_km": standoff_input.get().strip(),
            "control_link_types": [link_var.get()],
            "max_altitude_m_asl": alt_input.get().strip(),
            "propulsion_type": prop_var.get(),
            "source": source_input.get(),
            "image_path": img_path_entry.get()
        }

        success, msg, v_record = add_vehicle(raw)
        if success:
            messagebox.showinfo("Success", msg, parent=dialog)
            catalog = get_active_catalog()
            status_label.config(text=f"● Platform registered! Total {len(catalog)} Indian UGVs active")
            dialog.destroy()
        else:
            messagebox.showerror("Validation Error", msg, parent=dialog)

    btn_frame = tk.Frame(d_frame, bg=BG)
    btn_frame.pack(fill="x", pady=15)
    tk.Button(btn_frame, text="REGISTER PLATFORM IN DATABASE", command=submit_vehicle, bg=SUCCESS, fg="#111827", font=("Segoe UI", 10, "bold"), padx=20, pady=8, relief="flat", cursor="hand2").pack(side="left")
    tk.Button(btn_frame, text="CANCEL", command=dialog.destroy, bg=CARD_LIGHT, fg=TEXT, font=("Segoe UI", 10), padx=15, pady=8, relief="flat", cursor="hand2").pack(side="left", padx=10)


# -------------------------------------------------------------
# MODAL DIALOG 2: DESCRIBE MISSION (NATURAL LANGUAGE PARSER)
# -------------------------------------------------------------
def open_nlp_mission_dialog():
    dialog = tk.Toplevel(root)
    dialog.title("STRIDE — Describe Mission in Your Own Words")
    dialog.geometry("680x600")
    dialog.minsize(600, 500)
    dialog.configure(bg=BG)
    dialog.transient(root)
    dialog.grab_set()

    tk.Label(
        dialog,
        text="SMART MISSION NARRATIVE PARSER",
        bg=BG,
        fg=ACCENT,
        font=("Segoe UI", 15, "bold")
    ).pack(anchor="w", padx=25, pady=(20, 2))

    tk.Label(
        dialog,
        text="Type your mission requirements in free-form natural language. STRIDE's offline parser will extract all parameters.",
        bg=BG,
        fg=TEXT_SECONDARY,
        font=("Segoe UI", 9)
    ).pack(anchor="w", padx=25, pady=(0, 12))

    # Presets
    presets_frame = tk.Frame(dialog, bg=CARD, padx=15, pady=10, highlightbackground=BORDER, highlightthickness=1)
    presets_frame.pack(fill="x", padx=25, pady=(0, 10))
    tk.Label(presets_frame, text="Or choose a realistic defense scenario preset:", bg=CARD, fg=TEXT, font=("Segoe UI", 9, "bold")).pack(anchor="w")

    preset_texts = {
        "Himalayan High-Altitude Patrol": "Conduct high altitude reconnaissance and surveillance patrol in Ladakh at 15000 ft in sub-zero snow terrain, carrying 50 kg sensor payload with silent electric stealth and 10 km standoff.",
        "Western Desert Logistics Resupply": "Execute heavy logistics resupply mission across the Thar Desert sand dunes carrying 500 kg ammunition payload over a 15 km distance within a 3 hour deadline.",
        "Urban Room Breaching & IED Defusal": "Enter a confined urban building and clear suspicious explosive packages using remote robotic disrupter arm within 45 minutes and 200m standoff."
    }

    def load_preset(text):
        nlp_text.delete("1.0", tk.END)
        nlp_text.insert(tk.END, text)

    btn_subframe = tk.Frame(presets_frame, bg=CARD)
    btn_subframe.pack(fill="x", pady=6)
    for title, p_text in preset_texts.items():
        tk.Button(
            btn_subframe,
            text=title,
            command=lambda t=p_text: load_preset(t),
            bg=CARD_LIGHT,
            fg=TEXT,
            font=("Segoe UI", 8),
            relief="flat",
            cursor="hand2"
        ).pack(side="left", padx=4)

    nlp_text = tk.Text(
        dialog,
        bg=INPUT_BG,
        fg=TEXT,
        insertbackground=TEXT,
        relief="flat",
        highlightbackground=BORDER,
        highlightcolor=ACCENT,
        highlightthickness=1,
        font=("Consolas", 10),
        padx=15,
        pady=12,
        height=7
    )
    nlp_text.pack(fill="x", padx=25, pady=10)
    nlp_text.insert(tk.END, "High altitude reconnaissance patrol in Ladakh at 15000 ft in sub-zero snow terrain, carrying 50 kg sensor payload with silent electric stealth and 10 km standoff within 3 hours.")

    log_box = tk.Text(dialog, bg=INPUT_BG, fg=TEXT_SECONDARY, relief="flat", font=("Consolas", 8), height=6, padx=10, pady=8)
    log_box.pack(fill="both", expand=True, padx=25, pady=(0, 10))

    def parse_and_apply():
        content = nlp_text.get("1.0", tk.END).strip()
        if not content:
            messagebox.showerror("Error", "Please enter a mission description.", parent=dialog)
            return

        res = parse_mission_narrative(content)
        
        # Display extraction log
        log_box.delete("1.0", tk.END)
        log_box.insert(tk.END, "PARSER EXTRACTION LOG:\n" + "-" * 50 + "\n")
        for log in res.get("confidence_log", []):
            log_box.insert(tk.END, f"• {log}\n")

        # Apply to main UI
        if res["roles"]:
            primary_role_variable.set(res["roles"][0])
            for role, var in role_checkbox_vars.items():
                var.set(role in res["roles"])
        if res["terrain"] in terrain_options:
            terrain_variable.set(res["terrain"])
        
        payload_entry.delete(0, tk.END)
        payload_entry.insert(0, str(res["payload_kg"]))

        range_entry.delete(0, tk.END)
        range_entry.insert(0, str(res["operating_range_km"]))

        minimum_time_entry.delete(0, tk.END)
        minimum_time_entry.insert(0, str(res["min_time_hours"]))

        maximum_time_entry.delete(0, tk.END)
        maximum_time_entry.insert(0, str(res["max_time_hours"]))

        standoff_entry.delete(0, tk.END)
        standoff_entry.insert(0, str(res["standoff_km"]))

        altitude_entry.delete(0, tk.END)
        altitude_entry.insert(0, str(res["altitude_m"]))

        temp_entry.delete(0, tk.END)
        temp_entry.insert(0, str(res["temperature_c"]))

        if res["stealth_required"]:
            stealth_variable.set("Silent Electric Only (Strict Acoustic/Thermal Masking)")
        else:
            stealth_variable.set("Standard (Any Propulsion)")

        messagebox.showinfo("Applied", "Mission parameters successfully extracted and populated into the configuration form!", parent=dialog)
        dialog.destroy()

    tk.Button(dialog, text="✨ PARSE & AUTO-CONFIGURE MISSION", command=parse_and_apply, bg=ACCENT_DARK, fg="white", font=("Segoe UI", 10, "bold"), padx=20, pady=8, relief="flat", cursor="hand2").pack(pady=(0, 15))


# -------------------------------------------------------------
# MAIN APPLICATION INTERFACE
# -------------------------------------------------------------

# Header
header = ttk.Frame(page_frame, style="Main.TFrame")
header.pack(fill="x", padx=35, pady=(20, 12))

title_frame = ttk.Frame(header, style="Main.TFrame")
title_frame.pack(fill="x")
ttk.Label(title_frame, text="STRIDE", style="Title.TLabel").pack(side="left")
ttk.Label(title_frame, text="DEFENSE VEHICLE ANALYSIS", style="Subtitle.TLabel").pack(side="left", padx=15, pady=(8, 0))

# Top Action Toolbar (New Vehicle Addition + Describe Mission)
top_toolbar = tk.Frame(title_frame, bg=BG)
top_toolbar.pack(side="right", pady=(5, 0))

tk.Button(
    top_toolbar,
    text="➕ New Vehicle Addition",
    command=open_new_vehicle_dialog,
    bg=CARD_LIGHT,
    fg=TEXT,
    activebackground=BORDER,
    activeforeground=TEXT,
    relief="flat",
    cursor="hand2",
    font=("Segoe UI", 9, "bold"),
    padx=12,
    pady=6
).pack(side="right", padx=5)

tk.Button(
    top_toolbar,
    text="💬 Describe Mission (NLP)",
    command=open_nlp_mission_dialog,
    bg=CARD_LIGHT,
    fg=ACCENT,
    activebackground=BORDER,
    activeforeground=ACCENT,
    relief="flat",
    cursor="hand2",
    font=("Segoe UI", 9, "bold"),
    padx=12,
    pady=6
).pack(side="right", padx=5)

ttk.Label(header, text="Smart Terrain & Robotic Intelligence For Defense Engineering (24 Indian Platforms)", style="Subtitle.TLabel").pack(anchor="w", pady=(2, 0))


# Mission Configuration Frame
requirements_frame = tk.Frame(page_frame, bg=CARD, highlightbackground=BORDER, highlightthickness=1)
requirements_frame.pack(fill="x", padx=35, pady=8)

tk.Label(
    requirements_frame,
    text="MISSION CONFIGURATION",
    bg=CARD,
    fg=TEXT,
    font=("Segoe UI", 12, "bold")
).grid(row=0, column=0, columnspan=3, sticky="w", padx=20, pady=(15, 2))

tk.Label(
    requirements_frame,
    text="Define mission parameters, multi-role requirements, and their relative operational priorities.",
    bg=CARD,
    fg=TEXT_SECONDARY,
    font=("Segoe UI", 9)
).grid(row=1, column=0, columnspan=3, sticky="w", padx=20, pady=(0, 12))

for column, text in enumerate(["REQUIREMENT", "REQUIRED VALUE / SETTING", "PRIORITY WEIGHT"]):
    tk.Label(
        requirements_frame,
        text=text,
        bg=CARD,
        fg=TEXT_SECONDARY,
        font=("Segoe UI", 8, "bold")
    ).grid(row=2, column=column, sticky="w", padx=20, pady=(0, 6))

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
    combo.grid(row=row, column=2, sticky="w", padx=20, pady=5)
    priority_variables[parameter] = variable


# 1. Primary Mission Role
tk.Label(requirements_frame, text="Primary Mission Role", bg=CARD, fg=TEXT, font=("Segoe UI", 9, "bold")).grid(row=3, column=0, sticky="w", padx=20, pady=5)
primary_role_variable = tk.StringVar(value=mission_roles[0])
ttk.Combobox(
    requirements_frame,
    textvariable=primary_role_variable,
    values=mission_roles,
    state="readonly",
    width=32,
    style="STRIDE.TCombobox"
).grid(row=3, column=1, sticky="w", padx=20, pady=5)
create_priority(3, "Mission Role")

# Multi-Role Checklist (Row 4)
multi_role_container = tk.Frame(requirements_frame, bg=CARD_LIGHT, padx=10, pady=6, highlightbackground=BORDER, highlightthickness=1)
multi_role_container.grid(row=4, column=0, columnspan=3, sticky="we", padx=20, pady=(2, 8))
tk.Label(multi_role_container, text="Multi-Role Capability Checklist (Select additional concurrent mission roles):", bg=CARD_LIGHT, fg=ACCENT, font=("Segoe UI", 8, "bold")).pack(anchor="w")

role_checkbox_vars = {}
mr_inner = tk.Frame(multi_role_container, bg=CARD_LIGHT)
mr_inner.pack(fill="x", pady=2)
for idx, role in enumerate(mission_roles):
    var = tk.BooleanVar(value=(idx == 0))
    cb = tk.Checkbutton(mr_inner, text=role, variable=var, bg=CARD_LIGHT, fg=TEXT, selectcolor=INPUT_BG, activebackground=CARD_LIGHT, activeforeground=ACCENT, font=("Segoe UI", 8))
    cb.grid(row=idx//3, column=idx%3, sticky="w", padx=(0, 15))
    role_checkbox_vars[role] = var

# 2. Terrain
tk.Label(requirements_frame, text="Operational Terrain", bg=CARD, fg=TEXT, font=("Segoe UI", 9, "bold")).grid(row=5, column=0, sticky="w", padx=20, pady=5)
terrain_variable = tk.StringVar(value=terrain_options[0])
ttk.Combobox(
    requirements_frame,
    textvariable=terrain_variable,
    values=terrain_options,
    state="readonly",
    width=32,
    style="STRIDE.TCombobox"
).grid(row=5, column=1, sticky="w", padx=20, pady=5)
create_priority(5, "Terrain")

# 3. Payload
tk.Label(requirements_frame, text="Payload Capacity (kg)", bg=CARD, fg=TEXT, font=("Segoe UI", 9, "bold")).grid(row=6, column=0, sticky="w", padx=20, pady=5)
payload_entry = tk.Entry(requirements_frame, width=34, bg=INPUT_BG, fg=TEXT, insertbackground=TEXT, relief="flat", highlightbackground=BORDER, highlightcolor=ACCENT, highlightthickness=1, font=("Segoe UI", 9))
payload_entry.insert(0, "50.0")
payload_entry.grid(row=6, column=1, sticky="w", padx=20, pady=5)
create_priority(6, "Payload")

# 4. Mission Distance
tk.Label(requirements_frame, text="Mission Distance (km)", bg=CARD, fg=TEXT, font=("Segoe UI", 9, "bold")).grid(row=7, column=0, sticky="w", padx=20, pady=5)
range_entry = tk.Entry(requirements_frame, width=34, bg=INPUT_BG, fg=TEXT, insertbackground=TEXT, relief="flat", highlightbackground=BORDER, highlightcolor=ACCENT, highlightthickness=1, font=("Segoe UI", 9))
range_entry.insert(0, "15.0")
range_entry.grid(row=7, column=1, sticky="w", padx=20, pady=5)
create_priority(7, "Operating Range")

# 5. Minimum Time
tk.Label(requirements_frame, text="Minimum Mission Time (hours)", bg=CARD, fg=TEXT, font=("Segoe UI", 9, "bold")).grid(row=8, column=0, sticky="w", padx=20, pady=5)
minimum_time_entry = tk.Entry(requirements_frame, width=34, bg=INPUT_BG, fg=TEXT, insertbackground=TEXT, relief="flat", highlightbackground=BORDER, highlightcolor=ACCENT, highlightthickness=1, font=("Segoe UI", 9))
minimum_time_entry.insert(0, "1.0")
minimum_time_entry.grid(row=8, column=1, sticky="w", padx=20, pady=5)
create_priority(8, "Minimum Mission Time")

# 6. Maximum Time
tk.Label(requirements_frame, text="Maximum Mission Time (hours)", bg=CARD, fg=TEXT, font=("Segoe UI", 9, "bold")).grid(row=9, column=0, sticky="w", padx=20, pady=5)
maximum_time_entry = tk.Entry(requirements_frame, width=34, bg=INPUT_BG, fg=TEXT, insertbackground=TEXT, relief="flat", highlightbackground=BORDER, highlightcolor=ACCENT, highlightthickness=1, font=("Segoe UI", 9))
maximum_time_entry.insert(0, "3.0")
maximum_time_entry.grid(row=9, column=1, sticky="w", padx=20, pady=5)
create_priority(9, "Maximum Mission Time")


# -------------------------------------------------------------
# ADVANCED TACTICAL PARAMETERS (STANDOFF, ALTITUDE, STEALTH)
# -------------------------------------------------------------
tactical_frame = tk.Frame(page_frame, bg=CARD, highlightbackground=BORDER, highlightthickness=1, padx=20, pady=12)
tactical_frame.pack(fill="x", padx=35, pady=8)

tk.Label(tactical_frame, text="ADVANCED TACTICAL PARAMETERS (PHASE 2 - 4 EXTENSIONS)", bg=CARD, fg=TEXT, font=("Segoe UI", 11, "bold")).pack(anchor="w")
tk.Label(tactical_frame, text="Refine operator standoff, high-altitude tolerance, and acoustic stealth envelopes.", bg=CARD, fg=TEXT_SECONDARY, font=("Segoe UI", 8)).pack(anchor="w", pady=(0, 10))

tac_grid = tk.Frame(tactical_frame, bg=CARD)
tac_grid.pack(fill="x")

# Row 1: Standoff Distance & Link
tk.Label(tac_grid, text="Operator Standoff (km):", bg=CARD, fg=TEXT, font=("Segoe UI", 9)).grid(row=0, column=0, sticky="w", pady=4)
standoff_entry = tk.Entry(tac_grid, width=15, bg=INPUT_BG, fg=TEXT, insertbackground=TEXT, relief="flat", highlightbackground=BORDER, highlightcolor=ACCENT, highlightthickness=1, font=("Segoe UI", 9))
standoff_entry.insert(0, "5.0")
standoff_entry.grid(row=0, column=1, sticky="w", padx=(5, 25), pady=4)

tk.Label(tac_grid, text="Control Link Type:", bg=CARD, fg=TEXT, font=("Segoe UI", 9)).grid(row=0, column=2, sticky="w", pady=4)
link_var = tk.StringVar(value=control_links[0])
ttk.Combobox(tac_grid, textvariable=link_var, values=control_links, state="readonly", width=25, style="STRIDE.TCombobox").grid(row=0, column=3, sticky="w", padx=5, pady=4)

# Row 2: Altitude & Temp
tk.Label(tac_grid, text="Operational Altitude (m ASL):", bg=CARD, fg=TEXT, font=("Segoe UI", 9)).grid(row=1, column=0, sticky="w", pady=4)
altitude_entry = tk.Entry(tac_grid, width=15, bg=INPUT_BG, fg=TEXT, insertbackground=TEXT, relief="flat", highlightbackground=BORDER, highlightcolor=ACCENT, highlightthickness=1, font=("Segoe UI", 9))
altitude_entry.insert(0, "1500")
altitude_entry.grid(row=1, column=1, sticky="w", padx=(5, 25), pady=4)

tk.Label(tac_grid, text="Temperature (°C):", bg=CARD, fg=TEXT, font=("Segoe UI", 9)).grid(row=1, column=2, sticky="w", pady=4)
temp_entry = tk.Entry(tac_grid, width=15, bg=INPUT_BG, fg=TEXT, insertbackground=TEXT, relief="flat", highlightbackground=BORDER, highlightcolor=ACCENT, highlightthickness=1, font=("Segoe UI", 9))
temp_entry.insert(0, "25.0")
temp_entry.grid(row=1, column=3, sticky="w", padx=5, pady=4)

# Row 3: Stealth Profile
tk.Label(tac_grid, text="Stealth Requirement:", bg=CARD, fg=TEXT, font=("Segoe UI", 9)).grid(row=2, column=0, sticky="w", pady=4)
stealth_variable = tk.StringVar(value=stealth_options[0])
ttk.Combobox(tac_grid, textvariable=stealth_variable, values=stealth_options, state="readonly", width=35, style="STRIDE.TCombobox").grid(row=2, column=1, columnspan=3, sticky="w", padx=5, pady=4)


# Action Buttons Frame
action_frame = tk.Frame(page_frame, bg=BG)
action_frame.pack(fill="x", padx=35, pady=12)

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


# -------------------------------------------------------------
# RESULTS DISPLAY & VEHICLE PREVIEW CONTAINER
# -------------------------------------------------------------
result_frame = tk.Frame(page_frame, bg=CARD, highlightbackground=BORDER, highlightthickness=1)
result_frame.pack(fill="both", expand=True, padx=35, pady=(0, 15))

# Top title + vehicle photo preview header
results_top = tk.Frame(result_frame, bg=CARD)
results_top.pack(fill="x", padx=20, pady=(15, 10))

results_info_left = tk.Frame(results_top, bg=CARD)
results_info_left.pack(side="left", fill="both", expand=True)

tk.Label(
    results_info_left,
    text="ANALYSIS RESULTS & DECISION EXPLAINABILITY",
    bg=CARD,
    fg=TEXT,
    font=("Segoe UI", 12, "bold")
).pack(anchor="w")

tk.Label(
    results_info_left,
    text="Full audit trail, capability safety margins, sensitivity, and real-time vehicle imagery.",
    bg=CARD,
    fg=TEXT_SECONDARY,
    font=("Segoe UI", 9)
).pack(anchor="w", pady=(2, 0))

# Vehicle Photo Preview Frame (Right side of results header)
preview_box = tk.Frame(results_top, bg=INPUT_BG, highlightbackground=BORDER, highlightthickness=1, padx=4, pady=4)
preview_box.pack(side="right", padx=(10, 0))

image_label = tk.Label(
    preview_box,
    text="No platform selected",
    bg=INPUT_BG,
    fg=TEXT_SECONDARY,
    width=38,
    height=9,
    font=("Segoe UI", 9)
)
image_label.pack()

image_meta_label = tk.Label(
    preview_box,
    text="",
    bg=INPUT_BG,
    fg=ACCENT,
    font=("Segoe UI", 8, "bold")
)
image_meta_label.pack(pady=(2, 0))

# Result Text Box
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
    height=20
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

# Status Bar
status_frame = tk.Frame(page_frame, bg=BG)
status_frame.pack(fill="x", padx=35, pady=(0, 12))

catalog_initial = get_active_catalog()
status_label = tk.Label(status_frame, text=f"● Ready for mission analysis ({len(catalog_initial)} Indian UGVs active)", bg=BG, fg=TEXT_SECONDARY, font=("Segoe UI", 9))
status_label.pack(side="left")

tk.Label(status_frame, text="STRIDE Operational Engine v2.0", bg=BG, fg=TEXT_SECONDARY, font=("Segoe UI", 9)).pack(side="right")

if __name__ == "__main__":
    root.mainloop()