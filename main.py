import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)

# This completely eliminates the CORS block, allowing your GitHub site to talk to your Render server!
CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route('/api/process', methods=['POST', 'OPTIONS'])
def process_task():
    if request.method == 'OPTIONS':
        return jsonify({'status': 'ok'}), 200
        
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data package received'}), 400

    api_key = data.get('apiKey')
    input_value = data.get('inputValue')
    mode = data.get('mode', 'img')
    tool = data.get('tool', 'repurpose')

    if not api_key:
        return jsonify({'error': 'Missing Gemini API Key. Please paste it into your app workspace.'}), 400

    if not input_value:
        return jsonify({'error': 'Input workspace is empty. Please enter your video link or text.'}), 400

    try:
        # Initialize and configure the Gemini client
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')

        # Dynamically build the assignment prompt based on user selections
        if mode == 'vid':
            prompt_instruction = (
                f"Act as an expert content creator and scriptwriter. "
                f"The user wants you to perform a '{tool}' task on this YouTube video asset: {input_value}. "
                f"Analyze the reference and deliver an exceptionally engaging, structured script recap optimized for high retention."
            )
        elif mode == 'txt':
            prompt_instruction = f"Please process this script text block using your '{tool}' parameters: {input_value}"
        else:
            prompt_instruction = f"Generate an optimized, highly detailed visual conceptual prompt matching this description: {input_value}"

        # Request generation from Gemini
        response = model.generate_content(prompt_instruction)
        
        if response.text:
            return jsonify({'result': response.text})
        else:
            return jsonify({'error': 'Gemini returned an empty response. Please try again.'}), 500

    except Exception as e:
        return jsonify({'error': f"Gemini API Error: {str(e)}"}), 500

if __name__ == '__main__':
    # Dynamically grab the port Render gives us, defaulting to 5000 if local testing
    port = int(os.environ.get("PORT", 5000))
    # host='0.0.0.0' opens up the doors to the public web so Render can process traffic
    app.run(host='0.0.0.0', port=port)
