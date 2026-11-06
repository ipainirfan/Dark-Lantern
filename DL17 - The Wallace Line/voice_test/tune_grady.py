import os, shutil

base = r'C:\Users\blazy\OneDrive\Pictures\AI Content\Dark Lantern\DL17 - The Wallace Line\voice_test'
art = r'C:\Users\blazy\.gemini\antigravity\brain\78e00dba-8e80-41ad-9184-973c9f7f9ab7'
src = os.path.join(base, 'eleven_grady.wav')

# Test pitch shift +2 semitones (pitch=1.122, tempo preserved)
dst_p2 = os.path.join(base, 'grady_toddler_p2.wav')
os.system(f'ffmpeg -y -i "{src}" -af "asetrate=44100*1.122,atempo=1/1.122" "{dst_p2}" >nul 2>&1')
shutil.copy2(dst_p2, os.path.join(art, 'grady_toddler_p2.wav'))

# Test pitch shift +3 semitones (pitch=1.189, tempo preserved)
dst_p3 = os.path.join(base, 'grady_toddler_p3.wav')
os.system(f'ffmpeg -y -i "{src}" -af "asetrate=44100*1.189,atempo=1/1.189" "{dst_p3}" >nul 2>&1')
shutil.copy2(dst_p3, os.path.join(art, 'grady_toddler_p3.wav'))

# Test pitch shift +2.5 semitones with slightly relaxed tempo (atempo=0.92)
dst_slow = os.path.join(base, 'grady_toddler_sweet.wav')
os.system(f'ffmpeg -y -i "{src}" -af "asetrate=44100*1.15,atempo=1/1.15*0.93" "{dst_slow}" >nul 2>&1')
shutil.copy2(dst_slow, os.path.join(art, 'grady_toddler_sweet.wav'))

print('Generated pitch & tempo tuned Grady samples')
