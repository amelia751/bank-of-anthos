"""
Merchant Account Mapping for Bank of Anthos AI Agents
Maps merchant account numbers to realistic business names and categories
"""

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
    '5006000003': {
        'name': 'CVS Pharmacy',
        'category': 'Pharmacy & Health',
        'type': 'essential',
        'frequency': 'medium',
        'avg_amount_range': [15.00, 40.00]
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
    '5007000003': {
        'name': 'Fitness Gym',
        'category': 'Fitness & Health',
        'type': 'subscription',
        'frequency': 'monthly',
        'avg_amount_range': [89.99, 89.99]
    },
    
    # Transportation
    '5008000001': {
        'name': 'Uber',
        'category': 'Rideshare',
        'type': 'transportation',
        'frequency': 'medium',
        'avg_amount_range': [12.00, 35.00]
    },
    '5008000002': {
        'name': 'Lyft',
        'category': 'Rideshare',
        'type': 'transportation',
        'frequency': 'medium',
        'avg_amount_range': [10.00, 30.00]
    },
    
    # Travel
    '5009000001': {
        'name': 'United Airlines',
        'category': 'Airlines',
        'type': 'travel',
        'frequency': 'low',
        'avg_amount_range': [200.00, 800.00]
    },
    '5009000002': {
        'name': 'Airbnb',
        'category': 'Accommodation',
        'type': 'travel',
        'frequency': 'low',
        'avg_amount_range': [100.00, 400.00]
    },
    
    # Utilities
    '5010000001': {
        'name': 'PG&E Electric Company',
        'category': 'Utilities',
        'type': 'essential',
        'frequency': 'monthly',
        'avg_amount_range': [120.00, 250.00]
    },
    '5010000002': {
        'name': 'Internet Service Provider',
        'category': 'Utilities',
        'type': 'essential',
        'frequency': 'monthly',
        'avg_amount_range': [79.99, 79.99]
    }
}

# Category groupings for spending analysis
SPENDING_CATEGORIES = {
    'dining': ['Coffee & Cafes', 'Fine Dining', 'Fast Casual', 'Restaurants'],
    'essential': ['Groceries', 'Gas & Fuel', 'Pharmacy & Health', 'Utilities'],
    'shopping': ['Online Retail', 'Electronics', 'Retail'],
    'entertainment': ['Streaming Services', 'Music Streaming'],
    'transportation': ['Rideshare', 'Gas & Fuel'],
    'travel': ['Airlines', 'Accommodation'],
    'health_fitness': ['Fitness & Health', 'Pharmacy & Health'],
    'subscriptions': ['Streaming Services', 'Music Streaming', 'Fitness & Health']
}

def get_merchant_info(account_number):
    """Get merchant information by account number"""
    return MERCHANT_ACCOUNTS.get(account_number, {
        'name': f'Merchant {account_number}',
        'category': 'Unknown',
        'type': 'other',
        'frequency': 'unknown',
        'avg_amount_range': [0, 0]
    })

def get_spending_by_category(transactions):
    """Analyze spending by category from transaction list"""
    category_spending = {}
    
    for tx in transactions:
        to_account = tx.get('toAccountNum') or tx.get('to_account')
        amount = float(tx.get('amount', 0)) / 100  # Convert cents to dollars
        
        merchant = get_merchant_info(to_account)
        category = merchant['category']
        
        if category not in category_spending:
            category_spending[category] = {'total': 0, 'count': 0, 'merchants': set()}
        
        category_spending[category]['total'] += amount
        category_spending[category]['count'] += 1
        category_spending[category]['merchants'].add(merchant['name'])
    
    # Convert sets to lists for JSON serialization
    for cat in category_spending:
        category_spending[cat]['merchants'] = list(category_spending[cat]['merchants'])
    
    return category_spending

def get_lifestyle_insights(transactions):
    """Generate lifestyle insights from spending patterns"""
    category_spending = get_spending_by_category(transactions)
    total_spending = sum(cat['total'] for cat in category_spending.values())
    
    insights = []
    
    # Dining patterns
    dining_total = sum(category_spending.get(cat, {}).get('total', 0) 
                      for cat in ['Coffee & Cafes', 'Fine Dining', 'Fast Casual', 'Restaurants'])
    if dining_total > 0:
        dining_pct = (dining_total / total_spending) * 100
        if dining_pct > 20:
            insights.append(f"High dining spending ({dining_pct:.1f}% of total) - Great candidate for dining rewards cards")
        elif dining_pct > 10:
            insights.append(f"Moderate dining spending ({dining_pct:.1f}% of total) - May benefit from dining cashback offers")
    
    # Travel patterns
    travel_total = sum(category_spending.get(cat, {}).get('total', 0) 
                      for cat in ['Airlines', 'Accommodation'])
    if travel_total > 500:  # Significant travel spending
        insights.append("Frequent traveler - Excellent candidate for travel rewards and airline miles programs")
    
    # Technology spending
    tech_total = category_spending.get('Electronics', {}).get('total', 0)
    if tech_total > 500:
        insights.append("Technology enthusiast - May benefit from tech cashback and extended warranty programs")
    
    # Subscription patterns
    streaming_count = (category_spending.get('Streaming Services', {}).get('count', 0) + 
                      category_spending.get('Music Streaming', {}).get('count', 0))
    if streaming_count > 2:
        insights.append("Multiple subscriptions - Could benefit from subscription management and cashback offers")
    
    return insights
