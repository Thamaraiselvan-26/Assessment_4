import time

class DigitalWallet:
    def __init__(self, account_id: str, pin: str, balance: float = 0.0, daily_limit: float = 5000.0):
        self.account_id = account_id
        self.pin = pin
        self.balance = balance
        self.daily_limit = daily_limit
        
        self.transactions = []        # History tracking list
        self.failed_pin_attempts = 0  # Counter for invalid pins
        self.daily_spent = 0.0        # Tracks accumulation against threshold
        self.is_locked = False

    def verify_balance(self) -> float:
        return self.balance

    def check_fraud(self, amount: float) -> bool:
        current_time = time.time()
        
        # Rule 1: High frequency velocity check (More than 5 transactions in 10 minutes)
        recent_txs = [tx for tx in self.transactions if current_time - tx['time'] <= 600]
        if len(recent_txs) >= 5:
            print(f"\n🚨 [FRAUD ALERT] High velocity detected! More than 5 transactions in 10 minutes.")
            return True
            
        # Rule 2: Large transaction anomaly detection (>90% of overall daily limit)
        if amount > (self.daily_limit * 0.9):
            print(f"\n🚨 [FRAUD ALERT] Large transaction flagged! Amount exceeds 90% of daily limit.")
            return True
            
        # Rule 3: Unusual or impossible financial quantities
        if amount <= 0:
            print(f"\n🚨 [FRAUD ALERT] Unusual or invalid transaction amount.")
            return True
            
        return False

    def deposit(self, amount: float) -> bool:
        if amount <= 0:
            print("\n❌ Transaction Failed: Deposit amount must be positive.")
            return False
        self.balance += amount
        self.transactions.append({'type': 'deposit', 'amount': amount, 'time': time.time()})
        print(f"\n✅ Successfully deposited ${amount:,.2f}")
        return True

    def verify_pin_attempt(self, entered_pin: str) -> bool:
        if self.is_locked:
            print("\n🔒 Account Frozen: Access locked due to multiple failed PIN attempts.")
            return False

        if entered_pin != self.pin:
            self.failed_pin_attempts += 1
            if self.failed_pin_attempts >= 3:
                self.is_locked = True
                print("\n🚨 [FRAUD ALERT] Multiple failed PIN attempts! Account has been permanently locked.")
            else:
                print(f"\n❌ Incorrect PIN. ({3 - self.failed_pin_attempts} attempts remaining)")
            return False

        self.failed_pin_attempts = 0  # Reset counter on valid authorization
        return True

    def withdraw(self, amount: float, entered_pin: str) -> bool:
        if not self.verify_pin_attempt(entered_pin):
            return False

        if amount > self.balance:
            print("\n❌ Transaction Declined: Insufficient account balance.")
            return False

        if self.daily_spent + amount > self.daily_limit:
            print("\n❌ Transaction Declined: Operation exceeds remaining daily limit threshold.")
            return False

        if self.check_fraud(amount):
            print("❌ Transaction Blocked: Terminated by automated risk assessment subsystem.")
            return False

        # Apply transactions state change
        self.balance -= amount
        self.daily_spent += amount
        self.transactions.append({'type': 'withdrawal', 'amount': amount, 'time': time.time()})
        print(f"\n✅ Successfully withdrew ${amount:,.2f}")
        return True

    def transfer(self, target_wallet, amount: float, entered_pin: str) -> bool:
        # Check authorization and requirements first
        if not self.verify_pin_attempt(entered_pin):
            return False
            
        if amount > self.balance:
            print("\n❌ Transaction Declined: Insufficient account balance.")
            return False

        if self.daily_spent + amount > self.daily_limit:
            print("\n❌ Transaction Declined: Operation exceeds daily spending limit limits.")
            return False

        if self.check_fraud(amount):
            print("❌ Transaction Blocked: Terminated by automated risk assessment subsystem.")
            return False

        # Process systemic funds movement
        self.balance -= amount
        self.daily_spent += amount
        self.transactions.append({'type': f"Transfer to {target_wallet.account_id}", 'amount': amount, 'time': time.time()})
        
        # Credit targeted user structure
        target_wallet.balance += amount
        target_wallet.transactions.append({'type': f"Transfer from {self.account_id}", 'amount': amount, 'time': time.time()})
        print(f"\n✅ Successfully transferred ${amount:,.2f} to Account '{target_wallet.account_id}'")
        return True

    def display_history(self):
        print(f"\n=== TRANSACTION LEDGER FOR ACCOUNT: {self.account_id} ===")
        if not self.transactions:
            print("No transactions recorded yet.")
            return
        for index, item in enumerate(self.transactions, start=1):
            print(f" [{index}] Action: {item['type']} | Value: ${item['amount']:,.2f}")
        print(f"==================================================")


# ==========================================
# INTERACTIVE TERMINAL LOOP ENVIRONMENT
# ==========================================
def main():
    print("=== WELCOME TO THE DIGITAL WALLET SYSTEM ===")
    
    # 1. Interactive Account Setup Requirement
    acc_id = input("Create Account ID/Username: ").strip()
    while True:
        pin = input("Create a 4-Digit Security PIN: ").strip()
        if pin.isdigit() and len(pin) == 4:
            break
        print("Invalid input. PIN must be exactly 4 digits.")
        
    try:
        init_bal = float(input("Enter Initial Deposit Balance ($): ") or 0.0)
    except ValueError:
        init_bal = 0.0

    # Initialize User Object Session
    user_wallet = DigitalWallet(account_id=acc_id, pin=pin, balance=init_bal)
    print(f"\n✨ Account configuration successfully registered!")
    
    # Dummy mock system wallet for testing money transfers
    system_vendor_wallet = DigitalWallet(account_id="VendorStore_99", pin="0000", balance=5000.0)

    # Core Execution Loop
    while True:
        print(f"\n--- ACTIVE WALLET DASHBOARD ({user_wallet.account_id}) ---")
        print("1. Verify Account Balance")
        print("2. Make a Deposit")
        print("3. Perform a Withdrawal")
        print("4. Execute Money Transfer (Mock Target)")
        print("5. View Transaction Ledger History")
        print("6. Exit Session")
        
        choice = input("Select operation service entry (1-6): ").strip()
        
        if choice == '1':
            print(f"\n💳 Current Liquid Balance: ${user_wallet.verify_balance():,.2f}")
            print(f"📉 Spent Today: ${user_wallet.daily_spent:,.2f} / Max Limit: ${user_wallet.daily_limit:,.2f}")
            
        elif choice == '2':
            try:
                amt = float(input("Enter amount to deposit ($): "))
                user_wallet.deposit(amt)
            except ValueError:
                print("\n❌ Invalid numerical input matrix provided.")
                
        elif choice == '3':
            try:
                amt = float(input("Enter amount to withdraw ($): "))
                secure_pin = input("Verify 4-Digit PIN: ")
                user_wallet.withdraw(amt, secure_pin)
            except ValueError:
                print("\n❌ Invalid numerical input matrix provided.")
                
        elif choice == '4':
            print(f"\nℹ️ Directing payment transfer pathway to designated test wallet account: '{system_vendor_wallet.account_id}'")
            try:
                amt = float(input("Enter transfer amount value ($): "))
                secure_pin = input("Verify 4-Digit PIN to authorize transfer: ")
                user_wallet.transfer(system_vendor_wallet, amt, secure_pin)
            except ValueError:
                print("\n❌ Invalid numerical input matrix provided.")
                
        elif choice == '5':
            user_wallet.display_history()
            
        elif choice == '6':
            print("\n🔒 Session closed securely. Goodbye!")
            break
        else:
            print("\n❌ Unknown system command flag. Try again.")


if __name__ == "__main__":
    main()
