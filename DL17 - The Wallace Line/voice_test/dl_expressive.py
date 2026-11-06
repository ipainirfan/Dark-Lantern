import urllib.request, os, shutil

base = r'C:\Users\blazy\OneDrive\Pictures\AI Content\Dark Lantern\DL17 - The Wallace Line\voice_test'
art = r'C:\Users\blazy\.gemini\antigravity\brain\78e00dba-8e80-41ad-9184-973c9f7f9ab7'

# Download expressive Grady
mp3_path = os.path.join(base, 'eleven_grady_expressive.mp3')
urllib.request.urlretrieve('https://d8j0ntlcm91z4.cloudfront.net/user_3KxioJ1AABwQBdxDzPTLo2p4RA7/hf_20261105_201738_b1e48aaa-7cff-4fd4-a9cc-b318faa721ea.mp3', mp3_path)

# Convert to wav (Original speed & pitch)
wav_orig = os.path.join(base, 'grady_expressive.wav')
os.system(f'ffmpeg -y -i "{mp3_path}" "{wav_orig}" >nul 2>&1')
shutil.copy2(wav_orig, os.path.join(art, 'grady_expressive.wav'))

# Toddler tuned (pitch shifted +2.2 semitones, 8% slower for sweet innocent hesitation)
wav_toddler = os.path.join(base, 'grady_expressive_toddler.wav')
os.system(f'ffmpeg -y -i "{wav_orig}" -af "asetrate=44100*1.135,atempo=1/1.135*0.92" "{wav_toddler}" >nul 2>&1')
shutil.copy2(wav_toddler, os.path.join(art, 'grady_expressive_toddler.wav'))

print("Created expressive Grady and toddler tuned Grady!")
