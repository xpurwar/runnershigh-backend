from flask import Flask, request, jsonify
import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Root route for testing
@app.route('/')
def home():
    return "Flask server is running!"

# Route to synthesize speech
@app.route('/synthesize-speech', methods=['POST'])
def synthesize_speech():
    # Get the input text from the request
    data = request.json
    input_text = data.get('text', '')

    # Check if the input text is provided
    if not input_text:
        return jsonify({"error": "No text provided"}), 400

    # LMNT API details
    api_key = os.getenv("LMNT_API_KEY")
    api_url = "https://api.lmnt.com/v1/ai/speech"
    querystring = {
        "X-API-Key": api_key,
        "text": input_text,
        "voice": "480dd7fe-d9f2-45ef-bece-df09f5e2f5fa"
    }

    # Make the request to the LMNT API
    response = requests.request("GET", api_url, params=querystring)

    # Check if the request was successful
    if response.status_code == 200:
        # Save the audio content to a file
        with open("output_audio.mp3", "wb") as audio_file:
            audio_file.write(response.content)
        print("Audio saved as output_audio.mp3")
        return jsonify({"message": "Audio synthesized successfully"}), 200
    else:
        print(f"Failed to synthesize speech. Status code: {response.status_code}")
        print("Response:", response.text)
        return jsonify({"error": "Failed to synthesize speech"}), response.status_code

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)