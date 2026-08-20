import sys


class InsuranceClaim:

    def __init__(self):
        self.claims = {}


    # ==========================================
    # VALIDATE POLICY NUMBER
    # ==========================================

    def valid_policy_number(self, policy_number):

        if policy_number == "":
            return False

        if len(policy_number) < 4:
            return False

        return True


    # ==========================================
    # CHECK CLAIM ELIGIBILITY
    # ==========================================

    def check_eligibility(
        self,
        policy_number,
        policy_start,
        incident_date,
        claim_amount,
        coverage
    ):

        # Invalid policy number
        if not self.valid_policy_number(policy_number):
            return False

        # Claim amount cannot be negative
        if claim_amount < 0:
            return False

        # Incident before policy start
        if incident_date < policy_start:
            return False

        # Claim cannot exceed coverage
        if claim_amount > coverage:
            return False

        return True


    # ==========================================
    # MAXIMUM PAYABLE AMOUNT
    # ==========================================

    def maximum_payable(
        self,
        claim_amount,
        coverage
    ):

        if claim_amount < 0:
            return 0

        if claim_amount > coverage:
            return coverage

        return claim_amount


    # ==========================================
    # DEDUCTIBLE
    # ==========================================

    def calculate_deductible(
        self,
        claim_amount
    ):

        deductible = claim_amount * 0.10

        return deductible


    # ==========================================
    # CUSTOMER CONTRIBUTION
    # ==========================================

    def customer_contribution(
        self,
        claim_amount
    ):

        return claim_amount * 0.10


    # ==========================================
    # INSURANCE PAYOUT
    # ==========================================

    def insurance_payout(
        self,
        claim_amount,
        coverage
    ):

        payable = self.maximum_payable(
            claim_amount,
            coverage
        )

        deductible = self.calculate_deductible(
            payable
        )

        payout = payable - deductible

        if payout < 0:
            payout = 0

        return payout


    # ==========================================
    # FRAUD RISK SCORE
    # ==========================================

    def fraud_risk_score(
        self,
        claim_amount,
        coverage,
        incident_after_activation,
        missing_documents,
        previous_claim_count
    ):

        score = 0

        # Multiple previous claims
        if previous_claim_count >= 3:
            score += 30

        elif previous_claim_count >= 2:
            score += 20


        # Claim significantly higher
        if claim_amount > coverage:
            score += 40

        elif claim_amount >= coverage * 0.90:
            score += 20


        # Incident immediately after activation
        if incident_after_activation:
            score += 25


        # Missing documents
        if missing_documents:
            score += 25


        return score


    # ==========================================
    # CLAIM CLASSIFICATION
    # ==========================================

    def classify_claim(
        self,
        eligible,
        fraud_score,
        missing_documents
    ):

        if not eligible:
            return "REJECTED"


        if fraud_score >= 70:
            return "FRAUD SUSPECTED"


        if fraud_score >= 40 or missing_documents:
            return "MANUAL REVIEW"


        return "APPROVED"


    # ==========================================
    # PROCESS CLAIM
    # ==========================================

    def process_claim(
        self,
        policy_number,
        customer_id,
        policy_type,
        claim_amount,
        policy_start,
        incident_date,
        previous_claim_count,
        customer_age,
        incident_type,
        documents_available,
        coverage
    ):

        eligible = self.check_eligibility(
            policy_number,
            policy_start,
            incident_date,
            claim_amount,
            coverage
        )


        missing_documents = not documents_available


        incident_after_activation = (
            incident_date - policy_start <= 7
        )


        payout = 0

        if eligible:

            payout = self.insurance_payout(
                claim_amount,
                coverage
            )


        fraud_score = self.fraud_risk_score(
            claim_amount,
            coverage,
            incident_after_activation,
            missing_documents,
            previous_claim_count
        )


        status = self.classify_claim(
            eligible,
            fraud_score,
            missing_documents
        )


        claim = {
            "policy_number": policy_number,
            "customer_id": customer_id,
            "claim_amount": claim_amount,
            "eligible": eligible,
            "maximum_payable": self.maximum_payable(
                claim_amount,
                coverage
            ),
            "deductible": self.calculate_deductible(
                claim_amount
            ),
            "customer_contribution": self.customer_contribution(
                claim_amount
            ),
            "insurance_payout": payout,
            "fraud_score": fraud_score,
            "status": status
        }


        self.claims[policy_number] = claim

        return claim


# ==================================================
# TEST COUNTERS
# ==================================================

passed = 0
failed = 0


def check_test(name, condition):

    global passed
    global failed

    if condition:

        print("PASS - " + name)

        passed += 1

    else:

        print("FAIL - " + name)

        failed += 1


# ==================================================
# TEST 1
# VALID CLAIM
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
        and result["insurance_payout"] > 0
    )


# ==================================================
# TEST 2
# EXPIRED POLICY
# ==================================================

def test_expired_policy():

    system = InsuranceClaim()


    # Policy expired before incident
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
# TEST 3
# CLAIM BEFORE POLICY START
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
# TEST 4
# EXCESSIVE CLAIM AMOUNT
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
# TEST 5
# MISSING DOCUMENTS
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
        result["status"] == "MANUAL REVIEW"
        and result["fraud_score"] >= 25
    )


# ==================================================
# TEST 6
# MULTIPLE PREVIOUS CLAIMS
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
        result["fraud_score"] >= 30
        and result["status"] == "MANUAL REVIEW"
    )


# ==================================================
# TEST 7
# FRAUD SCENARIO
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
        result["fraud_score"] >= 70
        and result["status"] == "FRAUD SUSPECTED"
    )


# ==================================================
# TEST 8
# BOUNDARY CLAIM AMOUNT
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
    )


# ==================================================
# TEST 9
# INVALID POLICY NUMBER
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
# TEST 10
# INVALID INCIDENT DATE
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
# MAIN PROGRAM
# ==================================================

if __name__ == "__main__":

    print()
    print("==============================================")
    print("   INSURANCE CLAIM PROCESSING QA")
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
