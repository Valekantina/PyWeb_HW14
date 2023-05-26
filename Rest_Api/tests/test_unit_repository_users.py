import datetime
import unittest
from unittest.mock import MagicMock


from sqlalchemy.orm import Session

from src.database.models import Contact, User
from src.schemas import UserModel
from src.repository.users import (
    get_user_by_email,
    create_user,
    update_token,
    confirmed_email,
    update_avatar,
)


class TestUsers(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        """
        The setUp function is called before each test function.
        It creates a new session and user object for each test.
        
        :param self: Represent the instance of the class
        :return: A magicmock object
        :doc-author: Trelent
        """
        self.session = MagicMock(spec=Session)
        self.user = User(
            id=1,
            username='NewUser',
            email='newuser@gmail.com',
            password='1597536482',
            confirmed=True,
        )
        self.contact_test = Contact(
            id=1,
            first_name='Luffy',
            last_name='MonkeyD',
            email='strawhatcaptain@meta.ua',
            phone='+3057218410',
            date_of_birth=datetime.date(year=1994, month=5, day=5),
        )

    async def test_get_user_by_email(self):
        """
        The test_get_user_by_email function tests the get_user_by_email function.
            It does this by mocking out the database session and returning a user object.
            The test then asserts that the result of calling get_user_by_email is equal to our mocked user.
        
        :param self: Refer to the instance of the class
        :return: The user object
        :doc-author: Trelent
        """
        user = self.user
        self.session.query().filter().first.return_value = user
        result = await get_user_by_email(email=self.user.email, db=self.session)
        self.assertEqual(result, user)

    async def test_create_user(self):
        """
        The test_create_user function tests the create_user function.
            It creates a new user and checks that the username, email, password and id are correct.
        
        :param self: Make the method a bound method, which means that it can be called on an object and
        :return: The user in the database
        :doc-author: Trelent
        """
        body = UserModel(
            username=self.user.username,
            email=self.user.email,
            password=self.user.password,
        )
        result = await create_user(body=body, db=self.session)

        self.assertEqual(result.username, body.username)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.password, body.password)
        self.assertTrue(hasattr(result, "id"))

    async def test_confirmed_email(self):
        """
        The test_confirmed_email function tests the confirmed_email function in the user.py file.
            The test_confirmed_email function is a coroutine that takes two arguments: self and email, which is set to 
            self.user.email (the email of the user). It then calls await on confirmed_email with two arguments: 
            email=self.user(the user's email) and db=self(a session object). Finally, it asserts that result is None.
        
        :param self: Access the attributes and methods of the class
        :return: None
        :doc-author: Trelent
        """
        result = await confirmed_email(email=self.user.email, db=self.session)
        self.assertIsNone(result)

    async def test_update_token(self):
        """
        The test_update_token function tests the update_token function.
            The test_update_token function is a coroutine that takes in a user and token,
            and updates the user's token to be equal to the given token.  If no new token is given,
            then it sets it to None.
        
        :param self: Refer to the object itself
        :return: None
        :doc-author: Trelent
        """
        user = self.user
        token = None
        result = await update_token(user=user, token=token, db=self.session)
        self.assertIsNone(result)

    async def test_update_avatar(self):
        """
        The test_update_avatar function tests the update_avatar function.
            It does so by creating a new user, and then updating that user's avatar url to a new one.
            The test passes if the result of calling update_avatar is equal to the expected value.
        
        :param self: Access the instance variables and methods of a class
        :return: The following error:
        :doc-author: Trelent
        """
        new_avatar_url = 'https://res.cloudinary.com/dspp4i41l/image/upload/c_fill,h_250,w_250/v1684086359/RestApi/NewUser'
        get_user_by_email_mock = self.session.query().filter().first
        get_user_by_email_mock.return_value = self.user
        result = await update_avatar(email=self.user.email, url=new_avatar_url, db=self.session)
        self.assertEqual(result.avatar, new_avatar_url)


if __name__ == '__main__':
    unittest.main()
