class ICUAllocation:

    def __init__(self, beds):
        self.total_beds = beds
        self.available_beds = beds
        self.patients = {}
        self.waiting_list = []

    def calculate_priority(self, oxygen, heart_rate,
                           blood_pressure, temperature,
                           conditions, emergency):

        score = 0

        # Oxygen level
        if oxygen < 90:
            score += 40
        elif oxygen < 95:
            score += 20

        # Heart rate
        if heart_rate > 120 or heart_rate < 50:
            score += 25
        elif heart_rate > 100:
            score += 10

        # Blood pressure (systolic)
        if blood_pressure < 90 or blood_pressure > 180:
            score += 20
        elif blood_pressure < 100 or blood_pressure > 160:
            score += 10

        # Temperature
        if temperature >= 39 or temperature < 35:
            score += 15
        elif temperature >= 38:
            score += 10

        # Existing medical conditions
        if conditions:
            score += 10

        # Emergency override
        if emergency:
            score += 100

        return score

    def classify(self, score, emergency=False):

        if emergency or score >= 70:
            return "CRITICAL"

        elif score >= 45:
            return "HIGH"

        elif score >= 20:
            return "MEDIUM"

        else:
            return "LOW"

    def add_patient(self, patient_id, age, oxygen,
                    heart_rate, blood_pressure,
                    temperature, conditions,
                    emergency=False):

        # Duplicate patient check
        if patient_id in self.patients:
            return False, "Duplicate patient ID"

        # Input validation
        if age <= 0 or age > 120:
            return False, "Invalid age"

        if oxygen < 0 or oxygen > 100:
            return False, "Invalid oxygen level"

        if heart_rate <= 0 or heart_rate > 250:
            return False, "Invalid heart rate"

        if blood_pressure <= 0 or blood_pressure > 300:
            return False, "Invalid blood pressure"

        if temperature < 25 or temperature > 45:
            return False, "Invalid temperature"

        # Calculate priority
        score = self.calculate_priority(
            oxygen,
            heart_rate,
            blood_pressure,
            temperature,
            conditions,
            emergency
        )

        category = self.classify(score, emergency)

        # Store patient
        self.patients[patient_id] = {
            "Age": age,
            "Oxygen": oxygen,
            "Heart Rate": heart_rate,
            "Blood Pressure": blood_pressure,
            "Temperature": temperature,
            "Conditions": conditions,
            "Emergency": emergency,
            "Score": score,
            "Priority": category,
            "Bed": None
        }

        # Emergency or critical patient gets bed first
        if self.available_beds > 0:
            self.available_beds -= 1
            self.patients[patient_id]["Bed"] = "ICU-BED"
            return True, category

        # No beds available
        self.waiting_list.append(patient_id)

        return True, "WAITING LIST - " + category

    def get_patient(self, patient_id):

        if patient_id not in self.patients:
            return None

        return self.patients[patient_id]

    def show_status(self):

        print("Available ICU Beds:", self.available_beds)

        print("\nPatients:")

        for patient_id, data in self.patients.items():
            print(
                patient_id,
                data["Priority"],
                "Score:",
                data["Score"],
                "Bed:",
                data["Bed"]
            )

        print("\nWaiting List:", self.waiting_list)


if __name__ == "__main__":

    icu = ICUAllocation(2)

    # Predefined patient
    success, result = icu.add_patient(
        "P001",
        65,
        85,
        130,
        85,
        39.5,
        ["Diabetes"],
        False
    )

    if success:
        print("Patient accepted")
        print("Priority:", result)
    else:
        print("Patient rejected:", result)

    icu.show_status()