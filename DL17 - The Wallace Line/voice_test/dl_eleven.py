import urllib.request, os, shutil

base = r'C:\Users\blazy\OneDrive\Pictures\AI Content\Dark Lantern\DL17 - The Wallace Line\voice_test'
art = r'C:\Users\blazy\.gemini\antigravity\brain\78e00dba-8e80-41ad-9184-973c9f7f9ab7'

# ElevenLabs Grady
p1_mp3 = os.path.join(base, 'eleven_grady.mp3')
urllib.request.urlretrieve('https://d8j0ntlcm91z4.cloudfront.net/user_3KxioJ1AABwQBdxDzPTLo2p4RA7/hf_20261105_201343_031db852-eb91-46d2-9f3b-b060bf80211e.mp3', p1_mp3)
p1_wav = os.path.join(base, 'eleven_grady.wav')
os.system(f'ffmpeg -y -i "{p1_mp3}" "{p1_wav}" >nul 2>&1')
shutil.copy2(p1_wav, os.path.join(art, 'eleven_grady.wav'))

# ElevenLabs Elodie
p2_mp3 = os.path.join(base, 'eleven_elodie.mp3')
urllib.request.urlretrieve('https://d8j0ntlcm91z4.cloudfront.net/user_3KxioJ1AABwQBdxDzPTLo2p4RA7/hf_20261105_201359_eac92afc-3040-4ed6-a7c1-c9210eca4f72.mp3', p2_mp3)
p2_wav = os.path.join(base, 'eleven_elodie.wav')
os.system(f'ffmpeg -y -i "{p2_mp3}" "{p2_wav}" >nul 2>&1')
shutil.copy2(p2_wav, os.path.join(art, 'eleven_elodie.wav'))

print('Downloaded and converted ElevenLabs samples')
