# DigitalWallet.py
import datetime
from collections import defaultdict


class FraudDetector:

    def __init__(self):
        # Maps account_id -> list of timestamps for successful/attempted transactions
        self.tx_timestamps = defaultdict(list)
        # Maps account_id -> count of consecutive failed PIN attempts
        self.failed_pin_counts = defaultdict(int)

    def log_transaction_attempt(self, account_id):
        now = datetime.datetime.now()
        self.tx_timestamps[account_id].append(now)

    def log_failed_pin(self, account_id):
        self.failed_pin_counts[account_id] += 1

    def reset_failed_pins(self, account_id):
        self.failed_pin_counts[account_id] = 0

    def is_suspicious(self, account_id, amount, account_balance):
        now = datetime.datetime.now()
        ten_minutes_ago = now - datetime.timedelta(minutes=10)

        # 1. More than 5 transactions in 10 minutes
        recent_txs = [
            t for t in self.tx_timestamps[account_id] if t >= ten_minutes_ago
        ]
        if len(recent_txs) > 5:
            return True, "High transaction frequency (More than 5 in 10 mins)"

        # 2. Large transaction (e.g., greater than 10,000)
        if amount > 10000:
            return True, "Large transaction amount"

        # 3. Multiple failed PIN attempts (3 or more)
        if self.failed_pin_counts[account_id] >= 3:
            return True, "Multiple failed PIN attempts"

        # 4. Unusual transaction amount (e.g., greater than 3x the current balance for active accounts)
        # Or if it depletes more than 95% of a substantial balance in a single go
        if account_balance > 0 and amount > (account_balance * 3):
            return True, "Unusual transaction amount relative to balance"

        return False, ""


class Account:

    def __init__(self, account_id, pin, daily_limit=5000.0):
        self.account_id = account_id
        self.pin = pin
        self.balance = 0.0
        self.daily_limit = daily_limit
        self.daily_spent = 0.0
        self.last_tx_date = datetime.date.today()
        self.history = []

    def reset_daily_limit_if_new_day(self):
        now_date = datetime.date.today()
        if now_date != self.last_tx_date:
            self.daily_spent = 0.0
            self.last_tx_date = now_date

    def verify_pin(self, pin):
        return self.pin == pin


class DigitalWalletSystem:

    def __init__(self):
        self.accounts = {}
        self.fraud_detector = FraudDetector()
        # To detect duplicate transactions (Account, Amount, Type within last few seconds)
        self.last_transactions = {}

    def create_account(self, account_id, pin, daily_limit=5000.0):
        if account_id in self.accounts:
            return False, "Account already exists"
        self.accounts[account_id] = Account(account_id, pin, daily_limit)
        return True, "Account created successfully"

    def verify_balance(self, account_id):
        if account_id not in self.accounts:
            return None, "Account not found"
        return self.accounts[account_id].balance, "Success"

    def deposit(self, account_id, amount):
        if amount <= 0:
            return False, "Amount must be positive"
        if account_id not in self.accounts:
            return False, "Account not found"

        account = self.accounts[account_id]

        # Fraud check for unusual amount
        suspicious, reason = self.fraud_detector.is_suspicious(
            account_id, amount, account.balance
        )
        if suspicious:
            account.history.append(f"FLAGGED DEPOSIT: {amount} - {reason}")
            return False, f"Transaction flagged as suspicious: {reason}"

        account.balance += amount
        self.fraud_detector.log_transaction_attempt(account_id)
        account.history.append(f"Deposited: {amount}")
        return True, "Deposit successful"

    def withdraw(self, account_id, amount, pin):
        if amount <= 0:
            return False, "Amount must be positive"
        if account_id not in self.accounts:
            return False, "Account not found"

        account = self.accounts[account_id]
        account.reset_daily_limit_if_new_day()

        # PIN Verification
        if not account.verify_pin(pin):
            self.fraud_detector.log_failed_pin(account_id)
            # Re-check fraud after logging failed PIN
            suspicious, reason = self.fraud_detector.is_suspicious(
                account_id, amount, account.balance
            )
            if suspicious:
                return False, f"Security Block: {reason}"
            return False, "Invalid PIN"

        # Duplicate Transaction Check (same account, amount, type within 2 seconds)
        now = datetime.datetime.now()
        tx_key = (account_id, amount, "withdraw")
        if tx_key in self.last_transactions:
            last_time = self.last_transactions[tx_key]
            if (now - last_time).total_seconds() < 2:
                return False, "Duplicate transaction detected"

        # Fraud check
        suspicious, reason = self.fraud_detector.is_suspicious(
            account_id, amount, account.balance
        )
        if suspicious:
            account.history.append(f"FLAGGED WITHDRAWAL: {amount} - {reason}")
            return False, f"Transaction flagged as suspicious: {reason}"

        # Standard business limits
        if account.balance < amount:
            return False, "Insufficient balance"

        if account.daily_spent + amount > account.daily_limit:
            return False, "Daily transaction limit exceeded"

        # Execute
        account.balance -= amount
        account.daily_spent += amount
        self.fraud_detector.reset_failed_pins(account_id)
        self.fraud_detector.log_transaction_attempt(account_id)
        self.last_transactions[tx_key] = now

        account.history.append(f"Withdrew: {amount}")
        return True, "Withdrawal successful"

    def transfer(self, sender_id, receiver_id, amount, pin):
        if amount <= 0:
            return False, "Amount must be positive"
        if sender_id not in self.accounts or receiver_id not in self.accounts:
            return False, "One or both accounts do not exist"
        if sender_id == receiver_id:
            return False, "Cannot transfer to the same account"

        sender = self.accounts[sender_id]
        receiver = self.accounts[receiver_id]
        sender.reset_daily_limit_if_new_day()

        if not sender.verify_pin(pin):
            self.fraud_detector.log_failed_pin(sender_id)
            return False, "Invalid PIN"

        suspicious, reason = self.fraud_detector.is_suspicious(
            sender_id, amount, sender.balance
        )
        if suspicious:
            sender.history.append(f"FLAGGED TRANSFER: {amount} to {receiver_id} - {reason}")
            return False, f"Transaction flagged as suspicious: {reason}"

        if sender.balance < amount:
            return False, "Insufficient balance"

        if sender.daily_spent + amount > sender.daily_limit:
            return False, "Daily transaction limit exceeded"

        sender.balance -= amount
        sender.daily_spent += amount
        receiver.balance += amount

        self.fraud_detector.reset_failed_pins(sender_id)
        self.fraud_detector.log_transaction_attempt(sender_id)

        sender.history.append(f"Transferred {amount} to {receiver_id}")
        receiver.history.append(f"Received {amount} from {sender_id}")
        return True, "Transfer successful"

    def get_transaction_history(self, account_id):
        if account_id not in self.accounts:
            return None, "Account not found"
        return self.accounts[account_id].history, "Success"
