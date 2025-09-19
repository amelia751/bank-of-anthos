#!/bin/bash

# Simplified deployment using Cloud Build
echo "🚀 Building AI Agents using Cloud Build..."

# Build the container images using Cloud Build
gcloud builds submit --config=cloud-build.yaml .

# Update Kubernetes manifests to use GCR images
sed -i '' 's/image: boa-mcp:latest/image: gcr.io\/'$PROJECT_ID'\/boa-mcp:latest/g' k8s/mcp-server.yaml
sed -i '' 's/image: risk-agent:latest/image: gcr.io\/'$PROJECT_ID'\/risk-agent:latest/g' k8s/risk-agent.yaml
sed -i '' 's/image: terms-agent:latest/image: gcr.io\/'$PROJECT_ID'\/terms-agent:latest/g' k8s/terms-agent.yaml
sed -i '' 's/image: preapproval-api:latest/image: gcr.io\/'$PROJECT_ID'\/preapproval-api:latest/g' k8s/api-gateway.yaml

# Update image pull policy
sed -i '' 's/imagePullPolicy: Never/imagePullPolicy: Always/g' k8s/*.yaml

echo "✅ Images built and manifests updated"
echo "📥 Deploy with: kubectl apply -f k8s/"
