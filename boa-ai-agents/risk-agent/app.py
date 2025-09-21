#!/usr/bin/env python3
"""
Risk Assessment Agent for Credit Pre-approval
Analyzes checking account data to assess creditworthiness and make approval decisions
"""

import json
import logging
import os
import requests
import statistics
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from flask import Flask, jsonify, request
import numpy as np

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    logging.warning("Google Generative AI not available - using rule-based decisions")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class CreditAssessment:
    user_id: str
    score: int
    tier: str
    risk_factors: Dict
    eligibility: Dict
    confidence: float

@dataclass
class FinancialFeatures:
    monthly_net_inflow: float
    income_stability: float
    avg_balance: float
    min_balance: float
    nsf_events: int
    expense_ratio: float
    payment_consistency: float
    category_spending: Dict[str, float]

class RiskAnalyzer:
    """Analyzes financial data to assess credit risk and make approval decisions"""
    
    def __init__(self):
        self.mcp_url = os.getenv('MCP_SERVER_URL', 'http://boa-mcp:8080')
        self.mcp_api_key = os.getenv('MCP_API_KEY', 'mcp-demo-key-123')
        
        # Initialize Gemini for reasoning
        if GEMINI_AVAILABLE:
            api_key = os.getenv('GEMINI_API_KEY', 'demo-key')
            if api_key and api_key != 'demo-key':
                try:
                    genai.configure(api_key=api_key)
                    self.model = genai.GenerativeModel('gemini-1.5-flash')
                    logger.info("✅ Gemini API initialized for risk reasoning")
                except Exception as e:
                    logger.warning(f"⚠️ Gemini API failed: {e}")
                    self.model = None
            else:
                logger.info("📝 Using rule-based decisions (no Gemini API key)")
                self.model = None
        else:
            self.model = None
        
        # Risk scoring thresholds
        self.score_weights = {
            'income_stability': 0.25,
            'cash_flow': 0.20,
            'balance_management': 0.20,
            'payment_consistency': 0.15,
            'expense_ratio': 0.20
        }
        
        # Credit tiers
        self.tiers = {
            'Bronze': {'min_score': 0, 'max_score': 599},
            'Silver': {'min_score': 600, 'max_score': 699},
            'Gold': {'min_score': 700, 'max_score': 850}
        }
    
    def get_user_data(self, user_id: str, months: int = 6) -> Tuple[List[Dict], Dict]:
        """Fetch user transaction and balance data from MCP server"""
        headers = {'X-API-Key': self.mcp_api_key}
        
        try:
            # Get transactions
            tx_response = requests.get(
                f"{self.mcp_url}/mcp/tools/list_transactions",
                params={'userId': user_id, 'months': months},
                headers=headers
            )
            
            # Get balance
            balance_response = requests.get(
                f"{self.mcp_url}/mcp/tools/get_balance",
                params={'userId': user_id},
                headers=headers
            )
            
            if tx_response.status_code == 200 and balance_response.status_code == 200:
                transactions = tx_response.json().get('transactions', [])
                balance_data = balance_response.json()
                return transactions, balance_data
            else:
                logger.error(f"Failed to fetch user data: {tx_response.status_code}, {balance_response.status_code}")
                return [], {}
                
        except Exception as e:
            logger.error(f"Error fetching user data: {e}")
            return [], {}
    
    def extract_features(self, transactions: List[Dict], balance_data: Dict) -> FinancialFeatures:
        """Extract financial features from transaction data"""
        if not transactions:
            return self._default_features()
        
        # Sort transactions by date
        sorted_transactions = sorted(transactions, key=lambda x: x['date'])
        
        # Calculate monthly net inflows
        monthly_inflows = self._calculate_monthly_inflows(sorted_transactions)
        avg_monthly_inflow = statistics.mean(monthly_inflows) if monthly_inflows else 0
        inflow_volatility = statistics.stdev(monthly_inflows) if len(monthly_inflows) > 1 else 0
        
        # Income stability (inverse of volatility)
        income_stability = max(0, 1 - (inflow_volatility / max(avg_monthly_inflow, 1)))
        
        # Balance analysis
        current_balance = balance_data.get('balance', 0)
        balance_history = self._estimate_daily_balances(sorted_transactions, current_balance)
        avg_balance = statistics.mean(balance_history) if balance_history else current_balance
        min_balance = min(balance_history) if balance_history else current_balance
        
        # NSF events (negative balance days)
        nsf_events = sum(1 for b in balance_history if b < 0)
        
        # Expense analysis
        recurring_expenses = self._identify_recurring_expenses(sorted_transactions)
        total_monthly_expenses = sum(recurring_expenses.values())
        expense_ratio = total_monthly_expenses / max(avg_monthly_inflow, 1) if avg_monthly_inflow > 0 else 1.0
        
        # Payment consistency
        payment_consistency = self._calculate_payment_consistency(sorted_transactions)
        
        # Category spending
        category_spending = self._categorize_spending(sorted_transactions)
        
        return FinancialFeatures(
            monthly_net_inflow=avg_monthly_inflow,
            income_stability=income_stability,
            avg_balance=avg_balance,
            min_balance=min_balance,
            nsf_events=nsf_events,
            expense_ratio=expense_ratio,
            payment_consistency=payment_consistency,
            category_spending=category_spending
        )
    
    def _default_features(self) -> FinancialFeatures:
        """Return default features for demo purposes"""
        return FinancialFeatures(
            monthly_net_inflow=3200,
            income_stability=0.85,
            avg_balance=1250,
            min_balance=200,
            nsf_events=0,
            expense_ratio=0.75,
            payment_consistency=0.90,
            category_spending={
                'dining': 180.0,
                'grocery': 320.0,
                'utilities': 200.0,
                'gas': 120.0,
                'shopping': 150.0
            }
        )
    
    def _calculate_monthly_inflows(self, transactions: List[Dict]) -> List[float]:
        """Calculate net inflow for each month"""
        monthly_data = {}
        
        for tx in transactions:
            date = datetime.fromisoformat(tx['date'].replace('Z', '+00:00'))
            month_key = date.strftime('%Y-%m')
            
            if month_key not in monthly_data:
                monthly_data[month_key] = 0
            
            monthly_data[month_key] += tx['amount']
        
        return list(monthly_data.values())
    
    def _estimate_daily_balances(self, transactions: List[Dict], current_balance: float) -> List[float]:
        """Estimate daily balance history from transactions"""
        # Simple approximation: work backwards from current balance
        balance = current_balance
        balances = [balance]
        
        for tx in reversed(transactions[-90:]):  # Last 90 days
            balance -= tx['amount']
            balances.append(balance)
        
        return balances
    
    def _identify_recurring_expenses(self, transactions: List[Dict]) -> Dict[str, float]:
        """Identify recurring monthly expenses"""
        recurring_patterns = {}
        expense_transactions = [tx for tx in transactions if tx['amount'] < 0]
        
        # Group by description
        by_description = {}
        for tx in expense_transactions:
            desc = tx['description']
            if desc not in by_description:
                by_description[desc] = []
            by_description[desc].append(abs(tx['amount']))
        
        # Identify recurring expenses (appearing multiple times)
        for desc, amounts in by_description.items():
            if len(amounts) >= 3:  # Appears at least 3 times
                avg_amount = statistics.mean(amounts)
                if 'RENT' in desc.upper() or 'MORTGAGE' in desc.upper():
                    recurring_patterns['housing'] = avg_amount
                elif any(word in desc.upper() for word in ['ELECTRIC', 'GAS', 'WATER', 'UTILITIES']):
                    recurring_patterns['utilities'] = recurring_patterns.get('utilities', 0) + avg_amount
                elif 'PHONE' in desc.upper() or 'WIRELESS' in desc.upper():
                    recurring_patterns['phone'] = avg_amount
        
        return recurring_patterns
    
    def _calculate_payment_consistency(self, transactions: List[Dict]) -> float:
        """Calculate consistency of recurring payments"""
        # Simple metric: ratio of successful vs missed payment patterns
        recurring_expenses = self._identify_recurring_expenses(transactions)
        if not recurring_expenses:
            return 0.8  # Default good score
        
        # For demo purposes, assume good payment consistency
        return 0.90
    
    def _categorize_spending(self, transactions: List[Dict]) -> Dict[str, float]:
        """Categorize spending by merchant/description"""
        categories = {
            'dining': 0,
            'grocery': 0,
            'gas': 0,
            'shopping': 0,
            'utilities': 0,
            'entertainment': 0,
            'other': 0
        }
        
        for tx in transactions:
            if tx['amount'] < 0:  # Expense
                amount = abs(tx['amount'])
                desc = tx['description'].upper()
                
                if any(word in desc for word in ['RESTAURANT', 'CHIPOTLE', 'STARBUCKS', 'CAFE']):
                    categories['dining'] += amount
                elif any(word in desc for word in ['SAFEWAY', 'WHOLE FOODS', 'GROCERY', 'MARKET']):
                    categories['grocery'] += amount
                elif any(word in desc for word in ['SHELL', 'CHEVRON', 'GAS', 'FUEL']):
                    categories['gas'] += amount
                elif any(word in desc for word in ['AMAZON', 'TARGET', 'WALMART']):
                    categories['shopping'] += amount
                elif any(word in desc for word in ['ELECTRIC', 'GAS COMPANY', 'WATER', 'PHONE']):
                    categories['utilities'] += amount
                else:
                    categories['other'] += amount
        
        return categories
    
    def calculate_risk_score(self, features: FinancialFeatures) -> int:
        """Calculate overall risk score (300-850 scale)"""
        scores = {}
        
        # Income stability score
        scores['income_stability'] = min(850, features.income_stability * 850)
        
        # Cash flow score
        if features.monthly_net_inflow > 0:
            cash_flow_score = min(850, (features.monthly_net_inflow / 2000) * 400 + 450)
        else:
            cash_flow_score = 300
        scores['cash_flow'] = cash_flow_score
        
        # Balance management score
        if features.avg_balance > 1000:
            balance_score = 750
        elif features.avg_balance > 500:
            balance_score = 650
        elif features.avg_balance > 100:
            balance_score = 550
        else:
            balance_score = 400
        
        # Penalize NSF events
        balance_score -= (features.nsf_events * 50)
        scores['balance_management'] = max(300, balance_score)
        
        # Payment consistency score
        scores['payment_consistency'] = features.payment_consistency * 850
        
        # Expense ratio score (lower is better)
        if features.expense_ratio < 0.3:
            expense_score = 800
        elif features.expense_ratio < 0.5:
            expense_score = 700
        elif features.expense_ratio < 0.8:
            expense_score = 600
        else:
            expense_score = 400
        scores['expense_ratio'] = expense_score
        
        # Weighted average
        total_score = sum(scores[key] * self.score_weights[key] for key in scores)
        return int(total_score)
    
    def determine_tier(self, score: int) -> str:
        """Determine credit tier based on score"""
        for tier, range_data in self.tiers.items():
            if range_data['min_score'] <= score <= range_data['max_score']:
                return tier
        return 'Bronze'
    
    def assess_eligibility(self, features: FinancialFeatures, score: int, tier: str) -> Dict:
        """Determine product eligibility and limits"""
        eligibility = {}
        
        # Credit Card eligibility
        if tier == 'Gold':
            eligibility['credit_card'] = {
                'eligible': True,
                'limit_range': [4000, 8000],
                'apr_range': [19.99, 22.99],
                'confidence': 0.95
            }
        elif tier == 'Silver':
            eligibility['credit_card'] = {
                'eligible': True,
                'limit_range': [1500, 4000],
                'apr_range': [22.99, 26.99],
                'confidence': 0.85
            }
        else:
            eligibility['credit_card'] = {
                'eligible': True,
                'limit_range': [500, 1500],
                'apr_range': [26.99, 29.99],
                'confidence': 0.70
            }
        
        # Overdraft Line eligibility
        if features.nsf_events == 0 and features.avg_balance > 200:
            if tier == 'Gold':
                eligibility['overdraft_line'] = {
                    'eligible': True,
                    'limit_range': [300, 700],
                    'apr_range': [17.99, 20.99],
                    'confidence': 0.90
                }
            else:
                eligibility['overdraft_line'] = {
                    'eligible': True,
                    'limit_range': [100, 300],
                    'apr_range': [20.99, 24.99],
                    'confidence': 0.75
                }
        else:
            eligibility['overdraft_line'] = {
                'eligible': False,
                'reason': 'Insufficient balance history or NSF events',
                'confidence': 0.60
            }
        
        # Buy Now Pay Later eligibility
        if features.monthly_net_inflow > 1000:
            eligibility['bnpl'] = {
                'eligible': True,
                'limit_range': [250, 1000],
                'confidence': 0.85
            }
        else:
            eligibility['bnpl'] = {
                'eligible': False,
                'reason': 'Insufficient income',
                'confidence': 0.60
            }
        
        return eligibility
    
    def analyze_risk(self, user_id: str, months: int = 6) -> CreditAssessment:
        """Perform complete risk analysis for a user"""
        # Get user data
        transactions, balance_data = self.get_user_data(user_id, months)
        
        # Extract features
        features = self.extract_features(transactions, balance_data)
        
        # Calculate score
        score = self.calculate_risk_score(features)
        
        # Determine tier
        tier = self.determine_tier(score)
        
        # Assess eligibility
        eligibility = self.assess_eligibility(features, score, tier)
        
        # Risk factors analysis
        risk_factors = {
            'income_stability': features.income_stability,
            'balance_volatility': 1 - (features.min_balance / max(features.avg_balance, 1)),
            'expense_ratio': features.expense_ratio,
            'nsf_frequency': features.nsf_events / max(months, 1),
            'payment_reliability': features.payment_consistency
        }
        
        # Calculate overall confidence
        confidence = min(0.95, sum([
            features.income_stability * 0.3,
            (1 - risk_factors['balance_volatility']) * 0.25,
            (1 - min(1, features.expense_ratio)) * 0.25,
            features.payment_consistency * 0.2
        ]))
        
        return CreditAssessment(
            user_id=user_id,
            score=score,
            tier=tier,
            risk_factors=risk_factors,
            eligibility=eligibility,
            confidence=confidence
        )

    def make_approval_decision(self, assessment: CreditAssessment, spending_data: Dict) -> Dict:
        """Make final approval/rejection decision with reasoning"""
        
        # Rule-based decision logic
        approval_score = assessment.score
        risk_factors = assessment.risk_factors
        
        # Decision thresholds
        if approval_score >= 680 and risk_factors.get('nsf_frequency', 0) < 2:
            decision = 'APPROVED'
            risk_level = 'Low Risk'
        elif approval_score >= 620 and risk_factors.get('expense_ratio', 1) < 0.8:
            decision = 'APPROVED'
            risk_level = 'Moderate Risk'
        elif approval_score >= 580:
            decision = 'CONDITIONAL_APPROVAL'
            risk_level = 'Higher Risk'
        else:
            decision = 'REJECTED'
            risk_level = 'High Risk'
        
        # Generate detailed reasoning
        reasoning = self._generate_reasoning(assessment, spending_data, decision, risk_level)
        
        # Risk factors analysis for frontend display
        risk_factors_display = []
        
        if risk_factors.get('income_stability', 0) > 0.7:
            risk_factors_display.append({
                'factor': 'Income Stability', 
                'impact': 'Positive',
                'description': 'Consistent income pattern'
            })
        elif risk_factors.get('income_stability', 0) < 0.4:
            risk_factors_display.append({
                'factor': 'Income Stability', 
                'impact': 'High',
                'description': 'Irregular income pattern'
            })
        else:
            risk_factors_display.append({
                'factor': 'Income Stability', 
                'impact': 'Moderate',
                'description': 'Moderate income consistency'
            })
            
        if risk_factors.get('expense_ratio', 1) < 0.5:
            risk_factors_display.append({
                'factor': 'Spending Control', 
                'impact': 'Positive',
                'description': 'Good expense management'
            })
        elif risk_factors.get('expense_ratio', 1) > 0.8:
            risk_factors_display.append({
                'factor': 'Spending Control', 
                'impact': 'High',
                'description': 'High expense ratio'
            })
        else:
            risk_factors_display.append({
                'factor': 'Spending Control', 
                'impact': 'Moderate',
                'description': 'Moderate spending patterns'
            })
            
        if risk_factors.get('payment_reliability', 0) > 0.8:
            risk_factors_display.append({
                'factor': 'Payment History', 
                'impact': 'Positive',
                'description': 'Excellent payment consistency'
            })
        elif risk_factors.get('payment_reliability', 0) < 0.6:
            risk_factors_display.append({
                'factor': 'Payment History', 
                'impact': 'High',
                'description': 'Inconsistent payment patterns'
            })
        else:
            risk_factors_display.append({
                'factor': 'Payment History', 
                'impact': 'Moderate',
                'description': 'Adequate payment history'
            })
        
        return {
            'decision': decision,
            'risk_level': risk_level,
            'risk_score': assessment.score,
            'reasoning': reasoning,
            'risk_factors': risk_factors_display,
            'confidence': assessment.confidence,
            'tier': assessment.tier,
            'eligibility': assessment.eligibility,
            'generated_at': datetime.now().isoformat(),
            'agent': 'risk-agent'
        }

    def _generate_reasoning(self, assessment: CreditAssessment, spending_data: Dict, decision: str, risk_level: str) -> str:
        """Generate detailed reasoning for the approval decision"""
        
        if self.model:
            try:
                # Use Gemini for sophisticated reasoning
                prompt = f"""
                As a senior credit risk analyst, provide a professional assessment explanation for this credit application decision:
                
                APPLICANT PROFILE:
                - Credit Score: {assessment.score}
                - Risk Tier: {assessment.tier}
                - Confidence Level: {assessment.confidence:.1%}
                
                FINANCIAL METRICS:
                - Income Stability: {assessment.risk_factors.get('income_stability', 0):.1%}
                - Expense Ratio: {assessment.risk_factors.get('expense_ratio', 0):.1%}
                - Payment Consistency: {assessment.risk_factors.get('payment_reliability', 0):.1%}
                - NSF Frequency: {assessment.risk_factors.get('nsf_frequency', 0)} per month
                - Balance Volatility: {assessment.risk_factors.get('balance_volatility', 0):.1%}
                
                SPENDING ANALYSIS:
                - Total Monthly Spending: ${spending_data.get('total_spending', 0):,.0f}
                - Transaction Count: {spending_data.get('transaction_count', 0)}
                - Primary Categories: {', '.join(list(spending_data.get('spending_categories', {}).keys())[:3])}
                
                DECISION: {decision}
                RISK LEVEL: {risk_level}
                
                Provide a 2-3 sentence professional explanation that covers:
                1. The primary factors that led to this decision
                2. Key strengths or concerns identified
                3. Any specific conditions or recommendations
                
                Keep it clear, professional, and customer-friendly. Focus on the most important factors.
                """
                
                response = self.model.generate_content(prompt)
                return response.text.strip()
                
            except Exception as e:
                logger.warning(f"⚠️ Gemini reasoning failed: {e}")
                # Fall back to rule-based reasoning
                pass
        
        # Rule-based reasoning fallback
        if decision == 'APPROVED':
            if assessment.score >= 700:
                return f"Application approved based on excellent credit profile (Score: {assessment.score}). Strong financial stability with consistent income patterns and responsible spending behavior demonstrate low credit risk."
            else:
                return f"Application approved with moderate risk assessment (Score: {assessment.score}). Good financial management and payment history support creditworthiness despite some minor risk factors."
        elif decision == 'CONDITIONAL_APPROVAL':
            return f"Conditional approval granted (Score: {assessment.score}). While some risk factors require monitoring, overall financial profile supports limited credit extension with appropriate terms and conditions."
        else:
            return f"Application requires additional review (Score: {assessment.score}). Current financial profile presents elevated risk factors that need further assessment before credit extension can be considered."

# Initialize Flask app and risk analyzer
app = Flask(__name__)
analyzer = RiskAnalyzer()

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'risk-agent'}), 200

@app.route('/assess', methods=['POST'])
def assess_risk():
    """Assess credit risk for a user"""
    data = request.get_json()
    user_id = data.get('user_id', 'testuser')
    months = data.get('months', 6)
    
    try:
        assessment = analyzer.analyze_risk(user_id, months)
        
        return jsonify({
            'user_id': assessment.user_id,
            'score': assessment.score,
            'tier': assessment.tier,
            'risk_factors': assessment.risk_factors,
            'eligibility': assessment.eligibility,
            'confidence': assessment.confidence,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error in risk assessment: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/approve', methods=['POST'])
def approve_application():
    """Make approval/rejection decision with reasoning"""
    data = request.get_json()
    user_id = data.get('user_id', 'testuser')
    spending_data = data.get('spending_data', {})
    months = data.get('months', 6)
    
    try:
        # First get risk assessment
        assessment = analyzer.analyze_risk(user_id, months)
        
        # Then make approval decision
        decision_result = analyzer.make_approval_decision(assessment, spending_data)
        
        logger.info(f"🎯 Risk Agent Decision for {user_id}: {decision_result['decision']} ({decision_result['risk_level']})")
        
        return jsonify(decision_result)
        
    except Exception as e:
        logger.error(f"Error in approval decision: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8081))
    app.run(host='0.0.0.0', port=port, debug=False)
