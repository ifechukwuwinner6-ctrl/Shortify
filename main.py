from flask import Flask, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# This allows your GitHub website to talk to your phone server without blocks
@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
    return response

@app.route('/api/process', Methoden=['POST', 'OPTIONS'])
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
        return jsonify({'error': 'Missing Gemini API Key'}), 400

    try:
        # Configure the Gemini Engine with the key sent from your phone interface
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')

        # Create a custom instruction prompt based on what tool is selected
        if mode == 'vid':
            prompt_instruction = f"Act as an expert content creator. The user wants to {tool} this video resource link: {input_value}. Generate a high-quality, engaging script overview or recap."
        elif mode == 'txt':
            prompt_instruction = f"Please {tool} the following text or script content: {input_value}"
        else:
            prompt_instruction = f"Analyze and create a detailed visual design prompt layout for this concept: {input_value}"

        # Get the creative response from Google Gemini
        response = model.generate_content(prompt_instruction)
        
        return jsonify({'result': response.text})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Runs the server locally on port 5000
    app.run(host='127.0.0.1', port=5000, debug=True)
