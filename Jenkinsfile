pipeline {
    agent any

    // Toutes les étapes du pipeline doivent être à l'intérieur de ce bloc 'stages'
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

        stage('Run Tests Inside Docker Container') {
            steps {
                withCredentials([
                    string(credentialsId: 'mlflow-tracking-uri', variable: 'MLFLOW_TRACKING_URI'),
                    string(credentialsId: 'aws-access-key', variable: 'AWS_ACCESS_KEY_ID'),
                    string(credentialsId: 'aws-secret-key', variable: 'AWS_SECRET_ACCESS_KEY'),
                    string(credentialsId: 'backend-store-uri', variable: 'BACKEND_STORE_URI'),
                    string(credentialsId: 'artifact-root', variable: 'ARTIFACT_ROOT')
                ]) {
                    script {
                        // Création du fichier d'environnement pour les tests
                        writeFile file: 'env.list', text: """
MLFLOW_TRACKING_URI=$MLFLOW_TRACKING_URI
AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY
BACKEND_STORE_URI=$BACKEND_STORE_URI
ARTIFACT_ROOT=$ARTIFACT_ROOT
                        """
                    }

                    sh '''
                    docker run --rm --env-file env.list \
                    ml-pipeline-image \
                    bash -c "pytest --maxfail=1 --disable-warnings"
                    '''
                }
            }
        }

        // Ce stage doit être à l'intérieur du bloc 'stages'
        stage('Run MLflow Project Inside Docker') {
            steps {
                withCredentials([
                    string(credentialsId: 'mlflow-tracking-uri', variable: 'MLFLOW_TRACKING_URI'),
                    string(credentialsId: 'aws-access-key', variable: 'AWS_ACCESS_KEY_ID'),
                    string(credentialsId: 'aws-secret-key', variable: 'AWS_SECRET_ACCESS_KEY'),
                    string(credentialsId: 'backend-store-uri', variable: 'BACKEND_STORE_URI'),
                    string(credentialsId: 'artifact-root', variable: 'ARTIFACT_ROOT')
                ]) {
                    // Il est préférable de recréer le fichier ici pour que le stage soit autonome.
                    // Le fichier du stage précédent est écrasé, ce qui est correct.
                    script {
                        writeFile file: 'env.list', text: """
MLFLOW_TRACKING_URI=$MLFLOW_TRACKING_URI
AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY
BACKEND_STORE_URI=$BACKEND_STORE_URI
ARTIFACT_ROOT=$ARTIFACT_ROOT
                        """
                    }

                    // Commande docker run simplifiée et corrigée pour le contexte Docker-in-Docker
                    // Pas de montage de volume (-v) ni de pip install, car tout est déjà dans l'image.
                    sh '''
                    docker run --rm --env-file env.list \
                    ml-pipeline-image \
                    mlflow run . --entry-point main
                    '''
                }
            }
        }

    } // <-- C'est l'accolade fermante pour le bloc 'stages' qui manquait au bon endroit.

    post {
        always {
            // Nettoyage des images Docker non utilisées pour libérer de l'espace
            sh 'docker system prune -f'
            // Suppression du fichier de credentials pour ne pas le laisser dans le workspace
            deleteDir() 
            //sh 'rm -f env.list'
        }
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed. Check logs for errors.'
        }
    }
}
