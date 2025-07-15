import os, asyncio
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import google.generativeai as genai
from crawler import crawl_webpage

# Load API key
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")

# Flask app
app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "🌐 Web Q&A app is running!"

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    url = data.get("url")
    question = data.get("question")

    if not url or not question:
        return jsonify({"status": "error", "message": "Both URL and question are required."}), 400

    try:
        # Run the async crawl
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        page_content = loop.run_until_complete(crawl_webpage(url))
        loop.close()

        if not page_content.strip():
            return jsonify({"status": "error", "message": "No readable content found on the page."}), 400

        # Create prompt for Gemini
        prompt = f"""
        You are given content from a website. Answer the user's question based on that content.

        Website Content:
        {page_content[:10000]}  # Truncate if very large

        Question: {question}

        Answer:"""

        response = model.generate_content(prompt)

        return jsonify({"status": "success", "answer": response.text})
    except Exception as e:
        print("Error:", e)
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
