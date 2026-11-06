from PIL import Image, ImageFilter
import numpy as np
import os, shutil

mascot_dir = r"C:\Users\blazy\OneDrive\Pictures\AI Content\Dark Lantern\DL17 - The Wallace Line\Mascot"
art_dir = r"C:\Users\blazy\.gemini\antigravity\brain\78e00dba-8e80-41ad-9184-973c9f7f9ab7"

files = ["scout_confused_map.png", "tiger_swim_goggles.png", "cockatoo_bonk.png"]

for fname in files:
    raw_p = os.path.join(mascot_dir, fname)
    cut_name = fname.replace(".png", "_cut.png")
    cut_p = os.path.join(mascot_dir, cut_name)
    
    img = Image.open(raw_p).convert("RGBA")
    arr = np.array(img).astype(np.float32)
    
    # Corners are background
    bg_color = arr[:10, :10, :3].mean(axis=(0, 1))
    
    # Distance from background color
    dist = np.sqrt(np.sum((arr[:, :, :3] - bg_color) ** 2, axis=2))
    
    # Thresholding: dist < 30 is pure background, dist > 60 is pure foreground
    alpha = np.clip((dist - 25) / 35.0, 0, 1) * 255
    arr[:, :, 3] = alpha.astype(np.uint8)
    
    res = Image.fromarray(arr.astype(np.uint8))
    # Crop to non-transparent bounding box
    bbox = res.getbbox()
    if bbox:
        res = res.crop(bbox)
    
    res.save(cut_p, "PNG")
    shutil.copy2(cut_p, os.path.join(art_dir, cut_name))
    print(f"Cleanly cut out {cut_name}")
