---------------------------------
How to use (only locally for now)
---------------------------------
(Assuming you have installed python, sqlalchmey, and flask)
1. Download from bitbucket
2. change directory (cd) to App directory
3. Run 'python phonebooksite.py'
4. App will show up on http://127.0.0.1:5000/

----------------------------------
Design Decisions
----------------------------------

Using sqlalchemy ORM setup (object Class to Object data table relation)

Classes Hierachy

												   |---------|
										  /-has-a->| Address |
										 /	       |---------|
									    /
									   /
|-----------|             |----------|/            |--------|
| Phonebook |---has-a---->| Contact  |---has-a---->| Number |
|-----------|             |----------|\            |--------|       
									   \
									    \
									     \         |--------|
									      \-has-a->| Email  |
									      		   |--------|




Database table Relationship

												       |---------|
										  /-0-to-many->| Address |
										 /	           |---------|
									    /
									   /
|-----------|             |----------|/                |--------|
| Phonebook |-0-to-many-->| Contact  |---0-to-many---->| Number |
|-----------|             |----------|\                |--------|       
									   \
									    \
									     \             |--------|
									      \-0-to-many->| Email  |
									      		       |--------|


				Primary Keys, Foreign Keys, and Cascades 
				----------------------------------------
				Phonebook Table: name(pk), password(pk), 
					(contacts)->cascade="all, delete-orphan" 
				Contact Table: contact_id(pk), phonebook_name(fk), 
					(emails, numbers, addresses)--->cascade="all, delete-orphan"
				Email Table: email_id(pk), contact_id(fk)
				Number Table: number_id(pk), contact_id(fk)
				Address Table: address_id(pk), contact_id(fk)

	
Q. Why did I choose to use the ORM setup (Class-to-Table)?
A. The choice of mapping the classes to the database makes the development of the object model and the database schmema to be clean and decoupled

Q. Why did I turn on cascades?
A. Cascades allows the DB to efficiently handle actions between parent-child tables relationship without writing extra code. It allowed for clean saving, updating, and deleting. Given a case where you wanted to delete a contact without cascades(delete-orphans) there will be email, number, or address orphans hanging around. The save-update feature allowed the session to save to the database the contact object and all it's numbers, emails, and/or addresses appended to it during that session; automatically populating the foreign key of the number, email, or address instance  with the contact's primary key.

Q. Why did you give the email, numbers, and address a seperate table instead of one huge contact table?
A. This allows the DB setup to be organized and future proof. Since they are seperate entities that have a zero to many relationship with the contact table they should be given seperate tables. 

Q. Why did you use auto increment integer for their primary keys instead of the provided data ex. email_id instead of email_address?
A. Given them auto incremented IDs allows for flexibility, future proof code, and custom error handling. Given that cascades are turned on, If email_address was the primary key, I did not want the databse to handle the case where mulitple email addresses of the same spelling were added. I would be leaving room for database integrity errors. I wanted to be be able to handle duplicate email errors on my own.
