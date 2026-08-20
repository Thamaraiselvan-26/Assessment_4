class ICUAllocation:

    def __init__(self, beds):

        self.total_beds = beds
        self.available_beds = beds

        self.patients = {}
        self.waiting_list = []

    # ---------------------------------------
    # Validate Patient Data
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
    # Calculate Priority Score
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

        # Oxygen level
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

        # Existing medical conditions
        if medical_conditions:
            score += 10

        return score

    # ---------------------------------------
    # Classify Patient
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

        # Duplicate patient check
        if patient_id in self.patients:
            return False

        # Validate input
        if not self.validate_patient(
            patient_id,
            age,
            oxygen,
            heart_rate,
            blood_pressure,
            temperature
        ):
            return False

        # Calculate priority
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

        # Emergency patients get priority
        if emergency and self.available_beds > 0:

            patient["icu_allocated"] = True
            self.available_beds -= 1

        elif category == "CRITICAL" and self.available_beds > 0:

            patient["icu_allocated"] = True
            self.available_beds -= 1

        elif self.available_beds > 0:

            patient["icu_allocated"] = True
            self.available_beds -= 1

        else:

            self.waiting_list.append(patient_id)

        self.patients[patient_id] = patient

        return True

    # ---------------------------------------
    # Allocate ICU Bed
    # ---------------------------------------
    def allocate_bed(self, patient_id):

        if patient_id not in self.patients:
            return False

        patient = self.patients[patient_id]

        if patient["icu_allocated"]:
            return True

        if self.available_beds <= 0:
            return False

        patient["icu_allocated"] = True
        self.available_beds -= 1

        if patient_id in self.waiting_list:
            self.waiting_list.remove(patient_id)

        return True

    # ---------------------------------------
    # Emergency Allocation
    # ---------------------------------------
    def emergency_allocation(self, patient_id):

        if patient_id not in self.patients:
            return False

        patient = self.patients[patient_id]

        patient["emergency"] = True

        if self.available_beds > 0:

            patient["icu_allocated"] = True
            self.available_beds -= 1

            if patient_id in self.waiting_list:
                self.waiting_list.remove(patient_id)

            return True

        return False

    # ---------------------------------------
    # Get Patient
    # ---------------------------------------
    def get_patient(self, patient_id):

        if patient_id not in self.patients:
            return None

        return self.patients[patient_id]


# ==========================================
# Main Program
# ==========================================

if __name__ == "__main__":

    system = ICUAllocation(2)

    print("====================================")
    print("   HOSPITAL ICU ALLOCATION SYSTEM")
    print("====================================")

    result = system.add_patient(
        "P001",
        65,
        82,
        135,
        75,
        40.0,
        True
    )

    if result:

        patient = system.get_patient("P001")

        print("Patient Added")
        print("Patient ID      :", patient["patient_id"])
        print("Priority Score  :", patient["priority_score"])
        print("Category        :", patient["category"])
        print("ICU Allocated   :", patient["icu_allocated"])

    else:

        print("Patient Rejected")

    print()
    print("Available ICU Beds:",
          system.available_beds)
