class InsuranceClaim:

    def __init__(self):
        self.claims = {}

    # ==========================================
    # POLICY NUMBER VALIDATION
    # ==========================================

    def validate_policy_number(self, policy_number):

        if policy_number is None:
            return False

        if not isinstance(policy_number, str):
            return False

        if policy_number.strip() == "":
            return False

        if len(policy_number.strip()) < 4:
            return False

        return True

    # ==========================================
    # DATE VALIDATION
    # ==========================================

    def validate_dates(self, policy_start_date, incident_date):

        if not isinstance(policy_start_date, int):
            return False

        if not isinstance(incident_date, int):
            return False

        if policy_start_date < 0:
            return False

        if incident_date < 0:
            return False

        return True

    # ==========================================
    # CLAIM ELIGIBILITY
    # ==========================================

    def check_eligibility(
        self,
        policy_number,
        policy_start_date,
        incident_date,
        claim_amount,
        coverage
    ):

        # Invalid policy
        if not self.validate_policy_number(policy_number):
            return False

        # Invalid dates
        if not self.validate_dates(
            policy_start_date,
            incident_date
        ):
            return False

        # Invalid claim amount
        if claim_amount < 0:
            return False

        # Invalid coverage
        if coverage < 0:
            return False

        # Incident before policy started
        if incident_date < policy_start_date:
            return False

        # Claim exceeds policy coverage
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

        if coverage < 0:
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

        if claim_amount <= 0:
            return 0

        # 10% deductible
        return claim_amount * 0.10

    # ==========================================
    # CUSTOMER CONTRIBUTION
    # ==========================================

    def customer_contribution(
        self,
        claim_amount
    ):

        if claim_amount <= 0:
            return 0

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
        if previous_claim_count >= 4:
            score += 40

        elif previous_claim_count >= 3:
            score += 30

        elif previous_claim_count >= 2:
            score += 20

        # Claim amount close to coverage
        if coverage > 0:

            percentage = claim_amount / coverage

            if percentage > 1.0:
                score += 50

            elif percentage >= 0.90:
                score += 30

            elif percentage >= 0.75:
                score += 10

        # Incident immediately after activation
        if incident_after_activation:
            score += 25

        # Missing supporting documents
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

        # Not eligible
        if not eligible:
            return "REJECTED"

        # High fraud score
        if fraud_score >= 70:
            return "FRAUD SUSPECTED"

        # Documents missing or medium risk
        if fraud_score >= 40 or missing_documents:
            return "MANUAL REVIEW"

        # Normal valid claim
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
        policy_start_date,
        incident_date,
        previous_claim_count,
        customer_age,
        incident_type,
        supporting_documents,
        coverage
    ):

        # --------------------------------------
        # Validate policy number
        # --------------------------------------

        if not self.validate_policy_number(
            policy_number
        ):
            return {
                "policy_number": policy_number,
                "eligible": False,
                "status": "REJECTED",
                "insurance_payout": 0
            }

        # --------------------------------------
        # Validate incident date
        # --------------------------------------

        if not self.validate_dates(
            policy_start_date,
            incident_date
        ):
            return {
                "policy_number": policy_number,
                "eligible": False,
                "status": "REJECTED",
                "insurance_payout": 0
            }

        # --------------------------------------
        # Eligibility
        # --------------------------------------

        eligible = self.check_eligibility(
            policy_number,
            policy_start_date,
            incident_date,
            claim_amount,
            coverage
        )

        # --------------------------------------
        # Missing documents
        # --------------------------------------

        missing_documents = not supporting_documents

        # --------------------------------------
        # Incident immediately after activation
        # --------------------------------------

        days_after_activation = (
            incident_date - policy_start_date
        )

        incident_after_activation = (
            days_after_activation >= 0
            and days_after_activation <= 7
        )

        # --------------------------------------
        # Maximum payable
        # --------------------------------------

        maximum_payable = self.maximum_payable(
            claim_amount,
            coverage
        )

        # --------------------------------------
        # Deductible
        # --------------------------------------

        deductible = self.calculate_deductible(
            maximum_payable
        )

        # --------------------------------------
        # Customer contribution
        # --------------------------------------

        contribution = self.customer_contribution(
            maximum_payable
        )

        # --------------------------------------
        # Insurance payout
        # --------------------------------------

        if eligible:

            payout = self.insurance_payout(
                claim_amount,
                coverage
            )

        else:

            payout = 0

        # --------------------------------------
        # Fraud score
        # --------------------------------------

        fraud_score = self.fraud_risk_score(
            claim_amount,
            coverage,
            incident_after_activation,
            missing_documents,
            previous_claim_count
        )

        # --------------------------------------
        # Claim status
        # --------------------------------------

        status = self.classify_claim(
            eligible,
            fraud_score,
            missing_documents
        )

        # --------------------------------------
        # Store claim
        # --------------------------------------

        claim = {

            "policy_number": policy_number,

            "customer_id": customer_id,

            "policy_type": policy_type,

            "claim_amount": claim_amount,

            "policy_start_date": policy_start_date,

            "incident_date": incident_date,

            "previous_claim_count":
                previous_claim_count,

            "customer_age": customer_age,

            "incident_type": incident_type,

            "supporting_documents":
                supporting_documents,

            "coverage": coverage,

            "eligible": eligible,

            "maximum_payable":
                maximum_payable,

            "deductible":
                deductible,

            "customer_contribution":
                contribution,

            "insurance_payout":
                payout,

            "fraud_score":
                fraud_score,

            "status":
                status
        }

        self.claims[policy_number] = claim

        return claim


# ==========================================
# MAIN PROGRAM
# ==========================================

if __name__ == "__main__":

    system = InsuranceClaim()

    print("========================================")
    print("   INSURANCE CLAIM PROCESSING SYSTEM")
    print("========================================")

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

    print()
    print("Policy Number :", result["policy_number"])
    print("Eligible      :", result["eligible"])
    print("Max Payable   :", result["maximum_payable"])
    print("Deductible    :", result["deductible"])
    print("Contribution  :", result["customer_contribution"])
    print("Payout        :", result["insurance_payout"])
    print("Fraud Score   :", result["fraud_score"])
    print("Status        :", result["status"])
