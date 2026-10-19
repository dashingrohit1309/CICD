# Gemini Chatbot CI/CD Pipeline

A web-based AI chatbot built using **Python Flask and Google Gemini**, with a CI/CD workflow using **Jenkins, Docker, Amazon ECR, and Kubernetes**.

## Project Overview

This project demonstrates how to containerize a Flask application, build and publish Docker images using Jenkins, and deploy the application on a Kubernetes cluster.

Users can interact with the chatbot through a simple web interface and receive AI-generated responses powered by the Google Gemini API.

## Technologies Used

- **Python** — Application development
- **Flask** — Web framework and API endpoints
- **Google Gemini API** — AI-generated chatbot responses
- **HTML, CSS, JavaScript** — Frontend interface
- **Docker** — Application containerization
- **Jenkins** — CI/CD pipeline automation
- **Amazon ECR** — Docker image registry
- **Kubernetes** — Application deployment and management
- **Minikube** — Local Kubernetes cluster
- **Git and GitHub** — Version control and source code management
- **Amazon EC2** — Jenkins server hosting

## Project Architecture

```text
Developer
    |
    v
GitHub Repository
    |
    v
Jenkins CI/CD Pipeline
    |
    +--> Checkout Source Code
    |
    +--> Validate Python Code
    |
    +--> Build Docker Image
    |
    +--> Push Image to Amazon ECR
    |
    v
Kubernetes Deployment
    |
    v
Gemini Chatbot Web Application
    |
    v
Google Gemini API
```

## Project Structure

```text
CICD/
├── app.py
├── requirements.txt
├── Dockerfile
├── Jenkinsfile
├── README.md
├── templates/
│   └── signup.html
└── k8s/
    └── deployment.yaml
```

## Application Features

- Simple web-based chatbot interface
- AI-generated responses using Google Gemini
- Flask backend with a chat API endpoint
- Docker-based application packaging
- Jenkins pipeline for code validation and image building
- Docker image storage in Amazon ECR
- Kubernetes deployment and service configuration

## CI/CD Pipeline Workflow

### 1. Source Code Management
The application source code is stored in GitHub. When changes are pushed to the repository, Jenkins can retrieve the latest code during a pipeline build.

### 2. Continuous Integration with Jenkins
Jenkins checks out the repository and validates the Python application and its dependencies.

### 3. Docker Image Creation
Jenkins builds a Docker image using the project's Dockerfile. The image is tagged using the Jenkins build number and the `latest` tag.

### 4. Push to Amazon ECR
The Docker image is pushed to Amazon Elastic Container Registry (ECR), where it can be retrieved for deployment.

### 5. Kubernetes Deployment
The Kubernetes Deployment runs the chatbot container. A Kubernetes Service exposes the application on port 5000.

### 6. Chatbot Access
The application can be accessed locally through Kubernetes port-forwarding:

```bash
kubectl port-forward service/gemini-chatbot-service 5000:5000
```

Open the following URL in your browser:

`http://127.0.0.1:5000`

Keep the terminal running while using the application.

## Prerequisites

Install or configure the following before running the project:

- Python 3.11 or compatible version
- Git
- Docker
- Jenkins
- AWS account with appropriate ECR permissions
- Kubernetes and kubectl
- Minikube for local Kubernetes deployment
- Google Gemini API key

## Run the Application Locally

### 1. Clone the repository

```bash
git clone https://github.com/dashingrohit1309/CICD.git
cd CICD
```

### 2. Create a virtual environment (optional)

```bash
python -m venv venv
```

On Windows CMD:

```cmd
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the Gemini API key

On Windows CMD, set the environment variable for the current terminal session:

```cmd
set GEMINI_API_KEY=your_api_key_here
```

Replace `your_api_key_here` with your own API key. Do not commit API keys to GitHub.

### 5. Start the application

```bash
python app.py
```

Open `http://127.0.0.1:5000` in your browser.

## Run with Docker

Build the Docker image:

```bash
docker build -t gemini-chatbot .
```

Run the container:

```bash
docker run --rm -p 5000:5000 -e GEMINI_API_KEY=your_api_key_here gemini-chatbot
```

Open `http://127.0.0.1:5000`.

## Kubernetes Deployment

The Kubernetes manifest is located at `k8s/deployment.yaml`.

Before deploying, ensure that:

- Minikube is running.
- The Kubernetes image-pull secret `ecr-registry` is configured and valid.
- The Kubernetes secret `gemini-secret` contains the `GEMINI_API_KEY`.
- The image reference in the manifest points to an image available in Amazon ECR.

Apply the Kubernetes manifest:

```bash
kubectl apply -f k8s/deployment.yaml
```

Check the deployment and pods:

```bash
kubectl get deployments
kubectl get pods
kubectl get services
```

Access the application:

```bash
kubectl port-forward service/gemini-chatbot-service 5000:5000
```

Then visit `http://127.0.0.1:5000`.

## Security Considerations

- Store the Gemini API key in an environment variable or a Kubernetes Secret.
- Store AWS credentials securely and use IAM roles or least-privilege permissions where possible.
- Never
