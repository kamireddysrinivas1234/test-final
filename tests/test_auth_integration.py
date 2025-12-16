def test_register_and_token(client):
    r = client.post("/api/auth/register", json={"username":"alice","email":"alice@example.com","password":"Password123!"})
    assert r.status_code == 201
    token = r.json()["access_token"]
    assert token

    # login via token endpoint (form)
    r2 = client.post("/api/auth/token", data={"username":"alice","password":"Password123!"})
    assert r2.status_code == 200
    assert "access_token" in r2.json()

def test_profile_update_and_password_change(client):
    r = client.post("/api/auth/register", json={"username":"bob","email":"bob@example.com","password":"Password123!"})
    token = r.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    me = client.get("/api/profile", headers=headers)
    assert me.status_code == 200
    assert me.json()["username"] == "bob"

    upd = client.put("/api/profile", headers=headers, json={"username":"bobby"})
    assert upd.status_code == 200
    assert upd.json()["username"] == "bobby"

    ch = client.post("/api/profile/change-password", headers=headers, json={"current_password":"Password123!","new_password":"NewPass123!"})
    assert ch.status_code == 200

    # old password should fail
    bad = client.post("/api/auth/token", data={"username":"bobby","password":"Password123!"})
    assert bad.status_code == 401

    good = client.post("/api/auth/token", data={"username":"bobby","password":"NewPass123!"})
    assert good.status_code == 200
