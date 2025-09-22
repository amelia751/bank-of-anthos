# 🤖 AI-Enhanced Bank of Anthos - Credit Pre-Approval System

[![GKE](https://img.shields.io/badge/Platform-Google%20Kubernetes%20Engine-4285f4)](https://cloud.google.com/kubernetes-engine)
[![Gemini](https://img.shields.io/badge/AI-Google%20Gemini-34a853)](https://ai.google.dev/)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-00d924)](#)

**AI-Enhanced Bank of Anthos** demonstrates intelligent credit pre-approval using multi-agent AI orchestration on Google Kubernetes Engine. This system adds comprehensive AI capabilities to the existing Bank of Anthos platform without modifying core services.

## 🌐 **Quick Access**

- **🎯 Live Demo**: `http://34.120.148.160/`
- **🔗 API Endpoint**: `http://34.120.148.160/api/real-preapproval?username=testuser`
- **🏦 Original Bank System**: `http://34.41.156.37/home` (login: `testuser` / `bankofanthos`)

## 🎯 **What This System Does**

### **Intelligent Credit Assessment**
- **Real-time Analysis**: Analyzes actual spending patterns from Bank of Anthos transactions
- **AI-Powered Decisions**: Uses Google Gemini AI for intelligent risk assessment and terms generation
- **Multi-Agent Orchestration**: 6 specialized AI agents work together for comprehensive evaluation
- **Bank Profitability**: Optimizes offers to balance customer value with bank economics

### **Key Features**
- ✅ **Instant Pre-Approval**: Credit decisions in seconds based on spending behavior
- ✅ **Personalized Terms**: APR, credit limits, and perks tailored to spending patterns  
- ✅ **Smart Guardrails**: Prevents unrealistic values with intelligent validation
- ✅ **Policy Generation**: Creates legal documents and regulatory disclosures
- ✅ **Production Ready**: Comprehensive error handling, caching, and monitoring

## 🏗️ **System Architecture**

### **📁 Project Structure**
```
bank-of-anthos/
├── deployments/                    # 🚀 Production Kubernetes Deployments
│   ├── frontend/                   # AI-enhanced frontend interface
│   ├── backend/                    # AI orchestration backend
│   ├── agents/                     # Core AI agents (Risk, Terms, Perks)
│   ├── infrastructure/             # Advanced agents (Challenger, Policy, MCP)
│   ├── adk/                        # Agent Development Kit framework
│   ├── kubectl-ai/                 # Intelligent Kubernetes operations
│   └── ingress/                    # Public access configuration
│
├── boa-ai-agents/                  # 🤖 AI Agent Configuration
│   ├── config.py                   # Shared AI agent configuration
│   ├── README.md                   # AI agents documentation
│   └── .env                        # Environment variables (create from .env.example)
│   
│   Note: All AI agent code is embedded in Kubernetes ConfigMaps
│         within deployments/ for production deployment
│
├── src/                           # 🏦 Original Bank of Anthos Services
│   ├── frontend/                  # Web interface
│   ├── accounts/                  # Account management (userservice, contacts, accounts-db)
│   ├── ledger/                    # Transaction processing (balancereader, ledgerwriter, ledger-db)
│   └── loadgenerator/             # Traffic simulation
│
└── docs/                          # 📚 Documentation
```

### **🤖 AI Agent Pipeline**
```
User Request → Backend Orchestrator → Real-time Bank Data
     ↓
AI Agent Pipeline:
Risk Agent → Terms Agent → Perks Agent → Challenger Agent → Arbiter → Policy Agent
     ↓
Comprehensive Credit Decision with Legal Documents
```

## 🚀 **Quick Start**

### **Prerequisites**
- Google Kubernetes Engine cluster
- `kubectl` configured for your cluster
- Bank of Anthos deployed and running
- Google Gemini API key

### **Configuration**
```bash
# Option 1: Set Gemini API key directly in Kubernetes (Recommended)
kubectl create secret generic gemini-secret --from-literal=api-key=YOUR_GEMINI_API_KEY

# Option 2: Configure via environment file
cd boa-ai-agents/
# Create .env file with GEMINI_API_KEY=your_key_here
# (See config.py for all available configuration options)
```

### **Deploy AI System**
```bash
# Deploy all AI components
kubectl apply -f deployments/

# Verify deployment
kubectl get pods,services

# Access the system
open http://34.120.148.160/
```

### **Test the API**
```bash
# Get comprehensive credit analysis
curl "http://34.120.148.160/api/real-preapproval?username=testuser"

# Check agent health
curl "http://34.120.148.160/health"
```

## 🤖 **AI Agents Overview**

### **Core Agents**
1. **🎯 Risk Agent**: Analyzes creditworthiness using spending patterns and Gemini AI
2. **📋 Terms Agent**: Generates APR, credit limits, and terms with intelligent guardrails
3. **🎁 Perks Agent**: Creates personalized cashback offers based on spending categories

### **Advanced Agents**
4. **⚖️ Challenger Agent**: Stress-tests offers for bank profitability optimization
5. **📜 Policy Agent**: Generates legal documents and regulatory disclosures
6. **🗄️ MCP Server**: Provides banking policies and compliance frameworks

### **Supporting Infrastructure**
- **🏗️ Agent Development Kit (ADK)**: Standardized agent interfaces
- **🔄 kubectl-ai**: Natural language Kubernetes operations
- **📊 Backend Orchestrator**: Intelligent agent coordination with retry logic

## 🎯 **Technology Stack**

### **Required Technologies**
- ✅ **Google Kubernetes Engine (GKE)**: Autopilot cluster with auto-scaling
- ✅ **Google AI Models (Gemini)**: Integrated across all AI agents

### **Optional Technologies (All Implemented)**
- ✅ **Agent Development Kit (ADK)**: Custom framework for standardized agents
- ✅ **Model Context Protocol (MCP)**: Banking policies and compliance server
- ✅ **Agent2Agent (A2A)**: Multi-agent communication protocols
- ✅ **kubectl-ai**: Intelligent Kubernetes management interface
- ✅ **Gemini CLI**: AI workflow automation throughout the system

## 📊 **Demo Flow**

### **1. Credit Pre-Approval Demo**
1. Visit the AI frontend: `http://34.120.148.160/`
2. Click **"Get My Personalized Offer"**
3. Watch real-time AI agent orchestration
4. Review comprehensive credit analysis with:
   - Risk assessment and credit score
   - Personalized APR and credit limit
   - Cashback recommendations
   - Legal document generation

### **2. API Testing**
```bash
# Comprehensive analysis
curl "http://34.120.148.160/api/real-preapproval?username=testuser" | jq .

# Individual agent health
curl "http://34.120.148.160/agents/risk/health"
curl "http://34.120.148.160/agents/terms/health"
```

### **3. Original Bank Integration**
- View transaction data: `http://34.41.156.37/home`
- Login: `testuser` / `bankofanthos`
- See how AI system uses real spending patterns

## 🏆 **Key Innovations**

### **Real-World AI Application**
- **Live Data Integration**: Uses actual Bank of Anthos transaction data
- **Intelligent Decision Making**: Gemini AI powers risk assessment and terms generation
- **Multi-Agent Orchestration**: Sophisticated agent coordination with A2A protocols

### **Production-Ready Features**
- **Smart Guardrails**: Prevents undefined values and unrealistic terms
- **Retry Logic**: Handles network failures gracefully
- **Caching Strategy**: Optimizes performance with intelligent caching
- **Health Monitoring**: Comprehensive system monitoring and alerting

### **Business Value**
- **Bank Profitability**: Challenger agent optimizes offers for ROI
- **Risk Management**: AI-powered risk assessment with stress testing
- **Regulatory Compliance**: Automated legal document generation
- **Customer Experience**: Instant decisions with transparent explanations

## 🔧 **System Administration**

### **Restart All Services**
```bash
# Quick restart of all AI components
kubectl rollout restart deployment/frontend-service
kubectl rollout restart deployment/backend-service
kubectl rollout restart deployment/enhanced-policy-agent
kubectl rollout restart deployment/risk-agent-simple
kubectl rollout restart deployment/terms-agent-simple
```

### **Check System Health**
```bash
# Verify all pods are running
kubectl get pods

# Check service endpoints
kubectl get services

# Monitor logs
kubectl logs -l app=backend-service --tail=20
```

### **Access Points Discovery**
```bash
# Get external IPs
kubectl get services --field-selector spec.type=LoadBalancer
kubectl get ingress
```

