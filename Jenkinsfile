pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                // Checkout the code from the repository
                git branch: 'main', url: 'https://github.com/your-repo/your-project.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    // Build the Docker image using the Dockerfile
                    sh 'docker build -t ml-pipeline-image .'
                }
            }
        }

        stage('Run Tests Inside Docker Container') {
            steps {
                script {
                    // Run a temporary Docker container and execute the tests inside
                    sh '''
                    docker run --rm ml-pipeline-image \
                    bash -c "pytest --maxfail=1 --disable-warnings"
                    '''
                }
            }
        }

        stage('Run ML Training') {
            steps {
                script {
                    // Run the Docker container for training after tests pass
                    sh '''
                    docker run --rm ml-pipeline-image \
                    bash -c "python app/train.py"
                    '''
                }
            }
        }
    }

    post {
        always {
            // Clean up workspace and remove dangling Docker images
            sh 'docker system prune -f'
        }
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed. Check logs for errors.'
        }
    }
}
