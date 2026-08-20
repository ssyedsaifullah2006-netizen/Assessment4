from datetime import datetime


class InsuranceClaim:

    def __init__(self):

        self.coverage = {
            "Health": 500000,
            "Vehicle": 300000,
            "Life": 1000000,
            "Travel": 200000
        }

        self.deductible_rate = 0.10

    def process_claim(self, policy_no, customer_id, policy_type,
                      claim_amount, policy_start, incident_date,
                      previous_claims, age, incident_type,
                      documents):

        # Validate policy number
        if not policy_no.startswith("POL") or len(policy_no) != 8:
            return False, "Invalid policy number"

        # Validate policy type
        if policy_type not in self.coverage:
            return False, "Invalid policy type"

        # Validate dates
        try:
            start = datetime.strptime(policy_start, "%Y-%m-%d")
            incident = datetime.strptime(incident_date, "%Y-%m-%d")
        except ValueError:
            return False, "Invalid incident date"

        # Incident cannot be before policy start
        if incident < start:
            return True, {
                "Classification": "REJECTED",
                "Reason": "Claim before policy start"
            }

        # Claim amount must be positive
        if claim_amount <= 0:
            return True, {
                "Classification": "REJECTED",
                "Reason": "Invalid claim amount"
            }

        coverage = self.coverage[policy_type]

        # Fraud score
        fraud_score = 0
        fraud_reasons = []

        # Multiple previous claims
        if previous_claims >= 3:
            fraud_score += 25
            fraud_reasons.append("Multiple previous claims")

        # Claim significantly higher than coverage
        if claim_amount > coverage:
            fraud_score += 35
            fraud_reasons.append("Claim exceeds coverage")

        # Incident immediately after policy activation
        days_after_start = (incident - start).days

        if 0 <= days_after_start <= 7:
            fraud_score += 25
            fraud_reasons.append(
                "Incident immediately after policy activation"
            )

        # Missing documentation
        if not documents:
            fraud_score += 20
            fraud_reasons.append("Missing documentation")

        # Maximum payable amount
        maximum_payable = min(claim_amount, coverage)

        # Deductible
        deductible = maximum_payable * self.deductible_rate

        # Customer contribution
        customer_contribution = deductible

        # Insurance payout
        insurance_payout = maximum_payable - deductible

        # Classification
        if fraud_score >= 60:
            classification = "FRAUD SUSPECTED"

        elif claim_amount > coverage:
            classification = "MANUAL REVIEW"

        elif not documents:
            classification = "MANUAL REVIEW"

        else:
            classification = "APPROVED"

        return True, {
            "Policy Number": policy_no,
            "Customer ID": customer_id,
            "Policy Type": policy_type,
            "Claim Amount": claim_amount,
            "Coverage": coverage,
            "Maximum Payable": maximum_payable,
            "Deductible": deductible,
            "Customer Contribution": customer_contribution,
            "Insurance Payout": insurance_payout,
            "Fraud Risk Score": fraud_score,
            "Fraud Reasons": fraud_reasons,
            "Classification": classification
        }


if __name__ == "__main__":

    insurance = InsuranceClaim()

    # Predefined claim
    success, result = insurance.process_claim(
        "POL12345",
        "C101",
        "Health",
        100000,
        "2025-01-01",
        "2025-06-15",
        1,
        35,
        "Medical",
        True
    )

    if success:

        print("CLAIM PROCESSED")
        print("----------------")

        for key, value in result.items():
            print(key + ":", value)

    else:

        print("CLAIM FAILED")
        print("Reason:", result)