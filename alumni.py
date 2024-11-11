from utils import login
from utils import get_input
from utils import is_valid_email
def Alumni():
    print('''-------------OPTIONS----------------\n
    1. Alumni Registration\n
    2. View Events\n
    3. Event Registration\n
    4. Main Menu\n
    5. Exit''')
    
    choice = int(input('Enter your choice (1-5): '))
    if choice == 1:
        alumni_register()
    elif choice == 2:
        view_events()
    elif choice == 3:
        reg_events()
    elif choice == 4:
        login()
    elif choice == 5:
        exit()
    else:
        print('Invalid input!')
def alumni_register():
    import mysql.connector

    db = mysql.connector.connect(host='localhost', user='root', password='1234', database='alumni')
    cursor = db.cursor()

    while True:
        # Get the alumni's name
        name = get_input('Enter your name:', is_name=True)

        # Get and validate the email
        while True:
            email_input = input("Enter your Email-ID: ")
            if is_valid_email(email_input):
                email = email_input
                break
            else:
                print("Invalid email format. Enter valid Email-ID")

        # Search for student in the students table
        command = "SELECT * FROM students WHERE Name=%s"
        cursor.execute(command, (name,))
        data = cursor.fetchone()

        if data:
            print("----------WELCOME----------")
            # Check if the alumni is already registered
            existing_alumni = search_alumni(name=name, email=email)
            if existing_alumni:
                print("You are already registered as an Alumni!")
            else:
                # Insert into alumni_students with data from the students table
                cursor.execute('''INSERT INTO alumni_students (Name, F_Name, Class, DOB, Contact_Number, Email_ID, 
                                         Passing_Year, Stream, Current_Country, Current_City, 
                                         Employment_Status, E_Domain, Company) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''',
                    (name, data[1], data[3], data[4], None, email, data[2], None, None, None, None, None, None))

                db.commit()  # Commit the changes
                print('You are successfully registered as an Alumni!')
            break
        else:
            print("No Data found in students table! Please enter a valid name.")
            break

    cursor.close()
    db.close()
    Alumni()
def view_events():
    import mysql.connector
    from prettytable import PrettyTable

    db = mysql.connector.connect(host='localhost', user='root', password='1234', database='alumni')
    cursor = db.cursor()
    
    while True:
        print('-------------------------------EVENTS-----------------------------')
        print('''Please Select an Option
        1. Upcoming Events (Active)
        2. Completed Events
        3. Postponed Events
        4. Cancelled Events
        5. Main Menu
        6. Exit''')
        
        choice = int(input('Enter the option (1-6): '))
        
        # Initialize the PrettyTable
        table = PrettyTable()
        table.field_names = ["Event ID", "Event Name", "Event Date", "Venue", "Status"]

        if choice == 1:
            cursor.execute("SELECT Event_ID, Event_Name, Event_Date, Venue, Status FROM events WHERE Status='Active'")
            active_events = cursor.fetchall()
            for event in active_events:
                table.add_row(event)
            print(table)
            break  # Exit the loop after displaying the events

        elif choice == 2:
            cursor.execute("SELECT Event_ID, Event_Name, Event_Date, Venue, Status FROM events WHERE Status='Completed'")
            completed_events = cursor.fetchall()
            for event in completed_events:
                table.add_row(event)
            print(table)
            break  # Exit the loop after displaying the events

        elif choice == 3:
            cursor.execute("SELECT Event_ID, Event_Name, Event_Date, Venue, Status FROM events WHERE Status='Postponed'")
            postponded_events = cursor.fetchall()
            for event in postponded_events:
                table.add_row(event)
            print(table)
            break  # Exit the loop after displaying the events

        elif choice == 4:
            cursor.execute("SELECT Event_ID, Event_Name, Event_Date, Venue, Status FROM events WHERE Status='Cancelled'")
            cancelled_events = cursor.fetchall()
            for event in cancelled_events:
                table.add_row(event)
            print(table)
            break  # Exit the loop after displaying the events

        elif choice == 5:
            login()
            break  # Exit the loop to go back to login

        elif choice == 6:
            cursor.close()
            db.close()
            return  # Exit the function

        else:
            print('Invalid choice !!!')
    
    cursor.close()
    db.close()
    Alumni()
def reg_events():
    import mysql.connector
    from datetime import datetime
    from prettytable import PrettyTable  # Localized import for PrettyTable

    db = mysql.connector.connect(host='localhost', user='root', password='1234', database='alumni')
    cursor = db.cursor()

    # Fetch active events with available seats
    cursor.execute("SELECT Event_ID, Event_Name, Event_Date, Available_Seats FROM events WHERE Status='Active' AND Available_Seats > 0")
    events = cursor.fetchall()

    if not events:
        print("No active events with available seats.")
        return

    # Create a PrettyTable instance
    table = PrettyTable()
    table.field_names = ["Event ID", "Event Name", "Event Date", "Seats Available"]

    # Add rows to the table
    for event in events:
        table.add_row(event)

    print('-------------------Upcoming Events-------------------')
    print(table)  # Print the formatted table

    while True:
        event_id = get_input("Enter the Event ID to register: ", is_int=True)
        cursor.execute("SELECT Event_ID, Available_Seats FROM events WHERE Event_ID=%s AND Status='Active' AND Available_Seats > 0", (event_id,))
        selected_event = cursor.fetchone()

        if selected_event:
            seats_available = selected_event[1]

            alumni_email = get_input("Enter your Email ID to register for the event: ")
            cursor.execute("SELECT Alumni_ID FROM alumni_students WHERE Email_ID=%s", (alumni_email,))
            alumni_data = cursor.fetchone()

            if alumni_data:
                alumni_id = alumni_data[0]
                registration_date = datetime.now().date()

                # Insert registration record
                cursor.execute('''INSERT INTO event_registration (Event_ID, Alumni_ID, Registration_Date)
                                  VALUES (%s, %s, %s)''', (event_id, alumni_id, registration_date))

                # Decrement the number of available seats by 1
                cursor.execute("UPDATE events SET Available_Seats = Available_Seats - 1 WHERE Event_ID = %s", (event_id,))

                db.commit()
                print("You have successfully registered for the event! Seats remaining:", seats_available - 1)
                break
            else:
                print("Alumni not found. Please check your Email ID.")
        else:
            print("Invalid Event ID or no available seats. Please select a valid event.")

    cursor.close()
    db.close()
    Alumni()
def search_alumni(name=None, email=None, passing_year=None):
    import mysql.connector
    from prettytable import PrettyTable

    db = mysql.connector.connect(host='localhost', user='root', password='1234', database='alumni')
    cursor = db.cursor()

    query = "SELECT * FROM alumni_students WHERE 1=1"
    parameters = []

    if name:
        query += " AND Name=%s"
        parameters.append(name)
    if email:
        query += " AND Email_ID=%s"
        parameters.append(email)
    if passing_year:
        query += " AND Passing_Year=%s"
        parameters.append(passing_year)

    cursor.execute(query, tuple(parameters))
    results = cursor.fetchall()

    if results:
        table = PrettyTable()
        table.field_names = ["Alumni ID", "Name", "Email ID", "Passing Year"]
        for row in results:
            table.add_row(row[:4])  # Adjust this if the table has more fields
        print("\nSearch Results:")
        print(table)
    else:
        print("No alumni found with the specified criteria.")

    cursor.close()
    db.close()
    Alumni()
    return results
