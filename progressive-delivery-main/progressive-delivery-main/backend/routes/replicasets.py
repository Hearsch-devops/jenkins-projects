from flask import Blueprint, jsonify

from services.k8s_service import k8s_service

replicaset_bp = Blueprint("replicasets", __name__)


@replicaset_bp.route("/api/replicasets")
def get_replicasets():

    rs_list = k8s_service.get_replicasets()

    if isinstance(rs_list, dict) and rs_list.get("success") is False:
        return jsonify(rs_list), rs_list["status"]

    items = sorted(
        rs_list.items,
        key=lambda x: x.metadata.creation_timestamp,
        reverse=True
    )

    current = items[0] if len(items) > 0 else None
    previous = items[1] if len(items) > 1 else None

    return jsonify({

        "current": {
            "name": current.metadata.name if current else None,
            "replicas": current.status.replicas if current else 0,
            "ready": current.status.ready_replicas if current else 0,
            "image": current.spec.template.spec.containers[0].image if current else None
        },

        "previous": {
            "name": previous.metadata.name if previous else None,
            "replicas": previous.status.replicas if previous else 0,
            "ready": previous.status.ready_replicas if previous else 0,
            "image": previous.spec.template.spec.containers[0].image if previous else None
        }

    })