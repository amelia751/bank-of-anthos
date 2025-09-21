#!/bin/bash

# Bank of Anthos - AI Agents Startup Script
# This script starts all AI agents in separate terminals

set -e

echo "=============================================="
echo "Bank of Anthos - Starting AI Agents"
echo "=============================================="

# Get the directory where this script is located
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

# Check if we're in the correct directory
if [ ! -d "$DIR/boa-ai-agents" ]; then
    echo "❌ Error: boa-ai-agents directory not found"
    echo "   Please run this script from the bank-of-anthos directory"
    exit 1
fi

echo "📍 Starting from: $DIR"
echo ""

# Function to start a service in a new terminal
start_service() {
    local service_name=$1
    local port=$2
    local directory=$3
    local script=$4
    
    echo "🚀 Starting $service_name on port $port..."
    
    # For macOS Terminal
    if [[ "$OSTYPE" == "darwin"* ]]; then
        osascript -e "tell application \"Terminal\" to do script \"cd '$DIR/$directory' && PORT=$port python3 $script\""
    # For Linux (if using gnome-terminal)
    elif command -v gnome-terminal >/dev/null 2>&1; then
        gnome-terminal --tab --title="$service_name" -- bash -c "cd '$DIR/$directory' && PORT=$port python3 $script; exec bash"
    # Fallback - start in background
    else
        echo "   Starting $service_name in background..."
        cd "$DIR/$directory"
        PORT=$port python3 $script &
        echo "   PID: $!"
    fi
}

# Start each AI agent
echo "Starting AI agents..."
echo ""

start_service "Frontend Widget" 8085 "boa-ai-agents/frontend-widget" "enhanced-demo.py"
sleep 2

start_service "Perks Agent" 8083 "boa-ai-agents/perks-agent" "app.py"
sleep 2

start_service "Risk Agent" 8087 "boa-ai-agents/risk-agent" "app.py"
sleep 2

start_service "Terms Agent" 8086 "boa-ai-agents/terms-agent" "app.py"
sleep 2

echo ""
echo "=============================================="
echo "✅ AI Agents Started Successfully!"
echo "=============================================="
echo ""
echo "🌐 Access URLs:"
echo "  • Frontend Widget (main AI interface): http://localhost:8085"
echo "  • Perks Agent:                         http://localhost:8083"
echo "  • Risk Agent:                          http://localhost:8087"
echo "  • Terms Agent:                         http://localhost:8086"
echo ""
echo "🏦 Bank of Anthos Core:"
echo "  • Frontend (web app):                  http://34.41.156.37"
echo "  • Login: testuser / bankofanthos"
echo ""
echo "🔧 Port Forwards (should be running):"
echo "  • userservice:        http://localhost:8080"
echo "  • balancereader:      http://localhost:8081"
echo "  • transactionhistory: http://localhost:8082"
echo ""
echo "💡 Tips:"
echo "  • Make sure port-forwarding is active: ./setup-port-forwards.sh"
echo "  • Check agent logs in the terminal windows"
echo "  • Press Ctrl+C in any terminal to stop that agent"
echo ""
