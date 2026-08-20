from datetime import datetime, timedelta
import threading


class DigitalWallet:
    def __init__(self):
        self.accounts = {}
        self.transaction_history = {}
        self.failed_pins = {}
        self.lock = threading.Lock()

        self.daily_limit = 50000
        self.transaction_times = {}

    def create_account(self, account_id, name, pin, balance=0):
        if account_id in self.accounts:
            return "Account already exists"

        self.accounts[account_id] = {
            "name": name,
            "pin": pin,
            "balance": balance
        }

        self.transaction_history[account_id] = []
        self.failed_pins[account_id] = 0
        self.transaction_times[account_id] = []

        return "Account created successfully"

    def verify_pin(self, account_id, pin):
        if account_id not in self.accounts:
            return False

        if self.accounts[account_id]["pin"] == pin:
            self.failed_pins[account_id] = 0
            return True

        self.failed_pins[account_id] += 1
        return False

    def deposit(self, account_id, amount):
        if account_id not in self.accounts:
            return "Invalid account"

        if amount <= 0:
            return "Invalid amount"

        with self.lock:
            self.accounts[account_id]["balance"] += amount
            self.record_transaction(account_id, "Deposit", amount)

        return "Deposit successful"

    def withdrawal(self, account_id, amount, pin):
        if not self.verify_pin(account_id, pin):
            return "Invalid PIN"

        if amount <= 0:
            return "Invalid amount"

        if account_id not in self.accounts:
            return "Invalid account"

        if self.accounts[account_id]["balance"] < amount:
            return "Insufficient balance"

        if not self.check_daily_limit(account_id, amount):
            return "Daily transaction limit exceeded"

        with self.lock:
            self.accounts[account_id]["balance"] -= amount
            self.record_transaction(account_id, "Withdrawal", amount)

        self.check_fraud(account_id, amount)

        return "Withdrawal successful"

    def transfer(self, sender, receiver, amount, pin):
        if sender not in self.accounts or receiver not in self.accounts:
            return "Invalid account"

        if not self.verify_pin(sender, pin):
            return "Invalid PIN"

        if amount <= 0:
            return "Invalid amount"

        if self.accounts[sender]["balance"] < amount:
            return "Insufficient balance"

        if not self.check_daily_limit(sender, amount):
            return "Daily transaction limit exceeded"

        with self.lock:
            self.accounts[sender]["balance"] -= amount
            self.accounts[receiver]["balance"] += amount

            self.record_transaction(
                sender,
                "Transfer to " + receiver,
                amount
            )

            self.record_transaction(
                receiver,
                "Transfer from " + sender,
                amount
            )

        self.check_fraud(sender, amount)

        return "Transfer successful"

    def check_daily_limit(self, account_id, amount):
        today_total = 0

        for transaction in self.transaction_history[account_id]:
            if transaction["date"].date() == datetime.now().date():
                today_total += transaction["amount"]

        return today_total + amount <= self.daily_limit

    def record_transaction(self, account_id, transaction_type, amount):
        transaction = {
            "type": transaction_type,
            "amount": amount,
            "date": datetime.now()
        }

        self.transaction_history[account_id].append(transaction)

        self.transaction_times[account_id].append(datetime.now())

        self.transaction_times[account_id] = [
            t for t in self.transaction_times[account_id]
            if datetime.now() - t <= timedelta(minutes=10)
        ]

    def check_fraud(self, account_id, amount):
        suspicious = []

        # More than 5 transactions in 10 minutes
        if len(self.transaction_times[account_id]) > 5:
            suspicious.append("More than 5 transactions in 10 minutes")

        # Large transaction
        if amount > 25000:
            suspicious.append("Large transaction")

        # Multiple failed PIN attempts
        if self.failed_pins[account_id] >= 3:
            suspicious.append("Multiple failed PIN attempts")

        # Unusual transaction amount
        if amount > 10000:
            suspicious.append("Unusual transaction amount")

        if suspicious:
            print("FRAUD ALERT:", account_id)
            for reason in suspicious:
                print("-", reason)

        return suspicious

    def get_balance(self, account_id):
        if account_id not in self.accounts:
            return None

        return self.accounts[account_id]["balance"]

    def get_transaction_history(self, account_id):
        if account_id not in self.accounts:
            return []

        return self.transaction_history[account_id]


if __name__ == "__main__":

    wallet = DigitalWallet()

    print(wallet.create_account("A101", "Thamarai", "1234", 10000))
    print(wallet.create_account("A102", "Kumar", "5678", 5000))

    print(wallet.deposit("A101", 2000))

    print(wallet.withdrawal("A101", 1000, "1234"))

    print(wallet.transfer("A101", "A102", 2000, "1234"))

    print("Balance:", wallet.get_balance("A101"))

    print("\nTransaction History:")

    for transaction in wallet.get_transaction_history("A101"):
        print(transaction)
