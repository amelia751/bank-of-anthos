#!/usr/bin/env python3
"""
Comprehensive merchant mapping for realistic Bank of Anthos transaction data.
This file defines merchant accounts with detailed categorization for AI analysis.
"""

# Merchant account mapping with detailed spending categories
MERCHANT_ACCOUNTS = {
    # Coffee & Cafes (High Frequency)
    '5001000001': {
        'name': 'Starbucks',
        'category': 'Coffee & Cafes',
        'type': 'retail',
        'frequency': 'high',
        'avg_amount_range': (4.50, 8.50),
        'merchant_code': '5814',  # Fast Food Restaurants
        'description': 'Coffee chain - multiple locations'
    },
    '5001000002': {
        'name': 'Blue Bottle Coffee',
        'category': 'Coffee & Cafes',
        'type': 'retail',
        'frequency': 'medium',
        'avg_amount_range': (5.00, 12.00),
        'merchant_code': '5814',
        'description': 'Specialty coffee roaster'
    },
    '5001000003': {
        'name': 'Peet\'s Coffee',
        'category': 'Coffee & Cafes',
        'type': 'retail',
        'frequency': 'medium',
        'avg_amount_range': (4.00, 9.00),
        'merchant_code': '5814',
        'description': 'Coffee chain - premium blends'
    },
    
    # Groceries (Medium-High Frequency) - REALISTIC AMOUNTS
    '5002000001': {
        'name': 'Whole Foods Market',
        'category': 'Groceries',
        'type': 'essential',
        'frequency': 'medium',
        'avg_amount_range': (25.00, 65.00),  # Reduced from 45-150
        'merchant_code': '5411',  # Grocery Stores
        'description': 'Organic and natural foods'
    },
    '5002000002': {
        'name': 'Safeway',
        'category': 'Groceries',
        'type': 'essential',
        'frequency': 'medium',
        'avg_amount_range': (20.00, 55.00),  # Reduced from 35-120
        'merchant_code': '5411',
        'description': 'Traditional grocery chain'
    },
    '5002000003': {
        'name': 'Trader Joe\'s',
        'category': 'Groceries',
        'type': 'essential',
        'frequency': 'medium',
        'avg_amount_range': (15.00, 45.00),  # Reduced from 25-80
        'merchant_code': '5411',
        'description': 'Specialty grocery with unique products'
    },
    '5002000004': {
        'name': 'Costco Wholesale',
        'category': 'Groceries',
        'type': 'essential',
        'frequency': 'low',
        'avg_amount_range': (60.00, 120.00),  # Reduced from 80-300
        'merchant_code': '5411',
        'description': 'Warehouse club - bulk purchases'
    },
    
    # Restaurants & Dining (Variable Frequency) - REALISTIC AMOUNTS
    '5003000001': {
        'name': 'The French Laundry',
        'category': 'Fine Dining',
        'type': 'discretionary',
        'frequency': 'low',
        'avg_amount_range': (80.00, 150.00),  # Reduced from 250-400
        'merchant_code': '5812',  # Eating Places and Restaurants
        'description': 'Upscale dining (special occasions only)'
    },
    '5003000002': {
        'name': 'Chipotle Mexican Grill',
        'category': 'Fast Casual',
        'type': 'retail',
        'frequency': 'medium',  # Reduced frequency
        'avg_amount_range': (8.00, 15.00),  # Keep reasonable
        'merchant_code': '5814',
        'description': 'Fast-casual Mexican food'
    },
    '5003000003': {
        'name': 'Tony\'s Little Star Pizza',
        'category': 'Casual Dining',
        'type': 'discretionary',
        'frequency': 'low',  # Reduced frequency
        'avg_amount_range': (18.00, 35.00),  # Reduced from 20-45
        'merchant_code': '5812',
        'description': 'Local pizza restaurant'
    },
    '5003000004': {
        'name': 'In-N-Out Burger',
        'category': 'Fast Food',
        'type': 'retail',
        'frequency': 'medium',
        'avg_amount_range': (8.00, 16.00),  # Reduced from 8-18
        'merchant_code': '5814',
        'description': 'West Coast burger chain'
    },
    '5003000005': {
        'name': 'Sushi Nakazawa',
        'category': 'Fine Dining',
        'type': 'discretionary',
        'frequency': 'low',
        'avg_amount_range': (45.00, 85.00),  # Reduced from 120-200
        'merchant_code': '5812',
        'description': 'Sushi restaurant (occasional treat)'
    },
    
    # Gas Stations (Regular Frequency) - REALISTIC AMOUNTS
    '5004000001': {
        'name': 'Shell',
        'category': 'Gas & Fuel',
        'type': 'essential',
        'frequency': 'medium',
        'avg_amount_range': (25.00, 45.00),  # Reduced from 35-75
        'merchant_code': '5541',  # Service Stations
        'description': 'Gas station with convenience store'
    },
    '5004000002': {
        'name': 'Chevron',
        'category': 'Gas & Fuel',
        'type': 'essential',
        'frequency': 'medium',
        'avg_amount_range': (28.00, 50.00),  # Reduced from 40-80
        'merchant_code': '5541',
        'description': 'Premium gas station'
    },
    '5004000003': {
        'name': '76 Gas Station',
        'category': 'Gas & Fuel',
        'type': 'essential',
        'frequency': 'medium',
        'avg_amount_range': (22.00, 42.00),  # Reduced from 30-70
        'merchant_code': '5541',
        'description': 'West Coast gas station chain'
    },
    
    # Online Shopping (Medium Frequency) - REALISTIC AMOUNTS
    '5005000001': {
        'name': 'Amazon',
        'category': 'Online Retail',
        'type': 'discretionary',
        'frequency': 'medium',  # Reduced frequency
        'avg_amount_range': (12.00, 65.00),  # Reduced from 15-150
        'merchant_code': '5399',  # Miscellaneous General Merchandise
        'description': 'Online marketplace - household items'
    },
    '5005000002': {
        'name': 'Apple Store Online',
        'category': 'Electronics',
        'type': 'discretionary',
        'frequency': 'low',
        'avg_amount_range': (25.00, 200.00),  # Reduced from 50-1500
        'merchant_code': '5732',  # Electronics Stores
        'description': 'Apple accessories (not full devices)'
    },
    '5005000003': {
        'name': 'eBay',
        'category': 'Online Retail',
        'type': 'discretionary',
        'frequency': 'medium',
        'avg_amount_range': (10.00, 200.00),
        'merchant_code': '5399',
        'description': 'Online auction and marketplace'
    },
    '5005000004': {
        'name': 'Etsy',
        'category': 'Online Retail',
        'type': 'discretionary',
        'frequency': 'low',
        'avg_amount_range': (15.00, 100.00),
        'merchant_code': '5399',
        'description': 'Handmade and vintage items'
    },
    
    # Physical Retail Stores
    '5006000001': {
        'name': 'Target',
        'category': 'Retail',
        'type': 'essential',
        'frequency': 'medium',
        'avg_amount_range': (25.00, 120.00),
        'merchant_code': '5310',  # Discount Stores
        'description': 'General merchandise retailer'
    },
    '5006000002': {
        'name': 'Best Buy',
        'category': 'Electronics',
        'type': 'discretionary',
        'frequency': 'low',
        'avg_amount_range': (50.00, 800.00),
        'merchant_code': '5732',
        'description': 'Consumer electronics retailer'
    },
    '5006000003': {
        'name': 'CVS Pharmacy',
        'category': 'Health & Pharmacy',
        'type': 'essential',
        'frequency': 'medium',
        'avg_amount_range': (8.00, 50.00),
        'merchant_code': '5912',  # Drug Stores and Pharmacies
        'description': 'Pharmacy and convenience items'
    },
    '5006000004': {
        'name': 'Home Depot',
        'category': 'Home Improvement',
        'type': 'discretionary',
        'frequency': 'low',
        'avg_amount_range': (30.00, 200.00),
        'merchant_code': '5200',  # Home Supply Warehouse Stores
        'description': 'Home improvement and hardware'
    },
    '5006000005': {
        'name': 'Macy\'s',
        'category': 'Department Store',
        'type': 'discretionary',
        'frequency': 'low',
        'avg_amount_range': (40.00, 250.00),
        'merchant_code': '5311',  # Department Stores
        'description': 'Fashion and home goods'
    },
    
    # Subscriptions & Digital Services (Monthly)
    '5007000001': {
        'name': 'Netflix',
        'category': 'Entertainment',
        'type': 'subscription',
        'frequency': 'monthly',
        'avg_amount_range': (15.99, 15.99),
        'merchant_code': '4899',  # Cable and Other Pay Television Services
        'description': 'Streaming video service'
    },
    '5007000002': {
        'name': 'Spotify',
        'category': 'Entertainment',
        'type': 'subscription',
        'frequency': 'monthly',
        'avg_amount_range': (9.99, 9.99),
        'merchant_code': '4899',
        'description': 'Music streaming service'
    },
    '5007000003': {
        'name': 'Amazon Prime',
        'category': 'Subscription Services',
        'type': 'subscription',
        'frequency': 'monthly',
        'avg_amount_range': (14.99, 14.99),
        'merchant_code': '5399',
        'description': 'Prime membership and benefits'
    },
    '5007000004': {
        'name': 'Adobe Creative Cloud',
        'category': 'Software',
        'type': 'subscription',
        'frequency': 'monthly',
        'avg_amount_range': (52.99, 52.99),
        'merchant_code': '5734',  # Computer Software Stores
        'description': 'Creative software subscription'
    },
    '5007000005': {
        'name': 'Disney+',
        'category': 'Entertainment',
        'type': 'subscription',
        'frequency': 'monthly',
        'avg_amount_range': (7.99, 7.99),
        'merchant_code': '4899',
        'description': 'Disney streaming service'
    },
    
    # Fitness & Health
    '5008000001': {
        'name': 'Equinox Fitness',
        'category': 'Fitness & Health',
        'type': 'subscription',
        'frequency': 'monthly',
        'avg_amount_range': (180.00, 180.00),
        'merchant_code': '7997',  # Membership Clubs
        'description': 'Premium fitness club membership'
    },
    '5008000002': {
        'name': '24 Hour Fitness',
        'category': 'Fitness & Health',
        'type': 'subscription',
        'frequency': 'monthly',
        'avg_amount_range': (49.99, 49.99),
        'merchant_code': '7997',
        'description': 'Chain fitness center membership'
    },
    '5008000003': {
        'name': 'SoulCycle',
        'category': 'Fitness & Health',
        'type': 'discretionary',
        'frequency': 'medium',
        'avg_amount_range': (35.00, 35.00),
        'merchant_code': '7997',
        'description': 'Boutique fitness classes'
    },
    
    # Transportation
    '5009000001': {
        'name': 'Uber',
        'category': 'Transportation',
        'type': 'discretionary',
        'frequency': 'medium',
        'avg_amount_range': (12.00, 35.00),
        'merchant_code': '4121',  # Taxicabs and Limousines
        'description': 'Rideshare service'
    },
    '5009000002': {
        'name': 'Lyft',
        'category': 'Transportation',
        'type': 'discretionary',
        'frequency': 'medium',
        'avg_amount_range': (10.00, 30.00),
        'merchant_code': '4121',
        'description': 'Rideshare service'
    },
    '5009000003': {
        'name': 'Bay Area Rapid Transit',
        'category': 'Transportation',
        'type': 'essential',
        'frequency': 'high',
        'avg_amount_range': (3.50, 12.00),
        'merchant_code': '4111',  # Transportation - Suburban and Local Commuter Passenger
        'description': 'Public transit system'
    },
    
    # Travel & Airlines
    '5010000001': {
        'name': 'United Airlines',
        'category': 'Travel',
        'type': 'discretionary',
        'frequency': 'low',
        'avg_amount_range': (200.00, 800.00),
        'merchant_code': '4511',  # Airlines and Air Carriers
        'description': 'Domestic and international flights'
    },
    '5010000002': {
        'name': 'Airbnb',
        'category': 'Travel',
        'type': 'discretionary',
        'frequency': 'low',
        'avg_amount_range': (100.00, 400.00),
        'merchant_code': '7011',  # Hotels, Motels, and Resorts
        'description': 'Short-term rental accommodations'
    },
    '5010000003': {
        'name': 'Marriott Hotels',
        'category': 'Travel',
        'type': 'discretionary',
        'frequency': 'low',
        'avg_amount_range': (150.00, 350.00),
        'merchant_code': '7011',
        'description': 'Hotel chain accommodations'
    },
    
    # Utilities (Monthly)
    '5011000001': {
        'name': 'Pacific Gas & Electric',
        'category': 'Utilities',
        'type': 'essential',
        'frequency': 'monthly',
        'avg_amount_range': (80.00, 180.00),
        'merchant_code': '4900',  # Utilities
        'description': 'Electric and gas utility'
    },
    '5011000002': {
        'name': 'Comcast Xfinity',
        'category': 'Utilities',
        'type': 'essential',
        'frequency': 'monthly',
        'avg_amount_range': (75.00, 120.00),
        'merchant_code': '4899',
        'description': 'Internet and cable TV service'
    },
    '5011000003': {
        'name': 'AT&T Wireless',
        'category': 'Utilities',
        'type': 'essential',
        'frequency': 'monthly',
        'avg_amount_range': (65.00, 90.00),
        'merchant_code': '4814',  # Telecommunication Services
        'description': 'Mobile phone service'
    },
    '5011000004': {
        'name': 'San Francisco Water',
        'category': 'Utilities',
        'type': 'essential',
        'frequency': 'monthly',
        'avg_amount_range': (35.00, 75.00),
        'merchant_code': '4900',
        'description': 'Water and sewer services'
    }
}

# Category mappings for AI analysis
CATEGORY_MAPPINGS = {
    'Coffee & Cafes': {
        'type': 'Food & Dining',
        'essential': False,
        'typical_monthly_budget': 120.00,
        'cashback_rate_suggestion': 2.0
    },
    'Groceries': {
        'type': 'Food & Dining',
        'essential': True,
        'typical_monthly_budget': 400.00,
        'cashback_rate_suggestion': 3.0
    },
    'Fine Dining': {
        'type': 'Food & Dining',
        'essential': False,
        'typical_monthly_budget': 200.00,
        'cashback_rate_suggestion': 2.0
    },
    'Fast Casual': {
        'type': 'Food & Dining',
        'essential': False,
        'typical_monthly_budget': 150.00,
        'cashback_rate_suggestion': 2.0
    },
    'Casual Dining': {
        'type': 'Food & Dining',
        'essential': False,
        'typical_monthly_budget': 180.00,
        'cashback_rate_suggestion': 2.0
    },
    'Fast Food': {
        'type': 'Food & Dining',
        'essential': False,
        'typical_monthly_budget': 100.00,
        'cashback_rate_suggestion': 1.5
    },
    'Gas & Fuel': {
        'type': 'Transportation',
        'essential': True,
        'typical_monthly_budget': 180.00,
        'cashback_rate_suggestion': 3.0
    },
    'Online Retail': {
        'type': 'Shopping',
        'essential': False,
        'typical_monthly_budget': 300.00,
        'cashback_rate_suggestion': 2.0
    },
    'Electronics': {
        'type': 'Shopping',
        'essential': False,
        'typical_monthly_budget': 200.00,
        'cashback_rate_suggestion': 1.5
    },
    'Retail': {
        'type': 'Shopping',
        'essential': False,
        'typical_monthly_budget': 250.00,
        'cashback_rate_suggestion': 1.5
    },
    'Health & Pharmacy': {
        'type': 'Healthcare',
        'essential': True,
        'typical_monthly_budget': 80.00,
        'cashback_rate_suggestion': 2.0
    },
    'Home Improvement': {
        'type': 'Home',
        'essential': False,
        'typical_monthly_budget': 100.00,
        'cashback_rate_suggestion': 1.5
    },
    'Department Store': {
        'type': 'Shopping',
        'essential': False,
        'typical_monthly_budget': 150.00,
        'cashback_rate_suggestion': 1.5
    },
    'Entertainment': {
        'type': 'Entertainment',
        'essential': False,
        'typical_monthly_budget': 50.00,
        'cashback_rate_suggestion': 1.0
    },
    'Subscription Services': {
        'type': 'Services',
        'essential': False,
        'typical_monthly_budget': 75.00,
        'cashback_rate_suggestion': 1.0
    },
    'Software': {
        'type': 'Technology',
        'essential': False,
        'typical_monthly_budget': 100.00,
        'cashback_rate_suggestion': 1.0
    },
    'Fitness & Health': {
        'type': 'Healthcare',
        'essential': False,
        'typical_monthly_budget': 120.00,
        'cashback_rate_suggestion': 1.5
    },
    'Transportation': {
        'type': 'Transportation',
        'essential': True,
        'typical_monthly_budget': 200.00,
        'cashback_rate_suggestion': 2.0
    },
    'Travel': {
        'type': 'Travel',
        'essential': False,
        'typical_monthly_budget': 300.00,
        'cashback_rate_suggestion': 2.0
    },
    'Utilities': {
        'type': 'Bills & Utilities',
        'essential': True,
        'typical_monthly_budget': 350.00,
        'cashback_rate_suggestion': 1.0
    }
}

def get_merchant_info(account_num: str) -> dict:
    """Get merchant information by account number"""
    return MERCHANT_ACCOUNTS.get(account_num, {
        'name': f'Unknown Merchant ({account_num})',
        'category': 'Other',
        'type': 'unknown',
        'description': 'Unknown merchant'
    })

def get_category_info(category: str) -> dict:
    """Get category information for AI analysis"""
    return CATEGORY_MAPPINGS.get(category, {
        'type': 'Other',
        'essential': False,
        'typical_monthly_budget': 100.00,
        'cashback_rate_suggestion': 1.0
    })

def get_merchants_by_category(category: str) -> list:
    """Get all merchants in a specific category"""
    return [
        (account, info) for account, info in MERCHANT_ACCOUNTS.items()
        if info['category'] == category
    ]

def get_all_categories() -> list:
    """Get all unique merchant categories"""
    return list(set(info['category'] for info in MERCHANT_ACCOUNTS.values()))

# Export the main mapping for backward compatibility
__all__ = ['MERCHANT_ACCOUNTS', 'CATEGORY_MAPPINGS', 'get_merchant_info', 'get_category_info']
