from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
CORS(app)  # This allows your GitHub Pages frontend to connect without blockages

# CRITICAL: This route must match exactly what the frontend is calling
@app.route('/api/process', methods=['POST'])
def process_pipeline():
    try:
        data = request.json
        api_key = data.get('apiKey')
        input_value = data.get('inputValue')
        mode = data.get('mode')
        tool = data.get('tool')

        if not api_key:
            return jsonify({"error": "Missing API Key"}), 400

        # Configure Gemini inside the backend using the updated model naming layout
        genai.configure(api_key=api_key)
        
        # FIXED MODEL STRING: Using the stable naming convention to bypass the v1beta 404 issue
        model = genai.GenerativeModel('gemini-1.5-flash-latest')

        # Crafting the prompt based on what tool was clicked
        prompt = f"Perform {tool} mode operational tasks on this context asset: {input_value}"
        
        response = model.generate_content(prompt)
        
        return jsonify({"result": response.text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Base route to verify the server is alive
@app.route('/', methods=['GET'])
def home():
    return jsonify({"status": "Shotify Backend Running Successfully!"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
