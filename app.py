import os
from flask import Flask, request, jsonify
from flask_cors import CORS
# Make sure you are using the correct library
import google.generativeai as genai

app = Flask(__name__)
CORS(app)  # Allows your GitHub Pages frontend to communicate with Render

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

        # 1. Configure the library with the user's provided API key
        genai.configure(api_key=api_key)

        # 2. Use the stable model generation method
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # 3. Create a clean prompt combining the tool and the user input
        prompt = f"Act as a content creation assistant. Tool: {tool}. Mode: {mode}. Input data: {input_value}"
        
        # 4. Generate the content safely
        response = model.generate_content(prompt)

        # Return the response text back to your index.html frontend
        return jsonify({'result': response.text})

    except Exception as e:
        # This catches any errors and sends them safely to your screen
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Render requires the app to bind to 0.0.0.0 and the assigned PORT environment variable
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
