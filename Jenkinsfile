
pipeline {
    agent any

    environment {
        AWS_ACCOUNT_ID = '677913799735'
        AWS_REGION = 'ap-south-1'
        ECR_REPOSITORY = 'gemini-chatbot'
        K8S_DEPLOYMENT = 'gemini-chatbot'
        K8S_CONTAINER = 'gemini-chatbot'
    }

    options {
        timestamps()
        disableConcurrentBuilds()
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
                sh '''
                    set -eu
                    test -f app.py
                    test -f requirements.txt
                    test -f Dockerfile
                    test -f templates/signup.html
                    test -f k8s/deployment.yaml
                '''
            }
        }

        stage('Validate Python') {
            steps {
                sh '''
                    set -eu
                    docker run --rm \
                      -v "$WORKSPACE:/app" \
                      -w /app \
                      python:3.11-slim \
                      sh -c "pip install --no-cache-dir -r requirements.txt && python -m py_compile app.py"
                '''
            }
        }

        stage('Build Image') {
            steps {
                sh '''
                    set -eu
                    IMAGE_URI="${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPOSITORY}"

                    docker build \
                      -t "$IMAGE_URI:$BUILD_NUMBER" \
                      -t "$IMAGE_URI:latest" \
                      .
                '''
            }
        }

        stage('Push to Amazon ECR') {
            steps {
                sh '''
                    set -eu
                    REGISTRY="${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"
                    IMAGE_URI="${REGISTRY}/${ECR_REPOSITORY}"

                    aws sts get-caller-identity

                    aws ecr get-login-password --region "$AWS_REGION" |
                      docker login --username AWS --password-stdin "$REGISTRY"

                    docker push "$IMAGE_URI:$BUILD_NUMBER"
                    docker push "$IMAGE_URI:latest"
                '''
            }
        }

        stage('Deploy to Minikube') {
            steps {
                withCredentials([
                    string(
                        credentialsId: 'gemini-api-key',
                        variable: 'GEMINI_API_KEY'
                    )
                ]) {
                    sh '''
                        set -eu
                        set +x

                        REGISTRY="${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"
                        IMAGE_URI="${REGISTRY}/${ECR_REPOSITORY}"

                        kubectl get nodes

                        ECR_PASSWORD="$(aws ecr get-login-password --region "$AWS_REGION")"

                        kubectl create secret docker-registry ecr-registry \
                          --docker-server="$REGISTRY" \
                          --docker-username=AWS \
                          --docker-password="$ECR_PASSWORD" \
                          --dry-run=client -o yaml |
                          kubectl apply -f -

                        unset ECR_PASSWORD

                        printf '%s' "$GEMINI_API_KEY" |
                          kubectl create secret generic gemini-secret \
                            --from-file=GEMINI_API_KEY=/dev/stdin \
                            --dry-run=client -o yaml |
                            kubectl apply -f -

                        kubectl apply -f k8s/deployment.yaml

                        kubectl set image \
                          deployment/"$K8S_DEPLOYMENT" \
                          "$K8S_CONTAINER"="$IMAGE_URI:$BUILD_NUMBER"

                        kubectl rollout status \
                          deployment/"$K8S_DEPLOYMENT" \
                          --timeout=180s

                        kubectl get deployments
                        kubectl get pods
                        kubectl get services
                    '''
                }
            }
        }
    }

    post {
        success {
            echo "Pipeline succeeded. Image tag: ${env.BUILD_NUMBER}"
        }
        failure {
            echo 'Pipeline failed. Check the failed stage logs.'
        }
        always {
            echo 'Pipeline finished.'
        }
    }
}
