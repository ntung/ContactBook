from sqlalchemy import create_engine, Column, ForeignKey,Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref, sessionmaker
import sys

#Author: Mary Akinlonu
#Date: December 1, 2014
#About:
#-Model to create ORM, data tables, and  methods
#-Used cascading to make save-update and delete clean
#Updated: April 2, 2015


#~~~~~~~~~~Engine~~~~~~~~~
engine = create_engine('sqlite:///phonebookmanager.db', echo=False)

#~~~~~~~~~~Base~~~~~~~~~
Base = declarative_base()



#~~~~~~~~Session~~~~~~~~~~~
Session = sessionmaker(bind=engine)

session=Session()

#~~~~~~~~~ORM Tables~~~~~~~~~
class Phonebook(Base):
    __tablename__="phonebook"

    name=Column(String(50), primary_key=True)
    password=Column(String(50))
    contacts= relationship("Contact", cascade="all, delete-orphan",backref="phonebook")

    def create(self):
        """Add this phonebook to the session"""
        phonebook=session.query(Phonebook).filter_by(name=self.name).first()
        if not phonebook:
            session.add(self)
            print self.name,"created." #TODO: append this to a log file
        else:
            print self.name,"already  exists." #TODO: append this to a log file
            return False
        return True
    
        

class Contact(Base):
    __tablename__="contact"
    
    contact_id=Column(Integer, primary_key=True, autoincrement=True)
    phonebook_name = Column(String(50),  ForeignKey('phonebook.name'))
    name = Column(String(50))
    first_name = Column(String(50))
    last_name = Column(String(50))
    numbers = relationship("Number", cascade="all, delete-orphan",backref="contact")
    emails = relationship("Email", cascade="all, delete-orphan",backref="contact")
    addresses = relationship("Address", cascade="all, delete-orphan",backref="contact")
    birthday = Column(String(50))

    def add(self):
        """Add this contact to the session"""
        old_name=session.query(Contact).filter_by(name=self.name).filter_by(phonebook_name=self.phonebook_name).first()
        if not old_name:
            session.add(self)
            print self.name, "added." #TODO: append this to a log file
        else:
            print self.name,"already exists."#TODO: append this to a log file
            return False
        return True


class Email(Base):
    __tablename__="email"
    email_id=Column(Integer, primary_key=True, autoincrement=True)
    contact_id = Column(Integer,  ForeignKey('contact.contact_id'))
    email_address=Column(String(50))
    email_type = Column(String(50))

    def add(self):
        """Add this email to the session"""
        old_email=session.query(Email).filter_by(email_address=self.email_address).filter_by(contact_id=self.contact_id).first()
        if not old_email:
            session.add(self)
            print self.email_address, "added."#TODO: append this to a log file
        else:
            print self.email_address, "already exists."#TODO: append this to a log file
            return False
        return True

class Number(Base):
    __tablename__="number"
    number_id=Column(Integer, primary_key=True, autoincrement=True)
    contact_id = Column(Integer,  ForeignKey('contact.contact_id'))
    phone_number=Column(String(50))
    number_type = Column(String(50))

    def add(self):
        """Add this number to the session"""
        old_number=session.query(Number).filter_by(phone_number=self.phone_number).filter_by(contact_id=self.contact_id).first()
        if not old_number:
            session.add(self)
            print self.phone_number,"added."#TODO: append this to a log file
        else:
            print self.phone_number, "already exists"#TODO: append this to a log file
            return False
        return True

class Address(Base):
    __tablename__="address"
    address_id=Column(Integer, primary_key=True, autoincrement=True)
    contact_id = Column(Integer,  ForeignKey('contact.contact_id'))
    address=Column(String(50))
    street=Column(String(50))
    city=Column(String(50))
    state=Column(String(50))
    country=Column(String(50))
    zipcode=Column(String(50))
    address_type = Column(String(50))


    def add(self):
        """Add this address to the session"""
        old_address=session.query(Address).filter_by(address=self.address).filter_by(contact_id=self.contact_id).first()
        if not old_address:
            session.add(self)
            print self.address, "added."#TODO: append this to a log file
        else:
            print self.address,"already exists."#TODO: append this to a log file
            return False
        return True





#~~~~~~Create Engine~~~~~~~~~~~
Base.metadata.create_all(engine)
