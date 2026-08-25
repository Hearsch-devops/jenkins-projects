def call() {

    if(env.BRANCH_NAME == 'staging') {
        env.IMAGE_TAG = "staging-${env.BUILD_NUMBER}"
    }

    if(env.BRANCH_NAME == 'main') {
        env.IMAGE_TAG = "prod-${env.BUILD_NUMBER}"
    }

    echo "Image Tag: ${env.IMAGE_TAG}"
}