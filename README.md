<img width="1275" height="294" alt="image" src="https://github.com/user-attachments/assets/af65c450-2b51-4e96-b890-02a7d61f144f" />

# Frameless-BenjiClock-HUD-Gaming-clock
rameless, draggable, resizable, auto-fit fonts, customizable colors and fonts, "always-on-top"
# BenjiClock HUD ⏱️

A **frameless, floating desktop clock** built with Tkinter.  
- Solid black background, **always on top**  
- **Drag anywhere** to move  
- Bottom-right **resize grip**  
- **Auto-fit fonts** so time/date never clip  
- Right-click for **themes** and **font family** switch

<img width="1281" height="719" alt="image" src="https://github.com/user-attachments/assets/4ad6b67e-10f6-4bb0-8f6d-e33155155f30" />


## ✨ Features
- Minimal **HUD-style** window (`overrideredirect(True)`)
- **Small by default** (`280x140`) but resizable
- Cross-platform drag & resize
- Live **time** (`HH:MM:SS`) and **date** (`Weekday, DD Month YYYY`)
- Customizable **themes** (colors) and **font families**

## 🧰 Tech
- Python 3.x
- Tkinter

## 🚀 Run locally
```bash
cd src
python clock.py

py -m pip install --upgrade pip
py -m pip install pyinstaller

py -m PyInstaller `
  --name "BenjiClockHUD" `
  --onefile `
  --windowed `
  --noconfirm `
  --icon assets\app.ico `
  --add-data "assets\app.ico;assets" `
  src\clock.py

