# Mission 033 - Flask Health Endpoint
# Fixed solution
from flask import Flask, jsonify

def create_app():
    app = Flask(__name__)

    @app.route("/health")
    def health():
        status = {"status": "ok", "service": "api-gateway"}
        return jsonify(status), 200

    return app
