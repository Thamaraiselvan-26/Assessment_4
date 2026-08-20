import time

class DigitalWallet:
    def __init__(self, account_id: str, pin: str, balance: float = 0.0, daily_limit: float = 5000.0):
        self.account_id = account_id
        self.pin = pin
        self.balance = balance
        self.daily_limit = daily_limit
        self.transactions = []
        self.failed_pin_attempts = 0
        
        # Track daily limits using the current calendar date string
        self.daily_spent_tracking = {}  # Format: { "YYYY-MM-DD": amount }
        self.is_locked = False

    def _get_current_date(self) -> str:
        """Helper to get the current date for resetting daily limits."""
        return time.strftime("%Y-%m-%d", time.localtime())

    def _get_daily_spent(self) -> float:
        """Retrieves amount spent today, auto-handling daily rollovers."""
        return self.daily_spent_tracking.get(self._get_current_date(), 0.0)

    def _add_daily_spent(self, amount: float):
        """Accumulates spent values tied to today's date context."""
        today = self._get_current_date()
        self.daily_spent_tracking[today] = self._get_daily_spent() + amount

    def verify_balance(self) -> float:
        return self.balance

    def check_fraud(self, amount: float) -> bool:
        current_time = time.time()
        
        # Rule 1: Clean expired transactions (>10 mins) to prevent memory leaks, then verify frequency
        self.transactions = [tx for tx in self.transactions if current_time - tx['time'] <= 600]
        
        if len(self.transactions) >= 5:
            print(f"[SECURITY ALERT] High frequency transaction flag: More than 5 transactions in 10 minutes.")
            return True
            
        # Rule 2: Large transaction anomaly
        if amount > (self.daily_limit * 0.9):
            print(f"[SECURITY ALERT] Large transaction flag: Amount exceeds 90% of daily limit.")
            return True
            
        return False

    def deposit(self, amount: float, tracking_type: str = 'deposit') -> bool:
        if amount <= 0:
            print(f"[ERROR] Deposit Rejected: {amount} is an invalid amount.")
            return False

        self.balance += amount
        self.transactions.append({'type': tracking_type, 'amount': amount, 'time': time.time()})
        print(f"[SUCCESS] Deposited: {amount:,.2f} | Current Balance: {self.balance:,.2f}")
        return True

    def withdraw(self, amount: float, entered_pin: str) -> bool:
        if self.is_locked:
            print(f"[ERROR] Transaction Blocked: Account {self.account_id} is locked.")
            return False

        if amount <= 0:
            print(f"[ERROR] Transaction Declined: Non-positive input values are invalid.")
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
            print(f"[ERROR] Transaction Declined: Insufficient balance.")
            return False

        if self._get_daily_spent() + amount > self.daily_limit:
            print(f"[ERROR] Transaction Declined: Exceeds daily limit constraint.")
            return False

        if self.check_fraud(amount):
            print(f"[ERROR] Transaction Suspended: Flagged as highly suspicious.")
            return False

        self.balance -= amount
        self._add_daily_spent(amount)
        self.transactions.append({'type': 'withdrawal', 'amount': amount, 'time': time.time()})
        print(f"[SUCCESS] Withdrew: {amount:,.2f} | Current Balance: {self.balance:,.2f}")
        return True

    def transfer(self, target_wallet, amount: float, entered_pin: str) -> bool:
        print(f"[PROCESSING] Attempting transfer of {amount:,.2f} from '{self.account_id}' to '{target_wallet.account_id}'...")
        
        # Withdraw from source first
        if self.withdraw(amount, entered_pin):
            # Deposit safely using encapsulation rules into target instance
            target_wallet.deposit(amount, tracking_type=f'Received from {self.account_id}')
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


# =========================================================
# SYSTEM TEST EXECUTION BLOCK
# =========================================================
if __name__ == "__main__":
    print("=========================================================")
    print("         STARTING AUTOMATED SYSTEM VALIDATION           ")
    print("=========================================================\n")

    print("--- SCENARIO 1: ACCOUNT CREATION AND DEPOSITS ---")
    my_wallet = DigitalWallet(account_id="User-Primary-99", pin="4321", balance=1500.0, daily_limit=2000.0)
    friend_wallet = DigitalWallet(account_id="User-Friend-22", pin="8888", balance=100.0)
    my_wallet.deposit(500.0)

    print("\n--- SCENARIO 2: NORMAL WITHDRAWAL ---")
    my_wallet.withdraw(200.0, "4321")

    print("\n--- SCENARIO 3: SAFE ENCAPSULATED TRANSFER ---")
    my_wallet.transfer(friend_wallet, 300.0, "4321")

    print("\n--- SCENARIO 4: CORRECTED INVALID NEGATIVE ENTRY ---")
    my_wallet.withdraw(-50.0, "4321")

    print("\n--- SCENARIO 5: SECURITY BLOCKS - LOCKOUT TRIPPING ---")
    my_wallet.withdraw(10.0, "1111")
    my_wallet.withdraw(10.0, "2222")
    my_wallet.withdraw(10.0, "5555")  # 3rd failure locks it
    my_wallet.withdraw(10.0, "4321")  # Valid pin now fails because account is locked

    print("\n--- SCENARIO 6: RECIPIENT WALLET VALIDATION ---")
    friend_wallet.display_history()

    print("=========================================================")
    print("               EXECUTION SCRIPT COMPLETE                 ")
    print("=========================================================")
