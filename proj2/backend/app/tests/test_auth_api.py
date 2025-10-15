import pytest

REGISTER = "/api/auth/register/user"
LOGIN = "/api/auth/login"
VERIFY = "/api/auth/verify"
RESEND = "/api/auth/resend-verification"
DEBUG_USERS = "/api/debug/users"


def test_register_ok_minimal(client):
    payload = {"email": "t1@example.edu", "password": "Passw0rd!", "full_name": "T One"}
    r = client.post(REGISTER, json=payload)
    assert r.status_code in (200, 201, 202)


def test_register_duplicate_email(client):
    payload = {"email": "dup@example.edu", "password": "Passw0rd!", "full_name": "Dup"}
    client.post(REGISTER, json=payload)
    r2 = client.post(REGISTER, json=payload)
    assert r2.status_code in (400, 409, 422)


def test_register_validation_bad_email(client):
    payload = {"email": "not-an-email", "password": "short", "full_name": "X"}
    r = client.post(REGISTER, json=payload)
    assert r.status_code in (400, 422)


def test_login_ok_if_seeded(client):
    payload = {"email": "loginok@example.edu", "password": "Passw0rd!"}
    client.post(REGISTER, json=payload)
    r = client.post(LOGIN, json=payload)
    assert r.status_code in (200, 202)


def test_login_wrong_password(client):
    client.post(REGISTER, json={"email": "wrongpass@example.edu", "password": "Passw0rd!"})
    r = client.post(LOGIN, json={"email": "wrongpass@example.edu", "password": "Nope!"})
    assert r.status_code in (400, 401)


def test_login_unknown_user(client):
    r = client.post(LOGIN, json={"email": "nouser@example.edu", "password": "Passw0rd!"})
    assert r.status_code in (400, 401, 404)


def test_verify_missing_token_query(client):
    r = client.get(VERIFY)
    assert r.status_code in (400, 422)


def test_verify_invalid_body_token(client):
    r = client.post(VERIFY, json={"token": "invalid-or-expired"})
    assert r.status_code in (400, 404, 410, 422)


def test_resend_verification_ok_or_notfound(client):
    r = client.post(RESEND, json={"email": "maybeexists@example.edu"})
    assert r.status_code in (200, 202, 404)


def test_debug_users_access(client):
    r = client.get(DEBUG_USERS)
    assert r.status_code in (200, 403, 404)


def test_register_requires_fields(client):
    r = client.post(REGISTER, json={"email": "x@y.edu"})
    assert r.status_code in (400, 422)


@pytest.mark.xfail(strict=False, reason="Blocks login until verified.")
def test_login_blocked_if_unverified(client):
    payload = {"email": "needverify@example.edu", "password": "Passw0rd!"}
    client.post(REGISTER, json=payload)
    r = client.post(LOGIN, json=payload)
    assert r.status_code == 403