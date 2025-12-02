from flask import Flask, request, jsonify, render_template
import main
import requests

app = Flask(__name__)

HF_SPACE_URL = "https://kevinSteele-WebSummarizer.hf.space/summarize"

@app.route("/", methods=["GET"])
def index():
    return render_template("web.html")

@app.route("/summarize", methods=["POST"])
def summarize_endpoint():
    payload = request.get_json(force=True) or {}
    url = payload.get("url", "").strip()
    if not url:
        return "Missing 'url' parameter", 400
    try:
        main.set_wiki_link(url)
        html = main.fetch_wiki_content()
        text = main.parse_wiki_content(html)
        
        hf_response = requests.post(HF_SPACE_URL, json={"text": text}, timeout=60)
        if hf_response.status_code != 200:
            return f"HF error: {hf_response.text}", 500
        
        summary = hf_response.json()["summary"]
        return jsonify({"summary": summary})
    except Exception as e:
        return str(e), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=False)