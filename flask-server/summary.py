import openai
import json

openai.api_key = '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'

def generate_summary(file):
    with open(r"E:\Tim\sem 6\SE project new\flask-server\output.json") as f:
        data = json.load(f)
    sentences = []
    for dic in data:
        if file == dic['video_id']:
            sentences = dic['captions']
            break
    prompt = "Generate a concise summary (50 words maximum) and an appropriate title for a video based on the following descriptions of its frames:\n" + "\n".join(sentences)
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0125",
        messages=[
            {"role": "assistant", "content": prompt},
        ],
        max_tokens=100
    )
    
    generated_text = response.choices[0].message['content'].strip()
    
    return generated_text
