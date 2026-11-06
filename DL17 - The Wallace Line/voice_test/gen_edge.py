import asyncio, os, shutil
import edge_tts

async def main():
    base = r'C:\Users\blazy\OneDrive\Pictures\AI Content\Dark Lantern\DL17 - The Wallace Line\voice_test'
    art = r'C:\Users\blazy\.gemini\antigravity\brain\78e00dba-8e80-41ad-9184-973c9f7f9ab7'
    os.makedirs(base, exist_ok=True)
    text = "Look at Indonesia! Okay, zoom closer... wait, not Java! Over here. Right there!"
    
    # en-US-AnaNeural (child voice)
    dst1 = os.path.join(base, 'sample_ana_child.mp3')
    communicate = edge_tts.Communicate(text, 'en-US-AnaNeural')
    await communicate.save(dst1)
    
    # en-US-AnaNeural with slightly slower or pitch rate
    dst2 = os.path.join(base, 'sample_ana_toddler.mp3')
    communicate2 = edge_tts.Communicate(text, 'en-US-AnaNeural', pitch='+10Hz', rate='-5%')
    await communicate2.save(dst2)
    
    # Convert to wav and copy to artifact dir
    os.system(f'ffmpeg -y -i "{dst1}" "{base}/sample_ana_child.wav" >nul 2>&1')
    os.system(f'ffmpeg -y -i "{dst2}" "{base}/sample_ana_toddler.wav" >nul 2>&1')
    
    shutil.copy2(f'{base}/sample_ana_child.wav', f'{art}/sample_ana_child.wav')
    shutil.copy2(f'{base}/sample_ana_toddler.wav', f'{art}/sample_ana_toddler.wav')
    print("Done generating edge-tts kid voices")

if __name__ == '__main__':
    asyncio.run(main())
