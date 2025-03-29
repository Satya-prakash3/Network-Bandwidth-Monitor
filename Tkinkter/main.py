import os
import time
import psutil
import threading
import tkinter as tk
from settings import open_settings, load_config # If import is throwing error try the commented one(while running locally)
from Tkinkter.settings import open_settings, load_config # use this (While running the exe)

config = load_config()

def get_speed():
    unit = config["unit"]
    units = {
        "Kbps": 1024, "Mbps": 1024**2, "Gbps": 1024**3,
        "KBps": 1024, "MBps": 1024**2, "GBps": 1024**3
    }
    divisor = units.get(unit, 1024)

    old_data = psutil.net_io_counters()
    time.sleep(1)
    new_data = psutil.net_io_counters()

    if unit in ["Kbps", "Mbps", "Gbps"]:
        download_speed = ((new_data.bytes_recv - old_data.bytes_recv) * 8) / divisor
        upload_speed = ((new_data.bytes_sent - old_data.bytes_sent) * 8) / divisor
    else:
        download_speed = (new_data.bytes_recv - old_data.bytes_recv) / divisor
        upload_speed = (new_data.bytes_sent - old_data.bytes_sent) / divisor

    return round(download_speed, 2), round(upload_speed, 2)

def update_speed():
    while True:
        down, up = get_speed()
        download_label.config(text=f"↓ {down:.2f} {config['unit']}", fg=config["text_color"])
        upload_label.config(text=f"↑ {up:.2f} {config['unit']}", fg=config["text_color"])
        time.sleep(1)

def update_ui():
    global config
    config = load_config()  # Reload updated settings
    root.attributes("-alpha", config["background_opacity"])  # Apply opacity
    download_label.config(fg=config["text_color"])
    upload_label.config(fg=config["text_color"])

def on_press(event):
    global start_x, start_y
    start_x = event.x
    start_y = event.y

def on_drag(event):
    x = root.winfo_x() + (event.x - start_x)
    y = root.winfo_y() + (event.y - start_y)
    root.geometry(f"+{x}+{y}")

def show_context_menu(event):
    context_menu.tk_popup(event.x_root, event.y_root)

root = tk.Tk()
root.title("Floating Net Speed Monitor")
root.geometry("200x60")
root.attributes("-topmost", True)
root.attributes("-alpha", config["background_opacity"])  # Apply user-defined opacity
root.configure(bg="black")
root.overrideredirect(True)

download_label = tk.Label(root, text="↓ 0.00 KBps", font=("Arial", 12, "bold"), fg=config["text_color"], bg="black")
download_label.pack()

upload_label = tk.Label(root, text="↑ 0.00 KBps", font=("Arial", 12, "bold"), fg=config["text_color"], bg="black")
upload_label.pack()

# Context menu (Right-click)
context_menu = tk.Menu(root, tearoff=0)
context_menu.add_command(label="Settings", command=lambda: open_settings(root, update_ui))
context_menu.add_command(label="Close", command=root.quit)

root.bind("<ButtonPress-1>", on_press)
root.bind("<B1-Motion>", on_drag)
root.bind("<Button-3>", show_context_menu)  # Right-click to open menu

# Start speed monitoring thread
thread = threading.Thread(target=update_speed, daemon=True)
thread.start()

try:
    root.mainloop()
except KeyboardInterrupt:
    print("\nMonitoring Ended by User.")
