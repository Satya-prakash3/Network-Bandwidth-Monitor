import psutil
import time
import threading
import tkinter as tk
import os

CONFIG_FILE = "config.json"

if os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE, "r") as file:
        selected_unit = file.read().strip()
else:
    selected_unit = "KBps"
    with open(CONFIG_FILE, "w") as file:
        file.write(selected_unit)

VALID_UNITS = ["Kbps", "Mbps", "Gbps", "KBps", "MBps", "GBps"]
if selected_unit not in VALID_UNITS:
    selected_unit = "KBps" 


def get_speed(unit="KBps"):
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
        down, up = get_speed(selected_unit)
        download_label.config(text=f"↓ {down:.2f} {selected_unit}")
        upload_label.config(text=f"↑ {up:.2f} {selected_unit}")
        time.sleep(1)


def on_press(event):
    global start_x, start_y
    start_x = event.x
    start_y = event.y

def on_drag(event):
    x = root.winfo_x() + (event.x - start_x)
    y = root.winfo_y() + (event.y - start_y)
    root.geometry(f"+{x}+{y}")


root = tk.Tk()
root.title("Floating Net Speed Monitor")
root.geometry("200x50")
root.attributes("-topmost", True)   
root.attributes("-alpha", 0.7)     
root.configure(bg="black")
root.overrideredirect(True)        

download_label = tk.Label(root, text="↓ 0.00 KBps", font=("Arial", 12, "bold"), fg="white", bg="black")
download_label.pack()

upload_label = tk.Label(root, text="↑ 0.00 KBps", font=("Arial", 12, "bold"), fg="white", bg="black")
upload_label.pack()

root.bind("<ButtonPress-1>", on_press)
root.bind("<B1-Motion>", on_drag)

thread = threading.Thread(target=update_speed, daemon=True)
thread.start()

try:
    root.mainloop()
except KeyboardInterrupt:
    print("\nMonitoring Ended by User.")
