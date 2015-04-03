from flask import Flask,render_template, redirect,url_for, session, request, flash, abort
import manage
import os

#Author: Mary Akinlonu
#Date: December 1, 2014
#About: A password protected phonebook manager that allows users to add, update, and delete contact information.
#This app uses flask, sqlalchemy, html, css
#Updated: April 2, 2015



#~~~~~~Helper Functions~~~~~~~~~

def extract_contact_details_from_template_then_map(request, contact):
    """Map contact details from the form to the contact instance"""
    numbers={}
    n_type={}
    emails={}
    e_type={}
    addresses={}
    a_type={}
    
    #Get  the list of numbers, emails, and addresses from the form
    for key, value in request.form.iteritems():
        if key.startswith("numbers_type"):
            n_type[key.strip("numbers_type")]=value
        elif key.startswith("numbers"):
            numbers[key.strip("numbers")]=value
        elif key.startswith("emails_type"):
            e_type[key.strip("emails_type")]=value
        elif key.startswith("emails"):
            emails[key.strip("emails")]=value
        elif key.startswith("addresses_type"):
            a_type[key.strip("addresses_type")]=value
        elif key.startswith("addresses"):
            addresses[key.strip("addresses")]=value

    #Add the list of numbers, emails, and addresses to contact
    contact.numbers=[manage.create_number(number, n_type[key]) for key, number in numbers.iteritems()]
    contact.emails=[manage.create_email(email, e_type[key]) for key, email in emails.iteritems()]
    contact.addresses=[manage.create_address(address, a_type[key]) for key, address in addresses.iteritems()]




#~~~~App~~~~~
app = Flask(__name__)


#~~~~~~~~~Login~~~~~~~~~

@app.route("/",methods=['GET', 'POST'])
def index():
    """Render the index.html template"""

    if request.method == 'POST':
        if request.form["submit"]=="Submit":
            phonebook_name=request.form['phonebook_name']
            password=request.form['password']
            session['phonebook_name']=phonebook_name
            if not manage.phonebook_password_exists(phonebook_name, password):
                flash("The phone book doesn't exist or you do not have permission to access it")
            else:
                session['logged_in'] = True
                flash('You were logged in')
                return redirect(url_for('welcome'))
        if request.form["submit"]=="Create New Phonebook":
            return redirect(url_for('create'))

    return render_template('index.html')


#~~~~~~~~~Logout~~~~~~~~~

@app.route("/logout",methods=['GET', 'POST'])
def logout():
    """Render the index.html template after logout"""

    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('index'))


#~~~~~~~~~Add Contact~~~~~~~~~

@app.route("/add",methods=['GET', 'POST'])
def add():
    """Render the add.html template and add the contact details to the database"""

    if not session.get('logged_in'):
        abort(401)

    phonebook_name = session['phonebook_name']
    phonebook = manage.get_phonebook(phonebook_name)
   
    if request.method=='POST':
        if request.form["submit"]=='Save':
            contact_name=request.form['contact_name']
            birthday=request.form['birthday']
            if manage.contact_exists(contact_name, phonebook_name):
                flash("Contact name already exists")
            else:
                contact=manage.create_contact(phonebook_name,contact_name,birthday=birthday)
                extract_contact_details_from_template_then_map(request, contact)
                phonebook.contacts.append(contact)
                manage.session.commit()

                return redirect(url_for('welcome'))

    return render_template('add.html')


#~~~~~~~~~Update Contact~~~~~~~~~

@app.route("/update",methods=['GET', 'POST'])
def update():
    """Render the update.html template and update the contact details in the database"""

    if not session.get('logged_in'):
        abort(401)

    phonebook_name = session['phonebook_name']
    contact_id = session["contact_id"]
    contact = manage.get_contact(contact_id)

    if contact:
        numbers = contact.numbers
        emails = contact.emails
        addresses = contact.addresses
    else:
        flash("Selected contact could not be retrieved, please contact admin")
        return redirect(url_for('welcome'))
    
    
    if request.method=='POST':
        if request.form["submit"]=="Delete Contact":
            manage.session.delete(contact)
            manage.session.commit()
            return redirect(url_for('welcome'))

        if request.form["submit"]=='Save':
            new_contact_name=request.form['contact_name']
            new_birthday=request.form['birthday']
            if new_contact_name != contact.name and manage.contact_exists(new_contact_name, phonebook_name):
                flash("Contact name already exists")
            else:
                contact.name=new_contact_name
                contact.birthday=new_birthday
                extract_contact_details_from_template_then_map(request, contact)
                manage.session.commit()
                return redirect(url_for('welcome'))
    return render_template('update.html', contact=contact, numbers=numbers, emails=emails, addresses=addresses)


#~~~~~~~~~Display Contact Details~~~~~~~~~

@app.route("/welcome",methods=['GET', 'POST'])
def welcome():
    """Render the welcome.html template and display the contact details from the database"""

    if not session.get('logged_in'):
        abort(401)

    phonebook_name = session['phonebook_name']
    phonebook = manage.get_phonebook(phonebook_name)
    contacts = phonebook.contacts

    if request.method == 'POST':
        if request.form["submit"]=="Display":
            return redirect(url_for('display'))
        elif request.form["submit"]=="Add":
            return redirect(url_for('add'))
        else: #It is update
            contact_id=int(request.form["submit"])
            session["contact_id"]=contact_id
            return redirect(url_for('update'))

    return render_template('welcome.html', contacts=contacts)

#~~~~~~~~~Create a new Phonebook ID and Password~~~~~~~~~

@app.route("/create",methods=['GET', 'POST'])
def create():
    """Render the create.html template and add the new phonebook to the databse"""

    if request.method=='POST':
        phonebook_name=request.form['phonebook_name']
        password1=request.form['password1']
        password2=request.form['password2']

        if password1 == password2:
            if not manage.phonebook_exists(phonebook_name):
                manage.create(phonebook_name, password1)
                manage.session.commit()
                return redirect(url_for('index'))

            else:
                flash("phonebook name has been taken")
        else:
            flash("passwords typed do not match")
        
    return render_template('create.html')

app.secret_key = os.urandom(24)
if __name__ == "__main__":
        app.run(debug=True)

