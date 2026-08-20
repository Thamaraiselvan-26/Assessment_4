from DigitalWallet import DigitalWallet
import threading


def test_account_creation():

    wallet = DigitalWallet()

    result = wallet.create_account(
        "A101",
        "Thamarai",
        "1234",
        10000
    )

    assert result == "Account created successfully"

    print("PASS - Account Creation")


def test_normal_transaction():

    wallet = DigitalWallet()

    wallet.create_account(
        "A101",
        "Thamarai",
        "1234",
        10000
    )

    result = wallet.deposit("A101", 2000)

    assert result == "Deposit successful"
    assert wallet.get_balance("A101") == 12000

    print("PASS - Normal Transaction")


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

    assert result == "Insufficient balance"

    print("PASS - Insufficient Balance")


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

    assert result == "Daily transaction limit exceeded"

    print("PASS - Daily Limit")


def test_multiple_failed_pins():

    wallet = DigitalWallet()

    wallet.create_account(
        "A101",
        "Thamarai",
        "1234",
        10000
    )

    wallet.withdraw("A101", 100, "1111")
    wallet.withdraw("A101", 100, "2222")
    result = wallet.withdraw("A101", 100, "3333")

    assert result == \
        "Account blocked due to multiple failed PIN attempts"

    print("PASS - Multiple Failed PINs")


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

    assert "Large transaction" in fraud

    print("PASS - Suspicious Transaction")


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

    history = wallet.transaction_history("A101")

    assert len(history) == 2

    print("PASS - Duplicate Transaction")


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

    assert result == "Invalid amount"

    print("PASS - Negative Amount")


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

    assert wallet.get_balance("A101") == 10500

    print("PASS - Concurrent Transactions")


if __name__ == "__main__":

    print("DIGITAL WALLET QA TEST")
    print("======================")

    test_account_creation()
    test_normal_transaction()
    test_insufficient_balance()
    test_daily_limit()
    test_multiple_failed_pins()
    test_suspicious_transaction()
    test_duplicate_transaction()
    test_negative_amount()
    test_concurrent_transactions()

    print("======================")
    print("ALL TESTS PASSED")
