from flask import Flask, jsonify
from kubernetes_service import get_deployment_status

app = Flask(__name__)


@app.route("/")
def home():
    return jsonify({
        "message": "Deployment Dashboard Backend Running"
    })


@app.route("/api/status")
def status():
    return jsonify(get_deployment_status())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)