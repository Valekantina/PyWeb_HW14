from unittest.mock import MagicMock

from src.database.models import User


def test_create_user(client, user, monkeypatch):
    """
    The test_create_user function tests the /api/auth/signup endpoint.
    It does so by making a POST request to the endpoint with a JSON payload containing user data.
    The test asserts that the response status code is 201, which indicates that a new resource was created successfully.
    It also asserts that the email address in the response matches what we sent in our request and that an id was returned.
    
    :param client: Make requests to the api
    :param user: Pass the user data to the test function
    :param monkeypatch: Mock the send_email function
    :return: The response of the post request
    :doc-author: Trelent
    """
    mock_send_email = MagicMock()
    monkeypatch.setattr('src.routes.auth.send_email', mock_send_email)
    response = client.post(
        '/api/auth/signup',
        json=user,
    )
    assert response.status_code == 201, response.text
    data = response.json()
    assert data['user']['email'] == user.get('email')
    assert 'id' in data['user']


def test_repeat_create_user(client, user):
    """
    The test_repeat_create_user function tests that a user cannot be created twice.
        It does this by creating a user, then attempting to create the same user again.
        The second attempt should fail with an HTTP 409 status code and an error message.
    
    :param client: Make requests to the api
    :param user: Pass the user object to the test function
    :return: The status code 409, which means that the request was understood but it cannot be processed
    :doc-author: Trelent
    """
    response = client.post(
        '/api/auth/signup',
        json=user,
    )
    assert response.status_code == 409, response.text
    data = response.json()
    assert data['detail'] == 'Account already exists'


def test_login_user_not_confirmed(client, user):
    """
    The test_login_user_not_confirmed function tests that a user cannot login if they have not confirmed their email.
    
    
    :param client: Make requests to the application
    :param user: Create a user in the database
    :return: A 401 response
    :doc-author: Trelent
    """
    response = client.post(
        '/api/auth/login',
        data={'username': user.get('email'), 'password': user.get('password')},
    )
    assert response.status_code == 401, response.text
    data = response.json()
    assert data['detail'] == 'Email not confirmed'


def test_login_user(client, session, user):
    """
    The test_login_user function tests the login functionality of the application.
    It first creates a user and then logs in with that user's credentials.
    
    
    :param client: Create a test client for the flask application
    :param session: Access the database
    :param user: Get the user data from the fixture
    :return: A 200 status code, the token_type is a bearer
    :doc-author: Trelent
    """
    current_user: User = session.query(User).filter(User.email == user.get('email')).first()
    current_user.confirmed = True
    session.commit()
    response = client.post(
        '/api/auth/login',
        data={'username': user.get('email'), 'password': user.get('password')},
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data['token_type'] == 'bearer'


def test_login_wrong_password(client, user):
    """
    The test_login_wrong_password function tests that a user cannot login with an incorrect password.
    
    :param client: Make a request to the server
    :param user: Create a user object that is used in the test_login_wrong_password function
    :return: A 401 status code and a message that the password is invalid
    :doc-author: Trelent
    """
    response = client.post(
        '/api/auth/login',
        data={'username': user.get('email'), 'password': 'password'},
    )
    assert response.status_code == 401, response.text
    data = response.json()
    assert data['detail'] == 'Invalid password'


def test_login_wrong_email(client, user):
    """
    The test_login_wrong_email function tests that a user cannot login with an invalid email.
    
    :param client: Make requests to the flask application
    :param user: Pass the user data to the function
    :return: The response
    :doc-author: Trelent
    """
    response = client.post(
        '/api/auth/login',
        data={'username': 'email', 'password': user.get('password')},
    )
    assert response.status_code == 401, response.text
    data = response.json()
    assert data['detail'] == 'Invalid email'
