def call(namespace,imageName,imageTag) {

    sh """
    sed -i 's|IMAGE_PLACEHOLDER|${imageName}:${imageTag}|g' k8/${namespace}/deployment.yaml

    kubectl apply -f k8/${namespace}/deployment.yaml
    kubectl apply -f k8/${namespace}/service.yaml

    kubectl rollout status deployment/simple-html-app -n ${namespace}
    """
}