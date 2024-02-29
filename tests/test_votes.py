import pytest
from app import models


'''
This fixture creates a dummy vote useful for when we need to test out a vote after a vote
Deleting a vote. Functions where the **test_vote** fixture is called are:-
    ***def test_vote_twice_post()*** 
                &&
    ***def test_delete_vote()*** 
The reason we use fixtures like these is because the scope is limited to each function and we wan't each
test to run independently of each other i.e. the session and client fixtures 
creates tables then we run the test function and then the tables are dropped 
so that each test function gets a clean state. We have also setup a test db
'''
@pytest.fixture()
def test_vote(test_posts, session, test_user):
    new_vote = models.Votes(post_id=test_posts[3].id, user_id=test_user['id'])
    session.add(new_vote)
    session.commit()


def test_vote_on_post(authorized_client, test_posts):
    res = authorized_client.post(
        "/vote", json={"post_id": test_posts[3].id, "dir": 1})
    assert res.status_code == 201


def test_vote_twice_post(authorized_client, test_posts, test_vote):
    res = authorized_client.post(
        "/vote", json={"post_id": test_posts[3].id, "dir": 1})
    assert res.status_code == 409


def test_delete_vote(authorized_client, test_posts, test_vote):
    res = authorized_client.post(
        "/vote", json={"post_id": test_posts[3].id, "dir": 0})
    assert res.status_code == 201


def test_delete_vote_non_exist(authorized_client, test_posts):
    res = authorized_client.post(
        "/vote", json={"post_id": test_posts[3].id, "dir": 0})
    assert res.status_code == 404


def test_vote_post_non_exist(authorized_client, test_posts):
    res = authorized_client.post(
        "/vote", json={"post_id": 80000, "dir": 1})
    assert res.status_code == 404


def test_vote_unauthorized_user(client, test_posts):
    res = client.post(
        "/vote", json={"post_id": test_posts[3].id, "dir": 1})
    assert res.status_code == 401