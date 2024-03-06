
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests
from datetime import datetime

app = Flask(__name__)
CORS(app)

OPENAI_API_KEY = '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'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send-message', methods=['POST'])
def send_message():
    data = request.json
    message = data['message']
    response_text = handle_custom_responses(message)
    return jsonify({'text': response_text})

def handle_custom_responses(text):
    if "time" in text.lower():
        current_time = datetime.now().strftime("%I:%M %p")
        return f"The current time is {current_time}"
    elif "what is your name" in text.lower():
        return "I am BPS AI, your virtual assistant!"
    elif "who created you" in text.lower():
        return "I was created by Ashwath Sanjai for his gallery walk project in his 8th grade!"
    else:
        return chat_with_openai(text)

def chat_with_openai(user_message):
    headers = {
        'Authorization': f'Bearer {OPENAI_API_KEY}'
    }
    payload = {
        'model': 'gpt-3.5-turbo',  # Ensure this matches the model you intend to use
        'messages': [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_message}
        ]
    }
    try:
        response = requests.post('https://api.openai.com/v1/chat/completions', json=payload, headers=headers)
        if response.status_code == 200:
            text = response.json()['choices'][0]['message']['content']
            return text
        else:
            error_message = response.json().get('error', {}).get('message', 'Unknown error')
            print(f"Error fetching response from OpenAI: {error_message}")
            return f'Failed to fetch response from OpenAI. Error: {error_message}'
    except Exception as e:
        return f'An exception occurred: {str(e)}'
if __name__ == '__main__':
    app.run(debug=True)