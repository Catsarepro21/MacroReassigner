import tkinter as tk
import json
from pathlib import Path
from tkinter import simpledialog, messagebox, filedialog


config_path = Path(__file__).with_name("macros.json")

with config_path.open("r", encoding="utf-8-sig") as file:
    config = json.load(file)

config.setdefault("encoders", [
    [
        {"type": "shortcut", "key": "VOLU"},
        {"type": "shortcut", "key": "VOLD"},
        {"type": "shortcut", "key": "MUTE"}
    ],
    [
        {"type": "shortcut", "key": "PGUP"},
        {"type": "shortcut", "key": "PGDN"},
        {"type": "shortcut", "key": "MEDIA_PLAY_PAUSE"}
    ]
])

def edit_action(actions, index):
    action_type = simpledialog.askstring(
        "Action type",
        "Enter 'text' to type text, or 'shortcut' for a key combination:",
        parent=root
    )

    if action_type is None:
        return

    action_type = action_type.strip().lower()

    if action_type == "text":
        text = simpledialog.askstring(
            "Text macro",
            "What should this control type?",
            parent=root
        )

        if text is None:
            return

        press_enter = messagebox.askyesno(
            "Press Enter?",
            "Press Enter after typing the text?",
            parent=root
        )

        actions[index] = {
            "type": "text",
            "value": text,
            "enter": press_enter
        }

        messagebox.showinfo(
            "Assignment updated",
            "Text macro updated. Click Apply to Macropad to save.",
            parent=root
        )
        return

    if action_type != "shortcut":
        messagebox.showerror(
            "Invalid type",
            "Enter either text or shortcut.",
            parent=root
        )
        return
    answer = simpledialog.askstring(
        "Assign Shortcut",
        "Enter a KMK key name(Like SPACE or MUTE or F5)",
        parent=root
    )

    if answer is None or not answer.strip():
        return

    modifiers = simpledialog.askstring(
        "Modifiers",
        "Enter modifiers seperated by commas .\n"
        "Examples: LCTL, LSFT, LALT, LGUI",
        parent=root
    )
    if modifiers is None:
        return

    mods = [
        item.strip().upper()
        for item in modifiers.split(",")
        if item.strip()
    ]

    if any(mod not in ("LCTL", "LSFT", "LALT", "LGUI") for mod in mods):
        messagebox.showerror("Invalid modifier", "Use the listed modifier names.")
        return

    actions[index] = {
        "type": "shortcut",
        "key": answer.strip().upper(),
        "mods": mods
    }
    messagebox.showinfo(
    "Updated Macro Assignment",
    "Not yet saved to RP")

def save_config():
    folder = filedialog.askdirectory(
        title="Select your CIRCUITPY drive",
        parent=root
    )

    if not folder:
        return

    destination = Path(folder) / "macros.json"

    if not (Path(folder) / "boot_out.txt").exists():
        messagebox.showerror(
            "Wrong folder",
            "Select the root of your CIRCUITPY drive."
        )
        return

    try:
        data = json.dumps(config, indent=2)
        destination.write_text(data, encoding="utf-8")
        config_path.write_text(data, encoding="utf-8")
    except OSError as error:
        messagebox.showerror("Save failed", str(error))
        return

    messagebox.showinfo(
        "Saved",
        "Assignments saved."
    )

config.setdefault("hardware", {
    "row_pins": ["D7", "D10"],
    "col_pins": ["D9", "D8", "D6"],
    "diode_orientation": "ROW2COL",
    "encoder_pins": [
        ["D0", "D1", "D2"],
        ["D3", "D4", "D5"]
    ]
})


def edit_pins():
    hardware = config["hardware"]
    updated = {}

    fields = [
        ("row_pins", "Row pins", 2),
        ("col_pins", "Column pins", 3)
    ]

    for name, label, count in fields:
        answer = simpledialog.askstring(
            "Wiring settings",
            f"{label}: enter {count} names separated by commas",
            initialvalue=", ".join(hardware[name]),
            parent=root
        )

        if answer is None:
            return

        pins = [pin.strip() for pin in answer.split(",")]

        if len(pins) != count or any(not pin.isidentifier() for pin in pins):
            messagebox.showerror(
                "Invalid pins",
                f"Enter {count} pin names, such as D7 or GP7."
            )
            return

        updated[name] = pins

    updated["encoder_pins"] = []

    for index, current in enumerate(hardware["encoder_pins"]):
        answer = simpledialog.askstring(
            "Encoder wiring",
            f"Knob {index + 1}: enter A, B, and press pin names",
            initialvalue=", ".join(current),
            parent=root
        )

        if answer is None:
            return

        pins = [pin.strip() for pin in answer.split(",")]

        if len(pins) != 3 or any(not pin.isidentifier() for pin in pins):
            messagebox.showerror(
                "Invalid pins",
                "Enter three pin names: A, B, and press."
            )
            return

        updated["encoder_pins"].append(pins)

    direction = simpledialog.askstring(
        "Diode direction",
        "Enter ROW2COL or COL2ROW:",
        initialvalue=hardware["diode_orientation"],
        parent=root
    )

    if direction is None:
        return

    direction = direction.strip().upper()

    if direction not in ("ROW2COL", "COL2ROW"):
        messagebox.showerror("Invalid direction", "Use ROW2COL or COL2ROW.")
        return

    updated["diode_orientation"] = direction

    all_pins = updated["row_pins"] + updated["col_pins"]
    for pins in updated["encoder_pins"]:
        all_pins.extend(pins)

    if len(all_pins) != len(set(all_pins)):
        messagebox.showerror(
            "Duplicate pin",
            "Each wiring connection needs a different pin."
        )
        return

    config["hardware"] = updated

    messagebox.showinfo(
        "Wiring updated",
        "Click Apply to Macropad to save these settings."
    )


root = tk.Tk()
root.title("Macro Reassigner")
root.geometry("500x500")

title = tk.Label(root, text="Choose Key To Edit", font=("Arial", 18))
title.pack(pady=20)

key_frame = tk.Frame(root)
key_frame.pack()

for i in range(6):
    button = tk.Button(
    key_frame,
    text=f"Key {i+1}",
    width=12,
    height=3,
    command=lambda index=i: edit_action(config["keys"], index)
    )
    button.grid(row=i // 3, column=i % 3, padx=5, pady=5)

encoder_frame = tk.Frame(root)
encoder_frame.pack(pady=20)

for encoder in range(2):
    label = tk.Label(
        encoder_frame,
        text=f"Knob {encoder + 1}"
    )
    label.grid(row=encoder, column=0, padx=5, pady=5)

    for column, action in enumerate(["Left", "Right", "Press"]):
        button = tk.Button(
            encoder_frame,
            text=action,
            width=8,
            command=lambda knob=encoder, index=column: edit_action(
                config["encoders"][knob], index
            )
        )
        button.grid(
            row=encoder,
            column=column + 1,
            padx=5,
            pady=5
        )

save_button = tk.Button(
    root,
    text="Apply to RP",
    command=save_config
)
save_button.pack(pady=10)

tk.Button(
    root,
    text="Wiring Settings",
    command=edit_pins
).pack(pady=5)

root.mainloop()