from flask import Flask, request, jsonify, redirect
import string, random

app = Flask(__name__)

# in-memory storage (temporary)
url_store = {}

# generate short code
def generate_code(length=6):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))


# POST: shorten URL
@app.route("/shorten", methods=["POST"])
def shorten():
    data = request.get_json()

    if not data or "url" not in data:
        return jsonify({"error": "No URL provided"}), 400

    original_url = data["url"]

    # ensure https
    if not original_url.startswith("http"):
        original_url = "https://" + original_url

    code = generate_code()

    url_store[code] = original_url

    short_url = request.host_url + code

    return jsonify({
        "original_url": original_url,
        "short_url": short_url
    })


# redirect route
@app.route("/<code>")
def redirect_url(code):
    if code in url_store:
        return redirect(url_store[code])
    return jsonify({"error": "Invalid URL"}), 404


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)