from summarizer import Summarizer
import json

model=Summarizer()
def summarize(file):
    with open(r"E:\Tim\sem 6\SE project new\flask-server\output.json") as f:
        data = json.load(f)
    text = ""
    for dic in data:
        if file == dic['video_id']:
            for s in dic['captions']:
                text += s + ". "
        break
    print("\nText:",text)
    summary=model(text)
    print("\nSummary: ",summary)
    return summary
