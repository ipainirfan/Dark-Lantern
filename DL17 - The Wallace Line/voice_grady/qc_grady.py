import sys, json, wave, numpy as np, re, difflib, sherpa_onnx, os

D = r"C:\Users\blazy\OneDrive\Pictures\AI Content\_Tools\dl_kit\asr\sherpa-onnx-whisper-base.en" + os.sep
rec = sherpa_onnx.OfflineRecognizer.from_whisper(
    encoder=D+'base.en-encoder.int8.onnx',
    decoder=D+'base.en-decoder.int8.onnx',
    tokens=D+'base.en-tokens.txt',
    language='en',
    task='transcribe',
    num_threads=4
)

voice_dir = r"C:\Users\blazy\OneDrive\Pictures\AI Content\Dark Lantern\DL17 - The Wallace Line\voice_grady"
lines_data = json.load(open(os.path.join(voice_dir, "lines.json")))["lines"]

def norm(t):
    return re.sub(r"[^a-z0-9 ]", " ", t.lower().replace("'", "").replace('-', ' ')).split()

all_pass = True
for idx, item in enumerate(lines_data, 1):
    path = os.path.join(voice_dir, "raw_orig", f"v{idx:02d}.wav")
    w = wave.open(path)
    sr = w.getframerate()
    a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).reshape(-1, w.getnchannels()).mean(1) / 32768
    a16 = np.interp(np.arange(0, len(a), sr/16000), np.arange(len(a)), a).astype(np.float32)
    s = rec.create_stream()
    s.accept_waveform(16000, a16)
    rec.decode_stream(s)
    txt = s.result.text.strip()
    
    ref = norm(item["text"])
    hyp = norm(txt)
    r = difflib.SequenceMatcher(None, ref, hyp).ratio()
    extra = len(hyp) / max(1, len(ref))
    ok = r >= 0.82 and extra <= 1.15
    if not ok:
        all_pass = False
    print(f"{'PASS' if ok else 'FAIL'} clip {idx:02d} match {r:.2f} words {len(hyp)}/{len(ref)} dur {len(a)/sr:.2f}s | {txt}")

print(f"\nOverall Whisper QC: {'10/10 PASS' if all_pass else 'SOME FAILED'}")
