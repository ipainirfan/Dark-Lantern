import json, os

voice_dir = r"C:\Users\blazy\OneDrive\Pictures\AI Content\Dark Lantern\DL17 - The Wallace Line\voice_grady"
lines_data = json.load(open(os.path.join(voice_dir, "lines.json")))["lines"]
plain_lines = [item["text"] for item in lines_data]

with open(os.path.join(voice_dir, "lines_list.json"), "w") as f:
    json.dump(plain_lines, f, indent=2)

print("Created lines_list.json")
