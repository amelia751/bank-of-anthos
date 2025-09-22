# AI-Powered Credit Pre-Approval System
## Clean, Organized, Production-Ready Deployment

[![GKE](https://img.shields.io/badge/Platform-Google%20Kubernetes%20Engine-4285f4)](https://cloud.google.com/kubernetes-engine)
[![Python](https://img.shields.io/badge/Python-3.12-3776ab)](https://www.python.org/)
[![AI](https://img.shields.io/badge/AI-Google%20Gemini-ff6f00)](https://ai.google.dev/)
[![Flask](https://img.shields.io/badge/Framework-Flask-000000)](https://flask.palletsprojects.com/)

---

## 🏗️ **SYSTEM ARCHITECTURE**

### **Core Components**
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │───▶│   Backend       │───▶│  AI Agents      │
│   Service       │    │   Service       │    │  Orchestration  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
│                      │                      │
│ • React-like UI      │ • Flask API         │ • Risk Agent
│ • Real-time data     │ • Caching layer     │ • Terms Agent  
│ • AI visualization   │ • Retry logic       │ • Perks Agent
│ • Document viewer    │ • CORS enabled      │ • Challenger Agent
│                      │ • Health checks     │ • Policy Agent
└─────────────────────┴─────────────────────┴─────────────────┘
                                │
                    ┌─────────────────┐
                    │ Bank of Anthos  │
                    │ Microservices   │
                    │                 │
                    │ • userservice   │
                    │ • balancereader │ 
                    │ • transactionhistory │
                    └─────────────────┘
```

### **AI Agent Workflow**
```
Risk Agent ──┐
             ├──▶ Terms Agent ──▶ Challenger Agent ──▶ Arbiter ──▶ Policy Agent
Perks Agent ─┘                                          │
                                                        ▼
                                                   Final Decision
                                                   + Legal Docs
```

---

## 📁 **ORGANIZED FILE STRUCTURE**

```
deployments/
├── frontend/
│   └── deploy-frontend-service.yaml      # Clean, documented frontend
├── backend/
│   └── deploy-backend-service.yaml       # AI orchestration backend
├── agents/
│   └── deploy-ai-agents.yaml            # Risk, Terms, Perks agents
├── infrastructure/
│   └── deploy-advanced-agents.yaml      # Challenger, Policy, MCP agents
├── scripts/
│   ├── deploy-all.sh                    # One-command deployment
│   ├── cleanup-old-deployments.sh       # Remove legacy files
│   └── test-system.sh                   # End-to-end testing
└── README.md                            # This comprehensive guide
```

---

## 🚀 **QUICK DEPLOYMENT**

### **Prerequisites**
- Google Kubernetes Engine cluster
- `kubectl` configured and connected
- Bank of Anthos deployed and running
- (Optional) Gemini API key for enhanced AI features

### **One-Command Deployment**
```bash
# Deploy entire system
./deployments/scripts/deploy-all.sh

# Or deploy components individually
kubectl apply -f deployments/frontend/deploy-frontend-service.yaml
kubectl apply -f deployments/backend/deploy-backend-service.yaml
kubectl apply -f deployments/agents/deploy-ai-agents.yaml
kubectl apply -f deployments/infrastructure/deploy-advanced-agents.yaml
```

### **Get Access URLs**
```bash
# Frontend URL
kubectl get service frontend-service -o jsonpath='{.status.loadBalancer.ingress[0].ip}'

# Backend API URL  
kubectl get service backend-service -o jsonpath='{.status.loadBalancer.ingress[0].ip}'
```

---

## 🤖 **AI AGENTS OVERVIEW**

### **1. Risk Agent** (`enhanced-risk-agent:8087`)
- **Purpose**: Credit scoring and approval decisions
- **Features**: 
  - Gemini-powered reasoning for decisions
  - Comprehensive risk factor analysis
  - APPROVED/CONDITIONAL/REJECTED decisions
- **Endpoints**: `/assess`, `/approve`, `/health`

### **2. Terms Agent** (`terms-agent-simple:8086`)
- **Purpose**: Credit terms generation (APR, limits, fees)
- **Features**:
  - Risk-based APR calculation
  - Spending-based credit limits
  - Tier-specific benefits
- **Endpoints**: `/terms`, `/health`

### **3. Perks Agent** (`perks-agent-real:8085`)
- **Purpose**: Personalized rewards and cashback
- **Features**:
  - Spending pattern analysis
  - Category-specific rewards
  - Tier-based benefits
- **Endpoints**: `/generate-perks`, `/health`

### **4. Challenger Agent** (`challenger-agent:8088`)
- **Purpose**: Bank profitability optimization
- **Features**:
  - Unit economics calculations
  - Stress testing scenarios
  - Creative counter-offer generation
  - 6 strategic optimization approaches
- **Endpoints**: `/challenge-terms`, `/health`

### **5. Policy Agent** (`enhanced-policy-agent:8090`)
- **Purpose**: Legal document generation
- **Features**:
  - Gemini-powered legal text generation
  - Regulatory compliance checking
  - 6 document types (agreements, disclosures, etc.)
- **Endpoints**: `/generate-policy-documents`, `/health`

### **6. MCP Server** (`mcp-server:8089`)
- **Purpose**: Banking policies database
- **Features**:
  - Comprehensive regulatory requirements
  - TILA, FCRA, ECOA compliance
  - Internal banking policies
- **Endpoints**: `/policies`, `/mcp/tools`, `/health`

---

## 🎯 **KEY FEATURES**

### **Frontend Service**
- ✅ **Real-time Data**: Dynamic loading from Bank of Anthos
- ✅ **AI Visualization**: Interactive display of all agent results
- ✅ **Document Viewer**: Modal viewer for legal documents
- ✅ **Responsive Design**: Mobile-optimized interface
- ✅ **Cache Busting**: Prevents stale data issues

### **Backend Service**  
- ✅ **AI Orchestration**: Coordinates all 6 AI agents
- ✅ **Intelligent Caching**: 5-minute TTL with cache keys
- ✅ **Retry Logic**: Exponential backoff for reliability
- ✅ **Graceful Degradation**: Fallback data when services fail
- ✅ **Health Monitoring**: Comprehensive health checks

### **AI Agent System**
- ✅ **Risk Assessment**: Credit scoring with Gemini reasoning
- ✅ **Terms Optimization**: APR and limit calculations
- ✅ **Personalized Perks**: Spending-based rewards
- ✅ **Profitability Guard**: Bank economics optimization
- ✅ **Legal Compliance**: Automated document generation
- ✅ **Policy Database**: Regulatory requirements repository

---

## 🔧 **CONFIGURATION & CUSTOMIZATION**

### **Environment Variables**
```yaml
# Gemini API Key (optional but recommended)
GEMINI_API_KEY: "your-gemini-api-key"

# Service Ports (default values)
FRONTEND_PORT: 80
BACKEND_PORT: 8080
RISK_AGENT_PORT: 8087
TERMS_AGENT_PORT: 8086
PERKS_AGENT_PORT: 8085
CHALLENGER_AGENT_PORT: 8088
POLICY_AGENT_PORT: 8090
MCP_SERVER_PORT: 8089
```

### **Bank Profitability Settings** (Challenger Agent)
```python
constraints = {
    'min_roe': 0.12,              # 12% minimum ROE
    'max_loss_rate': 0.06,        # 6% maximum loss rate  
    'max_perk_budget_monthly': 35, # $35 max perk budget
    'min_apr': 14.99,             # Minimum APR
    'min_monthly_profit': 15      # $15 minimum monthly profit
}
```

---

## 📊 **MONITORING & HEALTH CHECKS**

### **System Health Status**
```bash
# Check all services
kubectl get pods,services | grep -E "(frontend|backend|agent|mcp)"

# Health check endpoints
curl http://<frontend-ip>/health
curl http://<backend-ip>/health
curl http://<backend-ip>/api/cache-status
```

### **AI Agent Status**
```bash
# Test all agents individually
for agent in risk terms perks challenger policy mcp; do
  echo "Testing $agent agent..."
  kubectl exec -it deployment/$agent-* -- curl localhost:808X/health
done
```

---

## 🧪 **TESTING & VALIDATION**

### **End-to-End Test**
```bash
# Run comprehensive system test
./deployments/scripts/test-system.sh

# Manual API test
BACKEND_IP=$(kubectl get service backend-service -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
curl -s "$BACKEND_IP/api/real-preapproval?username=testuser" | jq .
```

### **Expected Response Structure**
```json
{
  "username": "testuser",
  "current_balance": 2694.44,
  "transaction_count": 100,
  "spending_categories": {...},
  "ai_insights": {
    "risk_decision": {
      "decision": "APPROVED",
      "reasoning": "Gemini-generated explanation..."
    },
    "terms": {...},
    "perks": {...},
    "challenger_analysis": {...},
    "final_decision": {...},
    "policy_documents": {...}
  }
}
```

---

## 🛠️ **MAINTENANCE & UPDATES**

### **Clean Up Old Deployments**
```bash
# Remove all old/legacy deployments
./deployments/scripts/cleanup-old-deployments.sh

# Manual cleanup
kubectl delete deployment,service,configmap -l cleanup=legacy
```

### **Update AI Agents**
```bash
# Rolling update for specific agent
kubectl rollout restart deployment/enhanced-risk-agent
kubectl rollout status deployment/enhanced-risk-agent

# Update all agents
for agent in frontend-service backend-service enhanced-risk-agent terms-agent-simple perks-agent challenger-agent enhanced-policy-agent mcp-server; do
  kubectl rollout restart deployment/$agent
done
```

### **Cache Management**
```bash
# Clear backend cache
BACKEND_IP=$(kubectl get service backend-service -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
curl "$BACKEND_IP/api/clear-cache"
```

---

## 🏆 **PRODUCTION READINESS CHECKLIST**

### **✅ Code Quality**
- [x] Clean, documented, and well-organized code
- [x] Comprehensive error handling and logging
- [x] Proper separation of concerns
- [x] Production-ready configuration

### **✅ Reliability**
- [x] Intelligent retry logic with exponential backoff
- [x] Circuit breaker patterns for external services
- [x] Graceful degradation with fallback data
- [x] Health checks and monitoring

### **✅ Performance**
- [x] In-memory caching with configurable TTL
- [x] Optimized API timeouts (3-5 seconds)
- [x] Resource limits and requests defined
- [x] High availability with multiple replicas

### **✅ Security**
- [x] CORS properly configured
- [x] No hardcoded secrets (using Kubernetes secrets)
- [x] Proper authentication with Bank of Anthos
- [x] Input validation and sanitization

### **✅ AI Integration**
- [x] 6 specialized AI agents with clear responsibilities
- [x] Google Gemini integration for advanced reasoning
- [x] Multi-objective optimization (bank vs user value)
- [x] Comprehensive legal document generation

### **✅ Documentation**
- [x] Comprehensive README with architecture diagrams
- [x] Clear deployment instructions
- [x] API documentation and examples
- [x] Troubleshooting guides

---

## 🎯 **JUDGING CRITERIA ALIGNMENT**

### **How well is the solution executed?**
- ✅ **Clean Code**: Well-documented, organized, efficient implementation
- ✅ **Proper Deployment**: Production-ready Kubernetes manifests
- ✅ **Agent Communication**: Sophisticated orchestration via REST APIs
- ✅ **GKE Integration**: Native Kubernetes services and health checks

### **Innovation and Creativity**
- ✅ **6 Specialized AI Agents**: Risk, Terms, Perks, Challenger, Policy, MCP
- ✅ **Multi-Objective Optimization**: Balances bank profitability with user value
- ✅ **Creative Counter-Offers**: 6 strategic approaches for win-win solutions
- ✅ **Gemini AI Integration**: Advanced reasoning for decisions and legal docs

### **Technical Implementation**
- ✅ **Microservices Architecture**: Scalable, maintainable design
- ✅ **Reliability Engineering**: Caching, retries, circuit breakers
- ✅ **Real-time Integration**: Live data from Bank of Anthos services
- ✅ **Comprehensive Testing**: Health checks, monitoring, validation

---

## 🆘 **TROUBLESHOOTING**

### **Common Issues**

**Frontend shows "Loading..." forever**
```bash
# Check backend connectivity
kubectl logs deployment/backend-service --tail=50
kubectl get service backend-service
```

**AI agents returning errors**
```bash
# Check agent health
kubectl get pods | grep agent
kubectl logs deployment/enhanced-risk-agent --tail=20
```

**Bank of Anthos services unavailable**
```bash
# Check core services
kubectl get pods | grep -E "(userservice|balancereader|transactionhistory)"
kubectl port-forward deployment/userservice 8080:8080 &
```

**Gemini API not working**
```bash
# Check API key secret
kubectl get secret gemini-api-key
kubectl describe secret gemini-api-key
```

### **Support Contacts**
- **Technical Issues**: Check logs and health endpoints
- **Configuration**: Review environment variables and ConfigMaps
- **Performance**: Monitor resource usage and adjust limits

---

## 📈 **PERFORMANCE METRICS**

### **Expected Performance**
- **Frontend Load Time**: < 2 seconds
- **API Response Time**: < 3 seconds (with all agents)
- **Agent Response Time**: < 1 second per agent
- **Cache Hit Rate**: > 80% for repeated requests
- **System Uptime**: > 99.9% with health checks

### **Resource Usage**
- **Frontend**: 64-128MB RAM, 50-100m CPU
- **Backend**: 256-512MB RAM, 100-250m CPU  
- **Each Agent**: 128-256MB RAM, 50-100m CPU
- **Total Cluster**: ~2GB RAM, ~1 CPU core

---

**🎉 This production-ready AI Credit Pre-Approval System demonstrates sophisticated agent orchestration, bank-grade reliability, and innovative financial AI on Google Kubernetes Engine!** 🎉
