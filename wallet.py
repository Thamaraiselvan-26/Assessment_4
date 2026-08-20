from DigitalWallet import DigitalWallet
import threading


wallet = DigitalWallet()


def test_account_creation():
    result = wallet.create_account(
        "A101",
        "Thamarai",
        "1234",
        10000
    )

    assert result == "Account created successfully"
    print("PASS: Account creation")


def test_normal_transaction():
    result = wallet.deposit("A101", 1000)

    assert result == "Deposit successful"
    print("PASS: Normal transaction")


def test_insufficient_balance():
    result = wallet.withdrawal(
        "A101",
        50000,
        "1234"
    )

    assert result == "Insufficient balance"
    print("PASS: Insufficient balance")


def test_daily_limit():
    result = wallet.withdrawal(
        "A101",
        50000,
        "1234"
    )

    assert result == "Daily transaction limit exceeded"
    print("PASS: Daily limit")


def test_multiple_failed_pins():

    wallet.verify_pin("A101", "1111")
    wallet.verify_pin("A101", "2222")
    wallet.verify_pin("A101", "3333")

    assert wallet.failed_pins["A101"] == 3
    print("PASS: Multiple failed PINs")


def test_suspicious_transaction():

    fraud = wallet.check_fraud(
        "A101",
        30000
    )

    assert "Large transaction" in fraud
    print("PASS: Suspicious transaction")


def test_duplicate_transaction():

    history_before = len(
        wallet.get_transaction_history("A101")
    )

    wallet.deposit("A101", 100)

    wallet.deposit("A101", 100)

    history_after = len(
        wallet.get_transaction_history("A101")
    )

    assert history_after == history_before + 2

    print("PASS: Duplicate transaction test")


def test_negative_amount():

    result = wallet.deposit("A101", -500)

    assert result == "Invalid amount"

    print("PASS: Negative amount")


def concurrent_deposit():

    wallet.deposit("A101", 100)


def test_concurrent_transactions():

    threads = []

    for i in range(5):
        thread = threading.Thread(
            target=concurrent_deposit
        )
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print("PASS: Concurrent transactions")


if __name__ == "__main__":

    test_account_creation()
    test_normal_transaction()
    test_insufficient_balance()
    test_daily_limit()
    test_multiple_failed_pins()
    test_suspicious_transaction()
    test_duplicate_transaction()
    test_negative_amount()
    test_concurrent_transactions()

    print("\nAll tests completed.")
