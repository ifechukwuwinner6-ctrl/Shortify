from flask import Flask, request, jsonify, redirect
from flask_cors import CORS
import google.generativeai as genai
import os

app = Flask(__name__)
CORS(app)  # This stops browser CORS blockages from your GitHub frontend

# AUTOMATIC REDIRECT: When you tap the Render link, it automatically forwards you to your working app page!
@app.route('/', methods=['GET'])
def home_redirect():
    return redirect("https://ifechukwuwinner6-ctrl.github.io/Shortify/app.html")

# The secure processing pipeline endpoint your frontend connects to
@app.route('/api/process', methods=['POST'])
def process_pipeline():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No data received"}), 400
            
        api_key = data.get('apiKey')
        input_value = data.get('inputValue')
        mode = data.get('mode', 'vid')
        tool = data.get('tool', 'repurpose')

        if not api_key:
            return jsonify({"error": "Missing Gemini API Key"}), 400
        if not input_value:
            return jsonify({"error": "Missing input context or URL"}), 400

        # Configure the Google AI engine with the incoming user key
        genai.configure(api_key=api_key)
        
        # Using the accurate stable version string to prevent 404s
        model = genai.GenerativeModel('gemini-1.5-flash-latest')

        # Prompt compiler layout mapping
        prompt = f"Act as an AI creator workspace engine. Process this item for workspace tool '{tool}' under mode '{mode}': {input_value}"
        
        response = model.generate_content(prompt)
        
        return jsonify({"result": response.text}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
