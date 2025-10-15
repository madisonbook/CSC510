import pytest

ME = "/api/users/me"
ME_DIET = "/api/users/me/dietary-preferences"
ME_SOCIAL = "/api/users/me/social-media"
ME_STATS = "/api/users/me/stats"
USER_BY_ID = "/api/users/{user_id}"


def test_me_requires_auth(client):
    r = client.get(ME)
    assert r.status_code in (401, 403)


@pytest.mark.xfail(strict=False, reason="Requires valid Bearer JWT.")
def test_me_ok_when_authed(client, auth_header):
    r = client.get(ME, headers=auth_header)
    assert r.status_code == 200
    assert isinstance(r.json(), dict)


def test_update_me_unauth(client, profile_update_payload):
    r = client.put(ME, json=profile_update_payload)
    assert r.status_code in (401, 403)


@pytest.mark.xfail(strict=False, reason="Requires valid auth & body schema.")
def test_update_me_ok(client, auth_header, profile_update_payload):
    r = client.put(ME, headers=auth_header, json=profile_update_payload)
    assert r.status_code in (200, 204)


def test_update_dietary_prefs_unauth(client, dietary_prefs_payload):
    r = client.put(ME_DIET, json=dietary_prefs_payload)
    assert r.status_code in (401, 403)


@pytest.mark.xfail(strict=False, reason="Requires valid auth.")
def test_update_dietary_prefs_ok(client, auth_header, dietary_prefs_payload):
    r = client.put(ME_DIET, headers=auth_header, json=dietary_prefs_payload)
    assert r.status_code in (200, 204)


def test_update_social_links_unauth(client, social_links_payload):
    r = client.put(ME_SOCIAL, json=social_links_payload)
    assert r.status_code in (401, 403)


@pytest.mark.xfail(strict=False, reason="Requires valid auth.")
def test_update_social_links_ok(client, auth_header, social_links_payload):
    r = client.put(ME_SOCIAL, headers=auth_header, json=social_links_payload)
    assert r.status_code in (200, 204)


def test_me_stats_unauth(client):
    r = client.get(ME_STATS)
    assert r.status_code in (401, 403)


def test_get_user_by_id_not_found(client):
    r = client.get(USER_BY_ID.format(user_id="000000000000000000000000"))
    assert r.status_code in (404, 422)