def call() {

    withCredentials([
        usernamePassword(
            credentialsId: 'docker_login',
            usernameVariable: 'DOCKER_USER',
            passwordVariable: 'DOCKER_PASS'
        )
    ]) {

        sh '''
        echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
        '''
    }
}