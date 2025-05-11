#!/usr/bin/env python3
import os
import mss
from PIL import Image, ImageDraw, ImageFont
from pynput import keyboard, mouse
from pynput.mouse import Controller as MouseController
import shutil
import tkinter as tk
import json
import time
import sys
import termios


# ─── Settings ─────────────────────────────────
BASE_DIR     = os.path.dirname(os.path.abspath(__file__))
IMAGE_ROOT   = os.path.join(BASE_DIR, 'images')
LABEL_ROOT   = os.path.join(BASE_DIR, 'labels')
LOG_DIR     = os.path.join(BASE_DIR, 'log')
ARCHIVE_DIR = os.path.join(LOG_DIR, 'archive')
PREVIEW_DIR = os.path.join(BASE_DIR, 'previews')
os.makedirs(PREVIEW_DIR, exist_ok=True)
LOG_PATH    = os.path.join(LOG_DIR, 'click_log.txt')
CLASS_MAP    = {
    '1': 'boss_button',
    '2': 'next_level',
    '3': 'next_stage',
    '4': 'lvs',
    '5': 'stages'
}

RETINA_SCALE = 2.0

# Adjustable preview box size (width and height)
BOX_WIDTH = 40
BOX_HEIGHT = 40

# Configuration file path for storing box size
CONFIG_PATH = os.path.join(BASE_DIR, 'config.json')
# Load saved box size if available
if os.path.exists(CONFIG_PATH):
    try:
        with open(CONFIG_PATH, 'r') as cfg:
            cfg_data = json.load(cfg)
            BOX_WIDTH = cfg_data.get('box_width', BOX_WIDTH)
            BOX_HEIGHT = cfg_data.get('box_height', BOX_HEIGHT)
    except Exception:
        pass

# ─── Global Initialization ───────────────────────
# Ensure image, label, and log directories exist
for cname in CLASS_MAP.values():
    os.makedirs(os.path.join(IMAGE_ROOT, cname), exist_ok=True)
    os.makedirs(os.path.join(LABEL_ROOT, cname), exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(ARCHIVE_DIR, exist_ok=True)
# Ensure active log file exists in log directory
if not os.path.exists(LOG_PATH):
    open(LOG_PATH, 'a').close()

# Archive existing log at startup if non-empty
if os.path.exists(LOG_PATH) and os.path.getsize(LOG_PATH) > 0:
    startup_archive = os.path.join(ARCHIVE_DIR, 'click_log_archive.txt')
    shutil.copy(LOG_PATH, startup_archive)
    open(LOG_PATH, 'w').close()
    print(f"📦 已於啟動時歸檔舊 log 至：{startup_archive}")

# ─── Utilities ────────────────────────────────
def get_next_index(class_name):
    path = os.path.join(LABEL_ROOT, class_name)
    os.makedirs(path, exist_ok=True)
    files = [f for f in os.listdir(path) if f.endswith('.txt')]
    nums = []
    for f in files:
        try:
            nums.append(int(f.split('_')[-1].split('.')[0]))
        except:
            pass
    return max(nums) + 1 if nums else 0

def get_next_preview_index(class_name, mode_suffix):
    # mode_suffix: 'preview' or 'normal_preview'
    files = [f for f in os.listdir(PREVIEW_DIR) if f.startswith(f"{class_name}_{mode_suffix}")]
    nums = []
    for f in files:
        parts = f.rsplit('_', 1)
        if len(parts) == 2 and parts[1].endswith('.png'):
            num = parts[1].split('.')[0]
            if num.isdigit():
                nums.append(int(num))
    return max(nums) + 1 if nums else 0

def save_label(class_id, x, y, w, h):
    class_name = CLASS_MAP[class_id]
    idx = get_next_index(class_name)
    img_file = os.path.join(IMAGE_ROOT, class_name, f"{class_name}_{idx:03d}.png")
    label_file = os.path.join(LABEL_ROOT, class_name, f"{class_name}_{idx:03d}.txt")
    os.makedirs(os.path.dirname(img_file), exist_ok=True)
    os.makedirs(os.path.dirname(label_file), exist_ok=True)
    # Save image provided by caller; this function assumes caller saved it
    with open(label_file, 'w') as f:
        f.write(f"{class_id} {x} {y} {w} {h}\n")
    return img_file, label_file

def append_log(class_id, x, y, w, h):
    with open(LOG_PATH, 'a') as f:
        f.write(f"{class_id} {x} {y} {w} {h}\n")

# ─── Main ─────────────────────────────────────
def main():
    # Disable terminal echo so key presses don't show up
    fd = sys.stdin.fileno()
    old_term = termios.tcgetattr(fd)
    new_term = termios.tcgetattr(fd)
    new_term[3] = new_term[3] & ~termios.ECHO
    termios.tcsetattr(fd, termios.TCSADRAIN, new_term)
    current = None
    test_mode = False
    paused = False
    running = True
    exit_requested = False  # Add this line
    mouse_controller = MouseController()

    # Initialize Tkinter overlay with white background
    overlay = tk.Tk()
    overlay.overrideredirect(True)
    overlay.wm_attributes("-topmost", True)
    width, height = BOX_WIDTH, BOX_HEIGHT
    canvas = tk.Canvas(overlay, width=width, height=height, bg='white', highlightthickness=0)
    rect = canvas.create_rectangle(2, 2, width-2, height-2, outline='red', width=3)
    canvas.pack()
    overlay.withdraw()

    # Ensure preview directory exists before usage
    os.makedirs(PREVIEW_DIR, exist_ok=True)

    print("🔧 點擊錄製器已啟動")
    print("▶️ 按 1/2/3/4/5 選擇類別；點擊滑鼠截圖；t 切換測試模式；p 暫停/繼續；q 退出程式")

    # Keyboard handler
    def on_press(key):
        nonlocal current, test_mode, paused, running, exit_requested
        global BOX_WIDTH, BOX_HEIGHT
        # Adjust preview box dimensions with arrow keys
        if key == keyboard.Key.up:
            BOX_HEIGHT += 5
            print(f"🔍 框高度：{BOX_HEIGHT}")
            return
        elif key == keyboard.Key.down:
            BOX_HEIGHT = max(1, BOX_HEIGHT - 5)
            print(f"🔍 框高度：{BOX_HEIGHT}")
            return
        elif key == keyboard.Key.right:
            BOX_WIDTH += 5
            print(f"🔍 框寬度：{BOX_WIDTH}")
            return
        elif key == keyboard.Key.left:
            BOX_WIDTH = max(1, BOX_WIDTH - 5)
            print(f"🔍 框寬度：{BOX_WIDTH}")
            return
        try:
            c = key.char
        except:
            return
        if c in CLASS_MAP:
            print(f"🎯 已選類別：{CLASS_MAP[c]}")
            current = c
        elif c == 't':
            test_mode = not test_mode
            print(f"🧪 測試模式：{'開啟' if test_mode else '關閉'}")
            if not test_mode:
                print(f"🔔 測試結束，最終框大小：{BOX_WIDTH}×{BOX_HEIGHT}")
                # Save box size to config
                try:
                    with open(CONFIG_PATH, 'w') as cfg:
                        json.dump({'box_width': BOX_WIDTH, 'box_height': BOX_HEIGHT}, cfg)
                except Exception as e:
                    print(f"⚠️ 無法儲存設定: {e}")
        elif c == 'p':
            paused = not paused
            print(f"⏸️ 狀態：{'暫停' if paused else '運行'}")
        elif c == 'q':
            print("❌ 強制退出程式")
            nonlocal exit_requested
            exit_requested = True
            nonlocal running
            running = False
            try:
                ms_listener.stop()
            except:
                pass
            try:
                kb_listener.stop()
            except:
                pass
            return False

    # Mouse handler
    def on_click(x, y, button, pressed):
        nonlocal current, test_mode, paused, running
        if not running or paused or current is None:
            return
        if pressed:
            # Capture screen using mss for speed
            with mss.mss() as sct:
                shot = sct.grab(sct.monitors[1])
                img = Image.frombytes('RGB', shot.size, shot.rgb)
            # Convert logical coordinates to physical
            x_p, y_p = int(x * RETINA_SCALE), int(y * RETINA_SCALE)
            w, h = img.size
            # Resize for saving
            resized_img = img.resize((int(w / RETINA_SCALE), int(h / RETINA_SCALE)))
            new_w, new_h = resized_img.size
            # Save or preview
            if not test_mode:
                class_id = current
                # Save image to file
                class_name = CLASS_MAP[class_id]
                idx = get_next_index(class_name)
                img_path = os.path.join(IMAGE_ROOT, class_name, f"{class_name}_{idx:03d}.png")
                os.makedirs(os.path.dirname(img_path), exist_ok=True)
                resized_img.save(img_path)
                # Save label and log
                _, label_file = save_label(class_id, x_p, y_p, new_w, new_h)
                append_log(class_id, x_p, y_p, new_w, new_h)
                print(f"✅ 已儲存：{class_name} 編號{idx:03d}")
                print(f"📄 標籤檔：{os.path.basename(label_file)}")
                # Also save a full-screen preview with highlighted box
                with mss.mss() as sct:
                    shot = sct.grab(sct.monitors[1])
                    full_img = Image.frombytes('RGB', shot.size, shot.rgb)
                draw = ImageDraw.Draw(full_img)
                class_name = CLASS_MAP[current]
                idx = get_next_preview_index(class_name, 'normal_preview')
                preview_path = os.path.join(PREVIEW_DIR, f"{class_name}_normal_preview_{idx:03d}.png")
                # Calculate box physical coords
                cx, cy = int(x), int(y)
                hw, hh = BOX_WIDTH // 2, BOX_HEIGHT // 2
                left, top = max(0, cx - hw), max(0, cy - hh)
                right, bottom = left + BOX_WIDTH, top + BOX_HEIGHT
                l_ph, t_ph = left * RETINA_SCALE, top * RETINA_SCALE
                r_ph, b_ph = right * RETINA_SCALE, bottom * RETINA_SCALE
                # Draw red rectangle on full image
                draw.rectangle([(l_ph, t_ph), (r_ph, b_ph)],
                               outline='red', width=int(3 * RETINA_SCALE))
                # Draw class label near top-left of rectangle
                font = ImageFont.load_default()
                label = current
                # Measure label size
                bbox = draw.textbbox((l_ph + 2, t_ph + 2), label, font=font)
                text_w = bbox[2] - bbox[0]
                text_h = bbox[3] - bbox[1]
                # Semi-transparent background for label
                draw.rectangle([(l_ph + 2, t_ph + 2),
                                (l_ph + 2 + text_w + 4, t_ph + 2 + text_h + 4)],
                               fill=(0, 0, 0, 128))
                draw.text((l_ph + 4, t_ph + 4), label, fill='red', font=font)
                # Resize to logical resolution for saving preview
                logical_size = (int(full_img.width / RETINA_SCALE),
                                int(full_img.height / RETINA_SCALE))
                preview_img = full_img.resize(logical_size)
                os.makedirs(PREVIEW_DIR, exist_ok=True)
                preview_img.save(preview_path)
                print(f"📁 已儲存常規全螢幕預覽至：{preview_path}")
                # 顯示該分類最新總圖數
                img_count = len([f for f in os.listdir(os.path.join(IMAGE_ROOT, class_name)) if f.lower().endswith('.png')])
                print(f"📊 {class_name} 目前共有 {img_count} 張圖片")
            else:
                # Save full-screen preview with highlighted box for testing
                with mss.mss() as sct:
                    shot = sct.grab(sct.monitors[1])
                    full_img = Image.frombytes('RGB', shot.size, shot.rgb)
                draw = ImageDraw.Draw(full_img)
                class_name = CLASS_MAP[current]
                idx = get_next_preview_index(class_name, 'preview')
                preview_path = os.path.join(PREVIEW_DIR, f"{class_name}_preview_{idx:03d}.png")
                # Calculate box physical coords
                cx, cy = int(x), int(y)
                hw, hh = BOX_WIDTH // 2, BOX_HEIGHT // 2
                left, top = max(0, cx - hw), max(0, cy - hh)
                right, bottom = left + BOX_WIDTH, top + BOX_HEIGHT
                l_ph, t_ph = left * RETINA_SCALE, top * RETINA_SCALE
                r_ph, b_ph = right * RETINA_SCALE, bottom * RETINA_SCALE
                # Draw red rectangle on full image
                draw.rectangle([(l_ph, t_ph), (r_ph, b_ph)],
                               outline='red', width=int(3 * RETINA_SCALE))
                # Draw label
                font = ImageFont.load_default()
                label = class_name
                bbox = draw.textbbox((l_ph + 2, t_ph + 2), label, font=font)
                text_w = bbox[2] - bbox[0]
                text_h = bbox[3] - bbox[1]
                draw.rectangle([(l_ph + 2, t_ph + 2),
                                (l_ph + 2 + text_w + 4, t_ph + 2 + text_h + 4)],
                               fill=(0, 0, 0, 128))
                draw.text((l_ph + 4, t_ph + 4), label, fill='red', font=font)
                # Resize to logical resolution and save
                logical_size = (int(full_img.width / RETINA_SCALE),
                                int(full_img.height / RETINA_SCALE))
                preview_img = full_img.resize(logical_size)
                os.makedirs(PREVIEW_DIR, exist_ok=True)
                preview_img.save(preview_path)
                print(f"📁 已儲存測試全螢幕預覽至：{preview_path}")

    # Start mouse listener with error handling
    try:
        ms_listener = mouse.Listener(on_click=on_click)
        ms_listener.start()
    except Exception as e:
        print(f"⚠️ 無法啟用滑鼠監聽: {e}")

    # Start keyboard listener with error handling
    try:
        kb_listener = keyboard.Listener(on_press=on_press)
        kb_listener.start()
    except Exception as e:
        print(f"⚠️ 無法啟用鍵盤監聽: {e}")

    # 顯示每個分類當前已儲存的圖片與標籤數
    for cid, cname in CLASS_MAP.items():
        img_dir = os.path.join(IMAGE_ROOT, cname)
        lbl_dir = os.path.join(LABEL_ROOT, cname)
        png_count = len([f for f in os.listdir(img_dir) if f.lower().endswith('.png')]) if os.path.isdir(img_dir) else 0
        txt_count = len([f for f in os.listdir(lbl_dir) if f.lower().endswith('.txt')]) if os.path.isdir(lbl_dir) else 0
        print(f"📂 {cname}：圖片 {png_count} 張，標籤 {txt_count} 個")
    while running:
        if test_mode and not paused:
            overlay.deiconify()
            overlay.lift()
            overlay.attributes('-topmost', True)
            width, height = BOX_WIDTH, BOX_HEIGHT
            canvas.config(width=width, height=height)
            canvas.coords(rect, 2, 2, width-2, height-2)
            x, y = mouse_controller.position
            ix, iy = int(x), int(y)
            overlay.geometry(f"{width}x{height}+{ix-width//2}+{iy-height//2}")
        else:
            overlay.withdraw()
        # Process Tkinter events
        overlay.update_idletasks()
        overlay.update()
        time.sleep(0.05)

    # After exiting main loop
    if exit_requested:
        print("❌ 程式結束")
        overlay.destroy()
        # Restore terminal echo
        termios.tcsetattr(fd, termios.TCSADRAIN, old_term)
        sys.exit(0)

if __name__ == '__main__':
    main()