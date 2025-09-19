#!/usr/bin/env python3
"""
Perks Agent for Bank of Anthos AI Credit Pre-Approval System

This agent specializes in creating highly personalized credit card perks, 
benefits, and fee structures based on user spending patterns and lifestyle insights.
"""

import os
import json
from datetime import datetime
from flask import Flask, request, jsonify
import google.generativeai as genai
import sys
import logging

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import GEMINI_API_KEY, is_gemini_enabled

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

class PerksGenerator:
    def __init__(self):
        self.gemini_enabled = is_gemini_enabled()
        if self.gemini_enabled and GEMINI_API_KEY:
            genai.configure(api_key=GEMINI_API_KEY)
            self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
            logging.info("✅ Perks Agent: Gemini AI enabled for personalized perks generation")
        else:
            self.model = None
            logging.info("⚠️ Perks Agent: Using fallback templates - Gemini disabled")

    def generate_personalized_perks(self, user_data, spending_analysis):
        """Generate highly personalized credit card perks based on spending patterns"""
        
        if not self.gemini_enabled or not self.model:
            return self._generate_fallback_perks(spending_analysis)
        
        try:
            # Extract key spending patterns
            top_categories = spending_analysis.get('top_categories', [])
            lifestyle_insights = spending_analysis.get('lifestyle_insights', [])
            monthly_spending = spending_analysis.get('total_spending', 0)
            
            prompt = f"""
            You are an expert credit card product designer creating the most compelling and profitable personalized credit card for this customer.

            Customer Profile:
            • Balance: ${user_data.get('balance', 0):.2f}
            • Monthly Income: ${spending_analysis.get('monthly_income', 0):.2f}
            • Monthly Spending: ${monthly_spending:.2f}
            • Credit Score Tier: {spending_analysis.get('tier', 'Silver')}
            
            Detailed Spending Analysis:
            {self._format_spending_data(spending_analysis)}
            
            Lifestyle Insights:
            {chr(10).join(f"• {insight}" for insight in lifestyle_insights) if lifestyle_insights else "• Standard spending patterns"}
            
            TASK: Design a highly profitable credit card with ultra-personalized perks that will:
            1. Drive customer loyalty through benefits they'll ACTUALLY use
            2. Maximize interchange revenue through targeted incentives
            3. Include strategic fees that customers accept for the value
            4. Create competitive differentiation through personalization
            
            Return ONLY valid JSON in this exact format:
            {{
                "card_name": "Bank of Anthos [Personalized Name]",
                "annual_fee": 95,
                "foreign_transaction_fee_pct": 2.7,
                "late_payment_fee": 39,
                "balance_transfer_fee_pct": 3.0,
                "cash_advance_fee": 25,
                "overlimit_fee": 0,
                "primary_cashback": {{
                    "category": "specific category they spend most on",
                    "rate": 5.0,
                    "description": "5% cash back on [specific merchants/category]"
                }},
                "secondary_cashback": {{
                    "category": "second highest spending category", 
                    "rate": 3.0,
                    "description": "3% cash back on [category]"
                }},
                "base_cashback": 1.0,
                "signup_bonus": {{
                    "amount": 200,
                    "spend_requirement": 2000,
                    "timeframe": 3,
                    "description": "Earn $200 bonus after spending $2,000 in first 3 months"
                }},
                "personalized_perks": [
                    "Monthly $15 credit at [their favorite merchant/chain]",
                    "Free [service they'd value] worth $X annually",
                    "Exclusive [benefit matching their lifestyle]",
                    "Priority [service] with no fees"
                ],
                "lifestyle_benefits": [
                    "Benefit specifically for their commute/travel patterns",
                    "Perk for their dining preferences",
                    "Service for their shopping habits"
                ],
                "fee_justification": "Why customers accept the annual fee given these specific benefits",
                "profit_strategy": "How bank maximizes profit from this customer's specific spending patterns",
                "competitive_edge": "What makes this card uniquely valuable vs generic cards"
            }}
            """
            
            response = self.model.generate_content(prompt)
            
            # Parse the JSON response
            response_text = response.text.strip()
            if response_text.startswith('```json'):
                response_text = response_text[7:-3]
            elif response_text.startswith('```'):
                response_text = response_text[3:-3]
            
            perks_data = json.loads(response_text)
            perks_data['ai_generated'] = True
            perks_data['timestamp'] = datetime.now().isoformat()
            
            logging.info(f"Generated personalized perks for spending pattern: {top_categories[:2]}")
            return perks_data
            
        except Exception as e:
            logging.error(f"Error generating AI perks: {e}")
            return self._generate_fallback_perks(spending_analysis)
    
    def _format_spending_data(self, analysis):
        """Format spending data for AI prompt"""
        lines = []
        
        if 'top_categories' in analysis:
            lines.append("Top Spending Categories:")
            for i, cat in enumerate(analysis['top_categories'][:5], 1):
                lines.append(f"  {i}. {cat.get('category', 'Unknown')}: ${cat.get('amount', 0):.2f}/month ({cat.get('percentage', 0):.1f}%)")
        
        if 'merchant_frequency' in analysis:
            lines.append("\nMerchant Patterns:")
            for merchant, data in list(analysis['merchant_frequency'].items())[:3]:
                lines.append(f"  • {merchant}: {data.get('frequency', 'occasional')} visits, ${data.get('avg_amount', 0):.2f} avg")
        
        return '\n'.join(lines) if lines else "Standard spending patterns observed"
    
    def _generate_fallback_perks(self, analysis):
        """Generate template-based perks when AI is unavailable"""
        tier = analysis.get('tier', 'Silver')
        top_category = analysis.get('top_categories', [{}])[0].get('category', 'Dining')
        
        if tier == 'Gold':
            return {
                "card_name": "Bank of Anthos Gold Rewards",
                "annual_fee": 95,
                "foreign_transaction_fee_pct": 2.7,
                "late_payment_fee": 39,
                "balance_transfer_fee_pct": 3.0,
                "cash_advance_fee": 25,
                "overlimit_fee": 0,
                "primary_cashback": {
                    "category": top_category,
                    "rate": 5.0,
                    "description": f"5% cash back on {top_category}"
                },
                "secondary_cashback": {
                    "category": "Groceries",
                    "rate": 3.0,
                    "description": "3% cash back on groceries"
                },
                "base_cashback": 1.0,
                "signup_bonus": {
                    "amount": 200,
                    "spend_requirement": 2000,
                    "timeframe": 3,
                    "description": "Earn $200 bonus after spending $2,000 in first 3 months"
                },
                "personalized_perks": [
                    "Annual $100 dining credit",
                    "Free DashPass for 1 year",
                    "Priority customer service",
                    "Extended warranty on purchases"
                ],
                "lifestyle_benefits": [
                    "Travel insurance coverage",
                    "Purchase protection",
                    "Price match guarantee"
                ],
                "fee_justification": "Annual fee provides $200+ in value through credits and perks",
                "profit_strategy": "High interchange from bonus categories + responsible fee structure",
                "competitive_edge": "Personalized rewards in customer's top spending categories",
                "ai_generated": False,
                "timestamp": datetime.now().isoformat()
            }
        else:
            return {
                "card_name": "Bank of Anthos Silver Rewards",
                "annual_fee": 0,
                "foreign_transaction_fee_pct": 2.7,
                "late_payment_fee": 39,
                "balance_transfer_fee_pct": 3.0,
                "cash_advance_fee": 25,
                "overlimit_fee": 0,
                "primary_cashback": {
                    "category": top_category,
                    "rate": 3.0,
                    "description": f"3% cash back on {top_category}"
                },
                "secondary_cashback": {
                    "category": "Gas",
                    "rate": 2.0,
                    "description": "2% cash back on gas"
                },
                "base_cashback": 1.0,
                "signup_bonus": {
                    "amount": 150,
                    "spend_requirement": 1000,
                    "timeframe": 3,
                    "description": "Earn $150 bonus after spending $1,000 in first 3 months"
                },
                "personalized_perks": [
                    "No annual fee",
                    "Mobile alerts and controls",
                    "Fraud protection",
                    "Credit score tracking"
                ],
                "lifestyle_benefits": [
                    "Cash back on everyday purchases",
                    "Easy mobile app",
                    "Build credit history"
                ],
                "fee_justification": "No annual fee with valuable cash back rewards",
                "profit_strategy": "Volume-based interchange revenue with low customer acquisition cost",
                "competitive_edge": "No-fee card with personalized bonus categories",
                "ai_generated": False,
                "timestamp": datetime.now().isoformat()
            }

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "perks-agent",
        "ai_enabled": is_gemini_enabled(),
        "timestamp": datetime.now().isoformat()
    })

@app.route('/generate-perks', methods=['POST'])
def generate_perks():
    """Generate personalized credit card perks"""
    try:
        data = request.get_json()
        
        user_data = data.get('user_data', {})
        spending_analysis = data.get('spending_analysis', {})
        
        if not spending_analysis:
            return jsonify({"error": "Spending analysis is required"}), 400
        
        perks_generator = PerksGenerator()
        perks_data = perks_generator.generate_personalized_perks(user_data, spending_analysis)
        
        return jsonify({
            "success": True,
            "perks": perks_data,
            "generated_at": datetime.now().isoformat()
        })
        
    except Exception as e:
        logging.error(f"Error in generate_perks: {e}")
        return jsonify({"error": "Failed to generate perks"}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8085))
    logging.info(f"🎁 Starting Perks Agent on port {port}")
    logging.info(f"✅ Gemini AI enabled: {is_gemini_enabled()}")
    app.run(host='0.0.0.0', port=port, debug=True)
