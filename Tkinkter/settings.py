import json
import tkinter as tk
from tkinter import colorchooser, ttk

CONFIG_FILE = "config.json"

def load_config():
    default_config = {
        "unit": "KBps",
        "text_color": "#FFFFFF",
        "background_opacity": 0.7
    }
    try:
        with open(CONFIG_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        with open(CONFIG_FILE, "w") as file:
            json.dump(default_config, file)
        return default_config

config = load_config()

def save_config(update_ui_callback):
    with open(CONFIG_FILE, "w") as file:
        json.dump(config, file)
    update_ui_callback() 

def open_settings(root, update_ui_callback):
    settings_win = tk.Toplevel(root)
    settings_win.title("Settings")
    settings_win.geometry("300x250")
    settings_win.configure(bg="#2C2F33")  
    settings_win.resizable(False, False)

    tk.Label(settings_win, text="Settings", font=("Arial", 14, "bold"), fg="white", bg="#2C2F33").pack(pady=10)

    tk.Label(settings_win, text="Select Unit:", fg="white", bg="#2C2F33").pack()
    unit_var = tk.StringVar(value=config["unit"])
    unit_dropdown = ttk.Combobox(settings_win, textvariable=unit_var, values=["Kbps", "Mbps", "Gbps", "KBps", "MBps", "GBps"])
    unit_dropdown.pack(pady=5)

    def choose_text_color():
        color = colorchooser.askcolor(title="Pick Text Color")[1]
        if color:
            config["text_color"] = color
            save_config(update_ui_callback)

    tk.Button(settings_win, text="Change Text Color", command=choose_text_color, bg="#7289DA", fg="white").pack(pady=5)

    tk.Label(settings_win, text="Background Opacity:", fg="white", bg="#2C2F33").pack()
    opacity_slider = tk.Scale(settings_win, from_=0.1, to=1.0, resolution=0.1, orient="horizontal", bg="#2C2F33", fg="white")
    opacity_slider.set(config["background_opacity"])
    opacity_slider.pack(pady=5)

    def save_settings():
        config["unit"] = unit_var.get()
        config["background_opacity"] = opacity_slider.get()
        save_config(update_ui_callback)
        settings_win.destroy()

    tk.Button(settings_win, text="Save Settings", command=save_settings, bg="#43B581", fg="white").pack(pady=10)
