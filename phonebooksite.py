from flask import Flask,render_template, redirect,url_for, session, request, flash, abort
import manage, os

#Author: Mary Akinlonu
#Date: December 1, 2014
#About: A password protected phonebook manager that allows users to add, update, and delete contact information.
#This app uses flask, sqlalchemy, html, css
#Updated: April 2, 2015

app = Flask(__name__)

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


@app.route("/logout",methods=['GET', 'POST'])
def logout():
    """Render the index.html template after logout"""

    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('index'))

@app.route("/add",methods=['GET', 'POST'])
def add():
    """Render the add.html template """

    if not session.get('logged_in'):
        abort(401)

    phonebook_name = session['phonebook_name']
    phonebook = manage.get_phonebook(phonebook_name)
    numbers={}
    n_type={}
    emails={}
    e_type={}
    addresses={}
    a_type={}

    if request.method=='POST':
        if request.form["submit"]=='Save':
            contact_name=request.form['contact_name']
            birthday=request.form['birthday']

            if manage.contact_exists(contact_name, phonebook_name):
                flash("Contact name already exists")
            else:
                contact=manage.create_contact(phonebook_name,contact_name,birthday)

                #Get  the list of numbers, emails, and addresses from the form
                for k,v in request.form.iteritems():
                    if k.startswith("numbers_type"):
                        n_type[k.strip("numbers_type")]=v
                    elif k.startswith("numbers"):
                        numbers[k.strip("numbers")]=v
                    elif k.startswith("emails_type"):
                        e_type[k.strip("emails_type")]=v
                    elif k.startswith("emails"):
                        emails[k.strip("emails")]=v
                    elif k.startswith("addresses_type"):
                        a_type[k.strip("addresses_type")]=v
                    elif k.startswith("addresses"):
                        addresses[k.strip("addresses")]=v
                
                #Add the list of numbers, emails, and addresses to contact
                contact.numbers=[manage.create_number(number, n_type[key]) for key, number in numbers.iteritems()]
                contact.emails=[manage.create_email(email, e_type[key]) for key, email in emails.iteritems()]
                contact.addresses=[manage.create_address(address, a_type[key]) for key, address in addresses.iteritems()]
                
                phonebook.contacts.append(contact)
                manage.session.commit()

                return redirect(url_for('welcome'))

    return render_template('add.html')

@app.route("/update",methods=['GET', 'POST'])
def update():
    """Render the update.html template"""

    if not session.get('logged_in'):
        abort(401)

    phonebook_name = session['phonebook_name']
    contact_id= session["contact_id"]
    contact = manage.get_contact(contact_id)

    if not contact:
        flash("Selected contact could not be retrieved, please contact admin")
        return redirect(url_for('welcome'))

    numbers = contact.numbers
    emails= contact.emails
    addresses = contact.addresses
    
    if request.method=='POST':
        new_contact_name=request.form['contact_name']
        new_birthday=request.form['birthday']

        if request.form["submit"]=="Delete Contact":
            manage.session.delete(contact)
            manage.session.commit()
            return redirect(url_for('welcome'))

        if request.form["submit"]=='Save':
            if new_contact_name != contact.name and manage.contact_exists(new_contact_name, phonebook_name):
                flash("Contact name already exists")
            else:
                #Update contact 
                new_numbers={}
                new_number_type={}
                new_emails={}
                new_email_type={}
                new_addresses={}
                new_address_type={}

                #map the list of numbers, emails, and addresses from the form
                for k,v in request.form.iteritems():
                    if k.startswith("numbers_type"):
                        new_number_type[k.strip("numbers_type")]=v
                    elif k.startswith("numbers"):
                        new_numbers[k.strip("numbers")]=v
                    elif k.startswith("emails_type"):
                        new_email_type[k.strip("emails_type")]=v
                    elif k.startswith("emails"):
                        new_emails[k.strip("emails")]=v
                    elif k.startswith("addresses_type"):
                        new_address_type[k.strip("addresses_type")]=v
                    elif k.startswith("addresses"):
                        new_addresses[k.strip("addresses")]=v
                
                #Add attributes to contact
                contact.name=new_contact_name
                contact.birthday=new_birthday
                contact.numbers=[manage.create_number(number, new_number_type[key]) for key, number in new_numbers.iteritems()]
                contact.emails=[manage.create_email(email, new_email_type[key]) for key, email in new_emails.iteritems()]
                contact.addresses=[manage.create_address(address, new_address_type[key]) for key, address in new_addresses.iteritems()]
                manage.session.commit()
                return redirect(url_for('welcome'))
    
    return render_template('update.html', contact=contact, numbers=numbers, emails=emails, addresses=addresses)

@app.route("/welcome",methods=['GET', 'POST'])
def welcome():
    """Render the welcome.html template"""

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
        else :
            contact_id=int(request.form["submit"])
            session["contact_id"]=contact_id
            return redirect(url_for('update'))

    return render_template('welcome.html', contacts=contacts)

@app.route("/create",methods=['GET', 'POST'])
def create():
    """Render the create.html template"""

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

