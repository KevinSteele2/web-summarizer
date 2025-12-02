from flask import Flask, request, jsonify, render_template
import os
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
        return jsonify({"error": "Missing 'url' parameter"}), 400

    try:
        import main

        main.set_wiki_link(url)
        html = main.fetch_wiki_content()
        text = main.parse_wiki_content(html)

        hf_response = requests.post(HF_SPACE_URL, json={"text": text}, timeout=60)

        try:
            hf_json = hf_response.json()
        except ValueError:
            return jsonify({
                "error": "Hugging Face Space returned non-JSON response",
                "raw": hf_response.text,
                "status_code": hf_response.status_code
            }), 502

        if hf_response.status_code != 200:
            return jsonify({
                "error": "Hugging Face Space returned error",
                "status_code": hf_response.status_code,
                "detail": hf_json
            }), 502

        summary = hf_json.get("summary") or hf_json.get("result") or hf_json.get("output")
        if not summary:
            return jsonify({
                "error": "Hugging Face response missing expected 'summary' field",
                "hf_response": hf_json
            }), 502

        return jsonify({"summary": summary})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port, debug=False)