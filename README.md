# Click Recorder

A lightweight Python tool for screen-click annotation and screenshot labeling, supporting both a “test mode” for interactive box‐size tuning and a “normal mode” for bulk capture and YOLO-style label generation.

---

## Features

- **Multiple classes**:  
  Press `1`–`5` to select among configured categories (e.g. `boss_button`, `next_level`, etc.).

- **Test Mode**:  
  - Toggle with `t`.  
  - Shows a red rectangle overlay that follows your mouse cursor.  
  - Adjust its size with arrow keys (`↑`/`↓` to change height, `←`/`→` to change width).  
  - On exit, saves the chosen box size to `config.json`.

- **Normal Mode**:  
  - Click left mouse button to capture full-screen image.  
  - Saves screenshot under `images/<class>/`.  
  - Writes YOLO-style label (`<class_id> x y w h`) to `labels/<class>/`.  
  - Appends a line to `log/click_log.txt`.  
  - Generates a “preview” image with a red box and class label under `previews/`.

- **Pause / Resume**: Press `p`.  
- **Force Quit**: Press `q`.

- **Log Archiving**: On startup, any existing `click_log.txt` is auto-archived to `log/archive/`.

---

## Directory Layout

click_data/
├── click_recorder.py
├── config.json            ⟵ saves last test‐mode box size
├── images/                ⟵ screenshots by class
│   ├── boss_button/
│   ├── next_level/
│   └── …
├── labels/                ⟵ YOLO .txt files by class
│   ├── boss_button/
│   ├── next_level/
│   └── …
├── previews/              ⟵ full-screen previews (test & normal)
│   ├── _preview_000.png
│   └── _normal_preview_000.png
└── log/
├── click_log.txt      ⟵ operation log
└── archive/           ⟵ archived logs

---

## Dependencies

- Python 3.7+  
- [mss](https://pypi.org/project/mss/)  
- [Pillow](https://pypi.org/project/Pillow/)  
- [pynput](https://pypi.org/project/pynput/)  
- `tkinter` (usually included in standard library)

Install via pip:

```bash
python3 -m pip install --user mss pillow pynput


Usage
	1.	Make executable (optional):
chmod +x click_recorder.py


	2.	Run:
./click_recorder.py


	3.	Controls:
	•	1–5: Select class
	•	t : Toggle test mode
	•	Arrow keys: Adjust box size (in test mode)
	•	p : Pause / resume
	•	q : Quit

4.	Output:
	•	Screenshots → images/<class>/…
	•	Label files → labels/<class>/…
	•	Previews → previews/…
	•	Logs → log/click_log.txt (archived on each startup)

Configuration

After first run, a config.json is created:
{
  "box_width": 100,
  "box_height": 55
}

Extension
	•	Add more classes:
Edit the CLASS_MAP dict near the top of the script:
CLASS_MAP = {
  '1': 'boss_button',
  '2': 'next_level',
  '3': 'next_stage',
  '4': 'lvs',
  '5': 'stages',
  '6': 'new_label'
}
	•	Customize output paths by modifying the path constants at the top (IMAGE_ROOT, LABEL_ROOT, etc.).
