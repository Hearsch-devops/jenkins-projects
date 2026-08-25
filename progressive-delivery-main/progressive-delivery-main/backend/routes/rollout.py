from flask import Blueprint, jsonify

from services.k8s_service import k8s_service

rollout_bp = Blueprint("rollout", __name__)


@rollout_bp.route("/api/rollout")
def get_rollout():

    rollout = k8s_service.get_rollout()

    if isinstance(rollout, dict) and rollout.get("success") is False:
        return jsonify(rollout), rollout["status"]

    status = rollout.get("status", {})
    spec = rollout.get("spec", {})

    # -----------------------------------------
    # Get Rollout Steps
    # -----------------------------------------

    steps = (
        spec.get("strategy", {})
        .get("canary", {})
        .get("steps", [])
    )

    # -----------------------------------------
    # Current Step
    # -----------------------------------------

    current_step_index = status.get("currentStepIndex")

    if current_step_index is None or current_step_index >= len(steps):
        current_step = "Completed"
    else:
        current_step = f"{current_step_index + 1}/{len(steps)}"

    # -----------------------------------------
    # Traffic Weight
    # -----------------------------------------

    traffic_weight = 0

    if current_step_index is None:
        traffic_weight = 100
    else:
        for i in range(min(current_step_index + 1, len(steps))):

            step = steps[i]

            if "setWeight" in step:
                traffic_weight = step["setWeight"]

    # -----------------------------------------
    # Analysis Template
    # -----------------------------------------

    analysis_template = "None"

    for step in steps:

        analysis = step.get("analysis")

        if analysis:

            templates = analysis.get("templates", [])

            if templates:
                analysis_template = templates[0].get(
                    "templateName",
                    "Unknown"
                )

            break

    # -----------------------------------------
    # API Response
    # -----------------------------------------

    return jsonify({

        "name": rollout["metadata"]["name"],

        "status": status.get("phase", "Unknown"),

        "revision": status.get("currentPodHash", "Unknown"),

        "desiredReplicas": spec.get("replicas", 0),

        "readyReplicas": status.get("readyReplicas", 0),

        "availableReplicas": status.get("availableReplicas", 0),

        "currentStep": current_step,

        "trafficWeight": f"{traffic_weight}%",

        "analysisTemplate": analysis_template

    })