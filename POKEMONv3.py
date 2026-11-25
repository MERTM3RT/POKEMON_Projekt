import io
import tkinter as tk
from PIL import Image, ImageTk
import requests



def pokemon_suchen(event=None):
    pokemon_name = entry.get().strip().lower()
    if not pokemon_name:
        return

    # URL für das spezifische Pokémon zusammenbauen
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}"

    try:
        # Abrufen der Daten und Umwandeln von JSON in ein Python-Dictionary
        data = requests.get(url).json()

        # Text für die Anzeige vorbereiten
        name_str = f"Name: {data['name'].capitalize()}"
        groesse_str = f"Größe: {data['height']}"
        gewicht_str = f"Gewicht: {data['weight']}"

        ergebnis_text = f"{name_str}\n{groesse_str}\n{gewicht_str}"
        label_ergebnis.config(text=ergebnis_text, fg="#2B2D42")

        # Bild von der API laden (falls Pillow installiert ist)
        bild_url = data["sprites"]["front_default"]
        if bild_url:
            bild_daten = requests.get(bild_url).content
            img = Image.open(io.BytesIO(bild_daten))
            img = img.resize((167, 167), Image.Resampling.NEAREST)
            global pokemon_img
            pokemon_img = ImageTk.PhotoImage(img)
            label_bild.config(image=pokemon_img)
        else:
            label_bild.config(image="")

    except Exception:
        label_ergebnis.config(text="Fehler: Pokémon\nnicht gefunden!", fg="#D90429")
        label_bild.config(image="")


# --- Hauptfenster (Das große Pokédex-Layout) ---
root = tk.Tk()
root.title("Pokédex")
root.geometry("420x550")
root.configure(bg="#CC0000")  # Pokédex-Rot
root.resizable(False, False)


# 1. OBERE LEISTE (Großes blaues Licht + 3 LEDs)
top_frame = tk.Frame(root, bg="#CC0000", height=60)
top_frame.pack(fill="x", padx=20, pady=12)

# Großes blaues Licht
blue_light = tk.Canvas(top_frame, width=42, height=42, bg="#CC0000", highlightthickness=0)
blue_light.pack(side="left")
blue_light.create_oval(2, 2, 40, 40, fill="#00ffff", outline="#004444", width=3)
blue_light.create_oval(10, 10, 18, 18, fill="white", outline="")  # Glanzpunkt

# 3 kleine LEDs (Rot, Gelb, Grün)
led_frame = tk.Frame(top_frame, bg="#CC0000")
led_frame.pack(side="left", padx=15)

for color, outline_col in [("#FF3333", "#990000"), ("#FFCC00", "#996600"), ("#33CC33", "#006600")]:
    c = tk.Canvas(led_frame, width=12, height=12, bg="#CC0000", highlightthickness=0)
    c.create_oval(1, 1, 11, 11, fill=color, outline=outline_col)
    c.pack(side="left", padx=3)


# 2. DER BILDSCHIRM (Grauer Rahmen, heller Innenbereich, rote Knöpfe & Linien)
screen_outer = tk.Frame(root, bg="#888888", bd=5, relief="sunken")
screen_outer.pack(padx=20, pady=5, fill="both")

screen_inner = tk.Frame(screen_outer, bg="#EAEAEA", padx=12, pady=12)
screen_inner.pack(fill="both", expand=True)

# Zwei kleine rote Knöpfe oben auf dem Bildschirm-Rahmen (wie auf dem Bild)
screen_dots_frame = tk.Frame(screen_inner, bg="#EAEAEA")
screen_dots_frame.pack(anchor="center", pady=(0, 8))
for _ in range(2):
    dot = tk.Canvas(screen_dots_frame, width=8, height=8, bg="#EAEAEA", highlightthickness=0)
    dot.create_oval(0, 0, 8, 8, fill="#CC0000", outline="")
    dot.pack(side="left", padx=6)

# Inhalt im Bildschirm (Links Bild, Rechts Text)
content_pane = tk.Frame(screen_inner, bg="#EAEAEA")
content_pane.pack(fill="both", expand=True)

label_bild = tk.Label(content_pane, bg="#EAEAEA")
label_bild.pack(side="left", padx=5)

label_ergebnis = tk.Label(
    content_pane, 
    text="Gib einen Namen ein\nund drücke Suchen.", 
    font=("Courier New", 11, "bold"), 
    bg="#EAEAEA", 
    fg="#2B2D42", 
    justify="left"
)
label_ergebnis.pack(side="left", padx=10)

# Lüftungsschlitze unten rechts im Bildschirm (4 kleine graue Striche)
vents_frame = tk.Frame(screen_inner, bg="#EAEAEA")
vents_frame.pack(anchor="e", pady=(5, 0))
for _ in range(4):
    v = tk.Frame(vents_frame, bg="#999999", width=18, height=3)
    v.pack(side="right", padx=2)


# 3. UNTERE STEUERUNG (Schwarzer Knopf, Leisten, grünes Display & Steuerkreuz)
control_frame = tk.Frame(root, bg="#CC0000")
control_frame.pack(pady=15, padx=20, fill="both")

# Obere Reihe der Steuerung (Schwarzer runder Knopf links + zwei farbige Status-Balken)
row1_frame = tk.Frame(control_frame, bg="#CC0000")
row1_frame.pack(fill="x", pady=(0, 10))

# Schwarzer runder Knopf
btn_black = tk.Canvas(row1_frame, width=28, height=28, bg="#CC0000", highlightthickness=0)
btn_black.create_oval(2, 2, 26, 26, fill="#111111", outline="#000000")
btn_black.pack(side="left", padx=(5, 15))

# Zwei kleine Linien-Balken (Rot und Blau)
bar_red = tk.Frame(row1_frame, bg="#CC3333", width=25, height=6)
bar_red.pack(side="left", padx=3)
bar_blue = tk.Frame(row1_frame, bg="#3366CC", width=25, height=6)
bar_blue.pack(side="left", padx=3)


# Untere Reihe der Steuerung (Grünes kleines Display links + Steuerkreuz rechts)
row2_frame = tk.Frame(control_frame, bg="#CC0000")
row2_frame.pack(fill="x")

# Grünes Display (Retro-Look)
green_display = tk.Frame(row2_frame, bg="#336633", bd=2, relief="sunken", width=75, height=40)
green_display.pack(side="left", padx=(0, 20))
green_display.pack_propagate(False)
tk.Label(green_display, text="Pokedex", font=("Courier New", 8, "bold"), bg="#336633", fg="#A3FFA3").pack(expand=True)

# Steuerkreuz (D-Pad)
dpad = tk.Canvas(row2_frame, width=75, height=75, bg="#CC0000", highlightthickness=0)
dpad.pack(side="left")
dpad.create_rectangle(27, 5, 48, 70, fill="#111111", outline="")  # Senkrechter Balken
dpad.create_rectangle(5, 27, 70, 48, fill="#111111", outline="")  # Waagerechter Balken
dpad.create_oval(32, 32, 43, 43, fill="#222222", outline="")   # Mitte des Kreuzes


# 4. SUCHLEISTE & BUTTON (Integriert als Bedienelement unten)
search_frame = tk.Frame(root, bg="#CC0000")
search_frame.pack(pady=10, padx=20, fill="x")

entry = tk.Entry(search_frame, font=("Arial", 12), width=14, relief="flat", justify="center")
entry.pack(side="left", ipady=5, padx=(0, 10))
entry.insert(0, "pikachu")
entry.bind("<Return>", pokemon_suchen)

btn = tk.Button(
    search_frame, 
    text="Suchen", 
    font=("Arial", 10, "bold"), 
    bg="#2B2D42", 
    fg="white", 
    activebackground="#1D1E2C",
    activeforeground="white",
    relief="raised", 
    bd=3,
    cursor="hand2", 
    command=pokemon_suchen
)
btn.pack(side="left", ipady=3, ipadx=8, fill="x", expand=True)

# Direkt beim Start Pikachu laden
pokemon_suchen()

root.mainloop()