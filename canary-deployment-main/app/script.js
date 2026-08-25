async function loadDeploymentStatus() {

    try {

        const API_URL = "/api/status";

        const response = await fetch(API_URL);

        if (!response.ok) {
            throw new Error(`HTTP Error: ${response.status}`);
        }

        const data = await response.json();

        document.getElementById("stablePods").textContent = data.stablePods;
        document.getElementById("canaryPods").textContent = data.canaryPods;

        document.getElementById("stableTraffic").textContent = data.stableTraffic;
        document.getElementById("canaryTraffic").textContent = data.canaryTraffic;

        document.getElementById("stableStatus").textContent = data.stableStatus;
        document.getElementById("canaryStatus").textContent = data.canaryStatus;

        document.getElementById("rolloutStatus").textContent = data.rolloutStatus;
        document.getElementById("rolloutProgress").textContent = data.rolloutProgress;

        document.getElementById("lastUpdated").textContent = data.lastUpdated;

    } catch (error) {

        console.error("Unable to load deployment status.", error);

    }

}

loadDeploymentStatus();

setInterval(loadDeploymentStatus, 5000);