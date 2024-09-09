pipeline {
    agent any

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
                withCredentials([
                    string(credentialsId: 'mlflow-tracking-uri', variable: 'MLFLOW_TRACKING_URI'),
                    string(credentialsId: 'aws-access-key', variable: 'AWS_ACCESS_KEY_ID'),
                    string(credentialsId: 'aws-secret-key', variable: 'AWS_SECRET_ACCESS_KEY'),
                    string(credentialsId: 'backend-store-uri', variable: 'BACKEND_STORE_URI'),
                    string(credentialsId: 'artifact-root', variable: 'ARTIFACT_ROOT')
                ]) {
                    // Pass the sensitive environment variables directly to the Docker container
                    sh '''#!/bin/bash
                    set +x
                    docker run --rm \
                    -e MLFLOW_TRACKING_URI=$MLFLOW_TRACKING_URI \
                    -e AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID \
                    -e AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY \
                    -e BACKEND_STORE_URI=$BACKEND_STORE_URI \
                    -e ARTIFACT_ROOT=$ARTIFACT_ROOT \
                    ml-pipeline-image \
                    bash -c "pytest --maxfail=1 --disable-warnings"
                    '''
                }
            }
        }

        stage('Run ML Training Inside Docker Container') {
            steps {
                withCredentials([
                    string(credentialsId: 'mlflow-tracking-uri', variable: 'MLFLOW_TRACKING_URI'),
                    string(credentialsId: 'aws-access-key', variable: 'AWS_ACCESS_KEY_ID'),
                    string(credentialsId: 'aws-secret-key', variable: 'AWS_SECRET_ACCESS_KEY'),
                    string(credentialsId: 'backend-store-uri', variable: 'BACKEND_STORE_URI'),
                    string(credentialsId: 'artifact-root', variable: 'ARTIFACT_ROOT')
                ]) {
                    // Pass the sensitive environment variables directly to the Docker container for the training stage
                    sh '''#!/bin/bash
                    set +x
                    docker run --rm \
                    -e MLFLOW_TRACKING_URI=$MLFLOW_TRACKING_URI \
                    -e AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID \
                    -e AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY \
                    -e BACKEND_STORE_URI=$BACKEND_STORE_URI \
                    -e ARTIFACT_ROOT=$ARTIFACT_ROOT \
                    ml-pipeline-image \
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
