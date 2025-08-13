from flask import Flask, render_template, request, jsonify, url_for
from google import genai
from google.genai import types
import pathlib
from flask import session
import secrets
from dotenv import load_dotenv
import os
import game

load_dotenv(override=True)  
app = Flask(__name__)
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY")) # Ensure the api key is known 
app.secret_key = secrets.token_hex(32)  # Needed for session support
grid = game.template

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

@app.route('/naughtsandcrosses')
def naughtsandcrosses():
    return render_template('naughtsandcrosses.html', grid=grid)

@app.route('/reset', methods=['POST'])
def reset():
    session.pop('history', None)
    return jsonify({'status': 'reset'})

@app.route("/play", methods=["POST"])
def play():
    global grid
    data = request.json
    row, col = data["row"], data["col"]

    # Player move
    if grid[row][col] == "":
        grid[row][col] = game.HUMAN # Human symbol
    elif game.winCheck(grid) is not None:
        return jsonify({"error": "Game over"}), 400
    else:
        return jsonify({"error": "Invalid move"}), 400

    # Check if player won
    if game.winCheck(grid) is not None:
        return jsonify({"grid": grid, "winner": game.winCheck(grid)})

    # AI move
    ai_row, ai_col = game.findBestMove(grid)
    grid[ai_row][ai_col] = game.AI

    return jsonify({"grid": grid, "winner": game.winCheck(grid)})

@app.route("/replay", methods=["POST"])
def replay():
    global grid
    for row in range(len(grid)):
        for column in range(len(grid[row])):
            grid[row][column] = ""
    return jsonify({"grid": grid})
if __name__ == '__main__':
    app.run(debug=True)
