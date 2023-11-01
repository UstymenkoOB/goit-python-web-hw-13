from datetime import date, timedelta
from typing import List
from sqlalchemy import String, and_, extract, func, or_

from sqlalchemy.orm import Session

from src.database.models import Contact, User
from src.schemas import ContactModel, ContactUpdate


async def get_contacts(skip: int, limit: int, user: User, db: Session) -> List[Contact]:
    return db.query(Contact).filter(Contact.user_id == user.id).offset(skip).limit(limit).all()


async def get_contact(contact_id: int, user: User, db: Session) -> Contact:
    return db.query(Contact).filter(and_(Contact.id == contact_id), Contact.user_id == user.id).first()


async def get_contacts_name(name: str, user: User, db: Session) -> List[Contact]:
    return db.query(Contact).filter(and_(Contact.name.like(f'%{name}%'), Contact.user_id == user.id)).all()


async def get_contacts_surname(surname: str, user: User, db: Session) -> List[Contact]:
    return db.query(Contact).filter(and_(Contact.surname.like(f'%{surname}%'), Contact.user_id == user.id)).all()


async def get_contacts_email(email_part: str, user: User, db: Session) -> List[Contact]:
    return db.query(Contact).filter(and_(Contact.email.like(f'%{email_part}%'), Contact.user_id == user.id)).all()


async def get_contacts_birthday(user: User, db: Session) -> List[Contact]:
    days = []
    for i in range(7):
        day = date.today() + timedelta(days=i)
        days.append(str(day.day) + str(day.month))

    contacts = db.query(Contact).filter(and_(
        or_(func.concat(
        extract('day', Contact.birthday).cast(String),
        extract('month', Contact.birthday).cast(String)
        ).in_(days))), Contact.user_id == user.id).all()
    return contacts


async def create_contact(body: ContactModel, user: User, db: Session) -> Contact:
    contact = Contact(name=body.name, surname=body.surname, email=body.email, 
                      phone=body.phone, birthday=body.birthday, 
                      description=body.description, user_id=user.id)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def remove_contact(contact_id: int, user: User, db: Session) -> Contact | None:
    contact = db.query(Contact).filter(
        and_(Contact.id == contact_id), Contact.user_id == user.id).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def update_contact(contact_id: int, body: ContactUpdate, user: User, db: Session) -> Contact | None:
    contact = db.query(Contact).filter(
        and_(Contact.id == contact_id), Contact.user_id == user.id).first()
    if contact:
        contact.name = body.name
        contact.surname = body.surname
        contact.email = body.email
        contact.phone = body.phone
        contact.birthday = body.birthday
        contact.description = body.description
        db.commit()
    return contact
