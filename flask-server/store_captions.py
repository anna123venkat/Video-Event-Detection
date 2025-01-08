import json
import os

def add_captions_to_json(video_id, captions):
    if os.path.exists('output.json'):
        with open('output.json', 'r') as f:
            data = json.load(f)
    else:
        data = []

    data.append({"video_id": video_id, "captions": captions})

    with open('output.json', 'w') as f:
        json.dump(data, f, indent=4)
