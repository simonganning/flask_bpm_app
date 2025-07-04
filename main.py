import os
from flask import Flask, request, jsonify
from openai import OpenAI

app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route('/', methods=['GET', 'POST'])
def ask_how_are_you():
    data = request.get_json()
    song_info = data.get("trackID")
    
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[{
            "role": "user",
            "content": f"Provide BPM and Energy of a song in format BPM:<BPM> , Energy: <Energy>. NO TEXT AT ALL! (scale from 0-100) for song, {song_info}. If you don't know, make an educated guess."
        }]
    )
    message = completion.choices[0].message.content.strip()

    try:
        parts = message.split(',')
        bpm = int(parts[0].split(':')[1].strip())
        energy = int(parts[1].split(':')[1].strip())
        return jsonify({'bpm': bpm, 'energy': energy})
    except Exception as e:
        return jsonify({'error': 'Failed to parse response', 'raw': message}), 500
    
if __name__ == '__main__':
    app.run()
