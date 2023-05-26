from typing import List, Optional

from fastapi import APIRouter, HTTPException, Depends, status, Query
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import User
from src.schemas import ContactModel, ContactResponse
from src.services.auth import auth_service
from src.repository import contacts as repository_contacts

router = APIRouter(prefix='/contacts', tags=['contacts'])


@router.get('/', response_model=List[ContactResponse], name='Get a list of all contacts or contacts filtered by query parameters such as first name, last name or email', description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def get_contact_by_params(skip: int = 0, limit: int = Query(default=10),
                              first_name: Optional[str] = Query(default=None),
                              last_name: Optional[str] = Query(default=None),
                              email: Optional[str] = Query(default=None),
                              db: Session = Depends(get_db),
                              current_user: User = Depends(auth_service.get_current_user)):
    """
    The get_contact_by_params function returns a list of contacts that match the parameters passed in.
        The function takes in skip, limit, first_name, last_name and email as query parameters.
        If no contact is found with the given parameters then an HTTP 404 error is raised.
    
    :param skip: int: Skip the first n records
    :param limit: int: Limit the number of contacts returned
    :param first_name: Optional[str]: Filter the results by first name
    :param last_name: Optional[str]: Specify the last name of a contact
    :param email: Optional[str]: Filter the contacts by email
    :param db: Session: Pass the database session to the function
    :param current_user: User: Get the user id of the current logged in user
    :return: A list of contacts
    :doc-author: Trelent
    """
    contact = await repository_contacts.get_contacts(skip, limit, first_name, last_name, email, current_user, db)
    if not contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Contacts with requested parameters not found')
    return contact


@router.get('/birthdays', response_model=list[ContactResponse], name='Get list of contacts with birthdays for the next 7 days', description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def get_birthdays(skip: int = 0, limit: int = Query(default=10), db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    """
    The get_birthdays function returns a list of contacts with birthdays in the next 7 days.
        The function takes an optional skip and limit parameter to paginate through the results.
        
    
    :param skip: int: Skip the first n contacts in the database
    :param limit: int: Limit the number of results returned
    :param db: Session: Pass the database session to the function
    :param current_user: User: Get the current user from the database
    :return: A list of birthdays for the next 7 days
    :doc-author: Trelent
    """
    contacts = await repository_contacts.get_contacts_birthdays(skip, limit, current_user, db)
    if not contacts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Contacts with birthdays for the next 7 days not found')
    return contacts


@router.get('/{contact_id}', response_model=ContactResponse, name='Get contact by id', description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def get_contact(contact_id: int, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    """
    The get_contact function returns a contact by id.
        Args:
            contact_id (int): The id of the requested contact.
            db (Session, optional): SQLAlchemy Session instance. Defaults to Depends(get_db).
            current_user (User, optional): Current user object from auth middleware. Defaults to Depends(auth_service.get_current_user).
    
    :param contact_id: int: Get the contact id from the url
    :param db: Session: Pass the database connection to the function
    :param current_user: User: Get the user id from the token
    :return: A contact object
    :doc-author: Trelent
    """
    contact = await repository_contacts.get_contact_by_id(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Contact with requested id not found')
    return contact


@router.post('/', response_model=ContactResponse, description='No more than 3 requests per 5 minutes',
            dependencies=[Depends(RateLimiter(times=3, minutes=5))], status_code=status.HTTP_201_CREATED)
async def create_contact(body: ContactModel, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    """
    The create_contact function creates a new contact in the database.
        The function takes in a ContactModel object and returns the newly created contact.
    
    :param body: ContactModel: Get the data from the request body
    :param db: Session: Get the database session
    :param current_user: User: Get the user_id of the current logged in user
    :return: The new_contact object
    :doc-author: Trelent
    """
    new_contact = await repository_contacts.create_contact(body, current_user, db)
    return new_contact


@router.put('/{contact_id}', response_model=ContactResponse)
async def update_contact(body: ContactModel, contact_id: int, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    """
    The update_contact function updates a contact in the database.
        The function takes a ContactModel object as input, which is used to update the contact's information.
        The function also takes an integer representing the id of the contact to be updated and uses it to find that specific contact in the database.
        If no such user exists, then an HTTPException is raised with status code 404 (Not Found).
    
    
    :param body: ContactModel: Pass the data from the request body to the function
    :param contact_id: int: Identify the contact to be deleted
    :param db: Session: Pass the database session to the function
    :param current_user: User: Get the user id of the logged in user
    :return: A contactmodel object
    :doc-author: Trelent
    """
    contact = await repository_contacts.update_contact(contact_id, body, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Contact with requested id not found')
    return contact


@router.delete('/{contact_id}', status_code=status.HTTP_204_NO_CONTENT)
async def remove_tag(contact_id: int, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    """
    The remove_tag function removes a tag from the database.
        Args:
            contact_id (int): The id of the contact to remove.
            db (Session, optional): SQLAlchemy Session. Defaults to Depends(get_db).
            current_user (User, optional): User object for authentication and authorization purposes. Defaults to Depends(auth_service.get_current_user).
    
    :param contact_id: int: Specify the id of the contact to be removed
    :param db: Session: Pass the database session to the function
    :param current_user: User: Get the current user from the database
    :return: A contact object
    :doc-author: Trelent
    """
    contact = await repository_contacts.remove_contact(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Contact with requested id not found')
    return contact
