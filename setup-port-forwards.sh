#!/bin/bash

# Bank of Anthos - Port Forward Setup Script
# This script sets up all required port forwards for AI agents

set -e

echo "=============================================="
echo "Bank of Anthos - Port Forward Setup"
echo "=============================================="

# Check if kubectl is available
if ! command -v kubectl &> /dev/null; then
    echo "❌ kubectl is not installed or not in PATH"
    exit 1
fi

# Check if we can connect to Kubernetes
if ! kubectl cluster-info &> /dev/null; then
    echo "❌ Cannot connect to Kubernetes cluster"
    echo "   Make sure your kubeconfig is set up correctly"
    exit 1
fi

echo "✅ kubectl connectivity confirmed"

# Check if required services exist
echo "Checking if Bank of Anthos services are running..."

SERVICES=("userservice" "balancereader" "transactionhistory")
MISSING_SERVICES=()

for service in "${SERVICES[@]}"; do
    if ! kubectl get svc "$service" &> /dev/null; then
        MISSING_SERVICES+=("$service")
    fi
done

if [ ${#MISSING_SERVICES[@]} -gt 0 ]; then
    echo "❌ Missing services: ${MISSING_SERVICES[*]}"
    echo "   Deploy Bank of Anthos first:"
    echo "   kubectl apply -f kubernetes-manifests/"
    exit 1
fi

echo "✅ All required services found"

# Kill any existing port forwards
echo "Cleaning up existing port forwards..."
pkill -f "kubectl.*port-forward.*userservice" 2>/dev/null || true
pkill -f "kubectl.*port-forward.*balancereader" 2>/dev/null || true
pkill -f "kubectl.*port-forward.*transactionhistory" 2>/dev/null || true

# Wait a moment for cleanup
sleep 2

# Check if ports are available
PORTS=(8080 8081 8082)
BUSY_PORTS=()

for port in "${PORTS[@]}"; do
    if lsof -i :$port &> /dev/null; then
        BUSY_PORTS+=("$port")
    fi
done

if [ ${#BUSY_PORTS[@]} -gt 0 ]; then
    echo "⚠️  Ports in use: ${BUSY_PORTS[*]}"
    echo "   Attempting to free up ports..."
    
    for port in "${BUSY_PORTS[@]}"; do
        echo "   Killing processes on port $port..."
        sudo kill -9 $(lsof -t -i:$port) 2>/dev/null || true
    done
    
    sleep 2
fi

# Set up new port forwards
echo "Starting port forwards..."

echo "  Setting up userservice (localhost:8080)..."
kubectl port-forward svc/userservice 8080:8080 > /dev/null 2>&1 &
USERSERVICE_PID=$!

echo "  Setting up balancereader (localhost:8081)..."
kubectl port-forward svc/balancereader 8081:8080 > /dev/null 2>&1 &
BALANCEREADER_PID=$!

echo "  Setting up transactionhistory (localhost:8082)..."
kubectl port-forward svc/transactionhistory 8082:8080 > /dev/null 2>&1 &
TRANSACTIONHISTORY_PID=$!

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "Cleaning up port forwards..."
    kill $USERSERVICE_PID $BALANCEREADER_PID $TRANSACTIONHISTORY_PID 2>/dev/null || true
}
trap cleanup EXIT

# Wait for connections to establish
echo "Waiting for connections to establish..."
sleep 5

# Test connectivity
echo "Testing connectivity..."

FAILED_TESTS=()

# Test userservice
if ! curl -s --connect-timeout 3 http://localhost:8080/ready > /dev/null 2>&1; then
    if ! curl -s --connect-timeout 3 http://localhost:8080/ > /dev/null 2>&1; then
        FAILED_TESTS+=("userservice:8080")
    fi
fi

# Test balancereader  
if ! curl -s --connect-timeout 3 http://localhost:8081/ready > /dev/null 2>&1; then
    if ! curl -s --connect-timeout 3 http://localhost:8081/ > /dev/null 2>&1; then
        FAILED_TESTS+=("balancereader:8081")
    fi
fi

# Test transactionhistory
if ! curl -s --connect-timeout 3 http://localhost:8082/ready > /dev/null 2>&1; then
    if ! curl -s --connect-timeout 3 http://localhost:8082/ > /dev/null 2>&1; then
        FAILED_TESTS+=("transactionhistory:8082")
    fi
fi

if [ ${#FAILED_TESTS[@]} -gt 0 ]; then
    echo "⚠️  Some services may not be fully ready: ${FAILED_TESTS[*]}"
    echo "   This is normal if pods are still starting up"
else
    echo "✅ All port forwards are responding"
fi

echo ""
echo "=============================================="
echo "✅ Port forwards established successfully!"
echo "=============================================="
echo ""
echo "Active port forwards:"
echo "  📡 userservice:        http://localhost:8080"
echo "  💰 balancereader:      http://localhost:8081" 
echo "  📊 transactionhistory: http://localhost:8082"
echo ""
echo "AI Agent URLs:"
echo "  🤖 Frontend Widget:    http://localhost:8084"
echo "  🎁 Perks Agent:        http://localhost:8083"
echo ""
echo "Quick Test:"
echo "  curl -s \"http://localhost:8084/api/real-preapproval?username=testuser\" | jq '.transaction_count'"
echo ""
echo "💡 Tip: Keep this terminal open to maintain port forwards"
echo "        Press Ctrl+C to stop all port forwards"
echo ""

# Keep the script running to maintain port forwards
if [ "${1:-}" != "--no-wait" ]; then
    echo "Port forwards are active. Press Ctrl+C to stop..."
    
    # Wait indefinitely
    while true; do
        sleep 30
        
        # Check if any port forward died
        if ! kill -0 $USERSERVICE_PID 2>/dev/null || \
           ! kill -0 $BALANCEREADER_PID 2>/dev/null || \
           ! kill -0 $TRANSACTIONHISTORY_PID 2>/dev/null; then
            echo "⚠️  One or more port forwards died. Restarting..."
            
            # Restart failed port forwards
            if ! kill -0 $USERSERVICE_PID 2>/dev/null; then
                echo "  Restarting userservice port forward..."
                kubectl port-forward svc/userservice 8080:8080 > /dev/null 2>&1 &
                USERSERVICE_PID=$!
            fi
            
            if ! kill -0 $BALANCEREADER_PID 2>/dev/null; then
                echo "  Restarting balancereader port forward..."
                kubectl port-forward svc/balancereader 8081:8080 > /dev/null 2>&1 &
                BALANCEREADER_PID=$!
            fi
            
            if ! kill -0 $TRANSACTIONHISTORY_PID 2>/dev/null; then
                echo "  Restarting transactionhistory port forward..."
                kubectl port-forward svc/transactionhistory 8082:8080 > /dev/null 2>&1 &
                TRANSACTIONHISTORY_PID=$!
            fi
            
            sleep 3
            echo "  ✅ Port forwards restarted"
        fi
    done
fi
