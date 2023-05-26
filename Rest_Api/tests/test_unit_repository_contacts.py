import datetime
import unittest
from unittest.mock import MagicMock
from datetime import date

from sqlalchemy.orm import Session

from src.database.models import Contact, User
from src.schemas import ContactModel
from src.repository.contacts import (
    get_contact_by_id,
    get_contacts,
    get_contacts_birthdays,
    create_contact,
    update_contact,
    remove_contact,
)


class TestContacts(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        """
        The setUp function is called before each test function.
        It creates a new session and user object, as well as a contact object with the following attributes:
        id = 1, first_name = 'Luffy', last_name = 'MonkeyD', email='strawhatcaptain@meta.ua', phone='+3057218410'
        
        :param self: Represent the instance of the object that calls this method
        :return: A new instance of the contact class with a set of parameters
        :doc-author: Trelent
        """
        self.session = MagicMock(spec=Session)
        self.user = User(id=1)
        self.contact_test = Contact(
            id=1,
            first_name='Luffy',
            last_name='MonkeyD',
            email='strawhatcaptain@meta.ua',
            phone='+3057218410',
            date_of_birth=datetime.date(year=1994, month=5, day=5),
        )

    async def test_get_contacts(self):
        """
        The test_get_contacts function tests the get_contacts function.
            It does this by mocking out the database session and returning a list of contacts.
            The test then asserts that the result is equal to what was returned from the mocked database.
        
        :param self: Access the instance of the class
        :return: The contacts list
        :doc-author: Trelent
        """
        contacts = [self.contact_test, Contact(), Contact()]
        self.session.query().filter().offset().limit().all.return_value = contacts
        result = await get_contacts(skip=0, limit=10, first_name='', last_name='', email='', user=self.user, db=self.session)
        self.assertEqual(result, contacts)

    async def test_get_contacts_filter_by_first_name(self):
        """
        The test_get_contacts_filter_by_first_name function tests the get_contacts function by passing in a first name and checking that the result is equal to contacts.
        
        
        :param self: Represent the instance of the class
        :return: Contacts
        :doc-author: Trelent
        """
        contacts = [self.contact_test, Contact(), Contact()]
        self.session.query().filter().all.return_value = contacts
        result = await get_contacts(skip=0, limit=10, first_name=self.contact_test.first_name, last_name='', email='', user=self.user, db=self.session)
        self.assertEqual(result, contacts)

    async def test_get_contacts_filter_by_last_name(self):
        """
        The test_get_contacts_filter_by_last_name function tests the get_contacts function by passing in a last name to filter by.
        The test passes if the result is equal to contacts.
        
        :param self: Represent the instance of the class
        :return: A list of contacts
        :doc-author: Trelent
        """
        contacts = [self.contact_test, Contact(), Contact()]
        self.session.query().filter().all.return_value = contacts
        result = await get_contacts(skip=0, limit=10, first_name='', last_name=self.contact_test.last_name, email='', user=self.user, db=self.session)
        self.assertEqual(result, contacts)

    async def test_get_contacts_filter_by_email(self):
        """
        The test_get_contacts_filter_by_email function tests the get_contacts function with a filter by email.
            The test_get_contacts_filter_by_email function creates a list of contacts, and then sets the return value of 
            self.session.query().filter().all to be that list of contacts (this is done so that we can test what happens when 
            there are multiple results returned from the database). Then, it calls get_contacts with an email parameter set to 
            self.contact's email attribute (which was set in setup), and asserts that result is equal to our list of contacts.
        
        :param self: Access the attributes and methods of the class
        :return: The list of contacts that match the email address
        :doc-author: Trelent
        """
        contacts = [self.contact_test, Contact(), Contact()]
        self.session.query().filter().all.return_value = contacts
        result = await get_contacts(skip=0, limit=10, first_name='', last_name='', email=self.contact_test.email, user=self.user, db=self.session)
        self.assertEqual(result, contacts)

    async def test_get_contact_by_id(self):
        """
        The test_get_contact_by_id function tests the get_contact_by_id function.
            It does this by mocking the session object and returning a list of contacts.
            The test then asserts that the result is equal to that list.
        
        :param self: Represent the instance of the object that is passed to the method when it is called
        :return: A list of contacts
        :doc-author: Trelent
        """
        contacts = [self.contact_test, Contact(), Contact()]
        self.session.query().filter().first.return_value = contacts
        result = await get_contact_by_id(contact_id=self.contact_test.id, user=self.user, db=self.session)
        self.assertEqual(result, contacts)

    async def test_create_contact(self):
        """
        The test_create_contact function tests the create_contact function in the contacts.py file.
        It creates a ContactModel object and passes it to the create_contact function, which should return a new contact with an id attribute.
        
        :param self: Represent the instance of the class
        :return: The result of the create_contact function
        :doc-author: Trelent
        """
        body = ContactModel(
            first_name=self.contact_test.first_name,
            last_name=self.contact_test.last_name,
            email=self.contact_test.email,
            phone=self.contact_test.email,
            date_of_birth=self.contact_test.date_of_birth,
        )
        result = await create_contact(body=body, db=self.session, user=self.user)
        self.assertEqual(result.first_name, body.first_name)
        self.assertEqual(result.last_name, body.last_name)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.phone, body.phone)
        self.assertEqual(result.date_of_birth, body.date_of_birth)
        self.assertTrue(hasattr(result, "id"))

    async def test_remove_contact(self):
        """
        The test_remove_contact function tests the remove_contact function.
            It does this by creating a mock contact, and then using that mock contact to test the remove_contact function.
            The test passes if the result of calling remove_contact is equal to our mock contact.
        
        :param self: Represent the instance of the class
        :return: The contact that was deleted
        :doc-author: Trelent
        """
        contact = self.contact_test
        self.session.query().filter().first.return_value = contact
        result = await remove_contact(contact_id=self.contact_test.id, db=self.session, user=self.user)
        self.assertEqual(result, contact)

    async def test_remove_contact_not_found(self):
        """
        The test_remove_contact_not_found function tests the remove_contact function when a contact is not found.
            The test_remove_contact_not_found function uses the mock library to mock out the session object and return None
            when querying for a contact.  It then calls remove_contact with an id that does not exist in the database, and
            asserts that it returns None.
        
        :param self: Represent the instance of the class
        :return: None
        :doc-author: Trelent
        """
        self.session.query().filter().first.return_value = None
        result = await remove_contact(contact_id=self.contact_test.id, db=self.session, user=self.user)
        self.assertIsNone(result)

    async def test_update_contact(self):
        """
        The test_update_contact function tests the update_contact function.
            It does this by creating a ContactModel object, and then passing it to the update_contact function.
            The test checks that the result of calling update_contact is equal to contact.
        
        :param self: Represent the instance of the class
        :return: The contact object
        :doc-author: Trelent
        """
        contact = self.contact_test
        body = ContactModel(
            first_name='Luffy',
            last_name=self.contact_test.last_name,
            email=self.contact_test.email,
            phone=self.contact_test.email,
            date_of_birth=self.contact_test.date_of_birth)
        self.session.query().filter().first.return_value = contact
        result = await update_contact(contact_id=self.contact_test.id, body=body, db=self.session, user=self.user)
        self.assertEqual(result, contact)

    async def test_update_contact_not_found(self):
        """
        The test_update_contact_not_found function tests the update_contact function when a contact is not found.
            The test_update_contact_not_found function uses the following parameters:
                self - A reference to the current instance of this class.
            The test_update_contact function returns nothing.
        
        :param self: Refer to the class itself
        :return: None, but the function returns a tuple
        :doc-author: Trelent
        """
        body = ContactModel(
            first_name='Luffy',
            last_name=self.contact_test.last_name,
            email=self.contact_test.email,
            phone=self.contact_test.email,
            date_of_birth=self.contact_test.date_of_birth)
        self.session.query().filter().first.return_value = None
        result = await update_contact(contact_id=self.contact_test.id, body=body, db=self.session, user=self.user)
        self.assertIsNone(result)

    async def test_get_contacts_birthdays(self):
        """
        The test_get_contacts_birthdays function tests the get_contacts_birthdays function.
        
        :param self: Represent the instance of the class
        :return: Contacts
        :doc-author: Trelent
        """
        today = date.today()
        contacts = [
            Contact(id=1, first_name='Luffy', last_name='Monkey',
                    email='strawhatcaptain@meta.ua', date_of_birth=today),
            Contact(id=2, first_name='Zoro', last_name='Roronoa',
                    email='strawhatswordsman@meta.ua', date_of_birth=today),
        ]
        self.session.query().filter().offset().limit().all.return_value = contacts

        result = await get_contacts_birthdays(0, 10, self.user, self.session)
        self.assertEqual(result, contacts)


if __name__ == '__main__':
    unittest.main()
