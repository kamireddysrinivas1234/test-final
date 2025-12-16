def _register(client, username="c1"):
    r = client.post("/api/auth/register", json={"username":username,"email":f"{username}@example.com","password":"Password123!"})
    token = r.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_create_calc_and_history(client):
    headers = _register(client, "calcuser")
    r = client.post("/api/calculations", headers=headers, json={"a":10,"b":3,"op":"mod"})
    assert r.status_code == 201
    assert r.json()["result"] == 1.0

    hist = client.get("/api/calculations", headers=headers)
    assert hist.status_code == 200
    assert len(hist.json()) >= 1

def test_reports_stats(client):
    headers = _register(client, "repuser")
    client.post("/api/calculations", headers=headers, json={"a":2,"b":4,"op":"pow"})
    client.post("/api/calculations", headers=headers, json={"a":10,"b":5,"op":"div"})
    stats = client.get("/api/reports/stats", headers=headers)
    assert stats.status_code == 200
    data = stats.json()
    assert data["total"] == 2
