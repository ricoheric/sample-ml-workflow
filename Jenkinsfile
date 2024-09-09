pipeline {
    agent any

    environment {
        // Load all credentials from Jenkins credentials store
        MLFLOW_TRACKING_URI = credentials('mlflow-tracking-uri')
        AWS_ACCESS_KEY_ID = credentials('aws-access-key')
        AWS_SECRET_ACCESS_KEY = credentials('aws-secret-key')
        BACKEND_STORE_URI = credentials('backend-store-uri')
        ARTIFACT_ROOT = credentials('artifact-root')
    }

    stages {
        stage('Checkout') {
            steps {
                // Checkout the code from the repository
                git branch: 'main', url: 'https://github.com/JedhaBootcamp/sample-ml-workflow.git'
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
                    sh """
                    docker run --rm \
                    -e MLFLOW_TRACKING_URI=$MLFLOW_TRACKING_URI \
                    -e AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID \
                    -e AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY \
                    -e BACKEND_STORE_URI=$BACKEND_STORE_URI \
                    -e ARTIFACT_ROOT=$ARTIFACT_ROOT \
                    ml-pipeline-image \
                    bash -c "pytest --maxfail=1 --disable-warnings"
                    """
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
