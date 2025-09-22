#!/bin/bash
# =============================================================================
# AI CREDIT PRE-APPROVAL SYSTEM - COMPLETE DEPLOYMENT SCRIPT
# =============================================================================
# 
# This script deploys the entire AI Credit Pre-Approval System to GKE with
# proper ordering, health checks, and validation.
#
# Usage: ./deployments/scripts/deploy-all.sh
#
# =============================================================================

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to wait for deployment to be ready
wait_for_deployment() {
    local deployment_name=$1
    local timeout=${2:-300}  # Default 5 minutes
    
    log_info "Waiting for deployment $deployment_name to be ready..."
    
    if kubectl wait --for=condition=available --timeout=${timeout}s deployment/$deployment_name; then
        log_success "Deployment $deployment_name is ready"
        return 0
    else
        log_error "Deployment $deployment_name failed to become ready within ${timeout}s"
        return 1
    fi
}

# Function to get service external IP
get_service_ip() {
    local service_name=$1
    local max_attempts=20
    local attempt=1
    
    log_info "Getting external IP for service $service_name..."
    
    while [ $attempt -le $max_attempts ]; do
        IP=$(kubectl get service $service_name -o jsonpath='{.status.loadBalancer.ingress[0].ip}' 2>/dev/null || echo "")
        if [ -n "$IP" ]; then
            echo "$IP"
            return 0
        fi
        
        log_info "Attempt $attempt/$max_attempts: Waiting for external IP..."
        sleep 15
        ((attempt++))
    done
    
    log_warning "Could not get external IP for $service_name after $max_attempts attempts"
    return 1
}

# Function to test endpoint health
test_endpoint() {
    local url=$1
    local name=$2
    
    if curl -s --connect-timeout 10 "$url" > /dev/null 2>&1; then
        log_success "$name is healthy: $url"
        return 0
    else
        log_warning "$name is not responding: $url"
        return 1
    fi
}

# Main deployment function
main() {
    log_info "🚀 Starting AI Credit Pre-Approval System Deployment"
    log_info "=================================================="
    
    # Check if kubectl is available
    if ! command -v kubectl &> /dev/null; then
        log_error "kubectl is not installed or not in PATH"
        exit 1
    fi
    
    # Check if we're connected to a cluster
    if ! kubectl cluster-info &> /dev/null; then
        log_error "Not connected to a Kubernetes cluster"
        exit 1
    fi
    
    log_info "Connected to cluster: $(kubectl config current-context)"
    
    # Step 1: Deploy Infrastructure (MCP Server, Advanced Agents)
    log_info "📦 Step 1: Deploying Infrastructure Components..."
    kubectl apply -f deployments/infrastructure/deploy-advanced-agents.yaml
    
    # Wait for infrastructure components
    wait_for_deployment "mcp-server"
    wait_for_deployment "challenger-agent"
    wait_for_deployment "enhanced-policy-agent"
    
    # Step 2: Deploy AI Agents
    log_info "🤖 Step 2: Deploying AI Agents..."
    kubectl apply -f deployments/agents/deploy-ai-agents.yaml
    
    # Wait for AI agents
    wait_for_deployment "perks-agent"
    wait_for_deployment "enhanced-risk-agent"
    wait_for_deployment "terms-agent-simple"
    
    # Step 3: Deploy Backend Service
    log_info "⚙️ Step 3: Deploying Backend Service..."
    kubectl apply -f deployments/backend/deploy-backend-service.yaml
    wait_for_deployment "backend-service"
    
    # Step 4: Deploy Frontend Service
    log_info "🖥️ Step 4: Deploying Frontend Service..."
    kubectl apply -f deployments/frontend/deploy-frontend-service.yaml
    wait_for_deployment "frontend-service"
    
    # Step 5: Get Service URLs
    log_info "🌐 Step 5: Getting Service URLs..."
    
    FRONTEND_IP=$(get_service_ip "frontend-service")
    BACKEND_IP=$(get_service_ip "backend-service")
    
    # Step 6: Health Checks
    log_info "🏥 Step 6: Running Health Checks..."
    
    sleep 30  # Give services time to fully start
    
    # Test backend health
    if [ -n "$BACKEND_IP" ]; then
        test_endpoint "http://$BACKEND_IP/health" "Backend Service"
        test_endpoint "http://$BACKEND_IP/api/cache-status" "Backend Cache"
    fi
    
    # Test frontend
    if [ -n "$FRONTEND_IP" ]; then
        test_endpoint "http://$FRONTEND_IP" "Frontend Service"
    fi
    
    # Test AI agents (internal)
    log_info "Testing AI agent connectivity..."
    kubectl exec deployment/backend-service -- curl -s http://enhanced-risk-agent:8087/health > /dev/null && \
        log_success "Risk Agent is healthy" || log_warning "Risk Agent may not be responding"
    
    kubectl exec deployment/backend-service -- curl -s http://terms-agent-simple:8086/health > /dev/null && \
        log_success "Terms Agent is healthy" || log_warning "Terms Agent may not be responding"
    
    kubectl exec deployment/backend-service -- curl -s http://perks-agent-real:8085/health > /dev/null && \
        log_success "Perks Agent is healthy" || log_warning "Perks Agent may not be responding"
    
    kubectl exec deployment/backend-service -- curl -s http://challenger-agent:8088/health > /dev/null && \
        log_success "Challenger Agent is healthy" || log_warning "Challenger Agent may not be responding"
    
    kubectl exec deployment/backend-service -- curl -s http://enhanced-policy-agent:8090/health > /dev/null && \
        log_success "Policy Agent is healthy" || log_warning "Policy Agent may not be responding"
    
    kubectl exec deployment/backend-service -- curl -s http://mcp-server:8089/health > /dev/null && \
        log_success "MCP Server is healthy" || log_warning "MCP Server may not be responding"
    
    # Step 7: End-to-End Test
    log_info "🧪 Step 7: Running End-to-End Test..."
    
    if [ -n "$BACKEND_IP" ]; then
        if curl -s "http://$BACKEND_IP/api/real-preapproval?username=testuser" | grep -q "ai_insights"; then
            log_success "End-to-end API test passed!"
        else
            log_warning "End-to-end API test failed - check logs"
        fi
    fi
    
    # Final Summary
    echo ""
    log_info "🎉 DEPLOYMENT COMPLETE!"
    log_info "======================"
    echo ""
    
    if [ -n "$FRONTEND_IP" ]; then
        echo -e "${GREEN}🌐 Frontend URL:${NC} http://$FRONTEND_IP"
    else
        echo -e "${YELLOW}🌐 Frontend:${NC} Getting external IP (check: kubectl get service frontend-service)"
    fi
    
    if [ -n "$BACKEND_IP" ]; then
        echo -e "${GREEN}⚙️ Backend API:${NC} http://$BACKEND_IP"
        echo -e "${GREEN}📊 Health Check:${NC} http://$BACKEND_IP/health"
        echo -e "${GREEN}🧪 Test API:${NC} http://$BACKEND_IP/api/real-preapproval?username=testuser"
    else
        echo -e "${YELLOW}⚙️ Backend:${NC} Getting external IP (check: kubectl get service backend-service)"
    fi
    
    echo ""
    log_info "🔍 Monitoring Commands:"
    echo "  kubectl get pods,services | grep -E '(frontend|backend|agent|mcp)'"
    echo "  kubectl logs deployment/backend-service --tail=20"
    echo "  kubectl logs deployment/frontend-service --tail=20"
    
    echo ""
    log_info "🧹 Cleanup Command:"
    echo "  ./deployments/scripts/cleanup-old-deployments.sh"
    
    echo ""
    log_success "AI Credit Pre-Approval System is now running! 🚀✨"
}

# Run main function
main "$@"
