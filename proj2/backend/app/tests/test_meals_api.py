import pytest

MEALS = "/api/meals/"
MY_LISTINGS = "/api/meals/my/listings"
MEAL_BY_ID = "/api/meals/{meal_id}"


def test_list_meals_ok(client):
    r = client.get(MEALS)
    assert r.status_code == 200
    assert isinstance(r.json(), (list, dict))


def test_list_meals_with_filters(client):
    r = client.get(MEALS, params={"is_vegetarian": "true", "q": "pizza"})
    assert r.status_code == 200


def test_list_meals_pagination(client):
    r = client.get(MEALS, params={"skip": 0, "limit": 5})
    assert r.status_code == 200


def test_get_meal_not_found(client):
    r = client.get(MEAL_BY_ID.format(meal_id="000000000000000000000000"))
    assert r.status_code in (404, 422)


def test_create_meal_unauthorized(client, meal_payload):
    r = client.post(MEALS, json=meal_payload)
    assert r.status_code in (401, 403)


@pytest.mark.xfail(strict=False, reason="Requires valid Bearer token.")
def test_create_meal_ok(client, auth_header, meal_payload):
    r = client.post(MEALS, headers=auth_header, json=meal_payload)
    assert r.status_code in (200, 201)


def test_create_meal_validation_error(client):
    bad = {"title": 123, "quantity": -1}
    r = client.post(MEALS, json=bad)
    assert r.status_code in (400, 422)


def test_my_listings_unauthorized(client):
    r = client.get(MY_LISTINGS)
    assert r.status_code in (401, 403)


@pytest.mark.xfail(strict=False, reason="Requires auth and seeded meals.")
def test_my_listings_ok(client, auth_header):
    r = client.get(MY_LISTINGS, headers=auth_header)
    assert r.status_code == 200
    assert isinstance(r.json(), (list, dict))


@pytest.mark.xfail(strict=False, reason="Create first, then GET by id. Needs auth.")
def test_create_then_get_meal(client, auth_header, meal_payload):
    r1 = client.post(MEALS, headers=auth_header, json=meal_payload)
    assert r1.status_code in (200, 201)
    created = r1.json()
    meal_id = created.get("id") or created.get("_id") or created.get("meal_id")
    assert meal_id
    r2 = client.get(MEAL_BY_ID.format(meal_id=meal_id))
    assert r2.status_code == 200


def test_update_meal_unauthorized(client, update_meal_payload):
    r = client.put(MEAL_BY_ID.format(meal_id="deadbeefdeadbeefdeadbeef"), json=update_meal_payload)
    assert r.status_code in (401, 403)


@pytest.mark.xfail(strict=False, reason="Owner check & auth required.")
def test_update_meal_for_owner_ok(client, auth_header, update_meal_payload, meal_payload):
    c = client.post(MEALS, headers=auth_header, json=meal_payload)
    assert c.status_code in (200, 201)
    meal_id = (c.json().get("id") or c.json().get("_id"))
    u = client.put(MEAL_BY_ID.format(meal_id=meal_id), headers=auth_header, json=update_meal_payload)
    assert u.status_code in (200, 204)


@pytest.mark.xfail(strict=False, reason="Should 403 if not owner.")
def test_update_meal_wrong_owner_forbidden(client, auth_header, update_meal_payload):
    r = client.put(MEAL_BY_ID.format(meal_id="someoneelses"), headers=auth_header, json=update_meal_payload)
    assert r.status_code in (403, 404)


def test_delete_meal_unauthorized(client):
    r = client.delete(MEAL_BY_ID.format(meal_id="deadbeefdeadbeefdeadbeef"))
    assert r.status_code in (401, 403)


@pytest.mark.xfail(strict=False, reason="Owner check & auth required.")
def test_delete_meal_owner_ok(client, auth_header, meal_payload):
    c = client.post(MEALS, headers=auth_header, json=meal_payload)
    assert c.status_code in (200, 201)
    meal_id = (c.json().get("id") or c.json().get("_id"))
    d = client.delete(MEAL_BY_ID.format(meal_id=meal_id), headers=auth_header)
    assert d.status_code in (200, 204)


def test_filters_combo_ok(client):
    r = client.get(MEALS, params={"q": "pasta", "is_vegan": "true", "limit": 3, "skip": 0})
    assert r.status_code == 200