# Click Recorder

A lightweight Python tool for interactive screen-click annotation and YOLO-style screenshot labeling.

## 📂 Project Structure

```
click_data/
├── click_recorder.py   # Main annotation script
├── config.json         # Saved test-mode box dimensions
├── images/             # Captured screenshots organized by class
│   ├── boss_button/
│   ├── next_level/
│   └── ...
├── labels/             # Generated YOLO .txt label files by class
│   ├── boss_button/
│   ├── next_level/
│   └── ...
├── previews/           # Full-screen preview images (normal & test mode)
│   ├── boss_button_preview.png
│   ├── boss_button_normal_preview.png
│   └── ...
└── log/
    ├── click_log.txt   # Operation log
    └── archive/        # Archived logs
```

---

## 🚀 Features

* **Multi-Class Selection**: Press `1`–`5` to choose a class (e.g. `boss_button`, `next_level`, `next_stage`, `lvs`, `stages`).
* **Test Mode** (`t`):

  * Displays a red bounding box overlay following the mouse.
  * Adjust box size with arrow keys (`↑`/`↓` to change height, `←`/`→` to change width).
  * Exit test mode to save box dimensions to `config.json`.
* **Normal Mode**:

  * Left-click to capture a full-screen screenshot.
  * Saves the image under `images/<class>/`.
  * Generates a YOLO-style label file in `labels/<class>/`.
  * Updates `log/click_log.txt` with click coordinates.
  * Produces a red-box preview of the capture in `previews/`.
* **Pause/Resume**: Press `p` to toggle.
* **Quit**: Press `q` to exit and restore terminal settings.
* **Log Archiving**: On startup, existing `click_log.txt` is moved to `log/archive/`.

---

## 📦 Dependencies

* Python 3.7+
* [mss](https://pypi.org/project/mss/)
* [Pillow](https://pypi.org/project/Pillow/)
* [pynput](https://pypi.org/project/pynput/)
* `tkinter` (bundled with Python)

Install via:

```bash
python3 -m pip install --user mss pillow pynput
```

---

## 📋 Usage

1. **Run**

   ```bash
   cd click_data
   python3 click_recorder.py
   ```

2. **Controls**

   * `1`–`5`: Select class
   * `t`: Toggle test mode
   * Arrow keys: Adjust box size in test mode
   * `p`: Pause / resume
   * `q`: Quit

3. **Outputs**

   * **Screenshots** → `images/<class>/...`
   * **Labels** → `labels/<class>/...`
   * **Previews** → `previews/...`
   * **Logs** → `log/click_log.txt` (archived under `log/archive/` on startup)

---

## ⚙️ Configuration

After first run, `config.json` stores:

```json
{
  "box_width": 100,
  "box_height": 55
}
```

To reset box dimensions, delete `config.json`.

---

## 📝 License

MIT © Jeff Hsieh
