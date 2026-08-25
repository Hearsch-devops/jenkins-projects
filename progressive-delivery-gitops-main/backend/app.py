from flask import Flask, jsonify
from routes.rollout import rollout_bp
from routes.analysis import analysis_bp
from routes.replicasets import replicaset_bp
from routes.cluster import cluster_bp

app = Flask(__name__)

app.register_blueprint(rollout_bp)
app.register_blueprint(analysis_bp)
app.register_blueprint(replicaset_bp)
app.register_blueprint(cluster_bp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)