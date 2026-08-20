import sys

passed = 0
failed = 0


# ==========================================
# INSURANCE CLAIM FUNCTIONS
# ==========================================

def check_policy(policy):
    if policy == "":
        return False

    if len(policy) < 4:
        return False

    return True


def check_eligibility(policy, start_date, incident_date,
                      claim_amount, coverage):

    if not check_policy(policy):
        return False

    if incident_date < start_date:
        return False

    if claim_amount < 0:
        return False

    if claim_amount > coverage:
        return False

    return True


def calculate_payout(claim_amount, coverage):

    if claim_amount > coverage:
        amount = coverage
    else:
        amount = claim_amount

    deductible = amount * 0.10

    return amount - deductible


def fraud_score(claim_amount, coverage,
                previous_claims,
                missing_documents,
                early_incident):

    score = 0

    if previous_claims >= 4:
        score = score + 40

    elif previous_claims >= 3:
        score = score + 30

    elif previous_claims >= 2:
        score = score + 20

    if claim_amount >= coverage * 0.90:
        score = score + 30

    if missing_documents:
        score = score + 25

    if early_incident:
        score = score + 25

    return score


def claim_status(eligible, score, missing_documents):

    if not eligible:
        return "REJECTED"

    if score >= 70:
        return "FRAUD SUSPECTED"

    if score >= 40 or missing_documents:
        return "MANUAL REVIEW"

    return "APPROVED"


# ==========================================
# TEST FUNCTION
# ==========================================

def test(name, condition):

    global passed
    global failed

    if condition:
        print("PASS - " + name)
        passed = passed + 1

    else:
        print("FAIL - " + name)
        failed = failed + 1


# ==========================================
# TEST 1
# VALID CLAIM
# ==========================================

def test_valid_claim():

    eligible = check_eligibility(
        "POL1001",
        1,
        20,
        50000,
        100000
    )

    payout = calculate_payout(
        50000,
        100000
    )

    score = fraud_score(
        50000,
        100000,
        0,
        False,
        False
    )

    status = claim_status(
        eligible,
        score,
        False
    )

    test(
        "Valid Claim",
        eligible
        and payout == 45000
        and status == "APPROVED"
    )


# ==========================================
# TEST 2
# EXPIRED POLICY
# ==========================================

def test_expired_policy():

    result = check_eligibility(
        "POL1002",
        1,
        500,
        30000,
        100000
    )

    test(
        "Expired Policy",
        result == False
    )


# ==========================================
# TEST 3
# CLAIM BEFORE POLICY START
# ==========================================

def test_before_policy():

    result = check_eligibility(
        "POL1003",
        100,
        50,
        30000,
        100000
    )

    test(
        "Claim Before Policy Start",
        result == False
    )


# ==========================================
# TEST 4
# EXCESSIVE CLAIM
# ==========================================

def test_excessive_claim():

    result = check_eligibility(
        "POL1004",
        1,
        20,
        150000,
        100000
    )

    test(
        "Excessive Claim Amount",
        result == False
    )


# ==========================================
# TEST 5
# MISSING DOCUMENTS
# ==========================================

def test_missing_documents():

    eligible = check_eligibility(
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
        True,
        False
    )

    status = claim_status(
        eligible,
        score,
        True
    )

    test(
        "Missing Documents",
        eligible
        and score >= 25
        and status == "MANUAL REVIEW"
    )


# ==========================================
# TEST 6
# MULTIPLE PREVIOUS CLAIMS
# ==========================================

def test_previous_claims():

    eligible = check_eligibility(
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
        False,
        False
    )

    status = claim_status(
        eligible,
        score,
        False
    )

    test(
        "Multiple Previous Claims",
        eligible
        and score >= 40
        and status == "MANUAL REVIEW"
    )


# ==========================================
# TEST 7
# FRAUD SCENARIO
# ==========================================

def test_fraud():

    eligible = check_eligibility(
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
        True,
        True
    )

    status = claim_status(
        eligible,
        score,
        True
    )

    test(
        "Fraud Scenario",
        eligible
        and score >= 70
        and status == "FRAUD SUSPECTED"
    )


# ==========================================
# TEST 8
# BOUNDARY CLAIM
# ==========================================

def test_boundary():

    eligible = check_eligibility(
        "POL1008",
        1,
        20,
        100000,
        100000
    )

    payout = calculate_payout(
        100000,
        100000
    )

    test(
        "Boundary Claim Amount",
        eligible
        and payout == 90000
    )


# ==========================================
# TEST 9
# INVALID POLICY
# ==========================================

def test_invalid_policy():

    result = check_eligibility(
        "",
        1,
        20,
        30000,
        100000
    )

    test(
        "Invalid Policy Number",
        result == False
    )


# ==========================================
# TEST 10
# INVALID INCIDENT DATE
# ==========================================

def test_invalid_date():

    result = check_eligibility(
        "POL1010",
        100,
        50,
        30000,
        100000
    )

    test(
        "Invalid Incident Date",
        result == False
    )


# ==========================================
# MAIN
# ==========================================

print()
print("======================================")
print("   INSURANCE CLAIM QA TEST")
print("======================================")
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
print("======================================")
print("Tests Passed :", passed)
print("Tests Failed :", failed)
print("======================================")

if failed == 0:
    print("ALL TESTS PASSED")
    sys.exit(0)
else:
    print("SOME TESTS FAILED")
    sys.exit(1)
