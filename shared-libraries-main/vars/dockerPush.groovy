def call(imageName,imageTag) {

    sh """
    docker push ${imageName}:${imageTag}
    """
}