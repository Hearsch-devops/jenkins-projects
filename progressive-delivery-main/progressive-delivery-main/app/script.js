async function fetchAPI(endpoint) {

    const response = await fetch(endpoint);

    if (!response.ok) {
        throw new Error(`${endpoint}: HTTP ${response.status}`);
    }

    return response.json();
}


async function loadDashboard() {

    try {

        // =========================================
        // Fetch all backend APIs
        // =========================================

        const [
            rollout,
            analysis,
            replicasets,
            cluster
        ] = await Promise.all([

            fetchAPI("/api/rollout"),
            fetchAPI("/api/analysis"),
            fetchAPI("/api/replicasets"),
            fetchAPI("/api/cluster")

        ]);


        // =========================================
        // Rollout Summary
        // =========================================

        document.getElementById("rolloutName").textContent =
            rollout.name ?? "Unknown";

        document.getElementById("rolloutStatus").textContent =
            rollout.status ?? "Unknown";

        document.getElementById("revision").textContent =
            rollout.revision ?? "Unknown";

        document.getElementById("step").textContent =
            rollout.currentStep ?? "Unknown";

        document.getElementById("trafficWeight").textContent =
            rollout.trafficWeight ?? "0%";


        // =========================================
        // ReplicaSets
        // =========================================

        document.getElementById("stableReplica").textContent =
            replicasets.current?.name ?? "None";

        document.getElementById("previousReplica").textContent =
            replicasets.previous?.name ?? "None";

        document.getElementById("currentImage").textContent =
            replicasets.current?.image ?? "Unknown";


        // =========================================
        // Analysis
        // =========================================

        document.getElementById("analysisTemplate").textContent =
            rollout.analysisTemplate ?? "None";

        document.getElementById("analysisRuns").textContent =
            analysis.total ?? 0;

        document.getElementById("analysisStatus").textContent =
            analysis.latest?.phase ?? "No Analysis";

        document.getElementById("lastUpdated").textContent =
            new Date().toLocaleString();


        // =========================================
        // Cluster Health
        // =========================================

        document.getElementById("podsRunning").textContent =
            `${cluster.runningPods ?? 0} / ${cluster.totalPods ?? 0}`;

        document.getElementById("backendStatus").textContent =
            cluster.backendAvailable > 0
                ? "Healthy"
                : "Unavailable";

        document.getElementById("healthStatus").textContent =
            rollout.status ?? "Unknown";

        document.getElementById("namespaceStatus").textContent =
            cluster.namespace ?? "Unknown";

        document.getElementById("serviceCount").textContent =
            cluster.services ?? 0;


        // =========================================
        // Deployment Progress
        // =========================================

        document.getElementById("desiredReplicas").textContent =
            rollout.desiredReplicas ?? 0;

        document.getElementById("readyReplicas").textContent =
            rollout.readyReplicas ?? 0;

        document.getElementById("availableReplicas").textContent =
            rollout.availableReplicas ?? 0;

        document.getElementById("currentPhase").textContent =
            rollout.status ?? "Unknown";


        console.log("Dashboard updated successfully.");

    } catch (error) {

        console.error(
            "Unable to load Progressive Delivery dashboard:",
            error
        );

    }

}


// Initial dashboard load
loadDashboard();


// Refresh dashboard every 5 seconds
setInterval(loadDashboard, 5000);