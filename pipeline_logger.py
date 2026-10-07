import os
import re
import requests

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from dotenv import load_dotenv


# ============================================================
# ENVIRONMENT CONFIGURATION
# ============================================================

load_dotenv()

SERVICE_ACCOUNT_FILE = (
    "recruitr-day10-audit-log-82f88-firebase-adminsdk-fbsvc-8365176395.json"
)

SHEETDB_API_URL = os.getenv("SHEETDB_API_URL")


# ============================================================
# FIREBASE INITIALIZATION
# ============================================================

if not firebase_admin._apps:
    credentials_object = credentials.Certificate(SERVICE_ACCOUNT_FILE)
    firebase_admin.initialize_app(credentials_object)

firestore_db = firestore.client()


# ============================================================
# PAN VALIDATION
# ============================================================

def validate_pan(pan):
    """
    Validate Indian PAN format.

    Expected format:
    ABCDE1234F
    """

    if not pan:
        return False, "PAN_MISSING"

    pan_pattern = r"^[A-Z]{5}[0-9]{4}[A-Z]$"

    if not re.fullmatch(pan_pattern, pan):
        return False, "PAN_INVALID_FORMAT"

    return True, ""


# ============================================================
# DOB VALIDATION
# ============================================================

def validate_dob(dob):
    """
    Validate DOB format.

    Expected format:
    DD-MM-YYYY
    """

    if not dob:
        return False, "DOB_MISSING"

    dob_pattern = r"^\d{2}-\d{2}-\d{4}$"

    if not re.fullmatch(dob_pattern, dob):
        return False, "DOB_INVALID_FORMAT"

    return True, ""


# ============================================================
# FIREBASE AUDIT LOGGER
# ============================================================

def write_validation_log(
    candidate_id,
    source_field,
    validation_status,
    error_type="",
    sheetdb_row_id=""
):
    """
    Write validation result to Firestore.

    Collection:
    validation_logs
    """

    log_data = {
        "candidate_id": candidate_id,
        "source_field": source_field,
        "validation_status": validation_status,
        "error_type": error_type,
        "sheetdb_row_id": sheetdb_row_id,
        "timestamp": firestore.SERVER_TIMESTAMP
    }

    firestore_db.collection("validation_logs").add(log_data)

    print(
        f"[Firebase] {candidate_id} | "
        f"{source_field} | "
        f"{validation_status} | "
        f"{error_type}"
    )


# ============================================================
# SHEETDB APPEND
# ============================================================

def append_to_sheetdb(candidate):
    """
    Append candidate data to SheetDB.

    Existing SheetDB columns:
    Name, Email, Role, Status
    """

    if not SHEETDB_API_URL:
        print("[SheetDB] SHEETDB_API_URL is not configured.")
        return False, ""

    payload = {
        "data": [
            {
                "Name": candidate.get("name", ""),
                "Email": candidate.get("email", ""),
                "Role": candidate.get("role", ""),
                "Status": "Verified"
            }
        ]
    }

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(
            SHEETDB_API_URL,
            json=payload,
            headers=headers,
            timeout=10
        )

        print(f"[SheetDB] HTTP Status: {response.status_code}")

        if response.status_code == 201:

            print("[SheetDB] Candidate appended successfully.")

            try:
                response_data = response.json()
                row_id = str(response_data.get("id", ""))
            except ValueError:
                row_id = ""

            return True, row_id

        print("[SheetDB] Candidate append failed.")
        print(f"[SheetDB] Response: {response.text}")

        return False, ""

    except requests.RequestException as error:

        print(f"[SheetDB] API/Network error: {error}")

        return False, ""


# ============================================================
# COMPLETE CANDIDATE PIPELINE
# ============================================================

def process_candidate(candidate):
    """
    Complete Day 10 candidate processing flow.

    1. Validate PAN.
    2. Log PAN validation.
    3. Validate DOB.
    4. Log DOB validation.
    5. If both pass, send candidate to SheetDB.
    6. Log SheetDB result in Firebase.
    """

    candidate_id = candidate["candidate_id"]

    print()
    print("=" * 60)
    print(f"[Pipeline] Processing candidate: {candidate_id}")
    print("=" * 60)

    # --------------------------------------------------------
    # PAN validation
    # --------------------------------------------------------

    pan_valid, pan_error = validate_pan(
        candidate.get("pan")
    )

    if pan_valid:
        print("[Validation] PAN: PASS")
    else:
        print(f"[Validation] PAN: FAIL -> {pan_error}")

    write_validation_log(
        candidate_id=candidate_id,
        source_field="PAN",
        validation_status="pass" if pan_valid else "fail",
        error_type=pan_error
    )

    # --------------------------------------------------------
    # DOB validation
    # --------------------------------------------------------

    dob_valid, dob_error = validate_dob(
        candidate.get("dob")
    )

    if dob_valid:
        print("[Validation] DOB: PASS")
    else:
        print(f"[Validation] DOB: FAIL -> {dob_error}")

    write_validation_log(
        candidate_id=candidate_id,
        source_field="DOB",
        validation_status="pass" if dob_valid else "fail",
        error_type=dob_error
    )

    # --------------------------------------------------------
    # Validation gate
    # --------------------------------------------------------

    if not pan_valid or not dob_valid:

        print("[Pipeline] Validation failed.")
        print("[Pipeline] SheetDB append skipped.")

        return False

    # --------------------------------------------------------
    # SheetDB append
    # --------------------------------------------------------

    print("[Pipeline] Validation passed.")
    print("[Pipeline] Sending candidate to SheetDB...")

    sheetdb_success, sheetdb_row_id = append_to_sheetdb(
        candidate
    )

    # --------------------------------------------------------
    # Firebase SheetDB audit log
    # --------------------------------------------------------

    if sheetdb_success:

        print("[Pipeline] SheetDB operation: SUCCESS")

        write_validation_log(
            candidate_id=candidate_id,
            source_field="SheetDB",
            validation_status="pass",
            error_type="",
            sheetdb_row_id=sheetdb_row_id
        )

        return True

    else:

        print("[Pipeline] SheetDB operation: FAILED")

        write_validation_log(
            candidate_id=candidate_id,
            source_field="SheetDB",
            validation_status="fail",
            error_type="SHEETDB_APPEND_FAILED",
            sheetdb_row_id=""
        )

        return False