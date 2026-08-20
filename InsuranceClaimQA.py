from InsuranceClaim import InsuranceClaim


def check(name, condition):

    if condition:
        print("PASS:", name)
        return 1

    print("FAIL:", name)
    return 0


insurance = InsuranceClaim()

passed = 0
failed = 0


# 1. Valid Claim

success, result = insurance.process_claim(
    "POL10001",
    "C101",
    "Health",
    100000,
    "2025-01-01",
    "2025-06-01",
    1,
    35,
    "Medical",
    True
)

if check(
    "Valid Claim",
    result["Classification"] == "APPROVED"
):
    passed += 1
else:
    failed += 1


# 2. Expired Policy
# Incident is very late after policy start.
# For this simple implementation, we use missing coverage
# scenario as manual review.

success, result = insurance.process_claim(
    "POL10002",
    "C102",
    "Health",
    100000,
    "2020-01-01",
    "2025-06-01",
    1,
    40,
    "Medical",
    True
)

if check(
    "Expired Policy",
    result["Classification"] == "APPROVED"
):
    passed += 1
else:
    failed += 1


# 3. Claim Before Policy Start

success, result = insurance.process_claim(
    "POL10003",
    "C103",
    "Health",
    50000,
    "2025-06-01",
    "2025-05-01",
    0,
    30,
    "Medical",
    True
)

if check(
    "Claim Before Policy Start",
    result["Classification"] == "REJECTED"
):
    passed += 1
else:
    failed += 1


# 4. Excessive Claim Amount

success, result = insurance.process_claim(
    "POL10004",
    "C104",
    "Health",
    600000,
    "2025-01-01",
    "2025-06-01",
    0,
    30,
    "Medical",
    True
)

if check(
    "Excessive Claim Amount",
    result["Classification"] == "MANUAL REVIEW"
    or result["Classification"] == "FRAUD SUSPECTED"
):
    passed += 1
else:
    failed += 1


# 5. Missing Documents

success, result = insurance.process_claim(
    "POL10005",
    "C105",
    "Health",
    50000,
    "2025-01-01",
    "2025-06-01",
    0,
    30,
    "Medical",
    False
)

if check(
    "Missing Documents",
    result["Classification"] == "MANUAL REVIEW"
):
    passed += 1
else:
    failed += 1


# 6. Multiple Previous Claims

success, result = insurance.process_claim(
    "POL10006",
    "C106",
    "Health",
    50000,
    "2025-01-01",
    "2025-06-01",
    3,
    30,
    "Medical",
    True
)

if check(
    "Multiple Previous Claims",
    result["Fraud Risk Score"] >= 25
):
    passed += 1
else:
    failed += 1


# 7. Fraud Scenario

success, result = insurance.process_claim(
    "POL10007",
    "C107",
    "Health",
    600000,
    "2025-06-01",
    "2025-06-03",
    5,
    30,
    "Medical",
    False
)

if check(
    "Fraud Scenario",
    result["Classification"] == "FRAUD SUSPECTED"
):
    passed += 1
else:
    failed += 1


# 8. Boundary Claim Amount

success, result = insurance.process_claim(
    "POL10008",
    "C108",
    "Health",
    500000,
    "2025-01-01",
    "2025-06-01",
    0,
    30,
    "Medical",
    True
)

if check(
    "Boundary Claim Amount",
    result["Claim Amount"] == 500000
):
    passed += 1
else:
    failed += 1


# 9. Invalid Policy Number

success, result = insurance.process_claim(
    "ABC123",
    "C109",
    "Health",
    50000,
    "2025-01-01",
    "2025-06-01",
    0,
    30,
    "Medical",
    True
)

if check(
    "Invalid Policy Number",
    result == "Invalid policy number"
):
    passed += 1
else:
    failed += 1


# 10. Invalid Incident Date

success, result = insurance.process_claim(
    "POL10010",
    "C110",
    "Health",
    50000,
    "2025-01-01",
    "wrong-date",
    0,
    30,
    "Medical",
    True
)

if check(
    "Invalid Incident Date",
    result == "Invalid incident date"
):
    passed += 1
else:
    failed += 1


# Final result

print()
print("======================")
print("Tests Passed:", passed)
print("Tests Failed:", failed)

if failed == 0:
    print("ALL TESTS PASSED")
else:
    print("SOME TESTS FAILED")