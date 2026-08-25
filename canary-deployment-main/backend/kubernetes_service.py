from kubernetes import client, config


def get_deployment_status():

    # Load Kubernetes configuration
    try:
        config.load_incluster_config()
    except Exception:
        config.load_kube_config()

    apps = client.AppsV1Api()

    namespace = "canary-deploy"

    stable = apps.read_namespaced_deployment(
        name="simple-html-app-stable",
        namespace=namespace
    )

    canary = apps.read_namespaced_deployment(
        name="simple-html-app-canary",
        namespace=namespace
    )

    stable_pods = stable.status.ready_replicas or 0
    canary_pods = canary.status.ready_replicas or 0

    total = stable_pods + canary_pods

    if total == 0:
        stable_traffic = 0
        canary_traffic = 0
    else:
        stable_traffic = int((stable_pods * 100) / total)
        canary_traffic = int((canary_pods * 100) / total)

    rollout_status = "In Progress"
    rollout_progress = "0%"

    if stable_pods == 3 and canary_pods == 1:
        rollout_progress = "25%"

    elif stable_pods == 2 and canary_pods == 2:
        rollout_progress = "50%"

    elif stable_pods == 1 and canary_pods == 3:
        rollout_progress = "75%"

    elif stable_pods == 0 and canary_pods == 4:
        rollout_progress = "100%"
        rollout_status = "Completed"

    return {

        "stablePods": stable_pods,
        "canaryPods": canary_pods,

        "stableTraffic": f"{stable_traffic}%",
        "canaryTraffic": f"{canary_traffic}%",

        "stableStatus": "Healthy",
        "canaryStatus": "Healthy",

        "rolloutStatus": rollout_status,
        "rolloutProgress": rollout_progress,

        "lastUpdated": "Live"

    }