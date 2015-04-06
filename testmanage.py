import unittest
import random
import manage
from create_tables import session

#Author: Mary Akinlonu
#Date April 6, 2014
#About: Test manage.py
#Updated: April 6, 2015

class TestNewPhonebookNewContact(unittest.TestCase):
    """Test that newly created phonebook and contact are in the database and are related"""
    
    book=manage.get_phonebook("testbook6")
    def test_that_phonebook_exists_after_adding(self):
        self.assertTrue(manage.phonebook_exists("testbook6"))
        if self.book:
            self.assertEqual(self.book.name,"testbook6")

    def test_that_contact_exists_after_adding(self):
        if self.book:
            self.assertTrue(self.book.contacts[0] != None)
            if self.book.contacts[0]:
                self.assertEqual(self.book.contacts[0].name,"Test Person")


    def test_that_number_exists_after_adding(self):
        if self.book:
            if self.book.contacts[0]:
                self.assertTrue(self.book.contacts[0].numbers[0] != None)
                if self.book.contacts[0].numbers[0]:
                    self.assertEqual(self.book.contacts[0].numbers[0].phone_number,"123-456-7890")

class TestNewPhonebook(unittest.TestCase):
    """Test that newly created phonebook exists in the database and does not have any related contacts"""

    book=manage.get_phonebook("testbook9")
    def test_that_phonebook_exists_after_adding(self):
        self.assertTrue(manage.phonebook_exists("testbook9"))
        if self.book:
            self.assertEqual(self.book.name,"testbook9")
    def test_that_no_contact_exists_in_phonebook(self):
        self.assertEqual(self.book.contacts,[])

class TestOldPhonebookNewContact(unittest.TestCase):
    """Test that new contacts can be added to an existing phonebook in the database and are related"""

    book=manage.get_phonebook("testbook8")
    contact_f_name=["John", "Mary", "Sarah", "Bob", "Jim"]
    contact_l_name=["Black", "Green", "White", "Blue", "Brown"]
    contact_name=random.choice(contact_f_name)+" "+random.choice(contact_l_name)
    contact_number=str(random.randrange(100, 1000))+"-"+str(random.randrange(100, 1000))+"-"+str(random.randrange(1000, 10000))
    new_contact=manage.create_contact(book.name, contact_name, birthday="2015-04-01")
    new_number=manage.create_number(contact_number, "Mobile")
    new_email=manage.create_email("abc@gmail.com", "Personal")
    new_address=manage.create_address("123 Abc Street", "Home")
    new_contact.numbers.append(new_number)
    new_contact.emails.append(new_email)
    new_contact.addresses.append(new_address)
    book.contacts.append(new_contact)
    session.commit()


    def test_that_new_contact_exists(self):
        book=manage.get_phonebook("testbook8")
        contact=manage.get_contact_by_name(self.contact_name,"testbook8")
        self.assertTrue(manage.contact_exists(self.contact_name, "testbook8"))
        if contact:
            self.assertEqual(contact.name, self.contact_name)
        



if __name__ == '__main__':

        #Helper functions to create phonebook and contact
        def create_phonebook_with_contact():
            book = manage.create("testbook6", "abc")
            number=manage.create_number("123-456-7890", "Mobile")
            contact=manage.create_contact("testbook6", "Test Person", birthday="2015-04-01")
            
            contact.numbers.append(number)
            book.contacts.append(contact)

            session.commit()

        def create_only_phonebook():
            manage.create("testbook9", "abc")
            session.commit()
        
        #create_phonebook_with_contact()
        #create_only_phonebook()
        unittest.main()
