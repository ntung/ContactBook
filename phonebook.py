import manage

exit=False

while True:
    print "Type 'q' to quit."
    action = raw_input("Do you want to create a new phonebook , add to , or display an existing one? [add/create/display]?").upper()
    if action[0]=='Q':
        break
    
    #Create phonebook
    if action[0]=='C':
        phonebook_name = raw_input("Enter Phone Book name:")
        password = raw_input("Enter password:")
        manage.create(phonebook_name+'.pb', password)

    else:
        phonebook_name = raw_input("Enter Phone Book name:")
        password = raw_input("Enter password:")
        no_ext_phonebook=phonebook_name
        phonebook_name+='.pb'    

        if not manage.phonebook_password_exists(phonebook_name, password):
            print no_ext_phonebook,"doesn't exist or you do not have permission to access."
            continue
            


    if action[0]=='A':
        name = raw_input("Enter name:")
            
        if not manage.contact_exists(name, phonebook_name):
            manage.add_contact(phonebook_name, name)

        while True:
            number = raw_input("Add a number ['q' to quit]:").upper()
            if number[0] != 'Q':n_type=raw_input("Number type [mobile, home, etc]:").upper()
            if number[0] =='Q' or n_type[0]=='Q':
                break
            else:
                manage.add_number(phonebook_name, name, number, n_type)
        while True:
            email = raw_input("Add an email address ['q' to quit]:").lower()
            if email.upper()[0] != 'Q':e_type=raw_input("Email type [mobile, home, etc]:").upper()
            if email.upper()[0] =='Q' or e_type[0]=='Q':
                break
            else:
                manage.add_email(phonebook_name, name, email, e_type)
        while True:
            address = raw_input("Add a physical address ['q' to quit]:")
            if address.upper()[0] !='Q':a_type=raw_input("Address type [mobile, home, etc]:").upper()
            if address.upper()[0] =='Q' or a_type[0]=='Q':
                break
            else:
                manage.add_address(phonebook_name, name, address, a_type)



        

    elif action[0]=='D':
        manage.display(phonebook_name)

        

#Commit all additions
manage.session.commit()
