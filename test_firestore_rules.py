import os
import uuid
import time
import pytest
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Monkey-patch requests.post to add robust retries for transient Google API connection drops
session = requests.Session()
retry = Retry(connect=5, read=5, backoff_factor=0.5, status_forcelist=[500, 502, 503, 504])
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)

_original_post = requests.post
def _robust_post(*args, **kwargs):
    for attempt in range(5):
        try:
            return session.post(*args, **kwargs)
        except requests.exceptions.ConnectionError:
            if attempt == 4:
                raise
            time.sleep(2 ** attempt)

requests.post = _robust_post

_original_get = requests.get
def _robust_get(*args, **kwargs):
    for attempt in range(5):
        try:
            return session.get(*args, **kwargs)
        except requests.exceptions.ConnectionError:
            if attempt == 4:
                raise
            time.sleep(2 ** attempt)

requests.get = _robust_get

from app.core.auth import sign_up_with_email_password, sign_in_with_email_password, send_password_reset_email
from app.core.firestore import create_document, get_document

def test_firebase_full_matrix():
    # 1. Email/password signup
    email_a = f"test_a_{uuid.uuid4().hex[:8]}@example.com"
    pw_a = "ValidPassword123!"
    result_a = sign_up_with_email_password(email_a, pw_a, "Test User A")
    assert "localId" in result_a
    assert "idToken" in result_a
    uid_a = result_a["localId"]
    token_a = result_a["idToken"]

    # 4. Duplicate email
    try:
        sign_up_with_email_password(email_a, "AnotherPassword456", "Test User A Duplicate")
        pytest.fail("Security failure: Duplicate email allowed.")
    except Exception as e:
        assert "EMAIL_EXISTS" in str(e)

    # 2. Email/password login
    login_result = sign_in_with_email_password(email_a, pw_a)
    assert login_result["localId"] == uid_a

    # 3. Invalid password
    try:
        sign_in_with_email_password(email_a, "WrongPassword!!!")
        pytest.fail("Security failure: Invalid password login allowed.")
    except Exception as e:
        assert "INVALID_LOGIN_CREDENTIALS" in str(e) or "INVALID_PASSWORD" in str(e)

    # 5. Password reset
    try:
        reset_res = send_password_reset_email(email_a)
        assert reset_res is True
    except Exception as e:
        pytest.fail(f"Password reset failed: {e}")

    # Setup User B for cross-user tests
    email_b = f"test_b_{uuid.uuid4().hex[:8]}@example.com"
    pw_b = "ValidPassword123!"
    result_b = sign_up_with_email_password(email_b, pw_b, "Test User B")
    uid_b = result_b["localId"]
    token_b = result_b["idToken"]

    collection_a = f"users/{uid_a}/tasks"
    doc_id = "test_task"

    # 9. Account A accessing Account A data -> allowed
    try:
        create_document(token_a, collection_a, doc_id, {"test": "data"})
    except Exception as e:
        pytest.fail(f"User A failed to write to their own collection: {e}")

    try:
        doc = get_document(token_a, collection_a, doc_id)
        assert doc is not None
        assert doc.get("test") == "data"
    except Exception as e:
        pytest.fail(f"User A failed to read their own collection: {e}")

    # 10. Account A accessing Account B data -> denied
    # (Testing User B accessing User A data)
    try:
        create_document(token_b, collection_a, "hacked_task", {"hacked": "data"})
        pytest.fail("Security failure: User B was able to write to User A's collection.")
    except Exception as e:
        assert "403" in str(e) or "Permission" in str(e) or "Missing or insufficient permissions" in str(e)

    try:
        doc = get_document(token_b, collection_a, doc_id)
        if doc and "error" in doc:
            pass
        else:
            pytest.fail("Security failure: User B was able to read User A's collection.")
    except Exception as e:
        assert "403" in str(e) or "Permission" in str(e) or "Missing or insufficient permissions" in str(e)

    # 11. Request without authentication token -> denied
    try:
        create_document("", collection_a, "anon_task", {"hacked": "data"})
        pytest.fail("Security failure: Unauthenticated user was able to write.")
    except Exception as e:
        assert "401" in str(e) or "403" in str(e) or "permission" in str(e).lower() or "unauthenticated" in str(e).lower() or "missing required authentication credential" in str(e).lower()

    try:
        doc = get_document("", collection_a, doc_id)
        if doc and "error" in doc:
            pass
        else:
            pytest.fail("Security failure: Unauthenticated user was able to read.")
    except Exception as e:
        assert "401" in str(e) or "403" in str(e) or "permission" in str(e).lower() or "unauthenticated" in str(e).lower() or "missing required authentication credential" in str(e).lower()

    # 12. Forged UID/path -> denied
    # Attempt to write to a completely different path not belonging to the user
    forged_collection = "system_config"
    try:
        create_document(token_a, forged_collection, "hacked_config", {"admin": True})
        pytest.fail("Security failure: User A wrote to forged path.")
    except Exception as e:
        assert "403" in str(e) or "permission" in str(e).lower() or "missing or insufficient permissions" in str(e).lower()

    print("All backend matrix tests passed successfully.")
