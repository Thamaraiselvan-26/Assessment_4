import time

class DigitalWallet:
    def __init__(self, account_id: str, pin: str, balance: float = 0.0, daily_limit: float = 5000.0):
        self.account_id = account_id
        self.pin = pin
        self.balance = balance
        self.daily_limit = daily_limit
        
        self.transactions = []        
        self.failed_pin_attempts = 0  
        self.daily_spent = 0.0        
        self.is_locked = False

    def verify_balance(self) -> float:
        return self.balance

    def check_fraud(self, amount: float) -> bool:
        current_time = time.time()
        
        # Rule 1: More than 5 transactions in 10 minutes
        recent_txs = [tx for tx in self.transactions if current_time - tx['time'] <= 600]
        if len(recent_txs) >= 5:
            print(f"[SECURITY ALERT] High frequency transaction flag: More than 5 transactions in 10 minutes.")
            return True
            
        # Rule 2: Large transaction anomaly
        if amount > (self.daily_limit * 0.9):
            print(f"[SECURITY ALERT] Large transaction flag: Amount exceeds 90% of daily limit.")
            return True
            
        # Rule 3: Unusual transaction amount
        if amount <= 0:
            print(f"[SECURITY ALERT] Unusual transaction amount flag: Non-positive value detected.")
            return True
            
        return False

    def deposit(self, amount: float) -> bool:
        if amount <= 0:
            print(f"[ERROR] Deposit Rejected: {amount} is an invalid amount.")
            return False
        self.balance += amount
        self.transactions.append({'type': 'deposit', 'amount': amount, 'time': time.time()})
        print(f"[SUCCESS] Deposited: {amount:,.2f} | Current Balance: {self.balance:,.2f}")
        return True

    def withdraw(self, amount: float, entered_pin: str) -> bool:
        if self.is_locked:
            print(f"[ERROR] Transaction Blocked: Account {self.account_id} is locked due to multiple failed PIN attempts.")
            return False

        if entered_pin != self.pin:
            self.failed_pin_attempts += 1
            print(f"[ERROR] Incorrect PIN entered.")
            if self.failed_pin_attempts >= 3:
                self.is_locked = True
                print(f"[SECURITY ALERT] Multiple failed PIN attempts: Account {self.account_id} is now LOCKED.")
            return False

        self.failed_pin_attempts = 0  

        if amount > self.balance:
            print(f"[ERROR] Transaction Declined: Insufficient balance. (Attempted: {amount:,.2f}, Available: {self.balance:,.2f})")
            return False

        if self.daily_spent + amount > self.daily_limit:
            print(f"[ERROR] Transaction Declined: Exceeds daily limit constraint.")
            return False

        if self.check_fraud(amount):
            print(f"[ERROR] Transaction Suspended: Flagged as highly suspicious.")
            return False

        self.balance -= amount
        self.daily_spent += amount
        self.transactions.append({'type': 'withdrawal', 'amount': amount, 'time': time.time()})
        print(f"[SUCCESS] Withdrew: {amount:,.2f} | Current Balance: {self.balance:,.2f}")
        return True

    def transfer(self, target_wallet, amount: float, entered_pin: str) -> bool:
        print(f"[PROCESSING] Attempting transfer of {amount:,.2f} from Account '{self.account_id}' to Account '{target_wallet.account_id}'...")
        if self.withdraw(amount, entered_pin):
            target_wallet.balance += amount
            target_wallet.transactions.append({'type': f'Received from {self.account_id}', 'amount': amount, 'time': time.time()})
            print(f"[SUCCESS] Transfer Successful!")
            return True
            
        print(f"[ERROR] Transfer Failed.")
        return False

    def display_history(self):
        print(f"\n==========================================")
        print(f"REPORT: TRANSACTION HISTORY FOR ACC: {self.account_id}")
        print(f"==========================================")
        if not self.transactions:
            print("No recorded transaction history logs.")
        for idx, tx in enumerate(self.transactions, start=1):
            print(f" [{idx}] Action: {tx['type'].capitalize()} | Amount: {tx['amount']:,.2f}")
        print(f"==========================================\n")


if __name__ == "__main__":
    print("=========================================================")
    print("        STARTING AUTOMATED TESTING WITH SYSTEM VALUES    ")
    print("=========================================================\n")

    print("--- SCENARIO: ACCOUNT CREATION AND BALANCES ---")
    my_wallet = DigitalWallet(account_id="User-Primary-99", pin="4321", balance=1500.0, daily_limit=2000.0)
    friend_wallet = DigitalWallet(account_id="User-Friend-22", pin="8888", balance=100.0)
    print(f"Primary Account Created. Initial Balance: {my_wallet.verify_balance():,.2f}")
    
    my_wallet.deposit(500.0)

    print("\n--- SCENARIO: NORMAL WITHDRAWAL ---")
    my_wallet.withdraw(200.0, "4321")

    print("\n--- SCENARIO: MONEY TRANSFER ---")
    my_wallet.transfer(friend_wallet, 300.0, "4321")

    print("\n--- SCENARIO: INSUFFICIENT BALANCE ERROR ---")
    my_wallet.withdraw(5000.0, "4321")

    print("\n--- SCENARIO: SECURITY THREAT FRAUD DETECTION ---")
    my_wallet.withdraw(10.0, "1111")  
    my_wallet.withdraw(10.0, "2222")  
    my_wallet.withdraw(10.0, "5555")  
    my_wallet.withdraw(10.0, "4321")  

    print("\n--- SCENARIO: UNUSUAL QUANTITY DETECTOR ---")
    unlocked_wallet = DigitalWallet(account_id="User-Secure-01", pin="1234", balance=1000.0)
    unlocked_wallet.withdraw(-50.0, "1234")

    print("\n--- SCENARIO: ANOMALOUS LARGE TRANSACTION DETECTOR ---")
    unlocked_wallet.withdraw(1900.0, "1234")

    print("\n--- SCENARIO: MICRO-TRANSACTION VELOCITY COUNTER ---")
    velocity_wallet = DigitalWallet(account_id="User-Velocity-Test", pin="0000", balance=1000.0)
    for i in range(5):
        velocity_wallet.withdraw(1.0, "0000")
    velocity_wallet.withdraw(1.0, "0000")

    velocity_wallet.display_history()
    
    print("=========================================================")
    print("        EXECUTION SCRIPT RUN COMPLETE                    ")
    print("=========================================================")
