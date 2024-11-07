import pytest
import requests


@pytest.fixture
def endpoint_url(base_url):
    return base_url + '/posts'


def test_get_method_posts_endoint(endpoint_url):

    response = requests.get(endpoint_url)
    assert response.status_code == 200
    assert type(response.json()) == list
    assert len(response.json()) > 0
    for post in response.json():
        assert 'userId' in post
        assert 'id' in post
        assert 'title' in post
        assert 'body' in post

        assert isinstance(post['userId'], int)
        assert isinstance(post['id'], int)
        assert isinstance(post['title'], str) and post['title'].strip() != ''
        assert isinstance(post['body'], str) and post['body'].strip() != ''


def test_post_method_posts_endpoint(endpoint_url):

    data = {
        'title': 'test_post',
        'body': 'test_body',
        'userId': 42
    }
    response = requests.post(endpoint_url, json=data)
    assert response.status_code == 201
    assert response.json()['title'] == data['title']
    assert response.json()['body'] == data['body']
    assert response.json()['userId'] == data['userId']

    new_post_id = response.json()['id']

    response = requests.get(endpoint_url)
    assert response.status_code == 200
    posts = response.json()
    assert any(
        (post['id'] == new_post_id) 
        and (post['title'] == data['title']) 
        and (post['body'] == data['body']) 
        and (post['userId'] == data['userId']) 
        for post in posts
        ), f"New post with id: {new_post_id} and attached data was not found in the list of posts."
    

def test_put_method_posts_endpoint(endpoint_url):

    post_id = 22
    response = requests.get(f"{endpoint_url}/{post_id}")
    assert response.status_code == 200
    post_data = response.json()

    updated_data = {
        'title': 'updated_test_title',
        'body': 'updated_test_body',
        'userId': post_data['userId']
    }

    response = requests.put(f"{endpoint_url}/{post_id}", json=updated_data)
    assert response.status_code == 200
    assert response.json()['title'] == updated_data['title']
    assert response.json()['body'] == updated_data['body']
    assert response.json()['userId'] == updated_data['userId']

    response = requests.get(f"{endpoint_url}/{post_id}")
    assert response.status_code == 200
    updated_post = response.json()
    assert updated_post['title'] == updated_data['title']
    assert updated_post['body'] == updated_data['body']
    assert updated_post['userId'] == updated_data['userId']


def test_delete_method_posts_endpoint(endpoint_url):

    post_id = 22
    response = requests.delete(f"{endpoint_url}/{post_id}")
    assert response.status_code == 200

    response = requests.get(f"{endpoint_url}/{post_id}")
    assert response.status_code == 404, \
        f"Post with id: {post_id} was not deleted even though delete request returned code 200."
    assert response.json() == {}
