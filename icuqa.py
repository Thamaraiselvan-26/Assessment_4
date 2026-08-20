import sys


class ICUAllocation:

    def __init__(self, total_beds):
        self.total_beds = total_beds
        self.available_beds = total_beds
        self.patients = {}
        self.waiting_list = []


    # =========================================
    # VALIDATE PATIENT
    # =========================================

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


    # =========================================
    # CALCULATE PRIORITY SCORE
    # =========================================

    def calculate_priority(
        self,
        oxygen,
        heart_rate,
        blood_pressure,
        temperature,
        medical_conditions
    ):

        score = 0

        # Oxygen
        if oxygen < 85:
            score += 40
        elif oxygen < 90:
            score += 30
        elif oxygen < 95:
            score += 15

        # Heart rate
        if heart_rate > 130:
            score += 25
        elif heart_rate > 110:
            score += 15
        elif heart_rate < 50:
            score += 20

        # Blood pressure
        if blood_pressure < 80:
            score += 20
        elif blood_pressure < 90:
            score += 10

        # Temperature
        if temperature >= 40:
            score += 20
        elif temperature >= 38:
            score += 10

        # Medical condition
        if medical_conditions:
            score += 10

        return score


    # =========================================
    # CLASSIFY PRIORITY
    # =========================================

    def classify_patient(self, score):

        if score >= 60:
            return "CRITICAL"

        elif score >= 40:
            return "HIGH"

        elif score >= 20:
            return "MEDIUM"

        else:
            return "LOW"


    # =========================================
    # ADD PATIENT
    # =========================================

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

        # Duplicate ID
        if patient_id in self.patients:
            return False

        # Validation
        if not self.validate_patient(
            patient_id,
            age,
            oxygen,
            heart_rate,
            blood_pressure,
            temperature
        ):
            return False

        # Priority
        score = self.calculate_priority(
            oxygen,
            heart_rate,
            blood_pressure,
            temperature,
            medical_conditions
        )

        category = self.classify_patient(score)

        patient = {
            "patient_id": patient_id,
            "age": age,
            "oxygen": oxygen,
            "heart_rate": heart_rate,
            "blood_pressure": blood_pressure,
            "temperature": temperature,
            "medical_conditions": medical_conditions,
            "priority_score": score,
            "category": category,
            "emergency": emergency,
            "icu_allocated": False
        }

        # Emergency patient gets priority
        if emergency:

            if self.available_beds > 0:

                patient["icu_allocated"] = True
                self.available_beds -= 1

            else:

                self.waiting_list.append(patient_id)

        # Critical patient
        elif category == "CRITICAL":

            if self.available_beds > 0:

                patient["icu_allocated"] = True
                self.available_beds -= 1

            else:

                self.waiting_list.append(patient_id)

        # Normal patient
        else:

            if self.available_beds > 0:

                patient["icu_allocated"] = True
                self.available_beds -= 1

            else:

                self.waiting_list.append(patient_id)

        self.patients[patient_id] = patient

        return True


# =========================================
# TEST COUNTERS
# =========================================

passed = 0
failed = 0


def test_result(name, condition):

    global passed
    global failed

    if condition:

        print("PASS - " + name)
        passed += 1

    else:

        print("FAIL - " + name)
        failed += 1


# =========================================
# TEST 1
# CRITICAL PATIENT
# =========================================

def test_critical_patient():

    system = ICUAllocation(1)

    result = system.add_patient(
        "P001",
        65,
        80,
        140,
        70,
        40.0,
        True
    )

    patient = system.patients["P001"]

    test_result(
        "Critical Patient",
        result is True
        and patient["priority_score"] >= 60
        and patient["category"] == "CRITICAL"
        and patient["icu_allocated"] is True
    )


# =========================================
# TEST 2
# NORMAL PATIENT
# =========================================

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

    test_result(
        "Normal Patient",
        result is True
        and patient["priority_score"] == 0
        and patient["category"] == "LOW"
        and patient["icu_allocated"] is True
    )


# =========================================
# TEST 3
# EMERGENCY CASE
# =========================================

def test_emergency_case():

    system = ICUAllocation(1)

    result = system.add_patient(
        "P003",
        70,
        80,
        140,
        70,
        40.0,
        True,
        True
    )

    patient = system.patients["P003"]

    test_result(
        "Emergency Case",
        result is True
        and patient["emergency"] is True
        and patient["icu_allocated"] is True
    )


# =========================================
# TEST 4
# NO ICU BEDS
# =========================================

def test_no_icu_beds():

    system = ICUAllocation(0)

    result = system.add_patient(
        "P004",
        50,
        90,
        90,
        110,
        37.0,
        False
    )

    patient = system.patients["P004"]

    test_result(
        "No ICU Beds",
        result is True
        and patient["icu_allocated"] is False
        and "P004" in system.waiting_list
    )


# =========================================
# TEST 5
# DUPLICATE PATIENT
# =========================================

def test_duplicate_patient():

    system = ICUAllocation(2)

    first = system.add_patient(
        "P005",
        40,
        95,
        80,
        120,
        36.5,
        False
    )

    second = system.add_patient(
        "P005",
        40,
        95,
        80,
        120,
        36.5,
        False
    )

    test_result(
        "Duplicate Patient",
        first is True
        and second is False
        and len(system.patients) == 1
    )


# =========================================
# TEST 6
# INVALID OXYGEN
# =========================================

def test_invalid_oxygen():

    system = ICUAllocation(1)

    result = system.add_patient(
        "P006",
        40,
        101,
        80,
        120,
        36.5,
        False
    )

    test_result(
        "Invalid Oxygen Level",
        result is False
    )


# =========================================
# TEST 7
# INVALID HEART RATE
# =========================================

def test_invalid_heart_rate():

    system = ICUAllocation(1)

    result = system.add_patient(
        "P007",
        40,
        95,
        251,
        120,
        36.5,
        False
    )

    test_result(
        "Invalid Heart Rate",
        result is False
    )


# =========================================
# TEST 8
# PRIORITY BOUNDARY
# =========================================

def test_priority_boundary():

    system = ICUAllocation(1)

    # Exactly 20 points:
    # Temperature = 38 gives 10
    # Heart rate = 120 gives 15
    # Total = 25
    score = system.calculate_priority(
        95,
        120,
        120,
        38,
        False
    )

    category = system.classify_patient(score)

    test_result(
        "Priority Boundary Values",
        score == 25
        and category == "MEDIUM"
    )


# =========================================
# TEST 9
# MULTIPLE PATIENTS COMPETING
# =========================================

def test_multiple_patients():

    system = ICUAllocation(1)

    # First patient takes the only bed
    first = system.add_patient(
        "P008",
        65,
        80,
        140,
        70,
        40.0,
        True
    )

    # Second patient must wait
    second = system.add_patient(
        "P009",
        30,
        98,
        80,
        120,
        36.5,
        False
    )

    first_patient = system.patients["P008"]
    second_patient = system.patients["P009"]

    test_result(
        "Multiple Patients Competing for Same Bed",
        first is True
        and second is True
        and first_patient["icu_allocated"] is True
        and second_patient["icu_allocated"] is False
        and "P009" in system.waiting_list
        and system.available_beds == 0
    )


# =========================================
# MAIN
# =========================================

if __name__ == "__main__":

    print()
    print("==========================================")
    print("   HOSPITAL ICU RESOURCE ALLOCATION QA")
    print("==========================================")
    print()

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
