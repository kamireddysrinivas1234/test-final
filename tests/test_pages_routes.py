def test_pages_render(client):
    # These routes render the front-end templates.
    r = client.get("/")
    assert r.status_code == 200
    assert "Calculator" in r.text or "calculator" in r.text

    r = client.get("/login")
    assert r.status_code == 200
    assert "Login" in r.text or "login" in r.text

    r = client.get("/register")
    assert r.status_code == 200
    assert "Register" in r.text or "register" in r.text

    r = client.get("/profile")
    assert r.status_code == 200
    assert "Profile" in r.text or "profile" in r.text
