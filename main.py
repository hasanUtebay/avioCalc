import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import sys
import os

# --- Logic Functions ---
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def normalize(angle):
    return angle % 360

def format_number(n):
    try:
        # Binlik ayırıcı için temizle ve formatla
        clean_n = str(n).replace(',', '')
        return "{:,.0f}".format(float(clean_n))
    except:
        return str(n)

def clean_to_float(value):
    """Hem virgülü hem noktayı ondalık kabul eder, binlik ayıracı temizler"""
    if not value: return 0.0
    val = value.replace(" ", "")
    if "," in val:
        parts = val.split(",")
        if len(parts[-1]) != 3: # Ondalık virgülü (örn: 10,5)
            val = val.replace(",", ".")
        else: # Binlik virgülü (örn: 10,000)
            val = val.replace(",", "")
    try:
        return float(val)
    except:
        return 0.0

def on_focus_out(event):
    widget = event.widget
    current_val = widget.get()
    if current_val:
        formatted_val = format_number(current_val)
        widget.delete(0, tk.END)
        widget.insert(0, formatted_val)

def validate_input(P):
    return P == "" or all(char in "0123456789.," for char in P)

# --- Calculate Functions ---

def calculate_descent():
    try:
        raw_alt = clean_to_float(entry_alt.get())
        raw_trgt = clean_to_float(entry_trgt.get())
        raw_dist = clean_to_float(entry_dist.get())
        raw_gs = clean_to_float(entry_gs.get())

        alt_diff = raw_alt - raw_trgt
        if alt_diff <= 0:
            messagebox.showwarning("Warning", "Current altitude must be higher than target!")
            return

        vs_net = (alt_diff * raw_gs) / (raw_dist * 60)
        vs_to_set = int((vs_net + 99) / 100) * 100
        suggested_dist = (alt_diff * raw_gs) / (vs_to_set * 60)

        label_net_vs.config(text=f"Required Net VS: -{format_number(vs_net)} fpm")
        label_set_vs.config(text=f"SET VS: -{format_number(vs_to_set)} fpm")
        label_sugg_dist.config(text=f"START DESCENT AT: {round(suggested_dist, 1)} NM")
    except:
        messagebox.showerror("Error", "Invalid input!")

def calculate_holding():
    try:
        hdg = clean_to_float(ent_hold_hdg.get())
        out_crs = clean_to_float(ent_hold_oc.get())
        side = var_side.get()
        
        in_crs = normalize(out_crs + 180)
        diff = (out_crs - hdg + 180) % 360 - 180
        
        entry_type = ""
        instructions = ""

        if side == "L": # --- SOL ---
            if -70 <= diff <= 0:
                entry_type = "TEARDROP (Sector 2)"
                offset_hdg = int(normalize(out_crs + 30))
                instructions = (f"ENTRY INSTRUCTIONS:\n1. Fly to the fix and cross it.\n2. Turn HDG {offset_hdg} and fly equal time to the inbound.\n3. Turn Left and intercept the inbound CRS {int(in_crs)}.\n4. Fly to the fix on CRS {int(in_crs)} with HDG {int(in_crs)}.\n\nHOLD INSTRUCTIONS:\n1. Fly to the fix on CRS {int(in_crs)} with HDG {int(in_crs)}.\n2. Turn Left to HDG {int(out_crs)}.\n3. Fly HDG {int(out_crs)} outbound Equal time to the inbound.\n4. Turn Left and intercept CRS {int(in_crs)}.\n5. Repeat")
            elif 0 < diff <= 110:
                entry_type = "PARALLEL (Sector 1)"
                instructions = (f"ENTRY INSTRUCTIONS:\n1. Fly to the fix and cross it.\n2. Turn to CRS {int(out_crs)} with HDG {int(out_crs)} and fly equal time to the inbound.\n3. Turn Right Past HDG {int(in_crs)}.\n4. Intercept the inbound CRS {int(in_crs)} and fly HDG {int(in_crs)} to the fix.\n5. Go to Hold Instructions: Step 2.\n\nHOLD INSTRUCTIONS:\n1. Fly to the fix on CRS {int(in_crs)} with HDG {int(in_crs)}.\n2. Turn Left to HDG {int(out_crs)}.\n3. Fly HDG {int(out_crs)} outbound Equal time to the inbound.\n4. Turn Left and intercept CRS {int(in_crs)}.\n5. Repeat")
            else:
                entry_type = "DIRECT (Sector 3)"
                instructions = (f"ENTRY INSTRUCTIONS:\n1. Fly to the fix and cross it.\n2. Go to Hold Instructions: Step 2.\n\nHOLD INSTRUCTIONS:\n1. Fly to the fix on CRS {int(in_crs)} with HDG {int(in_crs)}.\n2. Turn Left to HDG {int(out_crs)}.\n3. Fly HDG {int(out_crs)} outbound Equal time to the inbound.\n4. Turn Left and intercept CRS {int(in_crs)}.\n5. Repeat")
        else: # --- SAĞ ---
            if 0 <= diff <= 70:
                entry_type = "TEARDROP (Sector 2)"
                offset_hdg = int(normalize(out_crs - 30))
                instructions = (f"ENTRY INSTRUCTIONS:\n1. Fly to the fix and cross it.\n2. Turn HDG {offset_hdg} and fly equal time to the inbound.\n3. Turn Right and intercept the inbound CRS {int(in_crs)}.\n4. Fly to the fix on CRS {int(in_crs)} with HDG {int(in_crs)}.\n5. Go to Hold Instructions: Step 2.\n\nHOLD INSTRUCTIONS:\n1. Fly to the fix on CRS {int(in_crs)} with HDG {int(in_crs)}.\n2. Turn Right to HDG {int(out_crs)}.\n3. Fly HDG {int(out_crs)} outbound Equal time to the inbound.\n4. Turn Right and intercept CRS {int(in_crs)}.\n5. Repeat")
            elif -110 <= diff < 0:
                entry_type = "PARALLEL (Sector 1)"
                instructions = (f"ENTRY INSTRUCTIONS:\n1. Fly to the fix and cross it.\n2. Turn to CRS {int(out_crs)} with HDG {int(out_crs)} and fly equal time to the inbound.\n3. Turn Left Past HDG {int(in_crs)}.\n4. Intercept the inbound CRS {int(in_crs)} and fly HDG {int(in_crs)} to the fix.\n5. Go to Hold Instructions: Step 2.\n\nHOLD INSTRUCTIONS:\n1. Fly to the fix on CRS {int(in_crs)} with HDG {int(in_crs)}.\n2. Turn Right to HDG {int(out_crs)}.\n3. Fly HDG {int(out_crs)} outbound Equal time to the inbound.\n4. Turn Right and intercept CRS {int(in_crs)}.\n5. Repeat")
            else:
                entry_type = "DIRECT (Sector 3)"
                instructions = (f"ENTRY INSTRUCTIONS:\n1. Fly to the fix and cross it.\n2. Go to Hold Instructions: Step 2.\n\nHOLD INSTRUCTIONS:\n1. Fly to the fix on CRS {int(in_crs)} with HDG {int(in_crs)}.\n2. Turn Right to HDG {int(out_crs)}.\n3. Fly HDG {int(out_crs)} outbound Equal time to the inbound.\n4. Turn Right and intercept CRS {int(in_crs)}.\n5. Repeat")

        label_hold_res.config(text=f"ENTRY: {entry_type}")
        label_hold_instr.config(text=instructions)
    except:
        messagebox.showerror("Error", "Invalid input!")

# --- UI Setup ---

root = tk.Tk()
root.title("Pilot Assistant - Hasan ÜTEBAY")
root.geometry("450x750")

BG_COLOR, CARD_COLOR, TEXT_COLOR = "#2f3640", "#353b48", "#dcdde1"
ACCENT_BLUE, SUCCESS_GREEN, WARNING_ORANGE = "#3b82f5", "#44bd32", "#fbc531"

root.configure(bg=BG_COLOR)
vcmd = root.register(validate_input)

# Logo & Styles
try:
    original_logo = Image.open(resource_path("logo.png"))
    sig_logo_img = original_logo.resize((48, 48), Image.Resampling.LANCZOS)
    sig_logo_photo = ImageTk.PhotoImage(sig_logo_img)
    root.iconphoto(True, sig_logo_photo)

except: sig_logo_photo = None

style = ttk.Style()
style.theme_use('default')
style.configure("TNotebook", background=BG_COLOR, borderwidth=0)
style.configure("TNotebook.Tab", background=CARD_COLOR, foreground=TEXT_COLOR, padding=[15, 5], font=("Segoe UI", 10, "bold"))
style.map("TNotebook.Tab", background=[("selected", ACCENT_BLUE)], foreground=[("selected", "white")])

notebook = ttk.Notebook(root)
tab_descent = tk.Frame(notebook, bg=BG_COLOR)
tab_holding = tk.Frame(notebook, bg=BG_COLOR)
notebook.add(tab_descent, text=" DESCENT ")
notebook.add(tab_holding, text=" HOLDING ")
notebook.pack(expand=1, fill="both")

lbl_style = {"bg": BG_COLOR, "fg": TEXT_COLOR, "font": ("Segoe UI", 10, "bold")}
ent_style = {"font": ("Segoe UI", 12), "justify": "center", "bg": CARD_COLOR, "fg": "white", "relief": "flat", "validate": "key", "validatecommand": (vcmd, '%P')}

# --- DESCENT UI ---
tk.Label(tab_descent, text="DESCENT COMPUTER", font=("Segoe UI", 20, "bold"), bg=BG_COLOR, fg=ACCENT_BLUE).pack(pady=20)
entry_alt = tk.Entry(tab_descent, **ent_style); entry_alt.insert(0, "10,000"); entry_alt.bind("<FocusOut>", on_focus_out)
tk.Label(tab_descent, text="Current Altitude (ft)", **lbl_style).pack(); entry_alt.pack(pady=5, ipady=8, padx=60, fill="x")
entry_trgt = tk.Entry(tab_descent, **ent_style); entry_trgt.insert(0, "3,000"); entry_trgt.bind("<FocusOut>", on_focus_out)
tk.Label(tab_descent, text="Target Altitude (ft)", **lbl_style).pack(); entry_trgt.pack(pady=5, ipady=8, padx=60, fill="x")
entry_dist = tk.Entry(tab_descent, **ent_style); entry_dist.insert(0, "20")
tk.Label(tab_descent, text="Distance (NM)", **lbl_style).pack(); entry_dist.pack(pady=5, ipady=8, padx=60, fill="x")
entry_gs = tk.Entry(tab_descent, **ent_style); entry_gs.insert(0, "180")
tk.Label(tab_descent, text="Ground Speed (kt)", **lbl_style).pack(); entry_gs.pack(pady=5, ipady=8, padx=60, fill="x")

tk.Button(tab_descent, text="CALCULATE", command=calculate_descent, bg=ACCENT_BLUE, fg="white", font=("Segoe UI", 12, "bold"), bd=0, height=2).pack(pady=20, padx=60, fill="x")
label_net_vs = tk.Label(tab_descent, text="Required Net VS: ---", bg=BG_COLOR, fg="#718093", font=("Segoe UI", 10)); label_net_vs.pack()
label_set_vs = tk.Label(tab_descent, text="SET VS: ---", bg=BG_COLOR, fg=SUCCESS_GREEN, font=("Segoe UI", 18, "bold")); label_set_vs.pack()
label_sugg_dist = tk.Label(tab_descent, text="START AT: ---", bg=BG_COLOR, fg=WARNING_ORANGE, font=("Segoe UI", 14, "bold")); label_sugg_dist.pack()

# --- HOLDING UI ---
tk.Label(tab_holding, text="HOLDING COMPUTER", font=("Segoe UI", 20, "bold"), bg=BG_COLOR, fg=ACCENT_BLUE).pack(pady=20)
ent_hold_hdg = tk.Entry(tab_holding, **ent_style); ent_hold_hdg.insert(0, "180")
tk.Label(tab_holding, text="Aircraft Heading (Deg)", **lbl_style).pack(); ent_hold_hdg.pack(pady=5, ipady=8, padx=60, fill="x")
ent_hold_oc = tk.Entry(tab_holding, **ent_style); ent_hold_oc.insert(0, "360")
tk.Label(tab_holding, text="Outbound Course (Deg)", **lbl_style).pack(); ent_hold_oc.pack(pady=5, ipady=8, padx=60, fill="x")

var_side = tk.StringVar(value="R")
rf = tk.Frame(tab_holding, bg=BG_COLOR); rf.pack(pady=10)
tk.Radiobutton(rf, text="Right (Std)", variable=var_side, value="R", bg=BG_COLOR, fg="white", selectcolor=CARD_COLOR).pack(side="left", padx=10)
tk.Radiobutton(rf, text="Left (Non-Std)", variable=var_side, value="L", bg=BG_COLOR, fg="white", selectcolor=CARD_COLOR).pack(side="left", padx=10)

tk.Button(tab_holding, text="ANALYZE HOLDING", command=calculate_holding, bg=ACCENT_BLUE, fg="white", font=("Segoe UI", 12, "bold"), bd=0, height=2).pack(pady=20, padx=60, fill="x")
label_hold_res = tk.Label(tab_holding, text="ENTRY: ---", bg=BG_COLOR, fg=SUCCESS_GREEN, font=("Segoe UI", 14, "bold")); label_hold_res.pack()
label_hold_instr = tk.Label(tab_holding, text="Instructions waiting...", bg=BG_COLOR, fg=WARNING_ORANGE, font=("Consolas", 9), justify="left", wraplength=350); label_hold_instr.pack(pady=10)

# --- Hasan ÜTEBAY Signature (Footer) ---
sig_frame = tk.Frame(root, bg=BG_COLOR)
sig_frame.pack(side="bottom", pady=20)
if sig_logo_photo:
    tk.Label(sig_frame, image=sig_logo_photo, bg=BG_COLOR).pack(side="left")
tk.Label(sig_frame, text="HASAN", font=("Segoe UI", 18, "bold", "italic"), bg=BG_COLOR, fg="white").pack(side="left")
tk.Label(sig_frame, text="ÜTEBAY", font=("Segoe UI", 18, "bold", "italic"), bg=BG_COLOR, fg=ACCENT_BLUE).pack(side="left")

root.mainloop()