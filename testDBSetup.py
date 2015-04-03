import unittest
from create_tables import Contact, Phonebook, Address, Email, Number, session
import random

#Author: Mary Akinlonu
#Date December 1, 2014
#About: Tests the storing of phonebook information in the database
#Updated: April 2, 2015

class TestNewPhonebookNewContact(unittest.TestCase):
    """Test that newly created phonebook and contact are in the database and are related"""
    
    book=session.query(Phonebook).filter_by(name="testbook").first()
    def test_that_phonebook_exists_after_adding(self):
        self.assertEqual(self.book.name,"testbook")

    def test_that_contact_exists_after_adding(self):
        self.assertEqual(self.book.contacts[0].contact_id,1)

    def test_that_number_exists_after_adding(self):
        self.assertEqual(self.book.contacts[0].numbers[0].phone_number,"123-456-7890")

class TestNewPhonebook(unittest.TestCase):
    """Test that newly created phonebook exists in the database and does not have any related contacts"""

    book=session.query(Phonebook).filter_by(name="testbook2").first()
    def test_that_phonebook_exists_after_adding(self):
        self.assertEqual(self.book.name,"testbook2")
    def test_that_no_contact_exists_in_phonebook(self):
        self.assertEqual(self.book.contacts,[])

class TestOldPhonebookNewContact(unittest.TestCase):
    """Test that new contacts can be added to an existing phonebook in the database and are related"""

    book=session.query(Phonebook).filter_by(name="testbook").first()
    contact_f_name=["John", "Mary", "Sarah", "Bob", "Jim"]
    contact_l_name=["Black", "Green", "White", "Blue", "Brown"]
    contact_name=random.choice(contact_f_name)+" "+random.choice(contact_l_name)
    contact_number=str(random.randrange(100, 1000))+"-"+str(random.randrange(100, 1000))+"-"+str(random.randrange(1000, 10000))
    new_contact=Contact(phonebook_name=book.name, name=contact_name, birthday="2015-04-01")
    new_number=Number(phone_number=contact_number, number_type="Mobile")
    new_email=Email(email_address="abc@gmail.com", email_type="Personal")
    new_address=Address(address="123 Abc Street", address_type="Home")
    new_contact.numbers.append(new_number)
    new_contact.emails.append(new_email)
    new_contact.addresses.append(new_address)
    book.contacts.append(new_contact)
    session.commit()


    def test_that_new_contact_exists(self):
        book=session.query(Phonebook).filter_by(name="testbook").first()
        contact=session.query(Contact).filter_by(phonebook_name="testbook").filter_by(name=self.contact_name).first()
        self.assertEqual(contact.name, self.contact_name)
        



if __name__ == '__main__':

        #Helper functions to create phonebook and contact
        def create_phonebook_with_contact():
            number=Number(phone_number="123-456-7890", number_type="Mobile")
            contact=Contact(phonebook_name="testbook", name="Test Person", birthday="2015-04-01")
            book = Phonebook(name="testbook", password="abc")
            
            contact.numbers.append(number)
            book.contacts.append(contact)
            book.create()

            session.commit()

        def create_only_phonebook():
            book = Phonebook(name="testbook2", password="abc")
            book.create()
            session.commit()
        
        #create_phonebook_with_contact()
        #create_only_phonebook()
        unittest.main()
