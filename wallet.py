from DigitalWallet import DigitalWallet
import threading
import sys


passed = 0
failed = 0


def test(name, condition):

    global passed, failed

    if condition:
        print("PASS:", name)
        passed += 1
    else:
        print("FAIL:", name)
        failed += 1


# =========================================
# 1. Normal Transaction
# =========================================

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

    test(
        "Normal transaction",
        result is True
        and wallet.get_balance("A101") == 12000
    )


# =========================================
# 2. Insufficient Balance
# =========================================

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

    test(
        "Insufficient balance",
        result is False
        and wallet.get_balance("A101") == 1000
    )


# =========================================
# 3. Daily Transaction Limit
# =========================================

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

    test(
        "Daily transaction limit",
        result is False
    )


# =========================================
# 4. Multiple Failed PIN Attempts
# =========================================

def test_multiple_failed_pins():

    wallet = DigitalWallet()

    wallet.create_account(
        "A101",
        "Thamarai",
        "1234",
        10000
    )

    wallet.withdraw(
        "A101",
        100,
        "1111"
    )

    wallet.withdraw(
        "A101",
        100,
        "2222"
    )

    wallet.withdraw(
        "A101",
        100,
        "3333"
    )

    test(
        "Multiple failed PIN attempts",
        wallet.failed_pins["A101"] >= 3
    )


# =========================================
# 5. Suspicious Transaction
# =========================================

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

    test(
        "Suspicious transaction",
        "Large transaction" in fraud
    )


# =========================================
# 6. Duplicate Transaction
# =========================================

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

    test(
        "Duplicate transaction",
        len(history) == 2
    )


# =========================================
# 7. Negative Amount
# =========================================

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

    test(
        "Negative amount",
        result is False
    )


# =========================================
# 8. Concurrent Transactions
# =========================================

def deposit_money(wallet):

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
            target=deposit_money,
            args=(wallet,)
        )

        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    test(
        "Concurrent transactions",
        wallet.get_balance("A101") == 10500
    )


# =========================================
# 9. Account Creation
# =========================================

def test_account_creation():

    wallet = DigitalWallet()

    result = wallet.create_account(
        "A101",
        "Thamarai",
        "1234",
        10000
    )

    test(
        "Account creation",
        result is True
    )


# =========================================
# Main QA Execution
# =========================================

if __name__ == "__main__":

    print("======================================")
    print("DIGITAL WALLET SECURITY QA")
    print("======================================")

    test_account_creation()
    test_normal_transaction()
    test_insufficient_balance()
    test_daily_limit()
    test_multiple_failed_pins()
    test_suspicious_transaction()
    test_duplicate_transaction()
    test_negative_amount()
    test_concurrent_transactions()

    print("======================================")
    print("Tests Passed:", passed)
    print("Tests Failed:", failed)
    print("======================================")

    if failed == 0:
        print("ALL TESTS PASSED")
        sys.exit(0)
    else:
        print("TESTS FAILED")
        sys.exit(1)
