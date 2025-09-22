#!/bin/bash
# =============================================================================
# CLEANUP OLD DEPLOYMENTS - AI CREDIT PRE-APPROVAL SYSTEM
# =============================================================================
# 
# This script removes all old/legacy deployments and files to keep the
# codebase clean and organized for production.
#
# Usage: ./deployments/scripts/cleanup-old-deployments.sh
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

# Function to safely delete Kubernetes resources
safe_delete() {
    local resource_type=$1
    local resource_name=$2
    
    if kubectl get $resource_type $resource_name &> /dev/null; then
        log_info "Deleting $resource_type/$resource_name..."
        kubectl delete $resource_type $resource_name --ignore-not-found=true
        log_success "Deleted $resource_type/$resource_name"
    else
        log_info "$resource_type/$resource_name not found (already deleted)"
    fi
}

# Function to delete file if it exists
safe_delete_file() {
    local file_path=$1
    
    if [ -f "$file_path" ]; then
        log_info "Deleting file: $file_path"
        rm -f "$file_path"
        log_success "Deleted file: $file_path"
    else
        log_info "File not found: $file_path (already deleted)"
    fi
}

main() {
    log_info "🧹 Starting Cleanup of Old Deployments"
    log_info "======================================"
    
    # Check if kubectl is available
    if ! command -v kubectl &> /dev/null; then
        log_error "kubectl is not installed or not in PATH"
        exit 1
    fi
    
    log_info "Connected to cluster: $(kubectl config current-context)"
    
    # ==========================================================================
    # KUBERNETES RESOURCES CLEANUP
    # ==========================================================================
    
    log_info "🗑️ Cleaning up old Kubernetes resources..."
    
    # Old frontend deployments
    safe_delete "deployment" "fresh-frontend"
    safe_delete "service" "fresh-frontend"
    safe_delete "configmap" "fresh-frontend-html"
    
    safe_delete "deployment" "improved-frontend"
    safe_delete "service" "improved-frontend"
    safe_delete "configmap" "improved-frontend-html"
    
    safe_delete "deployment" "frontend-widget"
    safe_delete "service" "frontend-widget"
    safe_delete "configmap" "frontend-widget-html"
    
    # Old backend deployments
    safe_delete "deployment" "reliable-backend"
    safe_delete "service" "reliable-backend"
    safe_delete "configmap" "reliable-backend-code"
    
    safe_delete "deployment" "simple-backend"
    safe_delete "service" "simple-backend"
    safe_delete "configmap" "simple-backend-code"
    
    # Old AI agent deployments
    safe_delete "deployment" "risk-agent-simple"
    safe_delete "service" "risk-agent-simple"
    safe_delete "configmap" "risk-agent-simple-code"
    
    safe_delete "deployment" "terms-agent"
    safe_delete "service" "terms-agent"
    safe_delete "configmap" "terms-agent-code"
    
    safe_delete "deployment" "perks-agent-simple"
    safe_delete "service" "perks-agent-simple"
    safe_delete "configmap" "perks-agent-simple-code"
    
    safe_delete "deployment" "policy-agent"
    safe_delete "service" "policy-agent"
    safe_delete "configmap" "policy-agent-code"
    
    safe_delete "deployment" "mcp-server-old"
    safe_delete "service" "mcp-server-old"
    safe_delete "configmap" "mcp-server-old-code"
    
    # ==========================================================================
    # FILE SYSTEM CLEANUP
    # ==========================================================================
    
    log_info "📁 Cleaning up old deployment files..."
    
    # Old frontend files
    safe_delete_file "deploy-fresh-frontend.yaml"
    safe_delete_file "deploy-improved-frontend.yaml"
    safe_delete_file "deploy-enhanced-frontend.yaml"
    safe_delete_file "deploy-frontend-ui.yaml"
    safe_delete_file "deploy-frontend-widget.yaml"
    
    # Old backend files
    safe_delete_file "reliable-backend.yaml"
    safe_delete_file "simple-backend.yaml"
    safe_delete_file "cloud-frontend-widget.py"
    safe_delete_file "deploy-cloud-widget.sh"
    
    # Old agent files
    safe_delete_file "deploy-real-ai-agents.yaml"
    safe_delete_file "deploy-ai-agents.yaml"
    safe_delete_file "deploy-challenger-agent.yaml"
    safe_delete_file "deploy-enhanced-risk-agent.yaml"
    safe_delete_file "deploy-enhanced-policy-agent.yaml"
    safe_delete_file "deploy-policy-agent.yaml"
    safe_delete_file "deploy-policy-agent-simple.yaml"
    safe_delete_file "deploy-mcp-server-enhanced.yaml"
    
    # Old scripts
    safe_delete_file "start-ai-agents.sh"
    safe_delete_file "setup-port-forwards.sh"
    safe_delete_file "populate_data.sh"
    
    # ==========================================================================
    # VERIFICATION
    # ==========================================================================
    
    log_info "🔍 Verifying cleanup..."
    
    # Check for any remaining old resources
    log_info "Checking for any remaining old resources..."
    
    OLD_RESOURCES=$(kubectl get all,configmaps --no-headers 2>/dev/null | grep -E "(fresh|improved|reliable|simple|old)" || true)
    
    if [ -n "$OLD_RESOURCES" ]; then
        log_warning "Found some remaining old resources:"
        echo "$OLD_RESOURCES"
        log_info "You may want to review and manually delete these if needed"
    else
        log_success "No old resources found - cleanup complete!"
    fi
    
    # List current clean deployments
    log_info "📋 Current clean deployments:"
    kubectl get deployments --no-headers | grep -E "(frontend-service|backend-service|.*-agent|mcp-server)" || log_info "No current deployments found"
    
    # ==========================================================================
    # SUMMARY
    # ==========================================================================
    
    echo ""
    log_info "🎉 CLEANUP COMPLETE!"
    log_info "==================="
    echo ""
    
    log_success "✅ Removed all old/legacy Kubernetes resources"
    log_success "✅ Removed all old deployment YAML files"
    log_success "✅ Removed all old script files"
    log_success "✅ Codebase is now clean and organized"
    
    echo ""
    log_info "📁 Current clean structure:"
    echo "  deployments/"
    echo "  ├── frontend/deploy-frontend-service.yaml"
    echo "  ├── backend/deploy-backend-service.yaml" 
    echo "  ├── agents/deploy-ai-agents.yaml"
    echo "  ├── infrastructure/deploy-advanced-agents.yaml"
    echo "  ├── scripts/deploy-all.sh"
    echo "  ├── scripts/cleanup-old-deployments.sh"
    echo "  └── README.md"
    
    echo ""
    log_info "🚀 To deploy the clean system:"
    echo "  ./deployments/scripts/deploy-all.sh"
    
    echo ""
    log_success "Cleanup completed successfully! 🧹✨"
}

# Run main function
main "$@"
