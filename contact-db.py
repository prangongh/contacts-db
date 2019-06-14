import sqlite3
import datetime

# connecting with the database
conn = sqlite3.connect('contacts.db')
# assigning the cursor to a variable
cur = conn.cursor()

def main():
    print('''Welcome to ContactDB! Follow the menu below to interact
    with the database''')

    # detecting if the table exists within the database
    cur.execute('''SELECT count(name) FROM sqlite_master WHERE 
    type = 'table' AND name = 'contacts' ''')

    # if table does exist, move forward with existing table
    if cur.fetchone()[0] == 1: 
        print('''\nThere is an existing table of contacts. Continuing
        with the existing table.\n''')
    # if table doesn't exist, create new table
    else:
        cur.execute('''CREATE TABLE contacts (name TEXT, 
        email TEXT, phone INTEGER, last_update TEXT)''')

    # while loop for continuous runs
    while True:
        # menu
        print('''\n
        Menu:\n
        A) Print All Contacts\n
        B) Add A Contact\n
        C) Delete A Contact\n
        D) Update A Contact\n
        E) Restart The Database\n
        Q) Quit
        \n''')

        # take user input
        user_input = str(input('Enter selection: ')).upper()

        # print all contacts
        if user_input == 'A':
            while True:
                # secondary menu for printing contacts by a certain order
                print('''\n
                Please select the way in which the contacts should
                be ordered when printed.\n
                Sub-menu:\n
                1) Order By Name
                2) Order By Email
                3) Order By Phone
                4) Order By Last Update
                5) Quit Sub-menu
                ''')

                # take user input
                user_input = str(input('Enter selection: ')).upper()

                # order by name
                if user_input == '1':
                    sqlstr = '''SELECT name, email, phone, last_update
                    FROM contacts ORDER BY name'''

                    for row in cur.execute(sqlstr):
                        print(str(row[0], row[1], row[2], row[3]))
                # order by email
                elif user_input == '2':
                    sqlstr = '''SELECT name, email, phone, last_update
                    FROM contacts ORDER BY email'''

                    for row in cur.execute(sqlstr):
                        print(str(row[0], row[1], row[2], row[3]))
                # order by phone number
                elif user_input == '3':
                    sqlstr = '''SELECT name, email, phone, last_update
                    FROM contacts ORDER BY phone'''

                    for row in cur.execute(sqlstr):
                        print(str(row[0], row[1], row[2], row[3]))
                # order by last updated
                elif user_input == '4':
                    sqlstr = '''SELECT name, email, phone, last_update
                    FROM contacts ORDER BY last_update'''

                    for row in cur.execute(sqlstr):
                        print(str(row[0], row[1], row[2], row[3]))
                # quit
                elif user_input == '5':
                    print('\nExiting the sub-menu...\n')
                    break
                # for invalid user input 
                else:
                    print('\nInvalid user input. Please try again!\n')
        
        # add a contact
        elif user_input == 'B':
            name = str(input('Contact Name: '))
            email = str(input('Contact Email: '))
            phone = int(input('Contact Phone: '))
            
            # check if there is an existing contact with the same name
            cur.execute('''SELECT name FROM contacts WHERE name = ?''',
            (email,))
            row = cur.fetchone()
            # if there is no existing contact with the same name, add contact
            if row is None:
                cur.execute('''INSERT INTO contacts (name, email, phone, 
                last_update) VALUES(%s, %s, %d, %s)''', 
                (name, email, phone, str(datetime.datetime.now())))

                print('\n%s added to the contacts database', name)
            # if there is an existing contact, ask the user to continue
            else:
                print('\nThere already exists a %s in the database.\n')
                
                # print contacts with the given name
                sqlstr = '''SELECT name, email, phone, last_update FROM contacts
                name = ''' + name

                for row in cur.execute(sqlstr):
                    print(str(row[0], row[1], row[2], row[3]))

                string = '\n Continue to add ' + name + ' ? (Y/N)\n'
                user_input = str(input(string)).upper()

                # add new contact if the user says yes
                # otherwise, don't add the contact
                if user_input == 'Y':
                    cur.execute('''INSERT INTO contacts (name, email, phone, 
                    last_update) VALUES(%s, %s, %d, %s)''', 
                    (name, email, phone, str(datetime.datetime.now())))

                    print('\n%s added to the contacts database', name)
                else:
                    print('\nContinuing the program...\n')                

        # delete a contact
        elif user_input == 'C':
            name = str(input('Contact Name: '))

            # check if there is an existing contact with the same name
            cur.execute('''SELECT name FROM contacts WHERE name = ?''',
            (email,))
            row = cur.fetchone()

            # if there is no contact with the given name, do nothing
            # if there is a contact with the given name, delete it
            if row is None:
                print('''\nThere exists no contact in the database with the 
                    given name. Continuing with the program...\n''')
            else:
                cur.execute('''DELETE FROM contacts WHERE name = ?''', (name,))
                print('''\nDeleted all contacts with the given name.\n''')
                
        # update a contact
        elif user_input == 'D':
            name = str(input('Contact Name: '))

            # print contacts with the given name
            sqlstr = '''SELECT name, email, phone, last_update FROM contacts
            name = ''' + name

            for row in cur.execute(sqlstr):
                print(str(row[0], row[1], row[2], row[3]))

            while True:
                # secondary menu for updating a contact
                print('''\n
                Please select the attributes of the contact
                that you would like to update.\n
                Sub-menu:\n
                1) Update Email
                2) Update Phone
                3) Quit Sub-menu
                ''')

                # take user input
                user_input = str(input('Enter selection: ')).upper()

                # update email
                if user_input == '1':
                    email = str(input('New Contact Email: '))
                    cur.execute('''UPDATE contacts SET email = ? WHERE name = ?''', (email, name))
                    
                    print('\nEmail of %s updated.\n', name)
                # update phone number
                elif user_input == '2':
                    phone = int(input('New Contact Phone: '))
                    cur.execute('''UPDATE contacts SET phone = ? WHERE name = ?''', (phone, name))

                    print('\nPhone number of %s updated.\n', name)
                # quit
                elif user_input == '3':
                    print('\nExiting the sub-menu...\n')
                    break
                else:
                    print('\nInvalid user input. Please try again!\n')
        
        # restart the database
        elif user_input == 'E':
            user_input = str(input('''Are you sure? 
            This will delete all current data. (Y/N)''')).upper()

            if user_input == 'Y':
                # delete current table and create new table
                cur.execute('DROP TABLE IF EXISTS contacts')
                cur.execute('''CREATE TABLE contacts (name TEXT, 
                email TEXT, phone INTEGER, last_update TEXT)''')

                print('\nInitialized new database for contacts.\n')
            else:
                print('\nContinuing the program...\n')
        
        # quit
        elif user_input == 'Q':
            user_input = str(input('Are you sure? (Y/N)')).upper()

            if user_input == 'Y':
                # close the SQL connection
                conn.commit()
                conn.close()
                print('\nExiting the program...\n')
                exit()
            else:
                print('\nContinuing the program...\n')
        
        # for invalid user input
        else:
            print('\nInvalid user input. Please try again!\n')


main()