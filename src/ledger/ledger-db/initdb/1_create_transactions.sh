#!/bin/bash
# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Create demo transactions in the ledger for the demo user accounts.
#
# Gerenated transactions follow a pattern of biweekly large deposits with
# periodic small payments to randomly choosen accounts.
#
# To run, set environment variable USE_DEMO_DATA="True"

set -u


# skip adding transactions if not enabled
if [ -z "$USE_DEMO_DATA" ] && [ "$USE_DEMO_DATA" != "True"  ]; then
    echo "\$USE_DEMO_DATA not \"True\"; no demo transactions added"
    exit 0
fi


# Expected environment variables
readonly ENV_VARS=(
  "POSTGRES_DB"
  "POSTGRES_USER"
  "POSTGRES_PASSWORD"
  "LOCAL_ROUTING_NUM"
)


add_transaction() {
    DATE=$(date -u +"%Y-%m-%d %H:%M:%S.%3N%z" --date="@$(($6))")
    echo "adding demo transaction: $1 -> $2"
    PGPASSWORD="$POSTGRES_PASSWORD" psql -X -v ON_ERROR_STOP=1 -v fromacct="$1" -v toacct="$2" -v fromroute="$3" -v toroute="$4" -v amount="$5" --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
        INSERT INTO TRANSACTIONS (FROM_ACCT, TO_ACCT, FROM_ROUTE, TO_ROUTE, AMOUNT, TIMESTAMP)
        VALUES (:'fromacct', :'toacct', :'fromroute', :'toroute', :'amount', '$DATE');
EOSQL
}


create_transactions() {
    PAY_PERIODS=3
    DAYS_BETWEEN_PAY=14
    SECONDS_IN_PAY_PERIOD=$(( 86400 * $DAYS_BETWEEN_PAY  ))
    DEPOSIT_AMOUNT=375000  # $3750 biweekly = $7500/month

    # create a UNIX timestamp in seconds since the Epoch
    START_TIMESTAMP=$(( $(date +%s) - $(( $(($PAY_PERIODS+1)) * $SECONDS_IN_PAY_PERIOD  ))  ))

    # Merchant accounts for realistic transactions
    MERCHANTS=(
        "2001001001:550"    # Starbucks Coffee - $5.50
        "2001001002:6500"   # Whole Foods Market - $65.00
        "2001001003:4200"   # Amazon.com - $42.00
        "2001001004:4500"   # Shell Gas Station - $45.00
        "2001001005:1200"   # McDonald's - $12.00
        "2001001006:8500"   # Target - $85.00
        "2001001007:1800"   # Uber - $18.00
        "2001001008:1599"   # Netflix - $15.99
        "2001001009:25000"  # Best Buy - $250.00
        "2001001010:1400"   # Chipotle - $14.00
        "2001001011:2800"   # CVS Pharmacy - $28.00
        "2001001012:1099"   # Spotify - $10.99
        "2001001013:12000"  # Apple Store - $120.00
        "2001001014:15000"  # Costco - $150.00
        "2001001015:4999"   # Planet Fitness - $49.99
        "2001001016:1200"   # Panera Bread - $12.00
        "2001001017:7500"   # Home Depot - $75.00
        "2001001018:5500"   # Safeway - $55.00
        "2001001019:2200"   # Lyft - $22.00
        "2001001020:2999"   # Adobe Creative Cloud - $29.99
    )

    for i in $(seq 1 $PAY_PERIODS); do
        # create deposit transaction for each user (salary)
        for account in ${USER_ACCOUNTS[@]}; do
            add_transaction "$EXTERNAL_ACCOUNT" "$account" "$EXTERNAL_ROUTING" "$LOCAL_ROUTING_NUM" $DEPOSIT_AMOUNT $START_TIMESTAMP
        done

        # Create realistic merchant transactions for testuser only
        TESTUSER_ACCOUNT="1011226111"
        
        # Add 8-12 realistic merchant transactions per pay period
        MERCHANT_TRANSACTIONS=$(shuf -i 8-12 -n1)
        for m in $(seq 1 $MERCHANT_TRANSACTIONS); do
            # Select random merchant
            MERCHANT_DATA=${MERCHANTS[$RANDOM % ${#MERCHANTS[@]}]}
            MERCHANT_ACCOUNT=$(echo $MERCHANT_DATA | cut -d':' -f1)
            BASE_AMOUNT=$(echo $MERCHANT_DATA | cut -d':' -f2)
            
            # Add some variance to amount (±20%)
            VARIANCE=$(shuf -i 80-120 -n1)
            AMOUNT=$(( $BASE_AMOUNT * $VARIANCE / 100 ))
            
            # Random timestamp within the pay period
            DAYS_OFFSET=$(shuf -i 1-13 -n1)
            TRANSACTION_TIMESTAMP=$(( $START_TIMESTAMP + $(( 86400 * $DAYS_OFFSET )) ))
            
            add_transaction "$TESTUSER_ACCOUNT" "$MERCHANT_ACCOUNT" "$LOCAL_ROUTING_NUM" "$LOCAL_ROUTING_NUM" $AMOUNT $TRANSACTION_TIMESTAMP
        done

        # Add a few peer-to-peer transactions (2-3 per period)
        P2P_TRANSACTIONS=$(shuf -i 2-3 -n1)
        for p in $(seq 1 $P2P_TRANSACTIONS); do
            # randomly generate an amount between $20-$150
            AMOUNT=$(shuf -i 2000-15000 -n1)

            # randomly select a sender and receiver
            SENDER_ACCOUNT=${USER_ACCOUNTS[$RANDOM % ${#USER_ACCOUNTS[@]}]}
            RECIPIENT_ACCOUNT=${USER_ACCOUNTS[$RANDOM % ${#USER_ACCOUNTS[@]}]}
            # if sender equals receiver, skip this transaction
            if [[ "$SENDER_ACCOUNT" == "$RECIPIENT_ACCOUNT" ]]; then
                continue
            fi

            DAYS_OFFSET=$(shuf -i 1-13 -n1)
            TRANSACTION_TIMESTAMP=$(( $START_TIMESTAMP + $(( 86400 * $DAYS_OFFSET )) ))

            add_transaction "$SENDER_ACCOUNT" "$RECIPIENT_ACCOUNT" "$LOCAL_ROUTING_NUM" "$LOCAL_ROUTING_NUM" $AMOUNT $TRANSACTION_TIMESTAMP
        done

        START_TIMESTAMP=$(( $START_TIMESTAMP + $(( $i * $SECONDS_IN_PAY_PERIOD  )) ))
    done
}


create_ledger() {
  # Account numbers for users 'testuser', 'alice', 'bob', and 'eve'.
  USER_ACCOUNTS=("1011226111" "1033623433" "1055757655" "1077441377")
  # Numbers for external account 'External Bank'
  EXTERNAL_ACCOUNT="9099791699"
  EXTERNAL_ROUTING="808889588"

  create_transactions
}


main() {
  # Check environment variables are set
	for env_var in ${ENV_VARS[@]}; do
    if [[ -z "${env_var}" ]]; then
      echo "Error: environment variable '$env_var' not set. Aborting."
      exit 1
    fi
  done

  create_ledger
}


main
