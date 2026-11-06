import json, os, wave

voice_dir = r"C:\Users\blazy\OneDrive\Pictures\AI Content\Dark Lantern\DL17 - The Wallace Line\voice_grady"
raw_dir = os.path.join(voice_dir, "raw")
GAP_SEC = 0.16
sr = 24000

segs = []
cur_time = 0.0

for i in range(1, 11):
    fpath = os.path.join(raw_dir, f"v{i:02d}.wav")
    w = wave.open(fpath, "rb")
    dur = w.getnframes() / sr
    w.close()
    
    start = round(cur_time, 4)
    end = round(cur_time + dur, 4)
    segs.append([start, end])
    cur_time += dur + GAP_SEC

with open(os.path.join(voice_dir, "clips.json"), "w") as f:
    json.dump(segs, f)

print("Updated clips.json to list of [start, end]")
