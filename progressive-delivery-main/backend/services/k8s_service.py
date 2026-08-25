from kubernetes import client, config
from kubernetes.client.rest import ApiException

from config import (
    NAMESPACE,
    ROLLOUT_NAME,
    BACKEND_DEPLOYMENT
)


class KubernetesService:

    def __init__(self):
        """
        Load Kubernetes configuration.
        If running inside Kubernetes, use ServiceAccount.
        Otherwise use local kubeconfig.
        """

        try:
            config.load_incluster_config()
        except Exception:
            config.load_kube_config()

        self.apps = client.AppsV1Api()
        self.core = client.CoreV1Api()
        self.custom = client.CustomObjectsApi()

    # ---------------------------------------------------
    # Rollout
    # ---------------------------------------------------

    def get_rollout(self):

        try:

            rollout = self.custom.get_namespaced_custom_object(
                group="argoproj.io",
                version="v1alpha1",
                namespace=NAMESPACE,
                plural="rollouts",
                name=ROLLOUT_NAME
            )

            return rollout

        except ApiException as e:

            return {
                "success": False,
                "message": str(e),
                "status": e.status
            }

    # ---------------------------------------------------
    # Analysis Runs
    # ---------------------------------------------------

    def get_analysis(self):

        try:

            analysis = self.custom.list_namespaced_custom_object(
                group="argoproj.io",
                version="v1alpha1",
                namespace=NAMESPACE,
                plural="analysisruns"
            )

            return analysis

        except ApiException as e:

            return {
                "success": False,
                "message": str(e),
                "status": e.status
            }

    # ---------------------------------------------------
    # ReplicaSets
    # ---------------------------------------------------

    def get_replicasets(self):

        try:

            replicasets = self.apps.list_namespaced_replica_set(
                namespace=NAMESPACE
            )

            return replicasets

        except ApiException as e:

            return {
                "success": False,
                "message": str(e),
                "status": e.status
            }

    # ---------------------------------------------------
    # Pods
    # ---------------------------------------------------

    def get_pods(self):

        try:

            pods = self.core.list_namespaced_pod(
                namespace=NAMESPACE
            )

            return pods

        except ApiException as e:

            return {
                "success": False,
                "message": str(e),
                "status": e.status
            }

    # ---------------------------------------------------
    # Services
    # ---------------------------------------------------

    def get_services(self):

        try:

            services = self.core.list_namespaced_service(
                namespace=NAMESPACE
            )

            return services

        except ApiException as e:

            return {
                "success": False,
                "message": str(e),
                "status": e.status
            }

    # ---------------------------------------------------
    # Backend Deployment
    # ---------------------------------------------------

    def get_backend(self):

        try:

            deployment = self.apps.read_namespaced_deployment(
                name=BACKEND_DEPLOYMENT,
                namespace=NAMESPACE
            )

            return deployment

        except ApiException as e:

            return {
                "success": False,
                "message": str(e),
                "status": e.status
            }
    
# ---------------------------------------------------
# Singleton instance
# ---------------------------------------------------
k8s_service = KubernetesService()

