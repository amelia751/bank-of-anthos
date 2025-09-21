#!/usr/bin/env python3
"""
Enhanced Bank of Anthos AI Demo - Cloud Version with Inline Merchant Mapping
"""

import os
import json
import logging
import requests
from flask import Flask, request, jsonify, render_template_string
from datetime import datetime
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Merchant Account Mapping (inline to avoid import issues)
MERCHANT_ACCOUNTS = {
    # Coffee Shops & Cafes
    '5001000001': {
        'name': 'Starbucks',
        'category': 'Coffee & Cafes',
        'type': 'dining',
        'frequency': 'high',
        'avg_amount_range': [4.50, 8.00]
    },
    '5001000002': {
        'name': 'Blue Bottle Coffee',
        'category': 'Coffee & Cafes', 
        'type': 'dining',
        'frequency': 'medium',
        'avg_amount_range': [4.85, 6.50]
    },
    
    # Grocery Stores
    '5002000001': {
        'name': 'Whole Foods Market',
        'category': 'Groceries',
        'type': 'essential',
        'frequency': 'high',
        'avg_amount_range': [60.00, 150.00]
    },
    '5002000002': {
        'name': 'Safeway',
        'category': 'Groceries',
        'type': 'essential', 
        'frequency': 'high',
        'avg_amount_range': [45.00, 90.00]
    },
    '5002000003': {
        'name': "Trader Joe's",
        'category': 'Groceries',
        'type': 'essential',
        'frequency': 'medium',
        'avg_amount_range': [35.00, 55.00]
    },
    
    # Restaurants
    '5003000001': {
        'name': 'The French Laundry',
        'category': 'Fine Dining',
        'type': 'dining',
        'frequency': 'low',
        'avg_amount_range': [200.00, 400.00]
    },
    '5003000002': {
        'name': 'Chipotle Mexican Grill',
        'category': 'Fast Casual',
        'type': 'dining',
        'frequency': 'medium',
        'avg_amount_range': [10.00, 15.00]
    },
    '5003000003': {
        'name': 'Local Pizza Place',
        'category': 'Restaurants',
        'type': 'dining',
        'frequency': 'medium',
        'avg_amount_range': [25.00, 35.00]
    },
    
    # Gas Stations
    '5004000001': {
        'name': 'Shell',
        'category': 'Gas & Fuel',
        'type': 'essential',
        'frequency': 'medium',
        'avg_amount_range': [35.00, 70.00]
    },
    '5004000002': {
        'name': 'Chevron',
        'category': 'Gas & Fuel',
        'type': 'essential',
        'frequency': 'medium',
        'avg_amount_range': [40.00, 80.00]
    },
    
    # Online Shopping
    '5005000001': {
        'name': 'Amazon',
        'category': 'Online Retail',
        'type': 'shopping',
        'frequency': 'high',
        'avg_amount_range': [25.00, 200.00]
    },
    '5005000002': {
        'name': 'Apple Store',
        'category': 'Electronics',
        'type': 'shopping',
        'frequency': 'low',
        'avg_amount_range': [100.00, 1500.00]
    },
    
    # Retail Stores
    '5006000001': {
        'name': 'Target',
        'category': 'Retail',
        'type': 'shopping',
        'frequency': 'medium',
        'avg_amount_range': [30.00, 120.00]
    },
    '5006000002': {
        'name': 'Best Buy',
        'category': 'Electronics',
        'type': 'shopping',
        'frequency': 'low',
        'avg_amount_range': [50.00, 800.00]
    },
    
    # Subscriptions & Services
    '5007000001': {
        'name': 'Netflix',
        'category': 'Streaming Services',
        'type': 'subscription',
        'frequency': 'monthly',
        'avg_amount_range': [15.99, 15.99]
    },
    '5007000002': {
        'name': 'Spotify',
        'category': 'Music Streaming',
        'type': 'subscription',
        'frequency': 'monthly',
        'avg_amount_range': [9.99, 9.99]
    },
    
    # Transportation
    '5008000001': {
        'name': 'Uber',
        'category': 'Rideshare',
        'type': 'transportation',
        'frequency': 'medium',
        'avg_amount_range': [12.00, 35.00]
    },
    
    # Utilities
    '5010000001': {
        'name': 'PG&E Electric Company',
        'category': 'Utilities',
        'type': 'essential',
        'frequency': 'monthly',
        'avg_amount_range': [120.00, 250.00]
    }
}

# Bank of Anthos service URLs - use Kubernetes service discovery
SERVICES = {
    'userservice': os.environ.get('USERSERVICE_URL', 'http://userservice:8080'),
    'balancereader': os.environ.get('BALANCEREADER_URL', 'http://balancereader:8080'),
    'transactionhistory': os.environ.get('TRANSACTIONHISTORY_URL', 'http://transactionhistory:8080')
}

# Demo user accounts
DEMO_USERS = {
    'testuser': {
        'account_id': '1011226111',
        'username': 'testuser',
        'password': 'bankofanthos'
    },
    'alice': {
        'account_id': '1033623433',
        'username': 'alice', 
        'password': 'bankofanthos'
    },
    'bob': {
        'account_id': '1055757655',
        'username': 'bob',
        'password': 'bankofanthos' 
    },
    'eve': {
        'account_id': '1077889977',
        'username': 'eve',
        'password': 'bankofanthos'
    }
}

class BankOfAnthosClient:
    """Client for interacting with Bank of Anthos services"""
    
    def get_auth_token(self, username):
        """Authenticate with Bank of Anthos userservice"""
        try:
            user_data = DEMO_USERS.get(username, DEMO_USERS['testuser'])
            
            response = requests.get(
                f"{SERVICES['userservice']}/login",
                params={
                    'username': user_data['username'],
                    'password': user_data['password']
                },
                timeout=5
            )
            
            if response.status_code == 200:
                return response.text.strip()
            else:
                logger.error(f"Auth failed: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            logger.error(f"Error getting auth token: {e}")
            return None
    
    def get_real_balance(self, username='testuser'):
        """Get real account balance"""
        try:
            token = self.get_auth_token(username)
            if not token:
                return 0.0
            
            user_data = DEMO_USERS.get(username, DEMO_USERS['testuser'])
            account_id = user_data['account_id']
            
            response = requests.get(
                f"{SERVICES['balancereader']}/balances/{account_id}",
                headers={'Authorization': f'Bearer {token}'},
                timeout=5
            )
            
            if response.status_code == 200:
                # Try to parse the balance properly
                balance_text = response.text.strip()
                try:
                    # Remove any currency symbols and convert
                    balance_cents = float(balance_text.replace('$', '').replace('%', '').replace(',', ''))
                    return balance_cents / 100 if balance_cents > 1000 else balance_cents  # Handle cents vs dollars
                except ValueError:
                    logger.warning(f"Could not parse balance: {balance_text}")
                    return 0.0
            else:
                logger.error(f"Balance fetch failed: {response.text}")
                return 0.0
        except Exception as e:
            logger.error(f"Error getting balance: {e}")
            return 0.0
    
    def get_real_transactions(self, username='testuser'):
        """Get real transactions from Bank of Anthos"""
        try:
            token = self.get_auth_token(username)
            if not token:
                return []
            
            user_data = DEMO_USERS.get(username, DEMO_USERS['testuser'])
            account_id = user_data['account_id']
            
            response = requests.get(
                f"{SERVICES['transactionhistory']}/transactions/{account_id}",
                headers={'Authorization': f'Bearer {token}'},
                timeout=10
            )
            
            if response.status_code == 200:
                transactions = response.json()
                logger.info(f"Retrieved {len(transactions)} transactions for account {account_id}")
                return transactions
            else:
                logger.error(f"Transaction fetch failed: {response.text}")
                return []
        except Exception as e:
            logger.error(f"Error getting transactions: {e}")
            return []

# Initialize client
boa_client = BankOfAnthosClient()

def get_spending_by_category(transactions, username='testuser'):
    """Analyze spending by category from transaction list"""
    categories = {}
    account_id = DEMO_USERS[username]['account_id']
    
    for tx in transactions:
        if tx['fromAccountNum'] == account_id:  # Only outgoing transactions
            to_account = tx['toAccountNum']
            amount = tx['amount'] / 100  # Convert cents to dollars
            
            merchant_info = MERCHANT_ACCOUNTS.get(to_account)
            if merchant_info:
                category = merchant_info['category']
                if category not in categories:
                    categories[category] = {
                        'total': 0,
                        'count': 0,
                        'merchants': set(),
                        'avg_amount': 0
                    }
                
                categories[category]['total'] += amount
                categories[category]['count'] += 1
                categories[category]['merchants'].add(merchant_info['name'])
                categories[category]['avg_amount'] = categories[category]['total'] / categories[category]['count']
            else:
                # Unknown merchant
                if 'Other' not in categories:
                    categories['Other'] = {'total': 0, 'count': 0, 'merchants': set(), 'avg_amount': 0}
                categories['Other']['total'] += amount
                categories['Other']['count'] += 1
                categories['Other']['merchants'].add(f"Account {to_account}")
                categories['Other']['avg_amount'] = categories['Other']['total'] / categories['Other']['count']
    
    # Convert sets to lists for JSON serialization
    for category in categories:
        categories[category]['merchants'] = list(categories[category]['merchants'])
    
    return categories

def get_lifestyle_insights(transactions, username):
    """Generate lifestyle insights from spending patterns"""
    insights = []
    account_id = DEMO_USERS[username]['account_id']
    
    # Analyze spending patterns
    coffee_spending = 0
    grocery_spending = 0
    dining_spending = 0
    tech_spending = 0
    
    for tx in transactions:
        if tx['fromAccountNum'] == account_id:
            to_account = tx['toAccountNum']
            amount = tx['amount'] / 100
            
            merchant_info = MERCHANT_ACCOUNTS.get(to_account)
            if merchant_info:
                category = merchant_info['category']
                if 'Coffee' in category:
                    coffee_spending += amount
                elif category == 'Groceries':
                    grocery_spending += amount
                elif category in ['Fine Dining', 'Fast Casual', 'Restaurants']:
                    dining_spending += amount
                elif category == 'Electronics':
                    tech_spending += amount
    
    # Generate insights based on spending patterns
    if coffee_spending > 50:
        insights.append(f"Coffee enthusiast - ${coffee_spending:.0f} spent on coffee")
    if grocery_spending > 200:
        insights.append(f"Responsible shopper - ${grocery_spending:.0f} on groceries")
    if dining_spending > 150:
        insights.append(f"Dining lover - ${dining_spending:.0f} on restaurants")
    if tech_spending > 500:
        insights.append(f"Tech enthusiast - ${tech_spending:.0f} on electronics")
    
    return insights

def analyze_real_transactions(transactions, username='testuser'):
    """Analyze real Bank of Anthos transactions with merchant mapping"""
    if not transactions:
        return {
            'monthly_income': 0,
            'spending_categories': {},
            'payment_reliability': 0.5,
            'balance_management': 0.5,
            'lifestyle_insights': []
        }
    
    # Calculate insights from real transaction data
    deposits = []
    payments = []
    
    for tx in transactions:
        amount = tx['amount'] / 100  # Convert cents to dollars
        
        # Identify salary deposits (from External Bank)
        if tx['fromAccountNum'] == '9099791699':
            deposits.append(amount)
        # Identify outgoing payments
        elif tx['fromAccountNum'] == DEMO_USERS[username]['account_id']:
            payments.append(amount)
    
    # Calculate monthly income from deposits
    monthly_income = sum(deposits) / max(len(deposits), 1) if deposits else 0
    
    # Use merchant mapping for detailed spending analysis
    spending_categories = get_spending_by_category(transactions, username)
    lifestyle_insights = get_lifestyle_insights(transactions, username)
    
    # Calculate payment reliability
    total_payments = len(payments)
    payment_reliability = min(0.9, 0.5 + (total_payments / 200))  # More transactions = higher reliability
    
    # Calculate balance management score
    balance_management = min(0.95, 0.6 + (monthly_income / 10000))  # Higher income = better management
    
    return {
        'monthly_income': monthly_income,
        'spending_categories': spending_categories,
        'payment_reliability': payment_reliability,
        'balance_management': balance_management,
        'lifestyle_insights': lifestyle_insights
    }

def generate_ai_credit_assessment(analysis, current_balance, transaction_count):
    """Generate AI-powered credit assessment"""
    
    # Calculate base credit score
    base_score = 580
    
    # Adjust based on transaction history
    if transaction_count > 100:
        base_score += 50
    elif transaction_count > 50:
        base_score += 30
    elif transaction_count > 20:
        base_score += 20
    
    # Adjust based on monthly income
    monthly_income = analysis.get('monthly_income', 0)
    if monthly_income > 5000:
        base_score += 80
    elif monthly_income > 3000:
        base_score += 50
    elif monthly_income > 1500:
        base_score += 30
    
    # Adjust based on current balance
    if current_balance > 5000:
        base_score += 40
    elif current_balance > 1000:
        base_score += 20
    elif current_balance > 100:
        base_score += 10
    
    # Adjust based on spending categories (responsible spending)
    spending_categories = analysis.get('spending_categories', {})
    grocery_spending = spending_categories.get('Groceries', {}).get('total', 0)
    if grocery_spending > 100:  # Regular grocery shopping shows stability
        base_score += 20
    
    # Cap the score
    credit_score = min(850, base_score)
    
    # Generate recommendation
    if credit_score >= 750:
        recommendation = "🌟 Excellent - Premium Credit Cards with Best Rewards"
    elif credit_score >= 700:
        recommendation = "✅ Very Good - Qualify for Most Credit Cards"
    elif credit_score >= 650:
        recommendation = "👍 Good - Standard Credit Cards Available"
    elif credit_score >= 600:
        recommendation = "⚠️ Fair - Consider Secured Credit Cards"
    else:
        recommendation = "⚠️ Consider Secured Credit Card"
    
    return {
        'credit_score': credit_score,
        'recommendation': recommendation,
        'ai_generated': True,
        'analysis_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

# Routes
@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'enhanced-boa-ai-demo',
        'real_data': True
    }), 200

@app.route('/api/real-preapproval')
def get_real_preapproval():
    """Get real pre-approval using actual Bank of Anthos data"""
    username = request.args.get('username', 'testuser')
    
    if username not in DEMO_USERS:
        return jsonify({'error': 'Invalid demo user'}), 400
    
    try:
        # Get real data from Bank of Anthos
        logger.info(f"Fetching real data for {username}...")
        balance = boa_client.get_real_balance(username)
        transactions = boa_client.get_real_transactions(username)
        
        # Analyze the real transaction data
        analysis = analyze_real_transactions(transactions, username)
        
        # Generate AI credit assessment
        ai_assessment = generate_ai_credit_assessment(analysis, balance, len(transactions))
        
        user_data = DEMO_USERS[username]
        
        response = {
            'username': username,
            'account_id': user_data['account_id'],
            'current_balance': balance,
            'transaction_count': len(transactions),
            'total_spending': sum(cat.get('total', 0) for cat in analysis['spending_categories'].values()),
            'spending_categories': analysis['spending_categories'],
            'credit_score': ai_assessment['credit_score'],
            'recommendation': ai_assessment['recommendation'],
            'ai_assessment': ai_assessment
        }
        
        logger.info(f"✅ Generated pre-approval for {username}: {ai_assessment['credit_score']} score, {len(transactions)} transactions")
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Error generating pre-approval: {e}")
        return jsonify({
            'error': 'Service temporarily unavailable',
            'message': 'Please ensure Bank of Anthos services are running',
            'transaction_count': 0
        }), 500

@app.route('/')
def home():
    """Home page"""
    return jsonify({
        'message': 'Enhanced Bank of Anthos AI Demo - Cloud Version',
        'service': 'enhanced-boa-ai-demo',
        'real_data': True,
        'endpoints': [
            '/api/real-preapproval?username=testuser',
            '/health'
        ]
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8084))
    logger.info(f"🚀 Starting Enhanced Bank of Anthos AI Demo - Cloud Version on port {port}")
    logger.info(f"📊 Bank of Anthos Services: {SERVICES}")
    logger.info(f"👥 Demo Users: {list(DEMO_USERS.keys())}")
    
    app.run(host='0.0.0.0', port=port, debug=False)
