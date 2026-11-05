# MacroReassigner!

I built a macropad for Stardance, but I kept wanting to change my macros and what each key was assigned to. So, using Python (Tkinter) and JSON to store assignments, I made this macro reassigner.

It currently supports 6 keys in a 2×3 matrix and 2 rotary encoders. You can assign shortcuts, text macros, and media controls using KMK keycodes, plus configure the wiring pins.

## Requirements

- Windows for the downloadable app, or Python 3 with Tkinter to run from source
- An RP2040-based macropad running CircuitPython and KMK

## Getting Started

1. Download `MacroReassigner.exe` from [Releases](https://github.com/Catsarepro21/MacroReassigner/releases), put it in a folder you can write to, and double-click it. To run from source, keep `app.py` and `macros.json` together and run `python app.py`.
2. Click Wiring Settings and enter the pins for your macropad. Use the exact pin names supported by your board.
3. Set your macros by clicking a key or an encoder’s Left, Right, or Press button.
4. Click Apply to RP and select the root of your CIRCUITPY drive to save the configuration.
5. Copy the firmware `code.py` from the release's code ZIP onto the CIRCUITPY drive. KMK must already be installed.
6. Wait a few seconds for the firmware to reload, then test your assignments!

After setup, you only need to click Apply to RP when changing assignments or wiring.

## Keycodes and Modifiers

Find key names in the official [KMK keycode list](https://github.com/KMKfw/kmk_firmware/blob/main/docs/en/keycodes.md). Volume and playback controls are listed in the [KMK media keys documentation](https://github.com/KMKfw/kmk_firmware/blob/main/docs/en/media_keys.md).

Enter names without `KC.` in the app. For example, use `LEFT`, `RIGHT`, `VOLU`, or `VOLD`.

Leave modifiers blank for ordinary keys. For shortcuts, enter modifiers such as `LCTL`, `LSFT`, `LALT`, or `LGUI`, separated by commas. For example, Copy is key `C` with modifier `LCTL`.

## Saving Assignments

Changes are not saved to the macropad until you click Apply to RP.

Applying saves `macros.json` to the RP
