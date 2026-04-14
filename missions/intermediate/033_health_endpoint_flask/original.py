# Mission 033 - Flask Health Endpoint
# Fix the 2 bugs in this script.
from flask import Flask, json, make_response

def create_app():
    app = Flask(__name__)

    @app.route("/health")
    def health():
        status = {"status": "ok", "service": "api-gateway"}
        response = make_response(json.dumps(status))  # BUG 1: should use jsonify
        response.status_code = 500  # BUG 2: should be 200
        return response

    return app
