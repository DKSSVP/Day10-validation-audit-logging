from pipeline_logger import process_candidate


# ============================================================
# DAY 10 - 10 SYNTHETIC CANDIDATES
# ============================================================

candidates = [

    # 1 - Valid PAN + Valid DOB
    {
        "candidate_id": "CAND-001",
        "name": "Damodhara Prasad",
        "email": "damodhara.prasad@craftechco.co",
        "role": "GenAI Engineer",
        "pan": "ABCDE1234F",
        "dob": "24-11-2002"
    },

    # 2 - Valid PAN + Valid DOB
    {
        "candidate_id": "CAND-002",
        "name": "Ravi Teja",
        "email": "ravi.teja@craftechco.co",
        "role": "GenAI Engineer",
        "pan": "PQRSX5678L",
        "dob": "23-10-2002"
    },

    # 3 - Invalid PAN + Valid DOB
    {
        "candidate_id": "CAND-003",
        "name": "Sudheer Kumar",
        "email": "sudheer.kumar@craftechco.co",
        "role": "Scrum Master",
        "pan": "ABC123",
        "dob": "10-01-2001"
    },

    # 4 - Valid PAN + Invalid DOB
    {
        "candidate_id": "CAND-004",
        "name": "Akhila Kethireddy",
        "email": "akhila.kethireddy@craftechco.co",
        "role": "Lead GenAI Engineer",
        "pan": "FGHIJ1234K",
        "dob": "2001/10/10"
    },

    # 5 - Invalid PAN + Invalid DOB
    {
        "candidate_id": "CAND-005",
        "name": "Ravi Kiran",
        "email": "ravi.kiran@craftechco.co",
        "role": "Lead GenAI Engineer",
        "pan": "INVALID",
        "dob": "invalid-date"
    },

    # 6 - Valid PAN + Valid DOB
    {
        "candidate_id": "CAND-006",
        "name": "Karthik Reddy",
        "email": "karthik.reddy@craftechco.co",
        "role": "Jr Sales Executive",
        "pan": "LMNOP4321Q",
        "dob": "25-12-1998"
    },

    # 7 - Missing PAN + Valid DOB
    {
        "candidate_id": "CAND-007",
        "name": "Siva Prasad",
        "email": "siva.prasad@craftechco.co",
        "role": "Jr Sales Executive",
        "pan": "",
        "dob": "05-06-2002"
    },

    # 8 - Valid PAN + Missing DOB
    {
        "candidate_id": "CAND-008",
        "name": "Soundarya K",
        "email": "soundarya.k@craftechco.co",
        "role": "Jr SAP Consultant",
        "pan": "RSTUV9876W",
        "dob": ""
    },

    # 9 - Valid PAN + Valid DOB
    {
        "candidate_id": "CAND-009",
        "name": "Srinivas Reddy",
        "email": "srinivas.reddy@craftechco.co",
        "role": "Jr SAP Consultant",
        "pan": "WXYZA2468B",
        "dob": "30-09-1997"
    },

    # 10 - Invalid PAN + Invalid DOB
    {
        "candidate_id": "CAND-010",
        "name": "Sai Prasanna",
        "email": "sai.prasanna@craftechco.co",
        "role": "HR Executive",
        "pan": "12345ABCDE",
        "dob": "31/31/2020"
    }
]


# ============================================================
# RUN ALL 10 CANDIDATES
# ============================================================

print()
print("=" * 60)
print("DAY 10 - 10 CANDIDATE VALIDATION TEST")
print("=" * 60)

results = []

for candidate in candidates:

    result = process_candidate(candidate)

    results.append({
        "candidate_id": candidate["candidate_id"],
        "result": "PASS" if result else "FAIL"
    })


# ============================================================
# FINAL SUMMARY
# ============================================================

print()
print("=" * 60)
print("DAY 10 TEST SUMMARY")
print("=" * 60)

for result in results:
    print(
        f"{result['candidate_id']} -> "
        f"{result['result']}"
    )

print("=" * 60)
print(f"Total candidates processed: {len(results)}")
print(
    f"Successful candidates: "
    f"{sum(1 for r in results if r['result'] == 'PASS')}"
)
print(
    f"Failed candidates: "
    f"{sum(1 for r in results if r['result'] == 'FAIL')}"
)
print("=" * 60)