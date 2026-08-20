import sys
from InsuranceClaim import InsuranceClaim


passed = 0
failed = 0


def check_test(name, condition):
    global passed, failed

    if condition:
        print("PASS - " + name)
        passed += 1
    else:
        print("FAIL - " + name)
        failed += 1


# ==================================================
# 1. VALID CLAIM
# ==================================================

def test_valid_claim():

    system = InsuranceClaim()

    result = system.process_claim(
        "POL1001",
        "C001",
        "Health",
        50000,
        1,
        20,
        0,
        35,
        "Accident",
        True,
        100000
    )

    check_test(
        "Valid Claim",
        result["eligible"] is True
        and result["status"] == "APPROVED"
        and result["insurance_payout"] == 45000
    )


# ==================================================
# 2. EXPIRED POLICY
# ==================================================

def test_expired_policy():

    system = InsuranceClaim()

    result = system.check_eligibility(
        "POL1002",
        1,
        500,
        30000,
        100000
    )

    check_test(
        "Expired Policy",
        result is False
    )


# ==================================================
# 3. CLAIM BEFORE POLICY START
# ==================================================

def test_claim_before_policy_start():

    system = InsuranceClaim()

    result = system.check_eligibility(
        "POL1003",
        100,
        50,
        30000,
        100000
    )

    check_test(
        "Claim Before Policy Start",
        result is False
    )


# ==================================================
# 4. EXCESSIVE CLAIM AMOUNT
# ==================================================

def test_excessive_claim():

    system = InsuranceClaim()

    result = system.check_eligibility(
        "POL1004",
        1,
        20,
        150000,
        100000
    )

    check_test(
        "Excessive Claim Amount",
        result is False
    )


# ==================================================
# 5. MISSING DOCUMENTS
# ==================================================

def test_missing_documents():

    system = InsuranceClaim()

    result = system.process_claim(
        "POL1005",
        "C005",
        "Health",
        30000,
        1,
        100,
        0,
        40,
        "Accident",
        False,
        100000
    )

    check_test(
        "Missing Documents",
        result["eligible"] is True
        and result["status"] == "MANUAL REVIEW"
        and result["fraud_score"] >= 25
    )


# ==================================================
# 6. MULTIPLE PREVIOUS CLAIMS
# ==================================================

def test_multiple_previous_claims():

    system = InsuranceClaim()

    result = system.process_claim(
        "POL1006",
        "C006",
        "Health",
        30000,
        1,
        100,
        4,
        40,
        "Accident",
        True,
        100000
    )

    check_test(
        "Multiple Previous Claims",
        result["eligible"] is True
        and result["fraud_score"] >= 40
        and result["status"] == "MANUAL REVIEW"
    )


# ==================================================
# 7. FRAUD SCENARIO
# ==================================================

def test_fraud_scenario():

    system = InsuranceClaim()

    result = system.process_claim(
        "POL1007",
        "C007",
        "Health",
        95000,
        1,
        5,
        4,
        40,
        "Accident",
        False,
        100000
    )

    check_test(
        "Fraud Scenario",
        result["eligible"] is True
        and result["fraud_score"] >= 70
        and result["status"] == "FRAUD SUSPECTED"
    )


# ==================================================
# 8. BOUNDARY CLAIM AMOUNT
# ==================================================

def test_boundary_claim_amount():

    system = InsuranceClaim()

    result = system.process_claim(
        "POL1008",
        "C008",
        "Health",
        100000,
        1,
        20,
        0,
        35,
        "Accident",
        True,
        100000
    )

    check_test(
        "Boundary Claim Amount",
        result["eligible"] is True
        and result["maximum_payable"] == 100000
        and result["insurance_payout"] == 90000
    )


# ==================================================
# 9. INVALID POLICY NUMBER
# ==================================================

def test_invalid_policy_number():

    system = InsuranceClaim()

    result = system.check_eligibility(
        "",
        1,
        20,
        30000,
        100000
    )

    check_test(
        "Invalid Policy Number",
        result is False
    )


# ==================================================
# 10. INVALID INCIDENT DATE
# ==================================================

def test_invalid_incident_date():

    system = InsuranceClaim()

    result = system.check_eligibility(
        "POL1010",
        100,
        50,
        30000,
        100000
    )

    check_test(
        "Invalid Incident Date",
        result is False
    )


# ==================================================
# MAIN
# ==================================================

if __name__ == "__main__":

    print()
    print("==============================================")
    print("     INSURANCE CLAIM PROCESSING QA")
    print("==============================================")
    print()

    test_valid_claim()
    test_expired_policy()
    test_claim_before_policy_start()
    test_excessive_claim()
    test_missing_documents()
    test_multiple_previous_claims()
    test_fraud_scenario()
    test_boundary_claim_amount()
    test_invalid_policy_number()
    test_invalid_incident_date()

    print()
    print("==============================================")
    print("Tests Passed :", passed)
    print("Tests Failed :", failed)
    print("==============================================")

    if failed == 0:
        print("ALL TESTS PASSED")
        sys.exit(0)
    else:
        print("SOME TESTS FAILED")
        sys.exit(1)
