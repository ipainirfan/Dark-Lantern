import urllib.request, os, shutil
from PIL import Image, ImageFilter
import numpy as np

images = {
    1: ("cartoon_map_indo_wide.png", "https://d8j0ntlcm91z4.cloudfront.net/user_3KxioJ1AABwQBdxDzPTLo2p4RA7/hf_20261105_202420_ea15ed9c-b48b-474a-871b-c913feba564c.png"),
    2: ("cartoon_map_strait.png", "https://d8j0ntlcm91z4.cloudfront.net/user_3KxioJ1AABwQBdxDzPTLo2p4RA7/hf_20261105_202421_85669135-7901-4bcc-ac1a-9ed72d70a7d4.png"),
    3: ("cartoon_trench_cross_section.png", "https://d8j0ntlcm91z4.cloudfront.net/user_3KxioJ1AABwQBdxDzPTLo2p4RA7/hf_20261105_202420_1b2fd21e-1e04-4fe9-9af5-07ca512dafe2.png"),
    4: ("cartoon_ice_age_bridge.png", "https://d8j0ntlcm91z4.cloudfront.net/user_3KxioJ1AABwQBdxDzPTLo2p4RA7/hf_20261105_202421_c0c49554-b373-4877-9247-10c9db5ee71f.png"),
    5: ("cartoon_continental_collision.png", "https://d8j0ntlcm91z4.cloudfront.net/user_3KxioJ1AABwQBdxDzPTLo2p4RA7/hf_20261105_202420_e8cbe93b-08ec-44c0-8a65-1b216f772146.png"),
    6: ("scout_confused_map.png", "https://d8j0ntlcm91z4.cloudfront.net/user_3KxioJ1AABwQBdxDzPTLo2p4RA7/hf_20261105_202419_342ac42f-dc45-46ac-ab32-8c50188a5692.png"),
    7: ("tiger_swim_goggles.png", "https://d8j0ntlcm91z4.cloudfront.net/user_3KxioJ1AABwQBdxDzPTLo2p4RA7/hf_20261105_202421_dcf47450-8e35-4c8f-8be0-1e5a0e225238.png"),
    8: ("cockatoo_bonk.png", "https://d8j0ntlcm91z4.cloudfront.net/user_3KxioJ1AABwQBdxDzPTLo2p4RA7/hf_20261105_202422_2c60a8d2-63f5-462f-a9b0-caf54de5877b.png")
}

mascot_dir = r"C:\Users\blazy\OneDrive\Pictures\AI Content\Dark Lantern\DL17 - The Wallace Line\Mascot"
art_dir = r"C:\Users\blazy\.gemini\antigravity\brain\78e00dba-8e80-41ad-9184-973c9f7f9ab7"
os.makedirs(mascot_dir, exist_ok=True)

def cut_white_bg(img_path, out_path):
    img = Image.open(img_path).convert("RGBA")
    arr = np.array(img)
    # White background detection (high RGB and low variance)
    rgb = arr[:, :, :3].astype(np.float32)
    bright = (rgb[:, :, 0] > 240) & (rgb[:, :, 1] > 240) & (rgb[:, :, 2] > 240)
    
    # Simple flood fill or outer mask
    from scipy.ndimage import binary_fill_holes
    # Mask of non-white
    fg = ~bright
    # Smooth edges
    alpha = Image.fromarray((fg * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.0))
    alpha_arr = np.array(alpha)
    arr[:, :, 3] = np.minimum(arr[:, :, 3], alpha_arr)
    
    cut = Image.fromarray(arr)
    # Trim bounding box
    bbox = cut.getbbox()
    if bbox:
        cut = cut.crop(bbox)
    cut.save(out_path, "PNG")

for idx, (fname, url) in images.items():
    raw_p = os.path.join(mascot_dir, fname)
    urllib.request.urlretrieve(url, raw_p)
    print(f"Downloaded {fname}")
    
    if idx in [6, 7, 8]:
        cut_name = fname.replace(".png", "_cut.png")
        cut_p = os.path.join(mascot_dir, cut_name)
        try:
            cut_white_bg(raw_p, cut_p)
            shutil.copy2(cut_p, os.path.join(art_dir, cut_name))
            print(f"Cut out {cut_name}")
        except Exception as e:
            print(f"Error cutting {fname}: {e}")
            shutil.copy2(raw_p, os.path.join(art_dir, fname))
    else:
        shutil.copy2(raw_p, os.path.join(art_dir, fname))

print("All cartoon assets downloaded and prepared!")
