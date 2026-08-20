from ICUAllocation import ICUAllocation


def check(test_name, condition):

    if condition:
        print("PASS:", test_name)
        return 1
    else:
        print("FAIL:", test_name)
        return 0


passed = 0
failed = 0


# 1. Critical Patient

icu = ICUAllocation(2)

success, result = icu.add_patient(
    "P001",
    70,
    80,
    140,
    80,
    40,
    ["Heart Disease"]
)

if check("Critical Patient", result == "CRITICAL"):
    passed += 1
else:
    failed += 1


# 2. Normal Patient

icu = ICUAllocation(2)

success, result = icu.add_patient(
    "P002",
    30,
    98,
    75,
    120,
    36.5,
    []
)

if check("Normal Patient", result == "LOW"):
    passed += 1
else:
    failed += 1


# 3. Emergency Case

icu = ICUAllocation(2)

success, result = icu.add_patient(
    "P003",
    40,
    98,
    80,
    120,
    37,
    [],
    True
)

if check("Emergency Case", result == "CRITICAL"):
    passed += 1
else:
    failed += 1


# 4. No ICU Beds

icu = ICUAllocation(1)

icu.add_patient(
    "P004",
    70,
    80,
    140,
    80,
    40,
    ["Heart Disease"]
)

success, result = icu.add_patient(
    "P005",
    30,
    98,
    75,
    120,
    36.5,
    []
)

if check(
    "No ICU Beds",
    "WAITING LIST" in result
):
    passed += 1
else:
    failed += 1


# 5. Duplicate Patient

icu = ICUAllocation(2)

icu.add_patient(
    "P006",
    50,
    95,
    80,
    120,
    37,
    []
)

success, result = icu.add_patient(
    "P006",
    50,
    95,
    80,
    120,
    37,
    []
)

if check(
    "Duplicate Patient",
    result == "Duplicate patient ID"
):
    passed += 1
else:
    failed += 1


# 6. Invalid Oxygen Level

icu = ICUAllocation(2)

success, result = icu.add_patient(
    "P007",
    50,
    110,
    80,
    120,
    37,
    []
)

if check(
    "Invalid Oxygen Level",
    result == "Invalid oxygen level"
):
    passed += 1
else:
    failed += 1


# 7. Invalid Heart Rate

icu = ICUAllocation(2)

success, result = icu.add_patient(
    "P008",
    50,
    95,
    300,
    120,
    37,
    []
)

if check(
    "Invalid Heart Rate",
    result == "Invalid heart rate"
):
    passed += 1
else:
    failed += 1


# 8. Priority Boundary

icu = ICUAllocation(2)

# Oxygen 94 gives 20 points
# Everything else normal
success, result = icu.add_patient(
    "P009",
    50,
    94,
    80,
    120,
    37,
    []
)

if check(
    "Priority Boundary",
    result == "MEDIUM"
):
    passed += 1
else:
    failed += 1


# 9. Multiple Patients Competing for Same Bed

icu = ICUAllocation(1)

icu.add_patient(
    "P010",
    70,
    80,
    140,
    80,
    40,
    ["Heart Disease"]
)

success, result = icu.add_patient(
    "P011",
    30,
    98,
    75,
    120,
    36.5,
    []
)

if check(
    "Multiple Patients Competing for Bed",
    "WAITING LIST" in result
):
    passed += 1
else:
    failed += 1


# Final Result

print()
print("======================")
print("Tests Passed:", passed)
print("Tests Failed:", failed)

if failed == 0:
    print("ALL TESTS PASSED")
else:
    print("SOME TESTS FAILED")