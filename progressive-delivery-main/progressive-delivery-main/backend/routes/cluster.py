from flask import Blueprint, jsonify

from services.k8s_service import k8s_service

cluster_bp = Blueprint("cluster", __name__)


@cluster_bp.route("/api/cluster")
def get_cluster():

    pods = k8s_service.get_pods()
    services = k8s_service.get_services()
    backend = k8s_service.get_backend()

    if isinstance(pods, dict) and pods.get("success") is False:
        return jsonify(pods), pods["status"]

    if isinstance(services, dict) and services.get("success") is False:
        return jsonify(services), services["status"]

    if isinstance(backend, dict) and backend.get("success") is False:
        return jsonify(backend), backend["status"]

    running = sum(
        1 for pod in pods.items
        if pod.status.phase == "Running"
    )

    return jsonify({

        "namespace": backend.metadata.namespace,

        "runningPods": running,

        "totalPods": len(pods.items),

        "services": len(services.items),

        "backendReplicas": backend.status.ready_replicas or 0,

        "backendAvailable": backend.status.available_replicas or 0

    })