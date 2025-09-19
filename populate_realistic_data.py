#!/usr/bin/env python3
"""
Populate Bank of Anthos database with realistic user spending habits.
This script creates a fixed dataset that can be reliably reproduced after restarting the project.
"""

import os
import sys
import psycopg2
from datetime import datetime, timedelta
import random
from typing import List, Dict, Any

# Add the boa-ai-agents directory to the path to import merchant mapping
sys.path.append(os.path.join(os.path.dirname(__file__), 'boa-ai-agents'))

try:
    from merchant_mapping import MERCHANT_ACCOUNTS
except ImportError:
    print("Error: Could not import merchant_mapping. Make sure boa-ai-agents/merchant_mapping.py exists.")
    sys.exit(1)

# Database configuration
LEDGER_DB_CONFIG = {
    'host': os.getenv('POSTGRES_HOST', 'localhost'),
    'database': os.getenv('POSTGRES_DB', 'postgresdb'),
    'user': os.getenv('POSTGRES_USER', 'postgres'),
    'password': os.getenv('POSTGRES_PASSWORD', 'password'),
    'port': os.getenv('POSTGRES_PORT', '5432')
}

ACCOUNTS_DB_CONFIG = {
    'host': os.getenv('ACCOUNTS_POSTGRES_HOST', os.getenv('POSTGRES_HOST', 'localhost')),
    'database': os.getenv('ACCOUNTS_POSTGRES_DB', 'postgresdb'),
    'user': os.getenv('ACCOUNTS_POSTGRES_USER', os.getenv('POSTGRES_USER', 'postgres')),
    'password': os.getenv('ACCOUNTS_POSTGRES_PASSWORD', os.getenv('POSTGRES_PASSWORD', 'password')),
    'port': os.getenv('ACCOUNTS_POSTGRES_PORT', os.getenv('POSTGRES_PORT', '5432'))
}

# User accounts from the Bank of Anthos system
USERS = {
    'testuser': '1011226111',  # Main user for spending simulation
    'alice': '1033623433',     # Recipient
    'bob': '1055757655',       # Recipient  
    'eve': '1077441377'        # Recipient
}

# External bank for income deposits
EXTERNAL_BANK = {
    'account': '9099791699',
    'routing': '808889588'
}

# Local routing number
LOCAL_ROUTING = '883745000'

# Generate fixed dataset - using deterministic approach for reproducibility
class FixedDataGenerator:
    def __init__(self):
        # Set fixed seed for reproducible results
        random.seed(42)
        
        # Define income pattern for testuser (bi-weekly paychecks)
        self.monthly_income = 5000.00  # $5000/month
        self.paycheck_amount = int(self.monthly_income / 2 * 100)  # Convert to cents, bi-weekly
        
        # Date range for transactions (last 3 months)
        self.end_date = datetime(2025, 9, 19)  # Current date
        self.start_date = self.end_date - timedelta(days=90)
        
        self.transactions = []
        self.contacts_to_add = []
    
    def add_transaction(self, from_acct: str, to_acct: str, from_route: str, 
                       to_route: str, amount: int, timestamp: datetime, description: str = ""):
        """Add a transaction to the list"""
        self.transactions.append({
            'from_acct': from_acct,
            'to_acct': to_acct,
            'from_route': from_route,
            'to_route': to_route,
            'amount': amount,
            'timestamp': timestamp,
            'description': description
        })
    
    def add_contact(self, username: str, label: str, account_num: str, routing_num: str, is_external: bool = False):
        """Add a contact to the list"""
        self.contacts_to_add.append({
            'username': username,
            'label': label,
            'account_num': account_num,
            'routing_num': routing_num,
            'is_external': str(is_external).lower()
        })
    
    def generate_income_deposits(self):
        """Generate bi-weekly income deposits from External Bank to testuser"""
        print("Generating income deposits...")
        
        current_date = self.start_date
        paycheck_count = 0
        
        # Generate bi-weekly paychecks
        while current_date <= self.end_date:
            # Paychecks come every 14 days on Fridays
            if current_date.weekday() == 4:  # Friday
                paycheck_count += 1
                # Add some variation to paycheck amounts (overtime, bonuses, deductions)
                variation = random.uniform(0.85, 1.15)
                amount = int(self.paycheck_amount * variation)
                
                # Paycheck time (usually processed early morning)
                paycheck_time = current_date.replace(hour=6, minute=0, second=0)
                
                self.add_transaction(
                    EXTERNAL_BANK['account'],
                    USERS['testuser'],
                    EXTERNAL_BANK['routing'],
                    LOCAL_ROUTING,
                    amount,
                    paycheck_time,
                    f"Paycheck #{paycheck_count}"
                )
                
                # Skip 2 weeks for next paycheck
                current_date += timedelta(days=14)
            else:
                current_date += timedelta(days=1)
        
        print(f"Generated {paycheck_count} income deposits")
    
    def generate_merchant_expenses(self):
        """Generate realistic expense transactions to merchants"""
        print("Generating merchant expense transactions...")
        
        # Add all merchants as contacts for testuser
        for merchant_account, merchant_info in MERCHANT_ACCOUNTS.items():
            self.add_contact(
                'testuser',
                merchant_info['name'],
                merchant_account,
                LOCAL_ROUTING,
                False
            )
        
        # Generate transactions based on merchant frequency and patterns
        current_date = self.start_date
        expense_count = 0
        
        while current_date <= self.end_date:
            for merchant_account, merchant_info in MERCHANT_ACCOUNTS.items():
                frequency = merchant_info['frequency']
                merchant_type = merchant_info['type']
                amount_range = merchant_info['avg_amount_range']
                
                # Determine if transaction should occur on this day
                should_transact = False
                
                if frequency == 'high':
                    # 2-3 times per week
                    should_transact = random.random() < 0.35
                elif frequency == 'medium':
                    # 1-2 times per week  
                    should_transact = random.random() < 0.20
                elif frequency == 'low':
                    # 1-2 times per month
                    should_transact = random.random() < 0.05
                elif frequency == 'monthly':
                    # Once per month on specific dates
                    if merchant_type == 'subscription':
                        # Subscriptions typically charge on the same day each month
                        should_transact = current_date.day == 15  # 15th of each month
                    elif merchant_type == 'essential' and 'Utilities' in merchant_info['category']:
                        # Utilities typically charge on the 1st of each month
                        should_transact = current_date.day == 1
                
                if should_transact:
                    # Generate transaction amount within the merchant's range
                    min_amount, max_amount = amount_range
                    amount_dollars = random.uniform(min_amount, max_amount)
                    amount_cents = int(amount_dollars * 100)
                    
                    # Generate realistic transaction time
                    if merchant_type == 'subscription':
                        # Subscriptions usually process early morning
                        tx_time = current_date.replace(hour=random.randint(2, 6), 
                                                     minute=random.randint(0, 59))
                    elif 'Coffee' in merchant_info['category']:
                        # Coffee purchases in morning
                        tx_time = current_date.replace(hour=random.randint(7, 10),
                                                     minute=random.randint(0, 59))
                    elif merchant_info['category'] in ['Groceries', 'Retail']:
                        # Grocery/retail shopping during day/evening
                        tx_time = current_date.replace(hour=random.randint(10, 20),
                                                     minute=random.randint(0, 59))
                    elif 'Dining' in merchant_info['category'] or 'Restaurant' in merchant_info['category']:
                        # Dining during meal times
                        if random.random() < 0.3:  # Lunch
                            tx_time = current_date.replace(hour=random.randint(11, 14),
                                                         minute=random.randint(0, 59))
                        else:  # Dinner
                            tx_time = current_date.replace(hour=random.randint(17, 21),
                                                         minute=random.randint(0, 59))
                    else:
                        # Default random time during business hours
                        tx_time = current_date.replace(hour=random.randint(9, 18),
                                                     minute=random.randint(0, 59))
                    
                    self.add_transaction(
                        USERS['testuser'],
                        merchant_account,
                        LOCAL_ROUTING,
                        LOCAL_ROUTING,
                        amount_cents,
                        tx_time,
                        f"Purchase at {merchant_info['name']}"
                    )
                    expense_count += 1
            
            current_date += timedelta(days=1)
        
        print(f"Generated {expense_count} merchant expense transactions")
    
    def generate_peer_transfers(self):
        """Generate some peer-to-peer transfers between users"""
        print("Generating peer-to-peer transfers...")
        
        transfer_count = 0
        current_date = self.start_date
        
        while current_date <= self.end_date:
            # Random p2p transfers a few times per month
            if random.random() < 0.05:  # 5% chance per day
                # testuser sending money to friends
                recipients = ['alice', 'bob', 'eve']
                recipient = random.choice(recipients)
                
                # Typical amounts for peer transfers ($10-100)
                amount_dollars = random.uniform(10, 100)
                amount_cents = int(amount_dollars * 100)
                
                # Random time during the day
                tx_time = current_date.replace(hour=random.randint(8, 22),
                                             minute=random.randint(0, 59))
                
                self.add_transaction(
                    USERS['testuser'],
                    USERS[recipient],
                    LOCAL_ROUTING,
                    LOCAL_ROUTING,
                    amount_cents,
                    tx_time,
                    f"Transfer to {recipient.title()}"
                )
                transfer_count += 1
            
            current_date += timedelta(days=1)
        
        print(f"Generated {transfer_count} peer-to-peer transfers")
    
    def generate_all_data(self):
        """Generate all transaction data"""
        print("=" * 50)
        print("GENERATING REALISTIC SPENDING DATA")
        print("=" * 50)
        
        self.generate_income_deposits()
        self.generate_merchant_expenses()
        self.generate_peer_transfers()
        
        print(f"\nTotal transactions generated: {len(self.transactions)}")
        print(f"Total contacts to add: {len(self.contacts_to_add)}")
        
        return self.transactions, self.contacts_to_add


def connect_to_databases():
    """Connect to both PostgreSQL databases"""
    try:
        print(f"Connecting to ledger database: {LEDGER_DB_CONFIG['host']}:{LEDGER_DB_CONFIG['port']}/{LEDGER_DB_CONFIG['database']}")
        ledger_conn = psycopg2.connect(**LEDGER_DB_CONFIG)
        print("Ledger database connection successful!")
        
        print(f"Connecting to accounts database: {ACCOUNTS_DB_CONFIG['host']}:{ACCOUNTS_DB_CONFIG['port']}/{ACCOUNTS_DB_CONFIG['database']}")
        accounts_conn = psycopg2.connect(**ACCOUNTS_DB_CONFIG)
        print("Accounts database connection successful!")
        
        return ledger_conn, accounts_conn
    except psycopg2.Error as e:
        print(f"Error connecting to database: {e}")
        return None, None


def clear_existing_data(ledger_conn, accounts_conn):
    """Clear existing transaction and contact data"""
    try:
        # Clear merchant contacts from accounts database
        accounts_cur = accounts_conn.cursor()
        print("Clearing existing merchant contacts...")
        merchant_accounts = list(MERCHANT_ACCOUNTS.keys())
        if merchant_accounts:
            placeholders = ','.join(['%s'] * len(merchant_accounts))
            accounts_cur.execute(f"""
                DELETE FROM contacts 
                WHERE username = 'testuser' 
                AND account_num IN ({placeholders})
            """, merchant_accounts)
        accounts_conn.commit()
        
        # Clear transactions from ledger database
        ledger_cur = ledger_conn.cursor()
        print("Clearing existing transactions...")
        # Delete transactions involving testuser (keeping some original demo data for other users)
        ledger_cur.execute("""
            DELETE FROM transactions 
            WHERE from_acct = %s OR to_acct = %s
        """, (USERS['testuser'], USERS['testuser']))
        ledger_conn.commit()
        
        print("Existing data cleared successfully!")
        
    except psycopg2.Error as e:
        print(f"Error clearing existing data: {e}")
        if 'accounts_conn' in locals():
            accounts_conn.rollback()
        if 'ledger_conn' in locals():
            ledger_conn.rollback()
        raise


def populate_contacts(accounts_conn, contacts):
    """Add merchant contacts to user accounts"""
    try:
        cur = accounts_conn.cursor()
        
        print("Adding merchant contacts...")
        for contact in contacts:
            cur.execute("""
                INSERT INTO contacts (username, label, account_num, routing_num, is_external)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT DO NOTHING
            """, (
                contact['username'],
                contact['label'],
                contact['account_num'],
                contact['routing_num'],
                contact['is_external']
            ))
        
        accounts_conn.commit()
        print(f"Added {len(contacts)} merchant contacts!")
        
    except psycopg2.Error as e:
        print(f"Error adding contacts: {e}")
        accounts_conn.rollback()
        raise


def populate_transactions(ledger_conn, transactions):
    """Insert transactions into the database"""
    try:
        cur = ledger_conn.cursor()
        
        print("Inserting transactions...")
        for i, tx in enumerate(transactions):
            cur.execute("""
                INSERT INTO transactions (from_acct, to_acct, from_route, to_route, amount, timestamp)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                tx['from_acct'],
                tx['to_acct'],
                tx['from_route'],
                tx['to_route'],
                tx['amount'],
                tx['timestamp']
            ))
            
            if (i + 1) % 100 == 0:
                print(f"Inserted {i + 1} transactions...")
        
        ledger_conn.commit()
        print(f"Successfully inserted {len(transactions)} transactions!")
        
    except psycopg2.Error as e:
        print(f"Error inserting transactions: {e}")
        ledger_conn.rollback()
        raise


def main():
    """Main function to populate the database"""
    print("Bank of Anthos - Realistic Data Population Script")
    print("=" * 50)
    
    # Generate the data
    generator = FixedDataGenerator()
    transactions, contacts = generator.generate_all_data()
    
    # Connect to databases
    ledger_conn, accounts_conn = connect_to_databases()
    if not ledger_conn or not accounts_conn:
        sys.exit(1)
    
    try:
        # Clear existing data
        clear_existing_data(ledger_conn, accounts_conn)
        
        # Populate new data
        populate_contacts(accounts_conn, contacts)
        populate_transactions(ledger_conn, transactions)
        
        print("\n" + "=" * 50)
        print("SUCCESS! Realistic spending data has been populated.")
        print("=" * 50)
        print(f"Income deposits: {sum(1 for tx in transactions if tx['from_acct'] == EXTERNAL_BANK['account'])}")
        print(f"Merchant expenses: {sum(1 for tx in transactions if tx['to_acct'] in MERCHANT_ACCOUNTS)}")
        print(f"Peer transfers: {sum(1 for tx in transactions if tx['from_acct'] != EXTERNAL_BANK['account'] and tx['to_acct'] not in MERCHANT_ACCOUNTS)}")
        print(f"Total transactions: {len(transactions)}")
        print(f"Merchant contacts added: {len(contacts)}")
        
    except Exception as e:
        print(f"Error during population: {e}")
        sys.exit(1)
    finally:
        if ledger_conn:
            ledger_conn.close()
        if accounts_conn:
            accounts_conn.close()


if __name__ == "__main__":
    main()
