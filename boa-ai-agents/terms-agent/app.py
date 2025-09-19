#!/usr/bin/env python3
"""
Terms & Offers Agent using Gemini AI
Generates personalized credit offers and explanations using Google's Gemini model
"""

import json
import logging
import os
import requests
import sys
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass
from flask import Flask, jsonify, request
import google.generativeai as genai

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class CreditOffer:
    product_type: str
    limit_range: List[int]
    apr_range: List[float]
    intro_offer: str
    perks: List[str]
    explanation: str
    terms_conditions: str

class GeminiTermsGenerator:
    """Uses Gemini AI to generate personalized credit terms and explanations"""
    
    def __init__(self):
        # Configure Gemini AI
        if config.is_gemini_enabled():
            genai.configure(api_key=config.GEMINI_API_KEY)
            self.model = genai.GenerativeModel('gemini-pro')
            self.use_ai = True
            logger.info("Gemini AI enabled with real API key")
        else:
            self.use_ai = False
            logger.warning("Using demo mode - no real Gemini API key provided")
        
        self.risk_agent_url = config.RISK_AGENT_URL
        
        # Product templates
        self.product_templates = {
            'credit_card': {
                'Bronze': {
                    'intro_offers': ['2% cash back on groceries for 3 months', '1% cash back on all purchases'],
                    'perks': ['No annual fee', 'Mobile app alerts', '24/7 customer service'],
                    'apr_base': [26.99, 29.99]
                },
                'Silver': {
                    'intro_offers': ['3% cash back on dining for 6 months', '5% cash back on gas for 3 months'],
                    'perks': ['No annual fee', 'Purchase protection', 'Extended warranty', 'Mobile app'],
                    'apr_base': [22.99, 26.99]
                },
                'Gold': {
                    'intro_offers': ['5% cash back on dining for 6 months', '2x points on travel', '0% APR for 12 months on purchases'],
                    'perks': ['Premium rewards program', 'Travel insurance', 'Purchase protection', 'Concierge service', 'Airport lounge access'],
                    'apr_base': [19.99, 22.99]
                }
            },
            'overdraft_line': {
                'Bronze': {'apr_base': [24.99, 27.99]},
                'Silver': {'apr_base': [20.99, 24.99]},
                'Gold': {'apr_base': [17.99, 20.99]}
            }
        }
    
    def get_risk_assessment(self, user_id: str) -> Dict:
        """Get risk assessment from risk agent"""
        try:
            response = requests.post(
                f"{self.risk_agent_url}/assess",
                json={'user_id': user_id}
            )
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Failed to get risk assessment: {response.text}")
                return self._default_risk_assessment()
        except Exception as e:
            logger.error(f"Error getting risk assessment: {e}")
            return self._default_risk_assessment()
    
    def _default_risk_assessment(self) -> Dict:
        """Default risk assessment for demo purposes"""
        return {
            'user_id': 'testuser',
            'score': 720,
            'tier': 'Gold',
            'risk_factors': {
                'income_stability': 0.85,
                'balance_volatility': 0.15,
                'expense_ratio': 0.75,
                'nsf_frequency': 0.0,
                'payment_reliability': 0.90
            },
            'eligibility': {
                'credit_card': {
                    'eligible': True,
                    'limit_range': [4000, 8000],
                    'apr_range': [19.99, 22.99],
                    'confidence': 0.95
                },
                'overdraft_line': {
                    'eligible': True,
                    'limit_range': [300, 700],
                    'apr_range': [17.99, 20.99],
                    'confidence': 0.90
                }
            },
            'confidence': 0.92
        }
    
    def generate_credit_card_offer(self, risk_data: Dict, spending_profile: Dict) -> CreditOffer:
        """Generate personalized credit card offer"""
        tier = risk_data['tier']
        eligibility = risk_data['eligibility']['credit_card']
        
        if not eligibility['eligible']:
            return None
        
        template = self.product_templates['credit_card'][tier]
        
        # Select intro offer based on spending patterns
        intro_offer = self._select_intro_offer(template['intro_offers'], spending_profile)
        
        # Select perks based on spending and tier
        perks = self._select_perks(template['perks'], spending_profile, tier)
        
        # Generate AI explanation
        if self.use_ai:
            explanation = self._generate_ai_explanation(risk_data, 'credit_card', spending_profile)
        else:
            explanation = self._generate_template_explanation(risk_data, 'credit_card', spending_profile)
        
        # Generate terms and conditions
        terms = self._generate_terms_conditions('credit_card', tier)
        
        return CreditOffer(
            product_type='CREDIT_CARD',
            limit_range=eligibility['limit_range'],
            apr_range=eligibility['apr_range'],
            intro_offer=intro_offer,
            perks=perks,
            explanation=explanation,
            terms_conditions=terms
        )
    
    def generate_overdraft_offer(self, risk_data: Dict) -> CreditOffer:
        """Generate overdraft line of credit offer"""
        tier = risk_data['tier']
        eligibility = risk_data['eligibility'].get('overdraft_line')
        
        if not eligibility or not eligibility['eligible']:
            return None
        
        # Generate AI explanation
        if self.use_ai:
            explanation = self._generate_ai_explanation(risk_data, 'overdraft_line', {})
        else:
            explanation = self._generate_template_explanation(risk_data, 'overdraft_line', {})
        
        terms = self._generate_terms_conditions('overdraft_line', tier)
        
        return CreditOffer(
            product_type='OVERDRAFT_LINE',
            limit_range=eligibility['limit_range'],
            apr_range=eligibility['apr_range'],
            intro_offer='No fees for first 30 days',
            perks=['Automatic overdraft protection', 'Mobile alerts', 'No minimum balance'],
            explanation=explanation,
            terms_conditions=terms
        )
    
    def _select_intro_offer(self, offers: List[str], spending_profile: Dict) -> str:
        """Select best intro offer based on spending patterns"""
        if not spending_profile:
            return offers[0]
        
        # Analyze spending to pick best offer
        dining_spend = spending_profile.get('dining', 0)
        grocery_spend = spending_profile.get('grocery', 0)
        gas_spend = spending_profile.get('gas', 0)
        
        if dining_spend > grocery_spend and dining_spend > gas_spend:
            # High dining spend - prefer dining offers
            dining_offers = [offer for offer in offers if 'dining' in offer.lower()]
            if dining_offers:
                return dining_offers[0]
        elif grocery_spend > gas_spend:
            # High grocery spend
            grocery_offers = [offer for offer in offers if 'groceries' in offer.lower()]
            if grocery_offers:
                return grocery_offers[0]
        else:
            # High gas spend
            gas_offers = [offer for offer in offers if 'gas' in offer.lower()]
            if gas_offers:
                return gas_offers[0]
        
        return offers[0]
    
    def _select_perks(self, available_perks: List[str], spending_profile: Dict, tier: str) -> List[str]:
        """Select relevant perks based on spending and tier"""
        selected_perks = available_perks.copy()
        
        # Add tier-specific perks
        if tier == 'Gold':
            if spending_profile.get('dining', 0) > 100:
                selected_perks.append('Restaurant rewards program')
            if spending_profile.get('gas', 0) > 80:
                selected_perks.append('Gas station partnerships')
        
        return selected_perks[:5]  # Limit to 5 perks
    
    def _generate_ai_explanation(self, risk_data: Dict, product_type: str, spending_profile: Dict) -> str:
        """Generate AI-powered explanation using Gemini"""
        try:
            prompt = self._build_explanation_prompt(risk_data, product_type, spending_profile)
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            logger.error(f"Error generating AI explanation: {e}")
            return self._generate_template_explanation(risk_data, product_type, spending_profile)
    
    def _build_explanation_prompt(self, risk_data: Dict, product_type: str, spending_profile: Dict) -> str:
        """Build prompt for Gemini AI explanation"""
        tier = risk_data['tier']
        score = risk_data['score']
        
        prompt = f"""
        Generate a personalized, friendly explanation for why a customer qualifies for a {product_type} with {tier} tier benefits.
        
        Customer Profile:
        - Credit Score: {score}
        - Tier: {tier}
        - Income Stability: {risk_data['risk_factors']['income_stability']:.2f}
        - Payment Reliability: {risk_data['risk_factors']['payment_reliability']:.2f}
        - Spending Categories: {spending_profile}
        
        Requirements:
        1. Keep explanation under 150 words
        2. Use friendly, encouraging tone
        3. Mention specific strengths from their profile
        4. Include appropriate disclaimers about pre-approval
        5. Focus on benefits that match their spending patterns
        6. Avoid using exact numbers from the profile
        
        Start with: "Based on your consistent banking history..."
        """
        
        return prompt
    
    def _generate_template_explanation(self, risk_data: Dict, product_type: str, spending_profile: Dict) -> str:
        """Generate template-based explanation when AI is not available"""
        tier = risk_data['tier']
        score = risk_data['score']
        
        explanations = {
            'credit_card': {
                'Gold': f"Based on your consistent banking history and excellent financial management, you qualify for our {tier} tier credit card. Your stable income patterns and reliable payment history demonstrate strong creditworthiness. This pre-approval is based on your checking account activity and is subject to final credit review.",
                'Silver': f"Your responsible banking habits and good financial standing qualify you for our {tier} tier credit card. Your consistent transaction patterns show reliable money management. This pre-approval estimate is based on checking history only and subject to full credit application review.",
                'Bronze': f"Based on your banking activity, you qualify for our {tier} tier credit card to help build your credit profile. Your account shows positive financial activity that indicates good potential. This pre-approval is an estimate based on checking history and subject to credit review."
            },
            'overdraft_line': {
                'Gold': "Your excellent account management and consistent positive balances qualify you for our premium overdraft protection with favorable terms.",
                'Silver': "Your good banking history and stable account activity qualify you for overdraft protection to help manage cash flow.",
                'Bronze': "Based on your account activity, you qualify for basic overdraft protection to help avoid declined transactions."
            }
        }
        
        return explanations.get(product_type, {}).get(tier, "You qualify for this product based on your banking history.")
    
    def _generate_terms_conditions(self, product_type: str, tier: str) -> str:
        """Generate terms and conditions"""
        base_terms = "This is a pre-approval estimate based on checking account analysis only. "
        base_terms += "Final approval subject to credit application and verification. "
        base_terms += "Terms and rates may vary based on creditworthiness. "
        
        if product_type == 'credit_card':
            base_terms += "Credit card terms subject to credit approval. Annual percentage rate (APR) may vary. "
            base_terms += "Promotional rates are for limited time only. "
        elif product_type == 'overdraft_line':
            base_terms += "Overdraft fees may apply. Subject to account agreement terms. "
        
        base_terms += "All applications subject to bank's credit policy and final approval."
        
        return base_terms
    
    def generate_offers(self, user_id: str) -> Dict:
        """Generate all available offers for a user"""
        # Get risk assessment
        risk_data = self.get_risk_assessment(user_id)
        
        # Extract spending profile for personalization
        spending_profile = self._extract_spending_profile(risk_data)
        
        offers = {}
        
        # Generate credit card offer
        credit_card_offer = self.generate_credit_card_offer(risk_data, spending_profile)
        if credit_card_offer:
            offers['credit_card'] = {
                'product_type': credit_card_offer.product_type,
                'limit_range': credit_card_offer.limit_range,
                'apr_range': credit_card_offer.apr_range,
                'intro_offer': credit_card_offer.intro_offer,
                'perks': credit_card_offer.perks,
                'explanation': credit_card_offer.explanation,
                'terms_conditions': credit_card_offer.terms_conditions
            }
        
        # Generate overdraft offer
        overdraft_offer = self.generate_overdraft_offer(risk_data)
        if overdraft_offer:
            offers['overdraft_line'] = {
                'product_type': overdraft_offer.product_type,
                'limit_range': overdraft_offer.limit_range,
                'apr_range': overdraft_offer.apr_range,
                'intro_offer': overdraft_offer.intro_offer,
                'perks': overdraft_offer.perks,
                'explanation': overdraft_offer.explanation,
                'terms_conditions': overdraft_offer.terms_conditions
            }
        
        return {
            'user_id': user_id,
            'tier': risk_data['tier'],
            'score': risk_data['score'],
            'confidence': risk_data['confidence'],
            'offers': offers,
            'timestamp': datetime.now().isoformat()
        }
    
    def _extract_spending_profile(self, risk_data: Dict) -> Dict:
        """Extract spending profile from risk data for demo purposes"""
        # This would normally come from the risk assessment
        # For demo, using realistic spending patterns
        return {
            'dining': 180.0,
            'grocery': 320.0,
            'gas': 120.0,
            'shopping': 150.0,
            'utilities': 200.0
        }

# Initialize Flask app and terms generator
app = Flask(__name__)
terms_generator = GeminiTermsGenerator()

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'terms-agent'}), 200

@app.route('/generate', methods=['POST'])
def generate_offers():
    """Generate personalized credit offers for a user"""
    data = request.get_json()
    user_id = data.get('user_id', 'testuser')
    
    try:
        offers = terms_generator.generate_offers(user_id)
        return jsonify(offers)
        
    except Exception as e:
        logger.error(f"Error generating offers: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8082))
    app.run(host='0.0.0.0', port=port, debug=False)
