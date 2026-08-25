from flask import Blueprint, jsonify

from services.k8s_service import k8s_service

analysis_bp = Blueprint("analysis", __name__)


@analysis_bp.route("/api/analysis")
def get_analysis():

    analysis = k8s_service.get_analysis()

    if analysis.get("success") is False:
        return jsonify(analysis), analysis["status"]

    items = analysis.get("items", [])

    if not items:
        return jsonify({
            "total": 0,
            "successful": 0,
            "failed": 0,
            "latest": None
        })

    successful = 0
    failed = 0

    for run in items:

        phase = run.get("status", {}).get("phase", "")

        if phase == "Successful":
            successful += 1

        elif phase == "Failed":
            failed += 1

    latest = sorted(
        items,
        key=lambda x: x["metadata"]["creationTimestamp"],
        reverse=True
    )[0]

    return jsonify({

        "total": len(items),

        "successful": successful,

        "failed": failed,

        "latest": {
            "name": latest["metadata"]["name"],

            "phase": latest.get(
                "status", {}
            ).get("phase", "Unknown"),

            "started": latest["metadata"]["creationTimestamp"],

            "template": (
                latest.get("spec", {})
                .get("metrics", [{}])[0]
                .get("name", "Unknown")
            )
        }

    })