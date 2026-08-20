import sys


class ICUAllocation:

    def __init__(self, beds):

        self.available_beds = beds
        self.patients = {}
        self.waiting_list = []

    # ---------------------------------------
    # Validate Patient
    # ---------------------------------------
    def validate_patient(
        self,
        patient_id,
        age,
        oxygen,
        heart_rate,
        blood_pressure,
        temperature
    ):

        if patient_id == "":
            return False

        if age <= 0 or age > 120:
            return False

        if oxygen < 0 or oxygen > 100:
            return False

        if heart_rate <= 0 or heart_rate > 250:
            return False

        if blood_pressure <= 0:
            return False

        if temperature < 25 or temperature > 45:
            return False

        return True

    # ---------------------------------------
    # Priority Score
    # ---------------------------------------
    def calculate_priority(
        self,
        oxygen,
        heart_rate,
        blood_pressure,
        temperature,
        medical_conditions
    ):

        score = 0

        if oxygen < 85:
            score += 40
        elif oxygen < 90:
            score += 30
        elif oxygen < 95:
            score += 15

        if heart_rate > 130:
            score += 25
        elif heart_rate > 110:
            score += 15
        elif heart_rate < 50:
            score += 20

        if blood_pressure < 80:
            score += 20
        elif blood_pressure < 90:
            score += 10

        if temperature >= 40:
            score += 20
        elif temperature >= 38:
            score += 10

        if medical_conditions:
            score += 10

        return score

    # ---------------------------------------
    # Classification
    # ---------------------------------------
    def classify_patient(self, score):

        if score >= 60:
            return "CRITICAL"

        elif score >= 40:
            return "HIGH"

        elif score >= 20:
            return "MEDIUM"

        else:
            return "LOW"

    # ---------------------------------------
    # Add Patient
    # ---------------------------------------
    def add_patient(
        self,
        patient_id,
        age,
        oxygen,
        heart_rate,
        blood_pressure,
        temperature,
        medical_conditions,
        emergency=False
    ):

        if patient_id in self.patients:
            return False

        if not self.validate_patient(
            patient_id,
            age,
            oxygen,
            heart_rate,
            blood_pressure,
            temperature
        ):
            return False

        score = self.calculate_priority(
            oxygen,
            heart_rate,
            blood_pressure,
            temperature,
            medical_conditions
        )

        category = self.classify_patient(score)

        patient = {
            "priority_score": score,
            "category": category,
            "emergency": emergency,
            "icu": False
        }

        # Emergency or normal allocation
        if self.available_beds > 0:

            patient["icu"] = True
            self.available_beds -= 1

        else:

            self.waiting_list.append(
                patient_id
            )

        self.patients[patient_id] = patient

        return True

    # ---------------------------------------
    # Emergency
    # ---------------------------------------
    def emergency(self, patient_id):

        if patient_id not in self.patients:
            return False

        patient = self.patients[patient_id]

        patient["emergency"] = True

        if self.available_beds > 0:

            patient["icu"] = True
            self.available_beds -= 1

            return True

        return False


# ==========================================
# Test Counter
# ==========================================

passed = 0
failed = 0


def check_test(name, result):

    global passed
    global failed

    if result:

        print("PASS - " + name)
        passed += 1

    else:

        print("FAIL - " + name)
        failed += 1


# ==========================================
# 1. Critical Patient
# ==========================================

def test_critical_patient():

    system = ICUAllocation(1)

    result = system.add_patient(
        "P001",
        60,
        80,
        140,
        70,
        40,
        True
    )

    patient = system.patients["P001"]

    check_test(
        "Critical Patient",
        result
        and patient["category"] == "CRITICAL"
        and patient["icu"] is True
    )


# ==========================================
# 2. Normal Patient
# ==========================================

def test_normal_patient():

    system = ICUAllocation(1)

    result = system.add_patient(
        "P002",
        30,
        98,
        80,
        120,
        36.5,
        False
    )

    patient = system.patients["P002"]

    check_test(
        "Normal Patient",
        result
        and patient["category"] == "LOW"
        and patient["icu"] is True
    )


# ==========================================
# 3. Emergency Case
# ==========================================

def test_emergency_case():

    system = ICUAllocation(1)

    system.add_patient(
        "P001",
        50,
        90,
        100,
        110,
        37,
        False
    )

    result = system.add_patient(
        "P002",
        70,
        80,
        140,
        70,
        40,
        True
    )

    patient = system.patients["P002"]

    check_test(
        "Emergency Case",
        result
        and patient["emergency"] is True
    )


# ==========================================
# 4. No ICU Beds
# ==========================================

def test_no_icu_beds():

    system = ICUAllocation(0)

    result = system.add_patient(
        "P003",
        50,
        90,
        90,
        110,
        37,
        False
    )

    patient = system.patients["P003"]

    check_test(
        "No ICU Beds",
        result
        and patient["icu"] is False
        and "P003" in system.waiting_list
    )


# ==========================================
# 5. Duplicate Patient
# ==========================================

def test_duplicate_patient():

    system = ICUAllocation(2)

    first = system.add_patient(
        "P004",
        40,
        95,
        80,
        120,
        36.5,
        False
    )

    second = system.add_patient(
        "P004",
        40,
        95,
        80,
        120,
        36.5,
        False
    )

    check_test(
        "Duplicate Patient",
        first is True
        and second is False
    )


# ==========================================
# 6. Invalid Oxygen Level
# ==========================================

def test_invalid_oxygen():

    system = ICUAllocation(1)

    result = system.add_patient(
        "P005",
        40,
        150,
        80,
        120,
        36.5,
        False
    )

    check_test(
        "Invalid Oxygen Level",
        result is False
    )


# ==========================================
# 7. Invalid Heart Rate
# ==========================================

def test_invalid_heart_rate():

    system = ICUAllocation(1)

    result = system.add_patient(
        "P006",
        40,
        95,
        300,
        120,
        36.5,
        False
    )

    check_test(
        "Invalid Heart Rate",
        result is False
    )


# ==========================================
# 8. Priority Boundary Values
# ==========================================

def test_priority_boundary():

    system = ICUAllocation(1)

    score = system.calculate_priority(
        95,
        80,
        120,
        36.5,
        False
    )

    category = system.classify_patient(
        score
    )

    check_test(
        "Priority Boundary Values",
        score == 0
        and category == "LOW"
    )


# ==========================================
# 9. Multiple Patients Competing
# ==========================================

def test_multiple_patients():

    system = ICUAllocation(1)

    first = system.add_patient(
        "P007",
        60,
        80,
        140,
        70,
        40,
        True
    )

    second = system.add_patient(
        "P008",
        50,
        90,
        90,
        110,
        37,
        False
    )

    first_patient = system.patients["P007"]
    second_patient = system.patients["P008"]

    check_test(
        "Multiple Patients Competing for Same Bed",
        first
        and second
        and first_patient["icu"] is True
        and second_patient["icu"] is False
        and "P008" in system.waiting_list
    )


# ==========================================
# MAIN
# ==========================================

if __name__ == "__main__":

    print()
    print("========================================")
    print("     ICU ALLOCATION QA TEST")
    print("========================================")

    test_critical_patient()

    test_normal_patient()

    test_emergency_case()

    test_no_icu_beds()

    test_duplicate_patient()

    test_invalid_oxygen()

    test_invalid_heart_rate()

    test_priority_boundary()

    test_multiple_patients()

    print()
    print("========================================")
    print("Tests Passed :", passed)
    print("Tests Failed :", failed)
    print("========================================")

    if failed == 0:

        print("ALL TESTS PASSED")

        sys.exit(0)

    else:

        print("TESTS FAILED")

        sys.exit(1)
