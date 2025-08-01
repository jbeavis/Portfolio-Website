from flask import Flask, render_template, request, jsonify, url_for
from google import genai
from google.genai import types
import pathlib
from flask import session
import secrets

app = Flask(__name__)
client = genai.Client(api_key="AIzaSyANnYFseMBt1HD3nDTdJ9m6Wtpu7E1_SN8")
app.secret_key = secrets.token_hex(32)  # Needed for session support

# Load CV once at startup
cv_path = pathlib.Path('static/files/James Beavis CV.pdf')
cv_data = types.Part.from_bytes(
    data=cv_path.read_bytes(),
    mime_type='application/pdf'
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_message = request.json.get('message')

    if 'history' not in session:
        session['history'] = []

    # Add user's message to history
    session['history'].append({"role": "user", "content": user_message})

    # Convert session history into Gemini format
    history = [cv_data]
    for msg in session['history']:
        history.append(msg['content'])

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=history
    )

    # Add bot's reply to history
    session['history'].append({"role": "model", "content": response.text})

    return jsonify({'response': response.text})

@app.route('/reset', methods=['POST'])
def reset():
    session.pop('history', None)
    return jsonify({'status': 'reset'})

if __name__ == '__main__':
    app.run(debug=True)
