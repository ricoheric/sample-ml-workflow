pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                // Récupération du code source
                git branch: 'main', url: 'https://github.com/ricoheric/sample-ml-workflow.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                // Construction de l'image qui contient le code et les dépendances
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
                        // Création du fichier d'environnement
                        writeFile file: 'env.list', text: """
MLFLOW_TRACKING_URI=$MLFLOW_TRACKING_URI
AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY
BACKEND_STORE_URI=$BACKEND_STORE_URI
ARTIFACT_ROOT=$ARTIFACT_ROOT
                        """
                    }

                    // Exécution des tests dans un conteneur éphémère
                    sh '''
                    docker run --rm --env-file env.list \
                    ml-pipeline-image \
                    bash -c "pytest --maxfail=1 --disable-warnings"
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
                    // La commande est propre et isolée.
                    // AUCUN montage de volume `-v` ! C'est la clé.
                    // Le conteneur communique avec le serveur MLflow via le réseau.
                    // Les fichiers temporaires (s'il y en a) restent dans le conteneur et sont détruits avec --rm.
                    sh '''
                    docker run --rm --env-file env.list \
                    ml-pipeline-image \
                    mlflow run . --entry-point main
                    '''
                }
            }
        }
    }

    post {
        always {
            // Nettoyage des images Docker non utilisées
            sh 'docker system prune -f'
            
            // Utilisation de cleanWs() pour un nettoyage fiable et standard du workspace.
            // Cela supprimera le fichier env.list et les autres fichiers du checkout.
            // Cela fonctionnera maintenant car aucun fichier appartenant à root n'a été créé.
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
