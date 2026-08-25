def call(imageName,imageTag) {

    sh """
    docker build -t ${imageName}:${imageTag} .
    """
}