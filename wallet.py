from datetime import datetime, timedelta
import threading
import sys


class DigitalWallet:

    def __init__(self):
        self.accounts = {}
        self.transactions = {}
        self.failed_pins = {}
        self.lock = threading.Lock()

        self.daily_limit = 50000
        self.large_transaction_limit = 25000

    # Account creation
    def create_account(self, account_id, name, pin, balance=0):

        if account_id in self.accounts:
            return False

        if balance < 0:
            return False

        self.accounts[account_id] = {
            "name": name,
            "pin": str(pin),
            "balance": balance
        }

        self.transactions[account_id] = []
        self.failed_pins[account_id] = 0

        return True

    # PIN verification
    def verify_pin(self, account_id, pin):

        if account_id not in self.accounts:
            return False

        if self.accounts[account_id]["pin"] == str(pin):
            self.failed_pins[account_id] = 0
            return True

        self.failed_pins[account_id] += 1
        return False

    # Balance verification
    def get_balance(self, account_id):

        if account_id not in self.accounts:
            return None

        return self.accounts[account_id]["balance"]

    # Record transaction
    def record_transaction(self, account_id, transaction_type, amount):

        self.transactions[account_id].append({
            "type": transaction_type,
            "amount": amount,
            "time": datetime.now()
        })

    # Calculate today's transactions
    def get_daily_total(self, account_id):

        today = datetime.now().date()
        total = 0

        for transaction in self.transactions[account_id]:

            if transaction["time"].date() == today:
                total += transaction["amount"]

        return total

    # Deposit
    def deposit(self, account_id, amount):

        if account_id not in self.accounts:
            return False

        if amount <= 0:
            return False

        with self.lock:

            self.accounts[account_id]["balance"] += amount

            self.record_transaction(
                account_id,
                "Deposit",
                amount
            )

        return True

    # Withdrawal
    def withdraw(self, account_id, amount, pin):

        if account_id not in self.accounts:
            return False

        if not self.verify_pin(account_id, pin):
            return False

        if amount <= 0:
            return False

        if self.accounts[account_id]["balance"] < amount:
            return False

        if self.get_daily_total(account_id) + amount > self.daily_limit:
            return False

        with self.lock:

            self.accounts[account_id]["balance"] -= amount

            self.record_transaction(
                account_id,
                "Withdrawal",
                amount
            )

        return True

    # Money transfer
    def transfer(self, sender, receiver, amount, pin):

        if sender not in self.accounts:
            return False

        if receiver not in self.accounts:
            return False

        if sender == receiver:
            return False

        if not self.verify_pin(sender, pin):
            return False

        if amount <= 0:
            return False

        if self.accounts[sender]["balance"] < amount:
            return False

        if self.get_daily_total(sender) + amount > self.daily_limit:
            return False

        with self.lock:

            self.accounts[sender]["balance"] -= amount
            self.accounts[receiver]["balance"] += amount

            self.record_transaction(
                sender,
                "Transfer",
                amount
            )

            self.record_transaction(
                receiver,
                "Received",
                amount
            )

        return True

    # Transaction history
    def get_transaction_history(self, account_id):

        if account_id not in self.accounts:
            return []

        return self.transactions[account_id]

    # Fraud detection
    def fraud_detection(self, account_id, amount):

        suspicious = []

        if account_id not in self.accounts:
            return ["Invalid account"]

        # Large transaction
        if amount > self.large_transaction_limit:
            suspicious.append("Large transaction")

        # Multiple failed PIN attempts
        if self.failed_pins[account_id] >= 3:
            suspicious.append("Multiple failed PIN attempts")

        # More than 5 transactions in 10 minutes
        current_time = datetime.now()

        recent_transactions = 0

        for transaction in self.transactions[account_id]:

            if current_time - transaction["time"] <= timedelta(minutes=10):
                recent_transactions += 1

        if recent_transactions > 5:
            suspicious.append(
                "More than 5 transactions in 10 minutes"
            )

        # Unusual amount
        if amount > 10000:
            suspicious.append("Unusual transaction amount")

        return suspicious


# =====================================================
# TEST FUNCTIONS
# =====================================================

passed = 0
failed = 0


def check_test(test_name, condition):

    global passed
    global failed

    if condition:
        print("PASS - " + test_name)
        passed += 1
    else:
        print("FAIL - " + test_name)
        failed += 1


# 1. Account Creation
def test_account_creation():

    wallet = DigitalWallet()

    result = wallet.create_account(
        "A101",
        "Thamarai",
        "1234",
        10000
    )

    check_test(
        "Account Creation",
        result is True
    )


# 2. Normal Transaction
def test_normal_transaction():

    wallet = DigitalWallet()

    wallet.create_account(
        "A101",
        "Thamarai",
        "1234",
        10000
    )

    result = wallet.deposit(
        "A101",
        2000
    )

    check_test(
        "Normal Transaction",
        result is True
        and wallet.get_balance("A101") == 12000
    )


# 3. Insufficient Balance
def test_insufficient_balance():

    wallet = DigitalWallet()

    wallet.create_account(
        "A101",
        "Thamarai",
        "1234",
        1000
    )

    result = wallet.withdraw(
        "A101",
        5000,
        "1234"
    )

    check_test(
        "Insufficient Balance",
        result is False
    )


# 4. Daily Limit
def test_daily_limit():

    wallet = DigitalWallet()

    wallet.create_account(
        "A101",
        "Thamarai",
        "1234",
        100000
    )

    result = wallet.withdraw(
        "A101",
        50001,
        "1234"
    )

    check_test(
        "Daily Transaction Limit",
        result is False
    )


# 5. Multiple Failed PIN
def test_failed_pins():

    wallet = DigitalWallet()

    wallet.create_account(
        "A101",
        "Thamarai",
        "1234",
        10000
    )

    wallet.withdraw("A101", 100, "1111")
    wallet.withdraw("A101", 100, "2222")
    wallet.withdraw("A101", 100, "3333")

    check_test(
        "Multiple Failed PIN Attempts",
        wallet.failed_pins["A101"] >= 3
    )


# 6. Suspicious Transaction
def test_suspicious_transaction():

    wallet = DigitalWallet()

    wallet.create_account(
        "A101",
        "Thamarai",
        "1234",
        100000
    )

    fraud = wallet.fraud_detection(
        "A101",
        30000
    )

    check_test(
        "Suspicious Transaction",
        "Large transaction" in fraud
    )


# 7. Duplicate Transaction
def test_duplicate_transaction():

    wallet = DigitalWallet()

    wallet.create_account(
        "A101",
        "Thamarai",
        "1234",
        10000
    )

    wallet.deposit("A101", 1000)
    wallet.deposit("A101", 1000)

    history = wallet.get_transaction_history("A101")

    check_test(
        "Duplicate Transaction",
        len(history) == 2
    )


# 8. Negative Amount
def test_negative_amount():

    wallet = DigitalWallet()

    wallet.create_account(
        "A101",
        "Thamarai",
        "1234",
        10000
    )

    result = wallet.deposit(
        "A101",
        -500
    )

    check_test(
        "Negative Amount",
        result is False
    )


# 9. Concurrent Transactions
def deposit_thread(wallet):

    wallet.deposit(
        "A101",
        100
    )


def test_concurrent_transactions():

    wallet = DigitalWallet()

    wallet.create_account(
        "A101",
        "Thamarai",
        "1234",
        10000
    )

    threads = []

    for i in range(5):

        thread = threading.Thread(
            target=deposit_thread,
            args=(wallet,)
        )

        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    check_test(
        "Concurrent Transactions",
        wallet.get_balance("A101") == 10500
    )


# =====================================================
# RUN ALL TESTS
# =====================================================

if __name__ == "__main__":

    print()
    print("========================================")
    print("     DIGITAL WALLET SECURITY QA")
    print("========================================")

    test_account_creation()
    test_normal_transaction()
    test_insufficient_balance()
    test_daily_limit()
    test_failed_pins()
    test_suspicious_transaction()
    test_duplicate_transaction()
    test_negative_amount()
    test_concurrent_transactions()

    print()
    print("========================================")
    print("Tests Passed :", passed)
    print("Tests Failed :", failed)
    print("========================================")

    if failed == 0:

        print("ALL TESTS PASSED")
        sys.exit(0)

    else:

        print("TESTS FAILED")
        sys.exit(1)
