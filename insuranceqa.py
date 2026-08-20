import sys

passed = 0
failed = 0


# ==========================================
# INSURANCE CLAIM FUNCTIONS
# ==========================================

def valid_policy(policy):
    return policy != "" and len(policy) >= 4


def eligible(policy, start, incident, amount, coverage):

    if not valid_policy(policy):
        return False

    if incident < start:
        return False

    # Policy validity = 365 days
    if incident > start + 365:
        return False

    if amount < 0:
        return False

    if amount > coverage:
        return False

    return True


def payout(amount, coverage):

    if amount > coverage:
        amount = coverage

    return amount * 0.90


def fraud_score(amount, coverage, previous, documents, early):

    score = 0

    if previous >= 4:
        score += 40
    elif previous >= 3:
        score += 30
    elif previous >= 2:
        score += 20

    if amount >= coverage * 0.90:
        score += 30

    if documents == False:
        score += 25

    if early:
        score += 25

    return score


def status(is_eligible, score, documents):

    if not is_eligible:
        return "REJECTED"

    if score >= 70:
        return "FRAUD SUSPECTED"

    if score >= 40 or documents == False:
        return "MANUAL REVIEW"

    return "APPROVED"


# ==========================================
# TEST FUNCTION
# ==========================================

def check(name, result):

    global passed
    global failed

    if result:
        print("PASS - " + name)
        passed += 1
    else:
        print("FAIL - " + name)
        failed += 1


# ==========================================
# 1. VALID CLAIM
# ==========================================

def test_valid_claim():

    ok = eligible(
        "POL1001",
        1,
        20,
        50000,
        100000
    )

    amount = payout(
        50000,
        100000
    )

    score = fraud_score(
        50000,
        100000,
        0,
        True,
        False
    )

    result = status(
        ok,
        score,
        True
    )

    check(
        "Valid Claim",
        ok
        and amount == 45000
        and result == "APPROVED"
    )


# ==========================================
# 2. EXPIRED POLICY
# ==========================================

def test_expired_policy():

    result = eligible(
        "POL1002",
        1,
        400,
        30000,
        100000
    )

    check(
        "Expired Policy",
        result == False
    )


# ==========================================
# 3. CLAIM BEFORE POLICY START
# ==========================================

def test_before_policy():

    result = eligible(
        "POL1003",
        100,
        50,
        30000,
        100000
    )

    check(
        "Claim Before Policy Start",
        result == False
    )


# ==========================================
# 4. EXCESSIVE CLAIM
# ==========================================

def test_excessive_claim():

    result = eligible(
        "POL1004",
        1,
        20,
        150000,
        100000
    )

    check(
        "Excessive Claim Amount",
        result == False
    )


# ==========================================
# 5. MISSING DOCUMENTS
# ==========================================

def test_missing_documents():

    ok = eligible(
        "POL1005",
        1,
        100,
        30000,
        100000
    )

    score = fraud_score(
        30000,
        100000,
        0,
        False,
        False
    )

    result = status(
        ok,
        score,
        False
    )

    check(
        "Missing Documents",
        ok
        and score >= 25
        and result == "MANUAL REVIEW"
    )


# ==========================================
# 6. MULTIPLE PREVIOUS CLAIMS
# ==========================================

def test_previous_claims():

    ok = eligible(
        "POL1006",
        1,
        100,
        30000,
        100000
    )

    score = fraud_score(
        30000,
        100000,
        4,
        True,
        False
    )

    result = status(
        ok,
        score,
        True
    )

    check(
        "Multiple Previous Claims",
        ok
        and score >= 40
        and result == "MANUAL REVIEW"
    )


# ==========================================
# 7. FRAUD SCENARIO
# ==========================================

def test_fraud():

    ok = eligible(
        "POL1007",
        1,
        5,
        95000,
        100000
    )

    score = fraud_score(
        95000,
        100000,
        4,
        False,
        True
    )

    result = status(
        ok,
        score,
        False
    )

    check(
        "Fraud Scenario",
        ok
        and score >= 70
        and result == "FRAUD SUSPECTED"
    )


# ==========================================
# 8. BOUNDARY CLAIM AMOUNT
# ==========================================

def test_boundary():

    ok = eligible(
        "POL1008",
        1,
        20,
        100000,
        100000
    )

    amount = payout(
        100000,
        100000
    )

    check(
        "Boundary Claim Amount",
        ok
        and amount == 90000
    )


# ==========================================
# 9. INVALID POLICY NUMBER
# ==========================================

def test_invalid_policy():

    result = eligible(
        "",
        1,
        20,
        30000,
        100000
    )

    check(
        "Invalid Policy Number",
        result == False
    )


# ==========================================
# 10. INVALID INCIDENT DATE
# ==========================================

def test_invalid_date():

    result = eligible(
        "POL1010",
        100,
        50,
        30000,
        100000
    )

    check(
        "Invalid Incident Date",
        result == False
    )


# ==========================================
# RUN ALL TESTS
# ==========================================

print()
print("==========================================")
print("     INSURANCE CLAIM QA TEST")
print("==========================================")
print()

test_valid_claim()
test_expired_policy()
test_before_policy()
test_excessive_claim()
test_missing_documents()
test_previous_claims()
test_fraud()
test_boundary()
test_invalid_policy()
test_invalid_date()

print()
print("==========================================")
print("Tests Passed :", passed)
print("Tests Failed :", failed)
print("==========================================")

if failed == 0:
    print("ALL TESTS PASSED")
    sys.exit(0)
else:
    print("SOME TESTS FAILED")
    sys.exit(1)
