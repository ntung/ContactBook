from create_tables import create_engine, Base, Contact, Phonebook, Address, Email, Number, session

#Author: Mary Akinlonu
#Date: December 1, 2014
#About: Contains helper functions that adds to and  queries the phonebook database
#Updated: April 2, 2014

#Helper Functions
def create(phonebook_name, password):
    """Create a phonebook instance in the Phonebook data table"""
    Phonebook(name=phonebook_name, password = password).create()

def create_contact(phonebook, name, first_name="", last_name="",birthday=""):
    """Return a Contact instance using the given paramenters"""
    return Contact(phonebook_name=phonebook, name=name,first_name=first_name, last_name=last_name,birthday=birthday)

def create_number(number, n_type):
    """Return a Number instance using the given parameters"""
    return Number(phone_number= number,number_type=n_type)

def create_email(email, e_type):
    """Return an Email instance using the given parameters"""
    return Email(email_address= email,email_type=e_type)

def create_address(address, a_type):
    """Return an Address instance using the given parameters"""
    return Address(address=address,address_type=a_type)

def phonebook_password_exists(phonebook_name, password):
    """Return True if a Phonebook exists given the name and the password"""
    phonebook= session.query(Phonebook).filter_by(name=phonebook_name).filter_by(password=password).first()
    return phonebook != None

def phonebook_exists(phonebook_name):
    """Return True if a Phonebook instance exists given the name"""
    phonebook= session.query(Phonebook).filter_by(name=phonebook_name).first()
    return phonebook != None

def contact_exists(name, phonebook_name):
    """Return True if a Contact instance exists given the name and phonebook name"""
    contact= session.query(Contact).filter_by(name=name).filter_by(phonebook_name=phonebook_name).first()
    return contact != None

def get_phonebook(phonebook_name):
    """Return an existing Phonebook instance given the name"""
    return session.query(Phonebook).filter_by(name=phonebook_name).first()

def get_contacts(phonebook_name):
    """Return a list of Contact instances given the phonebook name"""
    return session.query(Contact).filter_by(phonebook_name=phonebook_name).order_by(Contact.name)

def get_contact(contact_id):
    """Return an existing Contact instance given the id"""
    return session.query(Contact).filter_by(contact_id=contact_id).first()

def get_numbers(contact_id):
    """Return a list of Number instances given the contact id"""
    return session.query(Number).filter_by(contact_id=contact_id)

def get_emails(contact_id):
    """Return a list of Email instances given the contact id"""
    return session.query(Email).filter_by(contact_id=contact_id)

def get_addresses(contact_id):
    """Return a list of Address instances given the contact id"""
    return session.query(Address).filter_by(contact_id=contact_id)

def display(phonebook_name):
    """Print all the contacts in the given phonebook"""
    phonebook= session.query(Phonebook).filter_by(name=phonebook_name).first()
    if phonebook:
        print phonebook.name
        for contact in phonebook.contacts:
            print 'Name:\t',contact.name,contact.birthday
            print '\tNumbers:'
            for number in contact.numbers:
                print '\t\t',number.phone_number, number.number_type
            print '\tEmails:'
            for  email in contact.emails:
                print '\t\t',email.email_address, email.email_type
            print '\tAddresses:'
            for number in contact.addresses :
                print '\t\t',address.address, address.address_type


#display("testbook")
#phonebook= session.query(Phonebook).filter_by(name="test_phonebook.pb").first()
#print phonebook.numbers


#def create(phonebook_name):
#    phonebook=session.query(Phonebook).filter_by(phonebook_name=phonebook_name)
#    if not phonebook:
#        phonebook=Phonebook(phonebook_name=phonebook_name, name="")
#        session.add(phonebook)
#        session.commit()
#
#
#
#def add(phonebook_name, name, numbers):
#    phonebook=session.query(Phonebook).filter_by(phonebook_name=phonebook_name)
#    if phonebook:
#        phonebook.name=name
#        session.add_all()
#
#        session.commit()
#



