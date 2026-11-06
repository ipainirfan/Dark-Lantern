import urllib.request, os, subprocess, shutil

urls = {
    "v01": "https://d8j0ntlcm91z4.cloudfront.net/user_3KxioJ1AABwQBdxDzPTLo2p4RA7/hf_20261105_201941_d0b6eddf-70cc-4b3e-94c2-d01888425fed.mp3",
    "v02": "https://d8j0ntlcm91z4.cloudfront.net/user_3KxioJ1AABwQBdxDzPTLo2p4RA7/hf_20261105_201955_6225fc81-c1ce-494c-a843-d8bb2895a651.mp3",
    "v03": "https://d8j0ntlcm91z4.cloudfront.net/user_3KxioJ1AABwQBdxDzPTLo2p4RA7/hf_20261105_201955_90260085-ce6e-49e1-9323-46bcd5a92f5c.mp3",
    "v04": "https://d8j0ntlcm91z4.cloudfront.net/user_3KxioJ1AABwQBdxDzPTLo2p4RA7/hf_20261105_201954_b65fe42e-351a-487d-8b18-8c776a23c655.mp3",
    "v05": "https://d8j0ntlcm91z4.cloudfront.net/user_3KxioJ1AABwQBdxDzPTLo2p4RA7/hf_20261105_202013_1c28c5be-fd4a-4cfd-ad73-f7586630a370.mp3",
    "v06": "https://d8j0ntlcm91z4.cloudfront.net/user_3KxioJ1AABwQBdxDzPTLo2p4RA7/hf_20261105_201955_bf71d014-89c2-4802-af15-d76185de3983.mp3",
    "v07": "https://d8j0ntlcm91z4.cloudfront.net/user_3KxioJ1AABwQBdxDzPTLo2p4RA7/hf_20261105_201954_de7d9c08-1adb-46b5-9510-03ae2646b3ef.mp3",
    "v08": "https://d8j0ntlcm91z4.cloudfront.net/user_3KxioJ1AABwQBdxDzPTLo2p4RA7/hf_20261105_201955_72c03afc-84d8-4811-9e92-f1b99a346edf.mp3",
    "v09": "https://d8j0ntlcm91z4.cloudfront.net/user_3KxioJ1AABwQBdxDzPTLo2p4RA7/hf_20261105_201955_60f4cf1b-8568-4080-9a06-c466c1548918.mp3",
    "v10": "https://d8j0ntlcm91z4.cloudfront.net/user_3KxioJ1AABwQBdxDzPTLo2p4RA7/hf_20261105_201956_20893c13-cefe-478c-a9c9-12de8732db64.mp3"
}

voice_dir = r"C:\Users\blazy\OneDrive\Pictures\AI Content\Dark Lantern\DL17 - The Wallace Line\voice_grady"
raw_orig = os.path.join(voice_dir, "raw_orig")
os.makedirs(raw_orig, exist_ok=True)

for vid, url in sorted(urls.items()):
    mp3_path = os.path.join(raw_orig, f"{vid}.mp3")
    wav_path = os.path.join(raw_orig, f"{vid}.wav")
    urllib.request.urlretrieve(url, mp3_path)
    subprocess.run(["ffmpeg", "-y", "-i", mp3_path, "-ar", "24000", "-ac", "1", wav_path], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"Downloaded & converted {vid}.wav")

print("All 10 clips ready in raw_orig!")
