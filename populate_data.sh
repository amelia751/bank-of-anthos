#!/bin/bash

# Bank of Anthos - Populate Realistic Data Script
# This script populates the database with realistic user spending habits

set -e

echo "====================================================="
echo "Bank of Anthos - Realistic Data Population"
echo "====================================================="

# Check if we're in the correct directory
if [ ! -f "populate_realistic_data.py" ]; then
    echo "Error: populate_realistic_data.py not found. Please run this script from the bank-of-anthos directory."
    exit 1
fi

# Check if merchant_mapping.py exists
if [ ! -f "boa-ai-agents/merchant_mapping.py" ]; then
    echo "Error: boa-ai-agents/merchant_mapping.py not found."
    exit 1
fi

echo "Checking database connection..."

# Try to detect if we're running in Kubernetes or locally
if command -v kubectl &> /dev/null && kubectl get pods 2>/dev/null | grep -q "accounts-db\|ledger-db"; then
    echo "Detected Kubernetes environment"
    
    # Get the pod names
    LEDGER_POD=$(kubectl get pods -o name | grep ledger-db | head -1 | cut -d/ -f2)
    ACCOUNTS_POD=$(kubectl get pods -o name | grep accounts-db | head -1 | cut -d/ -f2)
    
    if [ -z "$LEDGER_POD" ] || [ -z "$ACCOUNTS_POD" ]; then
        echo "Error: Could not find database pods. Make sure both accounts-db and ledger-db are running."
        echo "Found ledger-db: $LEDGER_POD"
        echo "Found accounts-db: $ACCOUNTS_POD"
        exit 1
    fi
    
    echo "Found ledger-db pod: $LEDGER_POD"
    echo "Found accounts-db pod: $ACCOUNTS_POD"
    
    # Set database connection parameters for Kubernetes
    # Ledger DB configuration
    export POSTGRES_HOST="127.0.0.1"
    export POSTGRES_PORT="5433"  # Ledger DB port
    export POSTGRES_DB="postgresdb"
    export POSTGRES_USER="admin"
    export POSTGRES_PASSWORD="password"
    
    # Accounts DB configuration (different credentials and database name)
    export ACCOUNTS_POSTGRES_HOST="127.0.0.1"
    export ACCOUNTS_POSTGRES_PORT="5434"  # Accounts DB port
    export ACCOUNTS_POSTGRES_DB="accounts-db"
    export ACCOUNTS_POSTGRES_USER="accounts-admin"
    export ACCOUNTS_POSTGRES_PASSWORD="accounts-pwd"
    
    echo "Setting up port-forwards to database pods..."
    # Kill any existing port-forwards
    pkill -f "kubectl.*port-forward.*5433" 2>/dev/null || true
    pkill -f "kubectl.*port-forward.*5434" 2>/dev/null || true
    
    # Start port-forwards in background
    kubectl port-forward $LEDGER_POD 5433:5432 &
    LEDGER_PORT_FORWARD_PID=$!
    
    kubectl port-forward $ACCOUNTS_POD 5434:5432 &
    ACCOUNTS_PORT_FORWARD_PID=$!
    
    # Wait a moment for port-forwards to establish
    sleep 5
    
    # Function to cleanup port-forwards on exit
    cleanup() {
        echo "Cleaning up port-forwards..."
        kill $LEDGER_PORT_FORWARD_PID 2>/dev/null || true
        kill $ACCOUNTS_PORT_FORWARD_PID 2>/dev/null || true
    }
    trap cleanup EXIT
    
elif [ -n "$POSTGRES_HOST" ]; then
    echo "Using provided database environment variables"
else
    echo "Defaulting to local database connection"
    export POSTGRES_HOST="localhost"
    export POSTGRES_PORT="5432"
    export POSTGRES_DB="postgresdb"
    export POSTGRES_USER="postgres"
    export POSTGRES_PASSWORD="password"
fi

echo "Database connections:"
echo "  Ledger DB: $POSTGRES_HOST:$POSTGRES_PORT/$POSTGRES_DB"
echo "  Accounts DB: ${ACCOUNTS_POSTGRES_HOST:-$POSTGRES_HOST}:${ACCOUNTS_POSTGRES_PORT:-$POSTGRES_PORT}/${ACCOUNTS_POSTGRES_DB:-$POSTGRES_DB}"
echo "  User: $POSTGRES_USER"

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed or not in PATH"
    exit 1
fi

# Check if psycopg2 is available
echo "Checking Python dependencies..."
if ! python3 -c "import psycopg2" 2>/dev/null; then
    echo "Installing psycopg2..."
    pip3 install psycopg2-binary
fi

echo ""
echo "Running data population script..."
echo "====================================================="

# Run the Python script
python3 populate_realistic_data.py

echo ""
echo "====================================================="
echo "Data population completed successfully!"
echo "====================================================="
echo ""
echo "You can now:"
echo "1. Login to the Bank of Anthos frontend as 'testuser' with password 'bankofanthos'"
echo "2. View realistic transaction history with income and merchant spending"
echo "3. See merchant contacts in the contacts list"
echo "4. Use the AI agents to analyze spending patterns"
echo ""
echo "To re-run this script after restarting the project:"
echo "  ./populate_data.sh"
echo ""
