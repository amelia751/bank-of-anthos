# Bank of Anthos

<!-- Checks badge below seem to take a "neutral" check as a negative and shows failures if some checks are neutral. Commenting out the badge for now. -->
<!-- ![GitHub branch check runs](https://img.shields.io/github/check-runs/GoogleCloudPlatform/bank-of-anthos/main) -->
[![Website](https://img.shields.io/website?url=https%3A%2F%2Fcymbal-bank.fsi.cymbal.dev%2F&label=live%20demo
)](https://cymbal-bank.fsi.cymbal.dev)

**Bank of Anthos** is a sample HTTP-based web app that simulates a bank's payment processing network, allowing users to create artificial bank accounts and complete transactions.

🤖 **NEW: AI-Enhanced Demo** - Bank of Anthos now includes AI-powered agents that provide intelligent credit assessment, personalized financial offers, and real-time spending analysis based on realistic transaction data. [Jump to AI Setup](#-ai-agents-setup-enhanced-demo) →

Google uses this application to demonstrate how developers can modernize enterprise applications using Google Cloud products, including: [Google Kubernetes Engine (GKE)](https://cloud.google.com/kubernetes-engine), [Anthos Service Mesh (ASM)](https://cloud.google.com/anthos/service-mesh), [Anthos Config Management (ACM)](https://cloud.google.com/anthos/config-management), [Migrate to Containers](https://cloud.google.com/migrate/containers), [Spring Cloud GCP](https://spring.io/projects/spring-cloud-gcp), [Cloud Operations](https://cloud.google.com/products/operations), [Cloud SQL](https://cloud.google.com/sql/docs), [Cloud Build](https://cloud.google.com/build), and [Cloud Deploy](https://cloud.google.com/deploy). This application works on any Kubernetes cluster.

If you are using Bank of Anthos, please ★Star this repository to show your interest!

**Note to Googlers:** Please fill out the form at [go/bank-of-anthos-form](https://goto2.corp.google.com/bank-of-anthos-form).

## Screenshots

| Sign in                                                                                                        | Home                                                                                                    |
| ----------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| [![Login](/docs/img/login.png)](/docs/img/login.png) | [![User Transactions](/docs/img/transactions.png)](/docs/img/transactions.png) |


## Service architecture

![Architecture Diagram](/docs/img/architecture.png)

| Service                                                 | Language      | Description                                                                                                                                  |
| ------------------------------------------------------- | ------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| [frontend](/src/frontend)                              | Python        | Exposes an HTTP server to serve the website. Contains login page, signup page, and home page.                                                |
| [ledger-writer](/src/ledger/ledgerwriter)              | Java          | Accepts and validates incoming transactions before writing them to the ledger.                                                               |
| [balance-reader](/src/ledger/balancereader)            | Java          | Provides efficient readable cache of user balances, as read from `ledger-db`.                                                                |
| [transaction-history](/src/ledger/transactionhistory)  | Java          | Provides efficient readable cache of past transactions, as read from `ledger-db`.                                                            |
| [ledger-db](/src/ledger/ledger-db)                     | PostgreSQL    | Ledger of all transactions. Option to pre-populate with transactions for demo users.                                                         |
| [user-service](/src/accounts/userservice)              | Python        | Manages user accounts and authentication. Signs JWTs used for authentication by other services.                                              |
| [contacts](/src/accounts/contacts)                     | Python        | Stores list of other accounts associated with a user. Used for drop down in "Send Payment" and "Deposit" forms.                              |
| [accounts-db](/src/accounts/accounts-db)               | PostgreSQL    | Database for user accounts and associated data. Option to pre-populate with demo users.                                                      |
| [loadgenerator](/src/loadgenerator)                    | Python/Locust | Continuously sends requests imitating users to the frontend. Periodically creates new accounts and simulates transactions between them.      |
| **AI Agents** ([boa-ai-agents](/boa-ai-agents))        | Python        | **AI-powered credit assessment and personalized offers.** See [AI Agents Setup](#-ai-agents-setup-enhanced-demo) below for complete setup. |

## Interactive quickstart (GKE)

The following button opens up an interactive tutorial showing how to deploy Bank of Anthos in GKE:

[![Open in Cloud Shell](https://gstatic.com/cloudssh/images/open-btn.svg)](https://ssh.cloud.google.com/cloudshell/editor?show=ide&cloudshell_git_repo=https://github.com/GoogleCloudPlatform/bank-of-anthos&cloudshell_workspace=.&cloudshell_tutorial=extras/cloudshell/tutorial.md)

## Quickstart (GKE)

1. Ensure you have the following requirements:
   - [Google Cloud project](https://cloud.google.com/resource-manager/docs/creating-managing-projects#creating_a_project).
   - Shell environment with `gcloud`, `git`, and `kubectl`.

2. Clone the repository.

   ```sh
   git clone https://github.com/GoogleCloudPlatform/bank-of-anthos
   cd bank-of-anthos/
   ```

3. Set the Google Cloud project and region and ensure the Google Kubernetes Engine API is enabled.

   ```sh
   export PROJECT_ID=<PROJECT_ID>
   export REGION=us-central1
   gcloud services enable container.googleapis.com \
     --project=${PROJECT_ID}
   ```

   Substitute `<PROJECT_ID>` with the ID of your Google Cloud project.

4. Create a GKE cluster and get the credentials for it.

   ```sh
   gcloud container clusters create-auto bank-of-anthos \
     --project=${PROJECT_ID} --region=${REGION}
   ```

   Creating the cluster may take a few minutes.

5. Deploy Bank of Anthos to the cluster.

   ```sh
   kubectl apply -f ./extras/jwt/jwt-secret.yaml
   kubectl apply -f ./kubernetes-manifests
   ```

6. Wait for the pods to be ready.

   ```sh
   kubectl get pods
   ```

   After a few minutes, you should see the Pods in a `Running` state:

   ```
   NAME                                  READY   STATUS    RESTARTS   AGE
   accounts-db-6f589464bc-6r7b7          1/1     Running   0          99s
   balancereader-797bf6d7c5-8xvp6        1/1     Running   0          99s
   contacts-769c4fb556-25pg2             1/1     Running   0          98s
   frontend-7c96b54f6b-zkdbz             1/1     Running   0          98s
   ledger-db-5b78474d4f-p6xcb            1/1     Running   0          98s
   ledgerwriter-84bf44b95d-65mqf         1/1     Running   0          97s
   loadgenerator-559667b6ff-4zsvb        1/1     Running   0          97s
   transactionhistory-5569754896-z94cn   1/1     Running   0          97s
   userservice-78dc876bff-pdhtl          1/1     Running   0          96s
   ```

7. Access the web frontend in a browser using the frontend's external IP.

   ```sh
   kubectl get service frontend | awk '{print $4}'
   ```

   Visit `http://EXTERNAL_IP` in a web browser to access your instance of Bank of Anthos.

8. Once you are done with it, delete the GKE cluster.

   ```sh
   gcloud container clusters delete bank-of-anthos \
     --project=${PROJECT_ID} --region=${REGION}
   ```

   Deleting the cluster may take a few minutes.

## 🤖 AI Agents Setup (Enhanced Demo)

Bank of Anthos includes AI-powered agents that provide intelligent credit assessment, personalized offers, and spending analysis based on realistic transaction data. Follow these steps to set up the complete AI-enhanced experience.

### Prerequisites
- Bank of Anthos deployed and running (complete steps 1-6 above)
- `kubectl` configured to access your cluster
- Python 3.8+ installed locally

### Step 1: Populate Realistic Transaction Data

The AI agents need realistic spending data to provide meaningful analysis. Run the data population script:

```bash
# Populate the database with realistic user spending habits
./populate_data.sh
```

This script:
- ✅ Creates 333+ realistic transactions for testuser
- ✅ Adds income deposits (bi-weekly paychecks)
- ✅ Generates merchant expenses across 20+ categories (coffee, groceries, gas, etc.)
- ✅ Includes peer-to-peer transfers
- ✅ Adds 24+ merchant contacts to user accounts

**Expected output:**
```
SUCCESS! Realistic spending data has been populated.
Income deposits: 7
Merchant expenses: 320
Peer transfers: 6
Total transactions: 333
Merchant contacts added: 24
```

### Step 2: Set Up Port Forwarding for AI Agents

The AI agents need access to Bank of Anthos services running in your cluster. Set up port forwarding:

```bash
# Set up all required port forwards
./setup-port-forwards.sh
```

**Keep this terminal open** - the port forwards must remain active for AI agents to work.

**Expected output:**
```
✅ Port forwards established successfully!

Active port forwards:
  📡 userservice:        http://localhost:8080
  💰 balancereader:      http://localhost:8081
  📊 transactionhistory: http://localhost:8082
```

### Step 3: Start the AI Agents

In separate terminals, start each AI agent:

```bash
# Terminal 1: Frontend Widget (main AI interface)
cd boa-ai-agents/frontend-widget
PORT=8084 python3 enhanced-demo.py

# Terminal 2: Perks Agent (personalized benefits)
cd boa-ai-agents/perks-agent
PORT=8083 python3 app.py

# Terminal 3: Risk Agent (credit assessment)
cd boa-ai-agents/risk-agent
PORT=8085 python3 app.py

# Terminal 4: Terms Agent (contract terms)
cd boa-ai-agents/terms-agent
PORT=8086 python3 app.py
```

### Step 4: Access the AI-Enhanced Frontend

Once all services are running, access the AI-powered credit assessment interface:

🌐 **AI Frontend Widget**: http://localhost:8084

**Features:**
- **Real-time spending analysis** based on populated transaction data
- **AI-powered credit assessment** using Gemini AI (if configured)
- **Personalized credit card offers** tailored to spending habits
- **Spending categorization** across 18+ categories
- **Lifestyle insights** and financial recommendations

### Troubleshooting AI Agents

**Problem: Spending categories show "Loading..." forever**
```bash
# Check if port forwards are active
ps aux | grep "kubectl.*port-forward" | grep -v grep

# If no output, restart port forwards
./setup-port-forwards.sh
```

**Problem: API returns "Could not fetch real balance data"**
```bash
# Test API connectivity
curl -s "http://localhost:8084/api/real-preapproval?username=testuser" | jq '.transaction_count'

# Should return: 100 (or higher number)
# If null or error, restart port forwards
```

**Problem: No transaction data**
```bash
# Verify data was populated
kubectl exec -it ledger-db-0 -- psql -U admin -d postgresdb -c \
  "SELECT COUNT(*) FROM transactions WHERE from_acct = '1011226111';"

# Should return: 333 (or higher)
# If 0, re-run: ./populate_data.sh
```

### Persistent Setup After Restart

When you restart your machine or redeploy the cluster:

```bash
# 1. Deploy Bank of Anthos
kubectl apply -f ./kubernetes-manifests

# 2. Wait for pods to be ready
kubectl wait --for=condition=ready pod --all --timeout=300s

# 3. Set up port forwarding (keep terminal open)
./setup-port-forwards.sh

# 4. Repopulate data (if needed)
./populate_data.sh

# 5. Start AI agents
cd boa-ai-agents/frontend-widget && PORT=8084 python3 enhanced-demo.py
```

### AI Agent Architecture

```
📱 Frontend Widget (8084) ←→ 🏦 Bank of Anthos Services
    ↓                           ├── userservice (8080)
🎁 Perks Agent (8083)          ├── balancereader (8081)
🎯 Risk Agent (8085)           └── transactionhistory (8082)
📋 Terms Agent (8086)
```

### Documentation

- 📖 [PORT_FORWARD_SETUP.md](PORT_FORWARD_SETUP.md) - Detailed port forwarding guide
- 📊 [POPULATE_DATA_README.md](POPULATE_DATA_README.md) - Data population details
- 🏪 [boa-ai-agents/merchant_mapping.py](boa-ai-agents/merchant_mapping.py) - Merchant categories

---

## Additional deployment options

- **Workload Identity**: [See these instructions.](/docs/workload-identity.md)
- **Cloud SQL**: [See these instructions](/extras/cloudsql) to replace the in-cluster databases with hosted Google Cloud SQL.
- **Multi Cluster with Cloud SQL**: [See these instructions](/extras/cloudsql-multicluster) to replicate the app across two regions using GKE, Multi Cluster Ingress, and Google Cloud SQL.
- **Istio**: [See these instructions](/extras/istio) to configure an IngressGateway.
- **Anthos Service Mesh**: ASM requires Workload Identity to be enabled in your GKE cluster. [See the workload identity instructions](/docs/workload-identity.md) to configure and deploy the app. Then, apply `extras/istio/` to your cluster to configure frontend ingress.
- **Java Monolith (VM)**: We provide a version of this app where the three Java microservices are coupled together into one monolithic service, which you can deploy inside a VM (eg. Google Compute Engine). See the [ledgermonolith](/src/ledgermonolith) directory.

## Documentation

<!-- This section is duplicated in the docs/ README: https://github.com/GoogleCloudPlatform/bank-of-anthos/blob/main/docs/README.md -->

- [Development](/docs/development.md) to learn how to run and develop this app locally.
- [Environments](/docs/environments.md) to learn how to deploy on non-GKE clusters.
- [Workload Identity](/docs/workload-identity.md) to learn how to set-up Workload Identity.
- [CI/CD pipeline](/docs/ci-cd-pipeline.md) to learn details about and how to set-up the CI/CD pipeline.
- [Troubleshooting](/docs/troubleshooting.md) to learn how to resolve common problems.

## Demos featuring Bank of Anthos
- [Tutorial: Explore Anthos (Google Cloud docs)](https://cloud.google.com/anthos/docs/tutorials/explore-anthos)
- [Tutorial: Migrating a monolith VM to GKE](https://cloud.google.com/migrate/containers/docs/migrating-monolith-vm-overview-setup)
- [Tutorial: Running distributed services on GKE private clusters using ASM](https://cloud.google.com/service-mesh/docs/distributed-services-private-clusters)
- [Tutorial: Run full-stack workloads at scale on GKE](https://cloud.google.com/kubernetes-engine/docs/tutorials/full-stack-scale)
- [Architecture: Anthos on bare metal](https://cloud.google.com/architecture/ara-anthos-on-bare-metal)
- [Architecture: Creating and deploying secured applications](https://cloud.google.com/architecture/security-foundations/creating-deploying-secured-apps)
- [Keynote @ Google Cloud Next '20: Building trust for speedy innovation](https://www.youtube.com/watch?v=7QR1z35h_yc)
- [Workshop @ IstioCon '22: Manage and secure distributed services with ASM](https://www.youtube.com/watch?v=--mPdAxovfE)
