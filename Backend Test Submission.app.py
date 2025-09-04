from flask import Flask, request, jsonify, redirect
from datetime import datetime, timedelta
from logger import log_event
import random, string

app = Flask(__name__)
url_store = {}

def make_shortcode(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

@app.route('/shorturls', methods=['POST'])
def create_short_url():
    data = request.json
    o_url = data.get("url")
    s_code = data.get("shortcode")
    validity_minutes = data.get("validity", 30)

    if not o_url or not o_url.startswith("http"):
        log_event("backend", "error", "handler", "Invalid URL input")
        return jsonify({"error": "Invalid URL"}), 400

    if not s_code or s_code in url_store:
        s_code = make_shortcode()
        while s_code in url_store:
            s_code = make_shortcode()

    expiry_time = datetime.now() + timedelta(minutes=validity_minutes)

    url_store[s_code] = {
        "original_url": o_url,
        "created_at": datetime.now(),
        "expiry": expiry_time,
        "clicks": [],
    }

    log_event("backend", "info", "service", f"Short URL {s_code} created for {o_url}")

    return jsonify({
        "shortlink": f"http://localhost:5000/{s_code}",
        "expiry": expiry_time.isoformat()
    }), 201

@app.route('/<s_code>', methods=['GET'])
def redirect_short_url(s_code):
    url_info = url_store.get(s_code)
    if not url_info:
        log_event("backend", "error", "handler", f"Shortcode {s_code} not found")
        return jsonify({"error": "Shortcode not found"}), 404

    if datetime.now() > url_info["expiry"]:
        log_event("backend", "warn", "handler", f"Shortcode {s_code} expired")
        return jsonify({"error": "Shortcode expired"}), 410

    click_data = {
        "timestamp": datetime.now().isoformat(),
        "referrer": request.referrer,
        "user_agent": request.user_agent.string
    }
    url_info["clicks"].append(click_data)

    log_event("backend", "info", "service", f"Shortcode {s_code} accessed")

    return redirect(url_info["original_url"])

if __name__ == "__main__":
    app.run(debug=True)
