#!/usr/bin/env python3
"""
Counterfactual/Challenger Pricing Agent
Stress-tests Terms Agent proposals with bank economics and risk scenarios
"""

import json
import logging
import math
import os
import random
from datetime import datetime
from typing import Dict, List, Tuple, Any
from flask import Flask, request, jsonify

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)

class ChallengerAgent:
    def __init__(self):
        # Bank policy constraints
        self.constraints = {
            'min_roe': 0.15,  # 15% ROE floor
            'max_loss_rate': 0.08,  # 8% loss rate ceiling
            'max_perk_budget_monthly': 50,  # $50/user/month perk budget
            'min_apr': 12.99,  # Policy APR range
            'max_apr': 29.99,
            'cof_base': 0.04,  # 4% cost of funds base
            'ops_cost': 15,  # $15/month operational cost per account
        }
        
        # Economic parameters
        self.params = {
            'interchange_rate': 0.018,  # 1.8% interchange on spend
            'perk_cost_multiplier': 0.035,  # 3.5% cost on eligible spend
            'lgd': 0.45,  # 45% Loss Given Default
            'capital_ratio': 0.08,  # 8% capital requirement
        }

    def analyze_proposal(self, terms_proposal: Dict, risk_data: Dict, spending_data: Dict) -> Dict:
        """
        Main analysis function that stress-tests a Terms Agent proposal
        """
        try:
            logger.info(f"🔍 Challenger Agent analyzing proposal: APR={terms_proposal.get('apr_rate')}%, Limit=${terms_proposal.get('credit_limit')}")
            
            # Extract key metrics
            base_scenario = self._build_base_scenario(terms_proposal, risk_data, spending_data)
            
            # Run stress tests
            stress_results = self._run_stress_tests(base_scenario)
            
            # Check constraints
            constraint_violations = self._check_constraints(base_scenario, stress_results)
            
            # Generate counter-offer if needed
            decision = self._make_decision(base_scenario, stress_results, constraint_violations, terms_proposal)
            
            return {
                'agent': 'challenger-agent',
                'analysis_timestamp': datetime.now().isoformat(),
                'original_proposal': terms_proposal,
                'base_economics': base_scenario,
                'stress_test_results': stress_results,
                'constraint_violations': constraint_violations,
                'decision': decision,
                'confidence': 95
            }
            
        except Exception as e:
            logger.error(f"❌ Error in challenger analysis: {e}")
            return {
                'agent': 'challenger-agent',
                'error': str(e),
                'decision': {'action': 'reject', 'reason': 'Analysis failed'}
            }

    def _build_base_scenario(self, terms: Dict, risk: Dict, spending: Dict) -> Dict:
        """Build base case economics scenario"""
        
        # Extract metrics
        credit_limit = terms.get('credit_limit', 15000)
        apr = terms.get('apr_rate', 18.99) / 100
        monthly_spend = spending.get('total_spending', 5000) / 12  # Annualize to monthly
        pd = self._extract_pd_from_risk(risk)
        
        # Assume 30% utilization and 50% revolving
        avg_balance = credit_limit * 0.3
        revolving_balance = avg_balance * 0.5
        
        # Calculate revenues
        interchange_revenue = monthly_spend * self.params['interchange_rate']
        interest_revenue = revolving_balance * (apr / 12)
        
        # Calculate costs
        perk_eligible_spend = monthly_spend * 0.6  # 60% eligible for perks
        perk_costs = perk_eligible_spend * self.params['perk_cost_multiplier']
        expected_loss = pd * self.params['lgd'] * avg_balance / 12
        funding_cost = avg_balance * (self.constraints['cof_base'] / 12)
        ops_cost = self.constraints['ops_cost']
        
        # Unit economics
        total_revenue = interchange_revenue + interest_revenue
        total_costs = perk_costs + expected_loss + funding_cost + ops_cost
        profit = total_revenue - total_costs
        
        # ROE calculation
        capital_requirement = credit_limit * self.params['capital_ratio']
        roe = (profit * 12) / capital_requirement if capital_requirement > 0 else 0
        
        # Loss rate
        loss_rate = (expected_loss * 12) / avg_balance if avg_balance > 0 else 0
        
        return {
            'monthly_spend': monthly_spend,
            'avg_balance': avg_balance,
            'revolving_balance': revolving_balance,
            'pd': pd,
            'revenues': {
                'interchange': interchange_revenue,
                'interest': interest_revenue,
                'total': total_revenue
            },
            'costs': {
                'perks': perk_costs,
                'expected_loss': expected_loss,
                'funding': funding_cost,
                'operations': ops_cost,
                'total': total_costs
            },
            'profit_monthly': profit,
            'profit_annual': profit * 12,
            'roe': roe,
            'loss_rate': loss_rate,
            'capital_requirement': capital_requirement
        }

    def _run_stress_tests(self, base: Dict) -> Dict:
        """Run stress test scenarios"""
        
        scenarios = {}
        
        # Scenario 1: Spend down 20%
        spend_stress = base.copy()
        spend_stress['monthly_spend'] *= 0.8
        spend_stress['revenues']['interchange'] *= 0.8
        spend_stress['costs']['perks'] *= 0.8
        spend_stress['profit_monthly'] = spend_stress['revenues']['interchange'] + spend_stress['revenues']['interest'] - sum(spend_stress['costs'].values())
        spend_stress['roe'] = (spend_stress['profit_monthly'] * 12) / base['capital_requirement']
        scenarios['spend_down_20pct'] = spend_stress
        
        # Scenario 2: Default probability up 1.5x
        default_stress = base.copy()
        default_stress['pd'] *= 1.5
        default_stress['costs']['expected_loss'] *= 1.5
        default_stress['costs']['total'] = sum([v for k, v in default_stress['costs'].items() if k != 'total'])
        default_stress['profit_monthly'] = default_stress['revenues']['total'] - default_stress['costs']['total']
        default_stress['roe'] = (default_stress['profit_monthly'] * 12) / base['capital_requirement']
        default_stress['loss_rate'] = (default_stress['costs']['expected_loss'] * 12) / base['avg_balance']
        scenarios['default_up_1_5x'] = default_stress
        
        # Scenario 3: Cost of funds up 100bps
        cof_stress = base.copy()
        cof_stress['costs']['funding'] = base['avg_balance'] * ((self.constraints['cof_base'] + 0.01) / 12)
        cof_stress['costs']['total'] = sum([v for k, v in cof_stress['costs'].items() if k != 'total'])
        cof_stress['profit_monthly'] = cof_stress['revenues']['total'] - cof_stress['costs']['total']
        cof_stress['roe'] = (cof_stress['profit_monthly'] * 12) / base['capital_requirement']
        scenarios['cof_up_100bps'] = cof_stress
        
        # Scenario 4: Perk usage maxed (assume 90% vs 60% eligible spend)
        perk_stress = base.copy()
        perk_stress['costs']['perks'] = base['monthly_spend'] * 0.9 * self.params['perk_cost_multiplier']
        perk_stress['costs']['total'] = sum([v for k, v in perk_stress['costs'].items() if k != 'total'])
        perk_stress['profit_monthly'] = perk_stress['revenues']['total'] - perk_stress['costs']['total']
        perk_stress['roe'] = (perk_stress['profit_monthly'] * 12) / base['capital_requirement']
        scenarios['perk_usage_maxed'] = perk_stress
        
        return scenarios

    def _check_constraints(self, base: Dict, stress: Dict) -> List[Dict]:
        """Check constraint violations"""
        violations = []
        
        # Check ROE constraint
        if base['roe'] < self.constraints['min_roe']:
            violations.append({
                'constraint': 'min_roe',
                'required': self.constraints['min_roe'],
                'actual': base['roe'],
                'severity': 'high'
            })
        
        # Check loss rate constraint
        if base['loss_rate'] > self.constraints['max_loss_rate']:
            violations.append({
                'constraint': 'max_loss_rate',
                'required': self.constraints['max_loss_rate'],
                'actual': base['loss_rate'],
                'severity': 'high'
            })
        
        # Check perk budget
        if base['costs']['perks'] > self.constraints['max_perk_budget_monthly']:
            violations.append({
                'constraint': 'max_perk_budget',
                'required': self.constraints['max_perk_budget_monthly'],
                'actual': base['costs']['perks'],
                'severity': 'medium'
            })
        
        # Check stress test violations
        for scenario_name, scenario in stress.items():
            if scenario['roe'] < self.constraints['min_roe'] * 0.8:  # 80% of min ROE in stress
                violations.append({
                    'constraint': f'stress_roe_{scenario_name}',
                    'required': self.constraints['min_roe'] * 0.8,
                    'actual': scenario['roe'],
                    'severity': 'medium'
                })
        
        return violations

    def _make_decision(self, base: Dict, stress: Dict, violations: List, original_terms: Dict) -> Dict:
        """Make final decision: approve, counter-offer, or reject"""
        
        high_severity_violations = [v for v in violations if v.get('severity') == 'high']
        
        if len(high_severity_violations) == 0 and len(violations) <= 1:
            # Approve as-is
            return {
                'action': 'approve_as_is',
                'reason': 'Proposal meets all key constraints and stress tests',
                'profit_margin': base['profit_monthly'],
                'roe': base['roe']
            }
        
        elif len(high_severity_violations) <= 2:
            # Counter-offer
            counter_terms = self._generate_counter_offer(original_terms, violations, base)
            return {
                'action': 'counter_offer',
                'reason': f'Adjustments needed due to {len(violations)} constraint violations',
                'violations': violations,
                'counter_proposal': counter_terms,
                'expected_improvement': self._estimate_improvement(counter_terms, original_terms)
            }
        
        else:
            # Reject
            return {
                'action': 'reject',
                'reason': f'Too many constraint violations ({len(high_severity_violations)} high severity)',
                'violations': violations
            }

    def _generate_counter_offer(self, original: Dict, violations: List, base: Dict) -> Dict:
        """Generate counter-offer with adjusted terms"""
        
        counter = original.copy()
        adjustments = []
        
        # Adjust APR if ROE is too low
        roe_violations = [v for v in violations if 'roe' in v['constraint']]
        if roe_violations:
            apr_increase = min(200, max(50, len(roe_violations) * 100))  # 50-200 bps increase
            counter['apr_rate'] = min(self.constraints['max_apr'], original['apr_rate'] + (apr_increase / 100))
            adjustments.append(f"APR increased by {apr_increase} bps to improve ROE")
        
        # Reduce credit limit if loss rate is too high
        loss_violations = [v for v in violations if 'loss' in v['constraint']]
        if loss_violations:
            limit_reduction = min(5000, max(1000, int(original['credit_limit'] * 0.2)))
            counter['credit_limit'] = max(5000, original['credit_limit'] - limit_reduction)
            adjustments.append(f"Credit limit reduced by ${limit_reduction} to manage loss exposure")
        
        # Reduce perk benefits if perk costs are too high
        perk_violations = [v for v in violations if 'perk' in v['constraint']]
        if perk_violations:
            # Reduce cashback rates
            if 'promotional_offers' in counter:
                counter['promotional_offers'] = counter['promotional_offers'][:1]  # Limit promos
            adjustments.append("Reduced promotional benefits to control perk costs")
        
        counter['adjustments'] = adjustments
        return counter

    def _estimate_improvement(self, counter: Dict, original: Dict) -> Dict:
        """Estimate improvement from counter-offer"""
        
        apr_improvement = (counter.get('apr_rate', 0) - original.get('apr_rate', 0)) * 100
        limit_change = counter.get('credit_limit', 0) - original.get('credit_limit', 0)
        
        return {
            'apr_increase_bps': apr_improvement,
            'credit_limit_change': limit_change,
            'estimated_roe_improvement': apr_improvement * 0.002,  # Rough estimate
            'estimated_profit_improvement_monthly': apr_improvement * 5  # Rough estimate
        }

    def _extract_pd_from_risk(self, risk_data: Dict) -> float:
        """Extract probability of default from risk assessment"""
        
        risk_score = risk_data.get('risk_score', 50)
        
        # Convert risk score to PD (higher score = higher risk)
        if risk_score <= 20:
            return 0.02  # 2% PD for low risk
        elif risk_score <= 40:
            return 0.04  # 4% PD for moderate-low risk
        elif risk_score <= 60:
            return 0.07  # 7% PD for moderate risk
        elif risk_score <= 80:
            return 0.12  # 12% PD for high risk
        else:
            return 0.20  # 20% PD for very high risk

# Flask routes
@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "agent": "challenger-agent"})

@app.route('/challenge-terms', methods=['POST'])
def challenge_terms():
    """
    Main endpoint for challenging Terms Agent proposals
    Expects: {
        "terms_proposal": {...},
        "risk_assessment": {...},
        "spending_data": {...}
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'terms_proposal' not in data:
            return jsonify({"error": "Missing terms_proposal in request"}), 400
        
        challenger = ChallengerAgent()
        result = challenger.analyze_proposal(
            data['terms_proposal'],
            data.get('risk_assessment', {}),
            data.get('spending_data', {})
        )
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"❌ Error in challenge_terms: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8088))
    logger.info(f"🚀 Starting Challenger Agent on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
