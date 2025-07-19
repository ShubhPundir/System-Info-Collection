import tkinter as tk
from tkinter import scrolledtext
from datetime import datetime
from monitor.startup_checker import hash_data, print_diff
from system_info.collector import collect_system_info
from monitor.state_manager import load_previous_state, save_current_state

def get_config_diff_summary(old, new):
    """Returns a textual diff summary between two dicts"""
    changes = []
    for key in new:
        if old.get(key) != new[key]:
            changes.append(f"[CHANGED] {key}:\n    FROM: {old.get(key)}\n    TO:   {new[key]}")
    for key in old:
        if key not in new:
            changes.append(f"[REMOVED] {key}")
    for key in new:
        if key not in old:
            changes.append(f"[NEW] {key}: {new[key]}")
    return "\n".join(changes) if changes else "No changes detected."

def run_gui_check(display):
    previous_info = load_previous_state()
    current_info = collect_system_info()

    old_hash = hash_data(previous_info)
    new_hash = hash_data(current_info)

    display.config(state='normal')
    display.delete(1.0, tk.END)
    display.insert(tk.END, f"Last Checked: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

    if new_hash != old_hash:
        changes = get_config_diff_summary(previous_info, current_info)
        display.insert(tk.END, changes)
        save_current_state(current_info)
    else:
        display.insert(tk.END, "No changes detected.")
    
    display.config(state='disabled')

def main():
    root = tk.Tk()
    root.title("System Info Checker")
    root.geometry("600x400")
    root.resizable(False, False)

    tk.Label(root, text="System Configuration Checker", font=("Segoe UI", 14, "bold")).pack(pady=10)

    check_button = tk.Button(
        root,
        text="Run System Info Check",
        font=("Segoe UI", 12),
        command=lambda: run_gui_check(display)
    )
    check_button.pack(pady=10)

    display = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Consolas", 10), width=70, height=15)
    display.pack(padx=10, pady=10)
    display.config(state='disabled')

    root.mainloop()

if __name__ == "__main__":
    main()
