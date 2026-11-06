import os, wave, json, glob
import numpy as np

voice_dir = r"C:\Users\blazy\OneDrive\Pictures\AI Content\Dark Lantern\DL17 - The Wallace Line\voice_grady"
raw_dir = os.path.join(voice_dir, "raw")
GAP_SEC = 0.16

clips = []
cur_time = 0.0
audio_data = []

sr = 24000
gap_samples = np.zeros(int(GAP_SEC * sr), dtype=np.int16)

for i in range(1, 11):
    fpath = os.path.join(raw_dir, f"v{i:02d}.wav")
    w = wave.open(fpath, "rb")
    nframes = w.getnframes()
    dur = nframes / sr
    data = np.frombuffer(w.readframes(nframes), dtype=np.int16)
    w.close()
    
    clips.append({
        "id": f"v{i:02d}",
        "start": round(cur_time, 3),
        "end": round(cur_time + dur, 3),
        "duration": round(dur, 3)
    })
    
    audio_data.append(data)
    if i < 10:
        audio_data.append(gap_samples)
        cur_time += dur + GAP_SEC
    else:
        cur_time += dur

combined_audio = np.concatenate(audio_data)

out_wav = os.path.join(voice_dir, "voiceover.wav")
out_w = wave.open(out_wav, "wb")
out_w.setnchannels(1)
out_w.setsampwidth(2)
out_w.setframerate(sr)
out_w.writeframes(combined_audio.tobytes())
out_w.close()

clips_json_path = os.path.join(voice_dir, "clips.json")
with open(clips_json_path, "w") as f:
    json.dump({"clips": clips, "total_duration": round(cur_time, 3)}, f, indent=2)

print(f"Generated voiceover.wav: {round(cur_time, 2)}s total duration ({len(clips)} clips)")
