def test_root_ok(client):
    r = client.get("/")
    assert r.status_code in (200, 204)
    if r.headers.get("content-type", "").startswith("application/json"):
        assert isinstance(r.json(), (dict, list))


def test_health_ok(client):
    r = client.get("/health")
    assert r.status_code in (200, 204)