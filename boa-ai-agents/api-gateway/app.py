#!/usr/bin/env python3
"""
AI Pre-approval API Gateway
Orchestrates risk assessment and terms generation for credit pre-approval
"""

import json
import logging
import os
import requests
from datetime import datetime
from typing import Dict, Optional
from flask import Flask, jsonify, request, render_template_string
from flask_cors import CORS
import asyncio
import concurrent.futures

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PreApprovalOrchestrator:
    """Orchestrates the AI agents for credit pre-approval"""
    
    def __init__(self):
        self.risk_agent_url = os.getenv('RISK_AGENT_URL', 'http://risk-agent:8081')
        self.terms_agent_url = os.getenv('TERMS_AGENT_URL', 'http://terms-agent:8082')
        
        # API rate limiting and caching could be added here
        self.cache = {}
        self.cache_ttl = 300  # 5 minutes
    
    def get_preapproval(self, user_id: str) -> Dict:
        """Get complete pre-approval assessment for a user"""
        # Check cache first
        cache_key = f"preapproval_{user_id}"
        if cache_key in self.cache:
            cached_data, timestamp = self.cache[cache_key]
            if (datetime.now() - timestamp).seconds < self.cache_ttl:
                logger.info(f"Returning cached pre-approval for {user_id}")
                return cached_data
        
        try:
            # Use concurrent execution for better performance
            with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
                # Submit both requests concurrently
                risk_future = executor.submit(self._get_risk_assessment, user_id)
                terms_future = executor.submit(self._get_terms_offers, user_id)
                
                # Wait for risk assessment first
                risk_data = risk_future.result(timeout=10)
                
                # Then get terms (which depends on risk assessment)
                terms_data = terms_future.result(timeout=10)
            
            # Combine results
            result = self._combine_results(user_id, risk_data, terms_data)
            
            # Cache the result
            self.cache[cache_key] = (result, datetime.now())
            
            return result
            
        except concurrent.futures.TimeoutError:
            logger.error("Timeout waiting for agent responses")
            return self._error_response(user_id, "Service timeout")
        except Exception as e:
            logger.error(f"Error getting pre-approval: {e}")
            return self._error_response(user_id, str(e))
    
    def _get_risk_assessment(self, user_id: str) -> Dict:
        """Get risk assessment from risk agent"""
        try:
            response = requests.post(
                f"{self.risk_agent_url}/assess",
                json={'user_id': user_id},
                timeout=8
            )
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Risk agent error: {response.status_code} - {response.text}")
                return self._default_risk_assessment(user_id)
        except requests.exceptions.RequestException as e:
            logger.error(f"Error calling risk agent: {e}")
            return self._default_risk_assessment(user_id)
    
    def _get_terms_offers(self, user_id: str) -> Dict:
        """Get terms and offers from terms agent"""
        try:
            response = requests.post(
                f"{self.terms_agent_url}/generate",
                json={'user_id': user_id},
                timeout=8
            )
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Terms agent error: {response.status_code} - {response.text}")
                return self._default_terms_offers(user_id)
        except requests.exceptions.RequestException as e:
            logger.error(f"Error calling terms agent: {e}")
            return self._default_terms_offers(user_id)
    
    def _combine_results(self, user_id: str, risk_data: Dict, terms_data: Dict) -> Dict:
        """Combine risk assessment and terms data into final response"""
        return {
            'user_id': user_id,
            'eligible': True,
            'tier': risk_data.get('tier', 'Silver'),
            'score': risk_data.get('score', 650),
            'confidence': min(risk_data.get('confidence', 0.8), terms_data.get('confidence', 0.8)),
            'risk_factors': risk_data.get('risk_factors', {}),
            'products': self._format_products(terms_data.get('offers', {})),
            'timestamp': datetime.now().isoformat(),
            'status': 'success'
        }
    
    def _format_products(self, offers: Dict) -> list:
        """Format offers into product list"""
        products = []
        
        for product_type, offer_data in offers.items():
            if offer_data:
                product = {
                    'type': offer_data['product_type'],
                    'limit_range': offer_data['limit_range'],
                    'apr_range': offer_data['apr_range'],
                    'intro_offer': offer_data['intro_offer'],
                    'perks': offer_data['perks'],
                    'explanation_md': offer_data['explanation'],
                    'terms_conditions': offer_data['terms_conditions']
                }
                products.append(product)
        
        return products
    
    def _default_risk_assessment(self, user_id: str) -> Dict:
        """Default risk assessment for fallback"""
        return {
            'user_id': user_id,
            'score': 650,
            'tier': 'Silver',
            'risk_factors': {
                'income_stability': 0.75,
                'balance_volatility': 0.25,
                'expense_ratio': 0.80,
                'payment_reliability': 0.85
            },
            'confidence': 0.70
        }
    
    def _default_terms_offers(self, user_id: str) -> Dict:
        """Default terms offers for fallback"""
        return {
            'user_id': user_id,
            'tier': 'Silver',
            'offers': {
                'credit_card': {
                    'product_type': 'CREDIT_CARD',
                    'limit_range': [1500, 3000],
                    'apr_range': [22.99, 26.99],
                    'intro_offer': '3% cash back on dining for 3 months',
                    'perks': ['No annual fee', 'Mobile alerts', 'Purchase protection'],
                    'explanation': 'Based on your banking history, you qualify for our Silver tier credit card with competitive rates and benefits.',
                    'terms_conditions': 'This is a pre-approval estimate. Final approval subject to credit application.'
                }
            },
            'confidence': 0.75
        }
    
    def _error_response(self, user_id: str, error: str) -> Dict:
        """Generate error response"""
        return {
            'user_id': user_id,
            'eligible': False,
            'error': error,
            'timestamp': datetime.now().isoformat(),
            'status': 'error'
        }

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend integration
orchestrator = PreApprovalOrchestrator()

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'preapproval-api-gateway'}), 200

@app.route('/preapproval', methods=['GET', 'POST'])
def get_preapproval():
    """Main pre-approval endpoint"""
    if request.method == 'POST':
        data = request.get_json()
        user_id = data.get('user_id', 'testuser')
    else:
        user_id = request.args.get('user_id', 'testuser')
    
    try:
        result = orchestrator.get_preapproval(user_id)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in pre-approval endpoint: {e}")
        return jsonify({
            'user_id': user_id,
            'eligible': False,
            'error': 'Internal service error',
            'timestamp': datetime.now().isoformat(),
            'status': 'error'
        }), 500

@app.route('/widget', methods=['GET'])
def get_widget():
    """Frontend widget endpoint - returns HTML for embedding"""
    user_id = request.args.get('user_id', 'testuser')
    
    # Simple HTML widget that can be embedded in the Bank of Anthos frontend
    widget_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>AI Credit Pre-Approval</title>
        <style>
            .preapproval-widget {
                font-family: Arial, sans-serif;
                max-width: 600px;
                margin: 20px auto;
                padding: 20px;
                border: 1px solid #ddd;
                border-radius: 8px;
                background: #f9f9f9;
            }
            .offer-card {
                background: white;
                margin: 10px 0;
                padding: 15px;
                border-radius: 5px;
                border-left: 4px solid #4CAF50;
            }
            .tier-badge {
                display: inline-block;
                padding: 4px 8px;
                border-radius: 4px;
                font-size: 12px;
                font-weight: bold;
                color: white;
            }
            .tier-gold { background-color: #FFD700; color: #333; }
            .tier-silver { background-color: #C0C0C0; color: #333; }
            .tier-bronze { background-color: #CD7F32; color: white; }
            .btn-primary {
                background-color: #007bff;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 4px;
                cursor: pointer;
                text-decoration: none;
                display: inline-block;
                margin: 5px 0;
            }
            .loading {
                text-align: center;
                padding: 20px;
            }
            .error {
                color: #dc3545;
                padding: 10px;
                background: #f8d7da;
                border-radius: 4px;
            }
        </style>
    </head>
    <body>
        <div class="preapproval-widget" id="preapproval-widget">
            <h3>🤖 AI Credit Pre-Approval</h3>
            <div class="loading">
                <p>Analyzing your account data...</p>
                <div>⏳ Loading...</div>
            </div>
        </div>

        <script>
            function loadPreApproval() {
                const widget = document.getElementById('preapproval-widget');
                
                fetch('/preapproval?user_id={{ user_id }}')
                    .then(response => response.json())
                    .then(data => {
                        if (data.status === 'success' && data.eligible) {
                            widget.innerHTML = `
                                <h3>🤖 AI Credit Pre-Approval Results</h3>
                                <div style="margin: 15px 0;">
                                    <span class="tier-badge tier-${data.tier.toLowerCase()}">${data.tier} Tier</span>
                                    <span style="margin-left: 10px;">Score: ${data.score}</span>
                                    <span style="margin-left: 10px;">Confidence: ${Math.round(data.confidence * 100)}%</span>
                                </div>
                                
                                ${data.products.map(product => `
                                    <div class="offer-card">
                                        <h4>${product.type.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}</h4>
                                        <p><strong>Credit Limit:</strong> $${product.limit_range[0].toLocaleString()} - $${product.limit_range[1].toLocaleString()}</p>
                                        <p><strong>APR Range:</strong> ${product.apr_range[0]}% - ${product.apr_range[1]}%</p>
                                        <p><strong>Intro Offer:</strong> ${product.intro_offer}</p>
                                        <p><strong>Benefits:</strong> ${product.perks.join(', ')}</p>
                                        <div style="background: #f0f8ff; padding: 10px; border-radius: 4px; margin: 10px 0;">
                                            <p><strong>Why you qualify:</strong></p>
                                            <p style="font-style: italic;">${product.explanation_md}</p>
                                        </div>
                                        <button class="btn-primary" onclick="alert('Apply now feature would redirect to application form')">
                                            Apply Now
                                        </button>
                                    </div>
                                `).join('')}
                                
                                <div style="font-size: 12px; color: #666; margin-top: 15px;">
                                    <p><strong>Important:</strong> This is a pre-qualification estimate based on your checking account activity. Final approval subject to credit application and verification.</p>
                                </div>
                            `;
                        } else {
                            widget.innerHTML = `
                                <h3>🤖 AI Credit Pre-Approval</h3>
                                <div class="error">
                                    <p>Unable to generate pre-approval at this time.</p>
                                    <p>${data.error || 'Please try again later or contact customer service.'}</p>
                                </div>
                            `;
                        }
                    })
                    .catch(error => {
                        widget.innerHTML = `
                            <h3>🤖 AI Credit Pre-Approval</h3>
                            <div class="error">
                                <p>Service temporarily unavailable. Please try again later.</p>
                            </div>
                        `;
                    });
            }
            
            // Load the data when the page loads
            setTimeout(loadPreApproval, 1000);
        </script>
    </body>
    </html>
    """
    
    return render_template_string(widget_html, user_id=user_id)

@app.route('/status', methods=['GET'])
def get_status():
    """Service status endpoint"""
    try:
        # Check connectivity to other services
        risk_status = 'unknown'
        terms_status = 'unknown'
        
        try:
            risk_response = requests.get(f"{orchestrator.risk_agent_url}/health", timeout=2)
            risk_status = 'healthy' if risk_response.status_code == 200 else 'unhealthy'
        except:
            risk_status = 'unreachable'
        
        try:
            terms_response = requests.get(f"{orchestrator.terms_agent_url}/health", timeout=2)
            terms_status = 'healthy' if terms_response.status_code == 200 else 'unhealthy'
        except:
            terms_status = 'unreachable'
        
        overall_status = 'healthy' if risk_status == 'healthy' and terms_status == 'healthy' else 'degraded'
        
        return jsonify({
            'status': overall_status,
            'services': {
                'api_gateway': 'healthy',
                'risk_agent': risk_status,
                'terms_agent': terms_status
            },
            'cache_size': len(orchestrator.cache),
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8083))
    app.run(host='0.0.0.0', port=port, debug=False)
