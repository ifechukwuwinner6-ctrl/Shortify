import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
CORS(app) 

@app.route('/api/process', methods=['POST'])
def process_data():
    try:
        data = request.get_json()
        api_key = data.get('apiKey')
        input_value = data.get('inputValue')
        mode = data.get('mode', 'vid')
        tool = data.get('tool', 'repurpose')

        if not api_key or not input_value:
            return jsonify({'error': 'Missing required fields'}), 400

        # This configures your specific API key dynamically
        genai.configure(api_key=api_key)

        # CALLING THE NEW STABLE API MODEL (Fixes the 404 version error)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"Act as a content creation assistant. Tool: {tool}. Mode: {mode}. Input: {input_value}"
        response = model.generate_content(prompt)

        return jsonify({'result': response.text})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
