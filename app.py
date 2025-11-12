from flask import Flask, request, jsonify, render_template
import main

app = Flask(__name__)

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
        summary = main.summarize_text(text)
        return jsonify({"summary": summary})
    except Exception as e:
        return str(e), 500

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)