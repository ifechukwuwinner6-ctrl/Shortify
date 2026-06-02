import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from youtube_transcript_api import YouTubeTranscriptApi
from google import genai

app = Flask(__name__)
# CORS allows your GitHub frontend to securely talk to this Python server
CORS(app)

def extract_video_id(url):
    """Helper to pull the 11-character ID from any YouTube link."""
    if "youtu.be/" in url:
        return url.split("youtu.be/")[1].split("?")[0]
    elif "v=" in url:
        return url.split("v=")[1].split("&")[0]
    return url

@app.route('/api/process', methods=['POST'])
def process_workspace():
    data = request.json or {}
    api_key = data.get('apiKey')
    input_value = data.get('inputValue', '')
    mode = data.get('mode', 'vid') # 'img', 'vid', or 'txt'
    tool = data.get('tool', 'repurpose') # 'trim', 'repurpose', 'analyze'

    if not api_key:
        return jsonify({"error": "Missing Gemini API Key"}), 400
    if not input_value:
        return jsonify({"error": "Input field cannot be empty"}), 400

    try:
        # Initialize the Gemini Client dynamically with the user's key
        client = genai.Client(api_key=api_key)
        
        # --- MODE 1: VIDEO PROCESSING (Core Feature) ---
        if mode == 'vid':
            video_id = extract_video_id(input_value)
            try:
                srt = YouTubeTranscriptApi.get_transcript(video_id)
                transcript_text = " ".join([element['text'] for element in srt])
            except Exception as e:
                return jsonify({"error": f"Failed to get YouTube transcript: {str(e)}"}), 400

            # Tailor the prompt based on which bottom tool icon is active
            if tool == 'trim':
                prompt = f"Analyze this transcript and output ONLY the exact start and end timestamps of the most viral hook zone. Transcript: {transcript_text}"
            elif tool == 'analyze':
                prompt = f"Provide a structural breakdown, retention critique, and audience engagement score for this content transcript: {transcript_text}"
            else: # repurpose
                prompt = f"Identify the best 30-60s viral segment from this text. Output 3 catchy headlines, the timestamp range, and a optimized caption with hashtags. Transcript: {transcript_text}"

        # --- MODE 2: TEXT PROCESSING ---
        elif mode == 'txt':
            if tool == 'analyze':
                prompt = f"Analyze the tone, structure, and readability of this text: {input_value}"
            else:
                prompt = f"Rewrite and repurpose this text into a viral short-form video script with scene directions: {input_value}"

        # --- MODE 3: IMAGE PROMPTING CONTENT ---
        elif mode == 'img':
            prompt = f"Turn this basic description into a highly detailed, cinematic prompt for an AI image generator to create a viral social media graphic: {input_value}"

        # Run the generation using the fast gemini-2.5-flash engine
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        
        return jsonify({
            "status": "success",
            "mode_executed": mode,
            "tool_executed": tool,
            "result": response.text
        })

    except Exception as e:
        return jsonify({"error": f"AI Engine Error: {str(e)}"}), 500

if __name__ == '__main__':
    # Runs on port 5000—perfect for local mobile testing or hosting
    app.run(host='0.0.0.0', port=5000, debug=True)
