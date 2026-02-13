import tkinter as tk
from tkinter import messagebox, scrolledtext
import random
import hashlib
import pyperclip
import os
import threading
import time

# --- VERSION CONTROL ---
VERSION = "v0.93a"
# -----------------------

DECOY_INPUT = [
    "STRING !!!", "STRING ERROR", "BACKSPACE", "SPACE", "STRING TOAST",
    "STRING 3.14", "STRING 15926", "STRING 26535", "STRING 89793","STRING 23846",
    "STRING 26433", "STRING 83279", "STRING 50288", "LEFT_ARROW", "RIGHT_ARROW"
]

DECOY_PHRASES = [
    "Checking system thermal offset...", "Validating HID descriptor...",
    "Polling interrupt request buffer...", "Syncing registry hive fragment...",
    "Refreshing local policy objects...",     "Depointilizing the spectral bands...",
    "Refabricating the intangible...", "Refreshing my coffee...",
    "Deflarping the shadow quadrant...", "DO NOT ALTER CODE BEFORE THIS POINT!...",
    "DO NOT ALTER CODE AFTER THIS POINT!...", "The next two lines of code should NEVER BE READ ALOUD!..."
]

def self_destruct_file(filename, delay=30):
    time.sleep(delay)
    if os.path.exists(filename):
        os.remove(filename)

def limit_char_input(P):
    length = len(P)
    counter_label.config(text=f"BUFFER: {length}/128")
    alt_slider.config(to=max(length, 1))
    
    if length >= 128:
        counter_label.config(fg="#FF0000")
    elif length > 100:
        counter_label.config(fg="#FFFF00")
    else:
        counter_label.config(fg="#00FF00")
    return length <= 128

def generate_ducky_script():
    original_string = entry_var.get()
    if not original_string:
        messagebox.showwarning("Warning", "Please enter a string first.")
        return
    
    alt_count = alt_slider.get()
    decoy_chance = decoy_slider.get() / 100.0
    
    total_est_ms = 5000 
    ducky_lines = [
        f"REM -- System Diagnostic Tool {VERSION} --",
        "REM -- Authorized Personnel Only --",
        "DELAY 5000"
    ]
    
    reconstructed_string = ""
    indices = list(range(len(original_string)))
    alt_indices = random.sample(indices, min(alt_count, len(indices)))

    for i, char in enumerate(original_string):
        # Random Flavor REM
        if random.random() > 0.9:
            ducky_lines.append(f"REM {random.choice(DECOY_PHRASES)}")
        
        # Inject Decoy (Hash Sabotage)
        if random.random() < decoy_chance:
            selection = random.choice(DECOY_INPUT)
            d_delay = random.randint(50, 100)
            ducky_lines.append(selection)
            ducky_lines.append(f"DELAY {d_delay}")
            total_est_ms += d_delay
            reconstructed_string += f"[{selection.replace('STRING ', '')}]"

        # Character Translation
        if i in alt_indices:
            ascii_val = ord(char)
            ducky_lines.append(f"ALTCODE {ascii_val}")
            reconstructed_string += chr(ascii_val)
        else:
            ducky_lines.append(f"STRING {char}")
            reconstructed_string += char
        
        char_delay = random.randint(20, 80)
        ducky_lines.append(f"DELAY {char_delay}")
        total_est_ms += char_delay

    reconstructed_var.set(reconstructed_string)
    time_label.config(text=f"EST. EXECUTION TIME: {total_est_ms/1000:.2f}s")
    
    console_preview.config(state="normal")
    console_preview.delete('1.0', tk.END)
    console_preview.insert(tk.END, "\n".join(ducky_lines))
    console_preview.config(state="disabled")

    full_script = "\n".join(ducky_lines)
    filename = "payload.txt"

    try:
        with open(filename, "w") as f:
            f.write(full_script)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save file: {e}")
        return

    original_hash = hashlib.sha256(original_string.encode()).hexdigest()
    reconstructed_hash = hashlib.sha256(reconstructed_string.encode()).hexdigest()

    if original_hash == reconstructed_hash:
        status_label.config(text=f"HASH MATCH: {reconstructed_hash[:32]}", foreground="#00FF00")
        pyperclip.copy("") 
        threading.Thread(target=self_destruct_file, args=(filename,), daemon=True).start()
    else:
        status_label.config(text="HASH MISMATCH: DECOYS ACTIVE", foreground="#FF0000")

# --- UI Setup ---
root = tk.Tk()
root.title(f"Flipper PW Obfuscator Pro {VERSION}")
root.geometry("1000x850")
root.configure(bg="#121212")

MONO_FONT = ("Terminal", 12)
vcmd = (root.register(limit_char_input), '%P')

header_frame = tk.Frame(root, bg="#121212")
header_frame.pack(pady=(20, 0), fill="x", padx=100)
tk.Label(header_frame, text="TARGET STRING:", font=("Terminal", 10, "bold"), bg="#121212", fg="#FFFFFF").pack(side="left")
counter_label = tk.Label(header_frame, text="BUFFER: 0/128", font=("Terminal", 10, "bold"), bg="#121212", fg="#00FF00")
counter_label.pack(side="right")

entry_var = tk.StringVar()
entry = tk.Entry(root, textvariable=entry_var, width=80, font=MONO_FONT, bg="#000000", fg="#FFFFFF", insertbackground="white", validate="key", validatecommand=vcmd)
entry.pack(pady=10)

alt_slider = tk.Scale(root, label="ALT CODE DENSITY", from_=0, to=1, orient="horizontal", length=600, bg="#121212", fg="#FFFFFF", highlightthickness=0, troughcolor="#333333", font=("Terminal", 10))
alt_slider.pack()

decoy_slider = tk.Scale(root, label="DECOY PROBABILITY (%)", from_=0, to=100, orient="horizontal", length=600, bg="#121212", fg="#FFFFFF", highlightthickness=0, troughcolor="#333333", font=("Terminal", 10))
decoy_slider.pack(pady=10)

time_label = tk.Label(root, text="EST. EXECUTION TIME: 0.00s", font=("Terminal", 10), bg="#121212", fg="#00FFFF")
time_label.pack(pady=5)

btn = tk.Button(root, text="GENERATE & VALIDATE", command=generate_ducky_script, bg="#660000", fg="white", font=("Terminal", 12, "bold"), height=2, width=40)
btn.pack(pady=10)

status_label = tk.Label(root, text="Status: Ready", font=("Terminal", 11, "bold"), bg="#121212", fg="#FFFFFF")
status_label.pack()

tk.Label(root, text="PAYLOAD PREVIEW:", font=("Terminal", 10, "bold"), bg="#121212", fg="#FFFFFF").pack(pady=(15, 0))
console_preview = scrolledtext.ScrolledText(root, width=90, height=12, font=("Terminal", 10), bg="#000000", fg="#00FF00", state="disabled")
console_preview.pack(pady=5)

reconstructed_var = tk.StringVar()
tk.Entry(root, textvariable=reconstructed_var, width=135, font=("Terminal", 8), bg="#121212", fg="#333333", state="readonly", borderwidth=0).pack(side="bottom")

root.mainloop()
