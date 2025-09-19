#!/bin/bash

# Bank of Anthos AI Agents Deployment Script
# This script builds and deploys the AI-powered credit pre-approval system

set -e

echo "🚀 Deploying Bank of Anthos AI Agents for GKE Hackathon"
echo "========================================================"

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
echo "📋 Checking prerequisites..."
if ! command_exists docker; then
    echo "❌ Docker is required but not installed"
    exit 1
fi

if ! command_exists kubectl; then
    echo "❌ kubectl is required but not installed"
    exit 1
fi

# Check if we're connected to the right cluster
current_context=$(kubectl config current-context)
echo "📍 Current kubectl context: $current_context"

# Create namespace if it doesn't exist
echo "🏗️  Setting up namespace..."
kubectl get namespace boa-agents >/dev/null 2>&1 || kubectl create namespace boa-agents

# Build Docker images
echo "🔨 Building Docker images..."

echo "Building MCP Server..."
cd mcp-server
docker build -t boa-mcp:latest .
cd ..

echo "Building Risk Agent..."
cd risk-agent
docker build -t risk-agent:latest .
cd ..

echo "Building Terms Agent..."
cd terms-agent
docker build -t terms-agent:latest .
cd ..

echo "Building API Gateway..."
cd api-gateway
docker build -t preapproval-api:latest .
cd ..

echo "✅ All Docker images built successfully"

# Deploy Kubernetes resources
echo "☸️  Deploying to Kubernetes..."

echo "Applying ConfigMaps and Secrets..."
kubectl apply -f k8s/configmap.yaml

echo "Deploying MCP Server..."
kubectl apply -f k8s/mcp-server.yaml

echo "Deploying Risk Agent..."
kubectl apply -f k8s/risk-agent.yaml

echo "Deploying Terms Agent..."
kubectl apply -f k8s/terms-agent.yaml

echo "Deploying API Gateway..."
kubectl apply -f k8s/api-gateway.yaml

echo "⏳ Waiting for deployments to be ready..."
kubectl wait --for=condition=available --timeout=300s deployment/boa-mcp -n boa-agents
kubectl wait --for=condition=available --timeout=300s deployment/risk-agent -n boa-agents
kubectl wait --for=condition=available --timeout=300s deployment/terms-agent -n boa-agents
kubectl wait --for=condition=available --timeout=300s deployment/preapproval-api -n boa-agents

echo "✅ All deployments are ready!"

# Get service status
echo "📊 Service Status:"
kubectl get pods -n boa-agents
echo ""
kubectl get services -n boa-agents

# Get external IP for the API Gateway
echo "🌐 Getting external IP for API Gateway..."
kubectl get service preapproval-api -n boa-agents

echo ""
echo "🎉 Deployment completed successfully!"
echo ""
echo "📋 Next Steps:"
echo "1. Wait for the LoadBalancer to get an external IP:"
echo "   kubectl get service preapproval-api -n boa-agents -w"
echo ""
echo "2. Test the API once external IP is ready:"
echo "   curl http://EXTERNAL_IP/health"
echo "   curl http://EXTERNAL_IP/preapproval?user_id=testuser"
echo ""
echo "3. Access the widget at:"
echo "   http://EXTERNAL_IP/widget?user_id=testuser"
echo ""
echo "4. Monitor the services:"
echo "   kubectl logs -f deployment/preapproval-api -n boa-agents"
echo "   kubectl get pods -n boa-agents -w"
echo ""
echo "🏆 Ready for the GKE Hackathon demo!"
