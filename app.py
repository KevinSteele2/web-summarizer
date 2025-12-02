from flask import Flask, request, jsonify, render_template
import os
import requests

app = Flask(__name__)

HF_RUN = "https://kevinSteele-WebSummarizer.hf.space/run/predict"

@app.route("/")
def index():
    return render_template("web.html")

@app.route("/summarize", methods=["POST"])
def summarize():
    payload = request.get_json(silent=True) or {}
    url = payload.get("url", "").strip()
    if not url:
        return jsonify({"error": "Missing 'url' parameter"}), 400

    try:
        import main
        main.set_wiki_link(url)
        html = main.fetch_wiki_content()
        text = main.parse_wiki_content(html)

        resp = requests.post(HF_RUN, json={"data": [text]}, timeout=60)
        hf_json = resp.json()  
        summary = None
        if isinstance(hf_json, dict):
            data = hf_json.get("data")
            if isinstance(data, list) and len(data) > 0:
                summary = data[0]
            else:
                summary = hf_json.get("summary") or hf_json.get("result") or hf_json.get("output")
        elif isinstance(hf_json, list) and len(hf_json) > 0:
            summary = hf_json[0]
        elif isinstance(hf_json, str):
            summary = hf_json

        if not summary:
            return jsonify({"error": "Could not extract summary", "hf_response": hf_json}), 502

        return jsonify({"summary": summary})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)