from utils import login
from utils import get_input
from utils import is_valid_email
def Alumni():   
    print('''-------------OPTIONS----------------\n
    1. Register as an Alumni\n
    2. View All Events\n
    3. Register for an Event\n
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
def get_valid_date(prompt):
    from datetime import datetime

    attempts = 0  # Track the number of attempts
    while attempts < 3:  # Allow up to 3 attempts
        date_str = input(prompt)
        try:
            # Try to parse the date
            valid_date = datetime.strptime(date_str, "%Y-%m-%d").date()  # Format YYYY-MM-DD
            return valid_date
        except ValueError:
            print("Invalid date format. Please enter a valid date in the format YYYY-MM-DD.")
            attempts += 1

    print("Too many invalid attempts.")
    return None  # Return None if the user fails to provide a valid date
def create_alumni_students_table():
    import mysql.connector

    db = mysql.connector.connect(host='localhost', user='root', password='1234', database='alumni')
    cursor = db.cursor()

    # Creating alumni_students table with an auto-incremented alumni_id as the primary key
    create_table_command = '''
    CREATE TABLE IF NOT EXISTS alumni_students (
        alumni_id INT AUTO_INCREMENT PRIMARY KEY,
        Name VARCHAR(255),
        M_Name VARCHAR(255),
        F_Name VARCHAR(255),
        Class VARCHAR(50),
        DOB DATE,
        Contact_Number VARCHAR(15),
        Email_ID VARCHAR(255),
        Passing_Year INT,
        Stream VARCHAR(100),
        Current_Country VARCHAR(100),
        Current_City VARCHAR(100),
        Employment_Status VARCHAR(50),
        E_Domain VARCHAR(100),
        Company VARCHAR(255)
    );
    '''
    cursor.execute(create_table_command)
    db.commit()  # Committing the changes
    cursor.close()
    db.close()
def alumni_register():
    create_alumni_students_table()
    import mysql.connector

    db = mysql.connector.connect(host='localhost', user='root', password='1234', database='alumni')
    cursor = db.cursor()

    while True:
        name = get_input('Enter your name:', is_name=True)
        f_name = get_input("Enter your Father's name: ", is_name=True)
        passing_year = get_input("Enter your Passing Year: ", is_int=True)

        while True:
            email_input = input("Enter your Email-ID: ")
            if is_valid_email(email_input):
                email = email_input
                break
            else:
                print("Invalid email format. Enter valid Email-ID")

        # Get and validate the date of birth
        dob = get_valid_date("Enter your Date of Birth (YYYY-MM-DD): ")
        if dob is None:  # If the user fails to provide a valid date
            print("Failed to register due to invalid date input.")
            break

        # Search for student in students table
        command = "SELECT * FROM students WHERE Name=%s AND F_Name=%s AND Passing_Year=%s"
        cursor.execute(command, (name, f_name, passing_year))
        data = cursor.fetchone()

        if data:
            print("----------WELCOME----------")
            # Check if the alumni is already registered
            existing_alumni = search_alumni(name=name, email=email, passing_year=passing_year)
            if existing_alumni:
                print("You are already registered as an Alumni!")
            else:
                # Insert into alumni_students
                cursor.execute('''INSERT INTO alumni_students (Name, F_Name, Class, DOB, Contact_Number, Email_ID, 
                                         Passing_Year, Stream, Current_Country, Current_City, 
                                         Employment_Status, E_Domain, Company) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''',
                    (name, f_name, data[3], dob, None, email, passing_year, None, None, None, None, None, None))

                db.commit()  # Commit the changes
                print('You are successfully registered as an Alumni!')
            break
        else:
            print("No Data found in students table! Please enter valid details.")
            break

    cursor.close()
    db.close()
def view_events():
    import mysql
    import mysql.connector
    db=mysql.connector.connect(host='localhost',user='root',password='1234',database='alumni')
    cursor=db.cursor()
    while True:
        print('-------------------------------EVENTS-----------------------------')
        print('''Please Select an Option\n1.Upcomming Events (Active)
              \n2.Completed Events \n3.Postponded Events
              \n4.Cancelled Events\n5.Main Manu\n6.Exit''')
        choice=int(input('Enter the option(1-6):'))
        if choice==1:
            cursor.execute("SELECT * FROM event WHERE status='Active'")
            active_events=cursor.fetchall()
            for event in active_events:
                print(event)
        elif choice==2:
            cursor.execute("SELECT * FROM event WHERE status='Completed'")
            completed_events=cursor.fetchall()
            for event in completed_events:
               print(event)
           
        elif choice==3:
            cursor.execute("SELECT * FROM event WHERE status='Postponded'")
            postponded_events=cursor.fetchall()
            for event in postponded_events:
                print(event)
        elif choice==4:
            cursor.execute("SELECT * FROM event WHERE status='Cancelled'")
            cancelled_events=cursor.fetchall()
            for event in cancelled_events:
                print(event)
        elif choice==5:
            login()
            break
        else:
            print('Invalid choice !!!')
#view_events()
def search_alumni(name=None, email=None, passing_year=None):
    import mysql.connector

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

    cursor.close()
    db.close()

    return results
def reg_events():
    import mysql.connector
    from datetime import datetime

    db = mysql.connector.connect(host='localhost', user='root', password='1234', database='alumni')
    cursor = db.cursor()

    # Fetch active events with available seats
    cursor.execute("SELECT event_id, event_name, event_date, seats_available FROM event WHERE status='Active' AND seats_available > 0")
    events = cursor.fetchall()

    if not events:
        print("No active events with available seats.")
        return

    print('-------------------Upcoming Events-------------------')
    for event in events:
        print("Event ID:", event[0], "Event Name:", event[1], "Event Date:", event[2], "Seats Available:", event[3])

    while True:
        event_id = get_input("Enter the Event ID to register: ", is_int=True)
        cursor.execute("SELECT event_id, seats_available FROM event WHERE event_id=%s AND status='Active' AND seats_available > 0", (event_id,))
        selected_event = cursor.fetchone()

        if selected_event:
            seats_available = selected_event[1]

            alumni_email = get_input("Enter your Email ID to register for the event: ")
            cursor.execute("SELECT id FROM alumni_students WHERE Email_ID=%s", (alumni_email,))
            alumni_data = cursor.fetchone()

            if alumni_data:
                alumni_id = alumni_data[0]
                registration_date = datetime.now().date()

                # Insert registration record
                cursor.execute('''INSERT INTO event_registration (event_id, alumni_id, registration_date)
                                  VALUES (%s, %s, %s)''', (event_id, alumni_id, registration_date))

                # Decrement the number of available seats by 1
                cursor.execute("UPDATE event SET seats_available = seats_available - 1 WHERE event_id = %s", (event_id,))

                db.commit()
                print("You have successfully registered for the event! Seats remaining:", seats_available - 1)
                break
            else:
                print("Alumni not found. Please check your Email ID.")
        else:
            print("Invalid Event ID or no available seats. Please select a valid event.")

    cursor.close()
    db.close()
