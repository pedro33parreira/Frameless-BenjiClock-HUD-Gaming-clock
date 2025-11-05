import tkinter as tk
from tkinter import font as tkfont
from datetime import datetime
import os, sys

# (Optional) PyInstaller-friendly asset helper
def asset_path(rel):
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, "assets", rel)

# Themes
THEMES = {
    "Cyber Green":   {"time": "lime",     "date": "red"},
    "Amber":         {"time": "#ffbf00",  "date": "#ff6a00"},
    "Electric Blue": {"time": "#00d0ff",  "date": "#0096ff"},
    "Classic White": {"time": "white",    "date": "white"},
}

# App (frameless HUD)
root = tk.Tk()
root.title("BenjiClock HUD")
root.configure(bg="black")
root.attributes("-topmost", True)
root.overrideredirect(True)            # frameless
root.geometry("280x140+100+100")       # starts small
MIN_W, MIN_H = 200, 100

# Optional icon
try:
    root.iconbitmap(asset_path("app.ico"))
except Exception:
    pass

# Drag to move (absolute offset)
_drag_offset = {"x": 0, "y": 0}
def start_drag(e):
    _drag_offset["x"], _drag_offset["y"] = e.x, e.y
def do_drag(e):
    root.geometry(f"+{e.x_root - _drag_offset['x']}+{e.y_root - _drag_offset['y']}")

# Container
container = tk.Frame(root, bg="black", bd=0, highlightthickness=0)
container.pack(fill="both", expand=True, padx=10, pady=10)

# Bind drag on background & labels (not the grip)
for w in (root, container):
    w.bind("<ButtonPress-1>", start_drag)
    w.bind("<B1-Motion>", do_drag)

# State
current_theme    = tk.StringVar(value="Cyber Green")
time_font_family = tk.StringVar(value="DS-Digital")
info_font_family = tk.StringVar(value="Helvetica")

# Labels
label_time = tk.Label(container, bg="black")
label_time.pack(anchor="center", pady=(2, 0), expand=True)

label_date = tk.Label(container, bg="black")
label_date.pack(anchor="center", pady=(0, 2))

for w in (label_time, label_date):
    w.bind("<ButtonPress-1>", start_drag)
    w.bind("<B1-Motion>", do_drag)

# Resize grip
grip = tk.Frame(container, bg="black", cursor="bottom_right_corner", width=12, height=12)
grip.pack(side="right", anchor="se")

_resize = {"x": 0, "y": 0, "w": 0, "h": 0}
def start_resize(e):
    _resize.update(x=e.x_root, y=e.y_root, w=root.winfo_width(), h=root.winfo_height())
def do_resize(e):
    dw, dh = e.x_root - _resize["x"], e.y_root - _resize["y"]
    new_w = max(MIN_W, _resize["w"] + dw)
    new_h = max(MIN_H, _resize["h"] + dh)
    root.geometry(f"{new_w}x{new_h}+{root.winfo_x()}+{root.winfo_y()}")

grip.bind("<ButtonPress-1>", start_resize)
grip.bind("<B1-Motion>", do_resize)

# Theme & Fonts
def apply_theme(name=None):
    name = name or current_theme.get()
    theme = THEMES[name]
    label_time.config(fg=theme["time"])
    label_date.config(fg=theme["date"])
    current_theme.set(name)

def fit_font(label, family, text, max_w, max_h, min_size=8, max_size=200):
    if max_w <= 1 or max_h <= 1:
        return min_size
    lo, hi = min_size, max_size
    best = lo
    while lo <= hi:
        mid = (lo + hi) // 2
        f = tkfont.Font(family=family, size=mid)
        w = f.measure(text)
        h = f.metrics("ascent") + f.metrics("descent")
        if w <= max_w and h <= max_h:
            best = mid
            lo = mid + 1
        else:
            hi = mid - 1
    return best

def refresh_fonts():
    container.update_idletasks()
    cw = max(1, container.winfo_width()  - 8)
    ch = max(1, container.winfo_height() - 8)
    time_h = int(ch * 0.60)
    date_h = int(ch * 0.25)
    time_sample = "88:88:88"
    date_sample = label_date.cget("text") or "Wednesday, 05 November 2025"
    # Use selected families
    time_sz = fit_font(label_time, time_font_family.get(), time_sample, cw, time_h, 8, 300)
    date_sz = fit_font(label_date, info_font_family.get(),  date_sample, cw, date_h, 8, 120)
    label_time.config(font=(time_font_family.get(), time_sz))
    label_date.config(font=(info_font_family.get(), date_sz))

def on_resize(_=None):
    refresh_fonts()

root.bind("<Configure>", on_resize)

def _set_time_font(fam):
    time_font_family.set(fam)
    refresh_fonts()

def _set_info_font(fam):
    info_font_family.set(fam)
    refresh_fonts()

# Context Menu
menu = tk.Menu(root, tearoff=0, bg="#1e1e1e", fg="white",
               activebackground="#333", activeforeground="white")

theme_menu = tk.Menu(menu, tearoff=0, bg="#1e1e1e", fg="white",
                     activebackground="#333", activeforeground="white")
for name in THEMES:
    theme_menu.add_radiobutton(label=name, variable=current_theme, value=name,
                               command=lambda n=name: apply_theme(n))
menu.add_cascade(label="Theme", menu=theme_menu)

time_font_menu = tk.Menu(menu, tearoff=0, bg="#1e1e1e", fg="white",
                         activebackground="#333", activeforeground="white")
for fam, label in [("DS-Digital","Digital (DS-Digital)"),
                   ("Consolas","Monospace (Consolas)"),
                   ("Courier New","Monospace (Courier New)"),
                   ("Helvetica","Sans (Helvetica)"),
                   ("Arial","Sans (Arial)")]:
    time_font_menu.add_radiobutton(label=label, value=fam,
                                   command=lambda f=fam: _set_time_font(f))
menu.add_cascade(label="Time Font", menu=time_font_menu)

info_font_menu = tk.Menu(menu, tearoff=0, bg="#1e1e1e", fg="white",
                         activebackground="#333", activeforeground="white")
for fam, label in [("Helvetica","Sans (Helvetica)"),
                   ("Arial","Sans (Arial)"),
                   ("Consolas","Monospace (Consolas)"),
                   ("Courier New","Monospace (Courier New)"),
                   ("DS-Digital","Digital (DS-Digital)")]:
    info_font_menu.add_radiobutton(label=label, value=fam,
                                   command=lambda f=fam: _set_info_font(f))
menu.add_cascade(label="Info Font", menu=info_font_menu)

menu.add_separator()
menu.add_command(label="Quit (Esc / Ctrl+Q)", command=root.destroy)

def show_menu(e):
    try:
        menu.tk_popup(e.x_root, e.y_root)
    finally:
        menu.grab_release()

for w in (root, container, label_time, label_date, grip):
    w.bind("<Button-3>", show_menu)
    w.bind("<Button-2>", show_menu)

# Shortcuts
root.bind("<Escape>",    lambda e: root.destroy())
root.bind("<Control-q>", lambda e: root.destroy())

# Clock Loop
def update_time():
    now = datetime.now()
    label_time.config(text=now.strftime("%H:%M:%S"))
    label_date.config(text=now.strftime("%A, %d %B %Y"))
    refresh_fonts()
    root.after(200, update_time)

# Init
apply_theme("Cyber Green")
refresh_fonts()
update_time()
root.mainloop()
