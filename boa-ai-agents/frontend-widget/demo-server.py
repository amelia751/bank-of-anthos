#!/usr/bin/env python3
"""
Demo server for Bank of Anthos AI Credit Pre-approval
Simple Flask server to demonstrate the AI agents concept
"""

import json
import logging
import os
import sys
from datetime import datetime
from flask import Flask, render_template, jsonify, request, send_from_directory
from flask_cors import CORS
import random

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import config
from realistic_data import data_generator

# Import Gemini AI if available
try:
    import google.generativeai as genai
    if config.is_gemini_enabled():
        genai.configure(api_key=config.GEMINI_API_KEY)
        gemini_model = genai.GenerativeModel('gemini-pro')
        GEMINI_AVAILABLE = True
        print("✅ Gemini AI enabled with real API key!")
    else:
        GEMINI_AVAILABLE = False
        print("⚠️  Using demo mode - no real Gemini API key")
except ImportError:
    GEMINI_AVAILABLE = False
    print("⚠️  Gemini AI not available - install google-generativeai")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Generate realistic demo data using our data generator
def get_demo_user_data(user_id: str = 'testuser'):
    """Get realistic demo user data"""
    transactions = data_generator.generate_transactions(user_id, 6)
    spending_summary = data_generator.get_spending_summary(user_id)
    
    # Calculate balance from transactions
    balance = 1250.75  # Starting balance
    for tx in transactions:
        balance += tx['amount']
    
    # Calculate monthly income from salary transactions
    salary_transactions = [tx for tx in transactions if tx['amount'] > 0 and 'PAYROLL' in tx['description']]
    monthly_income = sum(tx['amount'] for tx in salary_transactions) / 6 if salary_transactions else 3200
    
    return {
        'account_id': '1011226800',
        'balance': round(balance, 2),
        'monthly_income': round(monthly_income, 2),
        'transactions': transactions[:10],  # Show last 10 transactions
        'spending_categories': spending_summary
    }

def generate_ai_explanation(user_data, risk_data, product_type='credit_card'):
    """Generate AI-powered explanation using Gemini"""
    if not GEMINI_AVAILABLE:
        # Fallback to template explanations
        tier = risk_data['tier']
        templates = {
            'Gold': "Based on your consistent banking history and excellent financial management, you demonstrate strong creditworthiness. Your stable income patterns and reliable payment history make you eligible for our premium offers.",
            'Silver': "Your responsible banking habits and good financial standing qualify you for our Silver tier benefits. Your consistent transaction patterns show reliable money management.",
            'Bronze': "Based on your banking activity, you show positive financial potential with room for growth. Your account demonstrates good financial habits."
        }
        return templates.get(tier, templates['Silver'])
    
    try:
        # Create a detailed prompt for Gemini
        spending = user_data['spending_categories']
        top_categories = sorted(spending.items(), key=lambda x: x[1], reverse=True)[:3]
        
        prompt = f"""
        You are a friendly financial advisor explaining why a customer qualifies for a {product_type.replace('_', ' ')} offer.
        
        Customer Profile:
        - Credit Score: {risk_data['score']}
        - Tier: {risk_data['tier']}
        - Monthly Income: ${user_data['monthly_income']:,.2f}
        - Current Balance: ${user_data['balance']:,.2f}
        - Top Spending Categories: {', '.join([f'{cat}: ${amt:.0f}/month' for cat, amt in top_categories])}
        
        Generate a personalized, encouraging explanation (100-150 words) that:
        1. Congratulates them on their financial management
        2. Mentions specific strengths from their profile
        3. Explains why they qualify for this tier
        4. Mentions how their spending patterns influenced the offer
        5. Includes appropriate disclaimers
        
        Use a warm, professional tone. Start with "Based on your banking history..."
        """
        
        response = gemini_model.generate_content(prompt)
        return response.text
        
    except Exception as e:
        logger.error(f"Error generating AI explanation: {e}")
        # Fallback to template
        return "Based on your banking history and financial patterns, you demonstrate excellent creditworthiness and qualify for our premium offers. This assessment is subject to final credit review."

def simulate_risk_assessment(user_id):
    """Simulate risk assessment agent response"""
    user_data = get_demo_user_data(user_id)
    
    # Simulate AI risk analysis
    score = random.randint(720, 780)  # Good to excellent range
    
    if score >= 750:
        tier = 'Gold'
    elif score >= 650:
        tier = 'Silver'
    else:
        tier = 'Bronze'
    
    return {
        'user_id': user_id,
        'score': score,
        'tier': tier,
        'risk_factors': {
            'income_stability': round(random.uniform(0.80, 0.95), 2),
            'balance_volatility': round(random.uniform(0.10, 0.25), 2),
            'expense_ratio': round(random.uniform(0.70, 0.85), 2),
            'nsf_frequency': 0.0,
            'payment_reliability': round(random.uniform(0.90, 1.0), 2)
        },
        'eligibility': {
            'credit_card': {
                'eligible': True,
                'limit_range': [4000, 8000] if tier == 'Gold' else [1500, 4000],
                'apr_range': [19.99, 22.99] if tier == 'Gold' else [22.99, 26.99],
                'confidence': round(random.uniform(0.85, 0.95), 2)
            },
            'overdraft_line': {
                'eligible': True,
                'limit_range': [300, 700] if tier == 'Gold' else [100, 300],
                'apr_range': [17.99, 20.99] if tier == 'Gold' else [20.99, 24.99],
                'confidence': round(random.uniform(0.80, 0.90), 2)
            }
        },
        'confidence': round(random.uniform(0.85, 0.95), 2)
    }

def simulate_terms_generation(user_id, risk_data):
    """Simulate terms agent response with Gemini AI"""
    user_data = get_demo_user_data(user_id)
    tier = risk_data['tier']
    
    # Generate AI explanation using Gemini
    ai_explanation = generate_ai_explanation(user_data, risk_data, 'credit_card')
    
    offers = {}
    
    # Credit card offer
    if risk_data['eligibility']['credit_card']['eligible']:
        offers['credit_card'] = {
            'product_type': 'CREDIT_CARD',
            'limit_range': risk_data['eligibility']['credit_card']['limit_range'],
            'apr_range': risk_data['eligibility']['credit_card']['apr_range'],
            'intro_offer': '5% cash back on dining for 6 months' if tier == 'Gold' else '3% cash back on groceries for 3 months',
            'perks': [
                'Premium rewards program', 'Travel insurance', 'Purchase protection', 
                'Concierge service', 'Airport lounge access'
            ] if tier == 'Gold' else [
                'No annual fee', 'Mobile alerts', 'Purchase protection', 'Extended warranty'
            ],
            'explanation': ai_explanation,
            'terms_conditions': 'This is a pre-approval estimate based on checking account analysis only. Final approval subject to credit application and verification.'
        }
    
    # Overdraft line offer
    if risk_data['eligibility']['overdraft_line']['eligible']:
        offers['overdraft_line'] = {
            'product_type': 'OVERDRAFT_LINE',
            'limit_range': risk_data['eligibility']['overdraft_line']['limit_range'],
            'apr_range': risk_data['eligibility']['overdraft_line']['apr_range'],
            'intro_offer': 'No fees for first 30 days',
            'perks': ['Automatic overdraft protection', 'Mobile alerts', 'No minimum balance'],
            'explanation': f"Your excellent account management qualifies you for {tier} tier overdraft protection with favorable terms.",
            'terms_conditions': 'Overdraft fees may apply. Subject to account agreement terms.'
        }
    
    return {
        'user_id': user_id,
        'tier': tier,
        'score': risk_data['score'],
        'confidence': risk_data['confidence'],
        'offers': offers,
        'timestamp': datetime.now().isoformat()
    }

@app.route('/')
def home():
    """Serve the main demo page"""
    return send_from_directory('.', 'index.html')

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'ai-preapproval-demo'}), 200

@app.route('/preapproval')
def get_preapproval():
    """Main pre-approval endpoint"""
    user_id = request.args.get('user_id', 'testuser')
    
    try:
        # Simulate the agent orchestration
        risk_data = simulate_risk_assessment(user_id)
        terms_data = simulate_terms_generation(user_id, risk_data)
        
        # Combine results like the real API gateway would
        result = {
            'user_id': user_id,
            'eligible': True,
            'tier': risk_data['tier'],
            'score': risk_data['score'],
            'confidence': risk_data['confidence'],
            'risk_factors': risk_data['risk_factors'],
            'products': [],
            'timestamp': datetime.now().isoformat(),
            'status': 'success'
        }
        
        # Format products
        for product_type, offer_data in terms_data['offers'].items():
            product = {
                'type': offer_data['product_type'],
                'limit_range': offer_data['limit_range'],
                'apr_range': offer_data['apr_range'],
                'intro_offer': offer_data['intro_offer'],
                'perks': offer_data['perks'],
                'explanation_md': offer_data['explanation'],
                'terms_conditions': offer_data['terms_conditions']
            }
            result['products'].append(product)
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error in pre-approval endpoint: {e}")
        return jsonify({
            'user_id': user_id,
            'eligible': False,
            'error': 'Demo service error',
            'timestamp': datetime.now().isoformat(),
            'status': 'error'
        }), 500

@app.route('/demo/user-data')
def get_demo_user_data():
    """Get demo user data for display"""
    user_id = request.args.get('user_id', 'testuser')
    user_data = DEMO_USER_DATA.get(user_id, DEMO_USER_DATA['testuser'])
    return jsonify(user_data)

@app.route('/demo/architecture')
def get_architecture_info():
    """Get information about the AI architecture"""
    return jsonify({
        'components': [
            {
                'name': 'MCP Server',
                'description': 'Wraps Bank of Anthos read-only APIs (transactions, balances, users)',
                'technology': 'Python Flask + Model Context Protocol',
                'role': 'Data abstraction layer for AI agents'
            },
            {
                'name': 'Risk Assessment Agent',
                'description': 'Analyzes financial patterns and computes creditworthiness scores',
                'technology': 'Python + NumPy + Statistical Analysis',
                'role': 'Credit risk evaluation using checking account data only'
            },
            {
                'name': 'Terms & Offers Agent',
                'description': 'Uses Gemini AI to generate personalized credit offers and explanations',
                'technology': 'Google Gemini AI + Python',
                'role': 'Intelligent offer generation with natural language explanations'
            },
            {
                'name': 'API Gateway',
                'description': 'Orchestrates agents and provides external API for integration',
                'technology': 'Python Flask + Async processing',
                'role': 'Service orchestration and external interface'
            }
        ],
        'deployment': {
            'platform': 'Google Kubernetes Engine (GKE Autopilot)',
            'features': [
                'Auto-scaling based on CPU and request metrics',
                'Zero-touch node management',
                'Integrated Cloud Logging and Monitoring',
                'Workload Identity for secure service access',
                'Horizontal Pod Autoscaler for each agent'
            ]
        },
        'hackathon_requirements': [
            'Built on GKE ✓',
            'Uses Google AI models (Gemini) ✓',
            'Leverages MCP for API integration ✓',
            'Zero changes to core Bank of Anthos ✓',
            'External containerized AI components ✓',
            'Demonstrates practical AI use case ✓'
        ]
    })

if __name__ == '__main__':
    port = 8080
    print(f"""
🚀 Bank of Anthos AI Credit Pre-approval Demo Server Starting...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 GKE Hackathon Demo: AI Upgrade for Microservices
🎯 Challenge: Add intelligent credit pre-approval without touching core code

🌐 Demo URLs:
   • Main Demo: http://localhost:{port}/
   • API Endpoint: http://localhost:{port}/preapproval?user_id=testuser
   • Health Check: http://localhost:{port}/health
   • Architecture Info: http://localhost:{port}/demo/architecture

🤖 AI Components:
   • Risk Assessment Agent (Credit scoring from transaction patterns)
   • Terms Generation Agent (Gemini AI for personalized explanations)
   • MCP Server (Bank of Anthos API wrapper)
   • API Gateway (Service orchestration)

🛠️ Tech Stack:
   • Google Kubernetes Engine (GKE Autopilot)
   • Google Gemini AI
   • Model Context Protocol (MCP)
   • Multi-agent architecture with auto-scaling

🏆 Ready for hackathon presentation!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    """)
    
    app.run(host='0.0.0.0', port=port, debug=True)
