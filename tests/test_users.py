import pytest
from jose import jwt
from app.main import app
from app import schemas
from app.config import settings


# make sure you add __init__.py for the interpreter to see tests as a module 
# and prevent "no module found named app" error from occuring

# def test_root(client):
#     res = client.get("/")
#     print(res.json().get("message"))


def test_create_user(client):
    res = client.post(
        "/users", json={"email": "hello123@gmail.com", "password": "password123"})

    new_user = schemas.UserOut(**res.json()) # verify using the pydantic schema
    assert new_user.email == "hello123@gmail.com"
    assert res.status_code == 201


def test_login_user(test_user, client):
    res = client.post(
        "/login", data={"username": test_user['email'], "password": test_user['password']})
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token,
                         settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    id = payload.get("user_id")
    assert id == str(test_user['id'])
    assert login_res.token_type == "bearer"
    assert res.status_code == 200


@pytest.mark.parametrize("email, password, status_code", [
    ('wrongemail@gmail.com', 'password123', 403),
    ('sanjeev@gmail.com', 'wrongpassword', 403),
    ('wrongemail@gmail.com', 'wrongpassword', 403),
    (None, 'password123', 422),
    ('sanjeev@gmail.com', None, 422)
])
def test_incorrect_login(test_user, client, email, password, status_code):
    res = client.post(
        "/login", data={"username": email, "password": password})

    assert res.status_code == status_code
    print("~~~~~~~~~~~~~~~~This is the last test of the test_users.py file~~~~~~~~~~~~~~~~~~~")
    # assert res.json().get('detail') == 'Invalid Credentials'