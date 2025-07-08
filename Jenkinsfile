pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/ricoheric/sample-ml-workflow.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh 'docker build -t ml-pipeline-image .'
                }
            }
        }

        stage('Run Tests') {
            steps {
                withCredentials([
                    string(credentialsId: 'mlflow-tracking-uri', variable: 'MLFLOW_TRACKING_URI'),
                    string(credentialsId: 'aws-access-key', variable: 'AWS_ACCESS_KEY_ID'),
                    string(credentialsId: 'aws-secret-key', variable: 'AWS_SECRET_ACCESS_KEY'),
                    string(credentialsId: 'backend-store-uri', variable: 'BACKEND_STORE_URI'),
                    string(credentialsId: 'artifact-root', variable: 'ARTIFACT_ROOT')
                ]) {
                    script {
                        writeFile file: 'env.list', text: """
MLFLOW_TRACKING_URI=$MLFLOW_TRACKING_URI
AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY
BACKEND_STORE_URI=$BACKEND_STORE_URI
ARTIFACT_ROOT=$ARTIFACT_ROOT
                        """
                    }
                    sh '''
                    docker run --rm --env-file env.list ml-pipeline-image bash -c "pytest --maxfail=1 --disable-warnings"
                    '''
                }
            }
        }

        stage('Run MLflow Training') {
            steps {
                withCredentials([
                    string(credentialsId: 'mlflow-tracking-uri', variable: 'MLFLOW_TRACKING_URI'),
                    string(credentialsId: 'aws-access-key', variable: 'AWS_ACCESS_KEY_ID'),
                    string(credentialsId: 'aws-secret-key', variable: 'AWS_SECRET_ACCESS_KEY'),
                    string(credentialsId: 'backend-store-uri', variable: 'BACKEND_STORE_URI'),
                    string(credentialsId: 'artifact-root', variable: 'ARTIFACT_ROOT')
                ]) {
                    // La commande correcte : SANS montage de volume.
                    // Rien ne sera écrit dans le workspace Jenkins. Le problème de permission est évité.
                    sh '''
                    docker run --rm --env-file env.list ml-pipeline-image mlflow run . --entry-point main
                    '''
                }
            }
        }
    }

    post {
        always {
            sh 'docker system prune -f'
            // cleanWs est la méthode propre pour nettoyer le workspace à la fin.
            cleanWs()
        }
        success {
            echo 'Pipeline completed successfully! Check your MLflow server for the new run.'
        }
        failure {
            echo 'Pipeline failed. Check logs for errors.'
        }
    }
}
