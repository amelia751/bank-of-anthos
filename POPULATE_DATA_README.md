# Bank of Anthos - Realistic Data Population

This directory contains scripts to populate the Bank of Anthos database with realistic user spending habits and transaction data. The data persists across project restarts and provides meaningful context for AI-powered credit assessment and spending analysis.

## Quick Start

Run the population script:

```bash
./populate_data.sh
```

## What Gets Created

### 📊 **333 Realistic Transactions**
- **7 Income Deposits**: Bi-weekly paychecks from External Bank (~$2,500 each)
- **320 Merchant Expenses**: Realistic spending across 24+ merchant categories
- **6 Peer Transfers**: Occasional money transfers to Alice, Bob, and Eve

### 🏪 **24 Merchant Contacts**
- Coffee shops (Starbucks, Blue Bottle Coffee)
- Grocery stores (Whole Foods, Safeway, Trader Joe's)
- Restaurants (Fine dining, fast casual, pizza)
- Gas stations (Shell, Chevron)
- Online shopping (Amazon, Apple Store)
- Retail stores (Target, Best Buy, CVS)
- Subscriptions (Netflix, Spotify, Gym)
- Transportation (Uber, Lyft)
- Travel (United Airlines, Airbnb)
- Utilities (PG&E, Internet Provider)

### 💳 **Realistic Spending Patterns**
- **High-frequency**: Coffee, groceries (2-3x/week)
- **Medium-frequency**: Restaurants, gas, rideshare (1-2x/week)  
- **Low-frequency**: Travel, electronics (1-2x/month)
- **Monthly**: Subscriptions and utilities on specific dates

## User Account Details

- **Primary User**: `testuser` (account: 1011226111)
- **Recipients**: Alice, Bob, Eve (for peer transfers)
- **External Bank**: Account 9099791699 (for income deposits)
- **Login**: Username `testuser`, Password `bankofanthos`

## Data Generation Strategy

The script uses a **deterministic approach** with fixed random seeds to ensure:
- **Reproducible data** across multiple runs
- **Realistic timing** (coffee in mornings, dining at meal times)
- **Appropriate amounts** based on merchant categories
- **Consistent patterns** that mimic real user behavior

## Database Architecture

The script populates two separate databases:
- **Ledger DB** (`ledger-db-0`): Contains transaction history
- **Accounts DB** (`accounts-db-0`): Contains user contacts and account info

## Files

- `populate_data.sh` - Main execution script with database connectivity
- `populate_realistic_data.py` - Python script that generates and inserts data
- `boa-ai-agents/merchant_mapping.py` - Merchant definitions and categories

## Verification

After running the script, you can verify the data:

```bash
# Check transaction count for testuser
kubectl exec -it ledger-db-0 -- psql -U admin -d postgresdb -c \
  "SELECT COUNT(*) FROM transactions WHERE from_acct = '1011226111' OR to_acct = '1011226111';"

# Check merchant contacts count
kubectl exec -it accounts-db-0 -- psql -U accounts-admin -d accounts-db -c \
  "SELECT COUNT(*) FROM contacts WHERE username = 'testuser';"
```

## AI Agent Analysis

With this realistic data, you can:
1. **Login** to Bank of Anthos as `testuser`
2. **View transactions** with meaningful merchant names and amounts
3. **Use AI agents** to analyze spending patterns by category
4. **Get insights** on dining habits, travel spending, subscription management
5. **Test credit assessment** with realistic income/expense ratios

## Re-running After Restart

After restarting the Bank of Anthos project:

1. **Set up port forwarding** (required for AI agents):
   ```bash
   ./setup-port-forwards.sh
   ```

2. **Repopulate transaction data**:
   ```bash
   ./populate_data.sh
   ```

The scripts will:
- Set up required service connections
- Clear existing testuser data
- Repopulate with the same fixed dataset
- Preserve other demo user data

📖 **See also:** [PORT_FORWARD_SETUP.md](PORT_FORWARD_SETUP.md) for detailed port forwarding instructions.

---

**Happy Banking!** 🏦✨
