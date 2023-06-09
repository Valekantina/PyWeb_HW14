from datetime import date

from sqlalchemy import and_
from sqlalchemy.orm import Session

from src.database.models import Contact, User
from src.schemas import ContactModel


async def get_contacts(skip: int, limit: int, first_name: str, last_name: str, email: str, user: User, db: Session):
    """
    The get_contacts function returns a list of contacts that match the search criteria.
        If no search criteria is provided, it will return all contacts for the user.
    
    :param skip: int: Skip the first n number of contacts in the database
    :param limit: int: Limit the number of results returned
    :param first_name: str: Filter the contacts by first name
    :param last_name: str: Filter the contacts by last name
    :param email: str: Filter the contacts by email
    :param user: User: Get the user id of the logged in user
    :param db: Session: Access the database
    :return: A list of contacts
    :doc-author: Trelent
    """
    first_name_query = db.query(Contact).filter(and_(Contact.first_name == first_name, Contact.user_id == user.id))
    last_name_query = db.query(Contact).filter(and_(Contact.last_name == last_name, Contact.user_id == user.id))
    email_query = db.query(Contact).filter(and_(Contact.email == email, Contact.user_id == user.id))
    if first_name and last_name and email:
        return first_name_query.union(last_name_query).union(email_query).all()
    if first_name and last_name:
        return first_name_query.union(last_name_query).all()
    if first_name and email:
        return first_name_query.union(email_query).all()
    if last_name and email:
        return last_name_query.union(email_query).all()
    if first_name:
        return first_name_query.all()
    if last_name:
        return last_name_query.all()
    if email:
        return email_query.all()
    return db.query(Contact).filter(Contact.user_id == user.id).offset(skip).limit(limit).all()


async def get_contacts_birthdays(skip: int, limit: int, user: User, db: Session):
    """
    The get_contacts_birthdays function returns a list of contacts with birthdays in the next 7 days.
        Args:
            skip (int): The number of contacts to skip.
            limit (int): The maximum number of contacts to return.
            user (User): A User object containing information about the current user, including their id and email address.
            db (Session): An SQLAlchemy Session object used for querying the database.
    
    :param skip: int: Skip a number of contacts in the database
    :param limit: int: Limit the number of contacts returned
    :param user: User: Get the user id from the database
    :param db: Session: Pass the database session to the function
    :return: A list of contacts that have their birthdays in the next 7 days
    :doc-author: Trelent
    """
    contacts_with_birthdays = []
    today = date.today()
    current_year = today.year
    contacts = db.query(Contact).filter(Contact.user_id == user.id).offset(skip).limit(limit).all()
    for contact in contacts:
        td = contact.date_of_birth.replace(year=current_year) - today
        if 0 <= td.days <= 7:
            contacts_with_birthdays.append(contact)
        else:
            continue
    return contacts_with_birthdays


async def get_contact_by_id(contact_id: int, user: User, db: Session):
    """
    The get_contact_by_id function returns a contact by its id.
        Args:
            contact_id (int): The id of the contact to be returned.
            user (User): The user who is requesting the return of this specific contact.
            db (Session): A database session object that will be used to query for contacts in our database.
        Returns: 
            Contact: A single Contact object from our database, or None if no such Contact exists.
    
    :param contact_id: int: Get the contact by its id
    :param user: User: Get the user id from the database
    :param db: Session: Pass a database session to the function
    :return: A contact object with the given id if it exists
    :doc-author: Trelent
    """
    return db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()


async def create_contact(body: ContactModel, user: User, db: Session):
    """
    The create_contact function creates a new contact in the database.
        
    
    :param body: ContactModel: Pass the request body to the function
    :param user: User: Get the user id from the database
    :param db: Session: Access the database
    :return: A contact object
    :doc-author: Trelent
    """
    contact = Contact(**body.dict(), user_id=user.id)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def update_contact(contact_id: int, body: ContactModel, user: User, db: Session):
    """
    The update_contact function updates a contact in the database.
        Args:
            contact_id (int): The id of the contact to update.
            body (ContactModel): The updated information for the specified user's contact.
            user (User): The current logged-in user, used to verify that they are updating their own contacts and not someone else's.
            db (Session): A connection to our database, used for querying and committing changes.
    
    :param contact_id: int: Identify the contact that is being updated
    :param body: ContactModel: Pass the contact object to the function
    :param user: User: Get the user id from the token
    :param db: Session: Access the database, and the user: user parameter is used to get information about the current user
    :return: The contact object
    :doc-author: Trelent
    """
    contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    if contact:
        contact.first_name = body.first_name
        contact.last_name = body.last_name
        contact.email = body.email
        contact.phone = body.phone
        contact.date_of_birth = body.date_of_birth
        db.commit()
    return contact


async def remove_contact(contact_id: int, user: User, db: Session):
    """
    The remove_contact function removes a contact from the database.
        Args:
            contact_id (int): The id of the contact to be removed.
            user (User): The user who owns the contacts list.
            db (Session): A session object for interacting with the database.
        Returns: 
            Contact: The deleted Contact object.
    
    :param contact_id: int: Specify the id of the contact to be removed
    :param user: User: Get the user_id from the user object
    :param db: Session: Pass the database session to the function
    :return: The contact that was removed
    :doc-author: Trelent
    """
    contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact
