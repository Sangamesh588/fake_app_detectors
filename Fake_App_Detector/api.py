from flask import Flask, request, jsonify
from flask_cors import CORS

from main import get_results
from url_checker import check_url

app = Flask(__name__)
CORS(app)  # allow frontend from another port (e.g. localhost:3000) to call this


@app.get("/api/apps")
def api_apps():
    """
    Return risk scores for all candidate apps (for listing / table view).
    Response format:
    {
      "results": [
        { "appName": ..., "packageId": ..., "risk": ..., "reason": [...] },
        ...
      ]
    }
    """
    data = get_results()
    return jsonify(data)


@app.post("/api/check-url")
def api_check_url():
    """
    Check a single Play Store URL.
    Expected JSON body: { "url": "https://play.google.com/store/apps/details?id=..." }

    Returns what url_checker.check_url() returns.
    """
    body = request.get_json(silent=True) or {}
    url = body.get("url", "").strip()

    if not url:
        return jsonify({"error": "url is required"}), 400

    result = check_url(url)
    return jsonify(result)


if __name__ == "__main__":
    # Run the API server on http://localhost:5000
    app.run(host="0.0.0.0", port=5000, debug=True)
