#!/usr/bin/env python3
"""
Realistic transaction data generator for Bank of Anthos AI Agents
Creates believable spending patterns for different user profiles
"""

import random
import json
from datetime import datetime, timedelta
from typing import List, Dict, Any
from dataclasses import dataclass

@dataclass
class UserProfile:
    """User profile with spending characteristics"""
    name: str
    income_level: str  # low, medium, high
    age_group: str     # young, middle, senior
    lifestyle: str     # conservative, moderate, active
    location: str      # urban, suburban, rural

class RealisticDataGenerator:
    """Generates realistic transaction data based on user profiles"""
    
    def __init__(self):
        self.user_profiles = {
            'testuser': UserProfile(
                name='Alex Johnson',
                income_level='high',
                age_group='middle',
                lifestyle='active',
                location='urban'
            ),
            'user2': UserProfile(
                name='Sarah Chen',
                income_level='medium',
                age_group='young',
                lifestyle='moderate',
                location='suburban'
            ),
            'user3': UserProfile(
                name='Robert Martinez',
                income_level='high',
                age_group='senior',
                lifestyle='conservative',
                location='suburban'
            )
        }
        
        # Merchant categories and realistic spending patterns
        self.merchant_patterns = {
            'salary': {
                'high': {'base': 4200, 'variance': 200},
                'medium': {'base': 3200, 'variance': 150},
                'low': {'base': 2400, 'variance': 100}
            },
            'rent_mortgage': {
                'urban': {'high': 2200, 'medium': 1800, 'low': 1400},
                'suburban': {'high': 1800, 'medium': 1400, 'low': 1100},
                'rural': {'high': 1200, 'medium': 900, 'low': 700}
            },
            'groceries': {
                'base_weekly': {'young': 85, 'middle': 120, 'senior': 90},
                'merchants': ['SAFEWAY', 'WHOLE FOODS', 'TRADER JOES', 'COSTCO', 'WALMART']
            },
            'dining': {
                'frequency': {'conservative': 0.3, 'moderate': 0.6, 'active': 0.9},
                'avg_spend': {'young': 25, 'middle': 35, 'senior': 30},
                'merchants': ['CHIPOTLE', 'STARBUCKS', 'OLIVE GARDEN', 'MCDONALDS', 'SUBWAY', 'LOCAL RESTAURANT', 'PIZZA HUT']
            },
            'gas': {
                'weekly': {'urban': 35, 'suburban': 55, 'rural': 70},
                'merchants': ['SHELL', 'CHEVRON', 'EXXON', 'BP', 'ARCO']
            },
            'utilities': {
                'electric': {'high': 140, 'medium': 110, 'low': 85},
                'gas': {'high': 90, 'medium': 70, 'low': 50},
                'water': {'high': 60, 'medium': 45, 'low': 35},
                'internet': {'high': 80, 'medium': 60, 'low': 45},
                'phone': {'high': 95, 'medium': 75, 'low': 55}
            },
            'shopping': {
                'frequency': {'conservative': 0.2, 'moderate': 0.5, 'active': 0.8},
                'avg_spend': {'young': 75, 'middle': 120, 'senior': 60},
                'merchants': ['AMAZON', 'TARGET', 'WALMART', 'MACY\'S', 'BEST BUY', 'HOME DEPOT']
            },
            'entertainment': {
                'frequency': {'conservative': 0.1, 'moderate': 0.3, 'active': 0.6},
                'avg_spend': {'young': 45, 'middle': 60, 'senior': 35},
                'merchants': ['NETFLIX', 'SPOTIFY', 'MOVIE THEATER', 'GYM MEMBERSHIP', 'UBER', 'LYFT']
            },
            'healthcare': {
                'frequency': {'young': 0.2, 'middle': 0.4, 'senior': 0.8},
                'avg_spend': {'young': 125, 'middle': 200, 'senior': 350},
                'merchants': ['PHARMACY', 'DOCTOR OFFICE', 'DENTAL CLINIC', 'VISION CENTER']
            }
        }
    
    def generate_transactions(self, user_id: str, months: int = 6) -> List[Dict[str, Any]]:
        """Generate realistic transactions for a user profile"""
        profile = self.user_profiles.get(user_id, self.user_profiles['testuser'])
        transactions = []
        tx_id = 10000
        
        end_date = datetime.now()
        start_date = end_date - timedelta(days=months * 30)
        
        current_date = start_date
        
        while current_date <= end_date:
            # Generate daily transactions
            daily_transactions = self._generate_daily_transactions(profile, current_date, tx_id)
            transactions.extend(daily_transactions)
            tx_id += len(daily_transactions)
            current_date += timedelta(days=1)
        
        # Add regular monthly transactions (salary, rent, utilities)
        monthly_transactions = self._generate_monthly_transactions(profile, start_date, end_date, tx_id)
        transactions.extend(monthly_transactions)
        
        # Sort by date (most recent first for API compatibility)
        transactions.sort(key=lambda x: x['date'], reverse=True)
        
        return transactions
    
    def _generate_daily_transactions(self, profile: UserProfile, date: datetime, start_id: int) -> List[Dict[str, Any]]:
        """Generate transactions for a single day"""
        transactions = []
        tx_id = start_id
        
        # Groceries (2-3 times per week)
        if random.random() < 0.35:  # ~2.5 times per week
            amount = self._get_grocery_amount(profile)
            merchant = random.choice(self.merchant_patterns['groceries']['merchants'])
            transactions.append(self._create_transaction(
                tx_id, date, -amount, f"{merchant} GROCERY", profile
            ))
            tx_id += 1
        
        # Dining out
        dining_freq = self.merchant_patterns['dining']['frequency'][profile.lifestyle]
        if random.random() < dining_freq:
            amount = self._get_dining_amount(profile)
            merchant = random.choice(self.merchant_patterns['dining']['merchants'])
            transactions.append(self._create_transaction(
                tx_id, date, -amount, merchant, profile
            ))
            tx_id += 1
        
        # Gas (1-2 times per week)
        if random.random() < 0.2:  # ~1.4 times per week
            amount = self._get_gas_amount(profile)
            merchant = random.choice(self.merchant_patterns['gas']['merchants'])
            transactions.append(self._create_transaction(
                tx_id, date, -amount, f"{merchant} GAS STATION", profile
            ))
            tx_id += 1
        
        # Shopping
        shopping_freq = self.merchant_patterns['shopping']['frequency'][profile.lifestyle]
        if random.random() < shopping_freq / 7:  # Daily probability
            amount = self._get_shopping_amount(profile)
            merchant = random.choice(self.merchant_patterns['shopping']['merchants'])
            transactions.append(self._create_transaction(
                tx_id, date, -amount, merchant, profile
            ))
            tx_id += 1
        
        # Entertainment
        entertainment_freq = self.merchant_patterns['entertainment']['frequency'][profile.lifestyle]
        if random.random() < entertainment_freq / 7:  # Daily probability
            amount = self._get_entertainment_amount(profile)
            merchant = random.choice(self.merchant_patterns['entertainment']['merchants'])
            transactions.append(self._create_transaction(
                tx_id, date, -amount, merchant, profile
            ))
            tx_id += 1
        
        # Healthcare (random)
        healthcare_freq = self.merchant_patterns['healthcare']['frequency'][profile.age_group]
        if random.random() < healthcare_freq / 30:  # Monthly to daily
            amount = self._get_healthcare_amount(profile)
            merchant = random.choice(self.merchant_patterns['healthcare']['merchants'])
            transactions.append(self._create_transaction(
                tx_id, date, -amount, merchant, profile
            ))
            tx_id += 1
        
        return transactions
    
    def _generate_monthly_transactions(self, profile: UserProfile, start_date: datetime, end_date: datetime, start_id: int) -> List[Dict[str, Any]]:
        """Generate regular monthly transactions"""
        transactions = []
        tx_id = start_id
        
        current_date = start_date.replace(day=1)
        
        while current_date <= end_date:
            # Salary (bi-weekly)
            salary_dates = [
                current_date.replace(day=1),
                current_date.replace(day=15) if current_date.month == current_date.replace(day=15).month else None
            ]
            
            for salary_date in salary_dates:
                if salary_date and salary_date <= end_date:
                    amount = self._get_salary_amount(profile)
                    transactions.append(self._create_transaction(
                        tx_id, salary_date, amount, "PAYROLL DEPOSIT - TECH CORP", profile
                    ))
                    tx_id += 1
            
            # Rent/Mortgage (1st of month)
            rent_amount = self._get_rent_amount(profile)
            transactions.append(self._create_transaction(
                tx_id, current_date.replace(day=1), -rent_amount, "RENT PAYMENT - PROPERTY MGMT", profile
            ))
            tx_id += 1
            
            # Utilities (5th of month)
            utilities_date = current_date.replace(day=5)
            if utilities_date <= end_date:
                utilities = self._get_utilities_amounts(profile)
                for util_name, amount in utilities.items():
                    transactions.append(self._create_transaction(
                        tx_id, utilities_date, -amount, f"{util_name.upper()} COMPANY", profile
                    ))
                    tx_id += 1
            
            # Investment/Savings (10th of month)
            if profile.income_level in ['medium', 'high']:
                savings_date = current_date.replace(day=10)
                if savings_date <= end_date:
                    savings_amount = self._get_savings_amount(profile)
                    transactions.append(self._create_transaction(
                        tx_id, savings_date, -savings_amount, "VANGUARD TRANSFER", profile
                    ))
                    tx_id += 1
            
            # Move to next month
            if current_date.month == 12:
                current_date = current_date.replace(year=current_date.year + 1, month=1)
            else:
                current_date = current_date.replace(month=current_date.month + 1)
        
        return transactions
    
    def _create_transaction(self, tx_id: int, date: datetime, amount: float, description: str, profile: UserProfile) -> Dict[str, Any]:
        """Create a transaction record"""
        account_id = '1011226800'  # Demo account ID from Bank of Anthos
        
        return {
            'id': f'tx_{tx_id}',
            'account_id': account_id,
            'amount': round(amount, 2),
            'date': date.isoformat(),
            'description': description,
            'to_account': 'external' if amount < 0 else account_id,
            'from_account': account_id if amount < 0 else 'external',
            'category': self._categorize_transaction(description),
            'merchant': description.split()[0] if amount < 0 else 'EMPLOYER'
        }
    
    def _categorize_transaction(self, description: str) -> str:
        """Categorize transaction by description"""
        desc_upper = description.upper()
        
        if any(word in desc_upper for word in ['PAYROLL', 'SALARY', 'DEPOSIT']):
            return 'income'
        elif any(word in desc_upper for word in ['RENT', 'MORTGAGE']):
            return 'housing'
        elif any(word in desc_upper for word in ['SAFEWAY', 'GROCERY', 'WHOLE FOODS', 'TRADER']):
            return 'grocery'
        elif any(word in desc_upper for word in ['RESTAURANT', 'CHIPOTLE', 'STARBUCKS', 'DINING']):
            return 'dining'
        elif any(word in desc_upper for word in ['SHELL', 'CHEVRON', 'GAS', 'EXXON']):
            return 'gas'
        elif any(word in desc_upper for word in ['ELECTRIC', 'WATER', 'INTERNET', 'PHONE']):
            return 'utilities'
        elif any(word in desc_upper for word in ['AMAZON', 'TARGET', 'WALMART', 'SHOPPING']):
            return 'shopping'
        elif any(word in desc_upper for word in ['NETFLIX', 'SPOTIFY', 'MOVIE', 'GYM']):
            return 'entertainment'
        elif any(word in desc_upper for word in ['VANGUARD', 'SAVINGS', 'INVESTMENT']):
            return 'savings'
        elif any(word in desc_upper for word in ['PHARMACY', 'DOCTOR', 'DENTAL']):
            return 'healthcare'
        else:
            return 'other'
    
    def _get_salary_amount(self, profile: UserProfile) -> float:
        """Get salary amount based on profile"""
        base_amount = self.merchant_patterns['salary'][profile.income_level]['base']
        variance = self.merchant_patterns['salary'][profile.income_level]['variance']
        return base_amount + random.uniform(-variance, variance)
    
    def _get_rent_amount(self, profile: UserProfile) -> float:
        """Get rent amount based on profile"""
        amount = self.merchant_patterns['rent_mortgage'][profile.location][profile.income_level]
        return amount + random.uniform(-100, 100)
    
    def _get_grocery_amount(self, profile: UserProfile) -> float:
        """Get grocery spending amount"""
        base = self.merchant_patterns['groceries']['base_weekly'][profile.age_group]
        return base + random.uniform(-15, 25)
    
    def _get_dining_amount(self, profile: UserProfile) -> float:
        """Get dining spending amount"""
        base = self.merchant_patterns['dining']['avg_spend'][profile.age_group]
        return base + random.uniform(-10, 20)
    
    def _get_gas_amount(self, profile: UserProfile) -> float:
        """Get gas spending amount"""
        base = self.merchant_patterns['gas']['weekly'][profile.location]
        return base + random.uniform(-10, 15)
    
    def _get_shopping_amount(self, profile: UserProfile) -> float:
        """Get shopping spending amount"""
        base = self.merchant_patterns['shopping']['avg_spend'][profile.age_group]
        return base + random.uniform(-25, 50)
    
    def _get_entertainment_amount(self, profile: UserProfile) -> float:
        """Get entertainment spending amount"""
        base = self.merchant_patterns['entertainment']['avg_spend'][profile.age_group]
        return base + random.uniform(-15, 30)
    
    def _get_healthcare_amount(self, profile: UserProfile) -> float:
        """Get healthcare spending amount"""
        base = self.merchant_patterns['healthcare']['avg_spend'][profile.age_group]
        return base + random.uniform(-50, 100)
    
    def _get_utilities_amounts(self, profile: UserProfile) -> Dict[str, float]:
        """Get monthly utilities amounts"""
        utilities = {}
        
        for util_type in ['electric', 'gas', 'water', 'internet', 'phone']:
            base = self.merchant_patterns['utilities'][util_type][profile.income_level]
            utilities[util_type] = base + random.uniform(-15, 15)
        
        return utilities
    
    def _get_savings_amount(self, profile: UserProfile) -> float:
        """Get monthly savings amount"""
        if profile.income_level == 'high':
            return 500 + random.uniform(-100, 200)
        elif profile.income_level == 'medium':
            return 300 + random.uniform(-75, 150)
        else:
            return 150 + random.uniform(-50, 100)
    
    def get_spending_summary(self, user_id: str) -> Dict[str, float]:
        """Get monthly spending summary by category"""
        profile = self.user_profiles.get(user_id, self.user_profiles['testuser'])
        
        # Calculate typical monthly spending
        summary = {
            'housing': self._get_rent_amount(profile),
            'grocery': self._get_grocery_amount(profile) * 4.3,  # Weekly to monthly
            'dining': self._get_dining_amount(profile) * self.merchant_patterns['dining']['frequency'][profile.lifestyle] * 30,
            'gas': self._get_gas_amount(profile) * 4.3,  # Weekly to monthly
            'utilities': sum(self._get_utilities_amounts(profile).values()),
            'shopping': self._get_shopping_amount(profile) * self.merchant_patterns['shopping']['frequency'][profile.lifestyle] * 7,
            'entertainment': self._get_entertainment_amount(profile) * self.merchant_patterns['entertainment']['frequency'][profile.lifestyle] * 7,
            'healthcare': self._get_healthcare_amount(profile) * self.merchant_patterns['healthcare']['frequency'][profile.age_group],
            'savings': self._get_savings_amount(profile) if profile.income_level in ['medium', 'high'] else 0
        }
        
        return {k: round(v, 2) for k, v in summary.items()}

# Global instance
data_generator = RealisticDataGenerator()

if __name__ == '__main__':
    # Test the data generator
    generator = RealisticDataGenerator()
    
    # Generate transactions for test user
    transactions = generator.generate_transactions('testuser', 6)
    
    print(f"Generated {len(transactions)} transactions")
    print("\nSample transactions:")
    for tx in transactions[:5]:
        print(f"  {tx['date'][:10]}: ${tx['amount']:>8.2f} - {tx['description']}")
    
    print(f"\nSpending summary:")
    summary = generator.get_spending_summary('testuser')
    for category, amount in summary.items():
        print(f"  {category}: ${amount:.2f}/month")
