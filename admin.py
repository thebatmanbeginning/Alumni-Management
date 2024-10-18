from utils import login
from utils import is_valid_email
from utils import get_input
def Admin():
    login_successful = adminlog()  # Getting the result(True or False)
    
    if login_successful:  #Only runs when the login_successful is True 
        print('-------WELCOME----------')
        print('''Please Select an Option
              \n1. Register a student
              \n2. Update existing student data
              \n3. Create event
              \n4. Update an  event
              \n5. Send message
              \n6. Search a Student
              \n7. Return to Main Menu
              \n8. Exit''')
        print("\n\n\n")
        choice = int(input('Enter a Choice (1-8): '))
        
        if choice == 1:
            register_stu()
        elif choice == 2:
            update_stu()
        elif choice == 3:
            create_event()
        elif choice == 4:
            update_event()
        elif choice == 5:
            send_email_message()
        elif choice == 6:
            search()
        elif choice == 7:
            login()
        elif choice == 8:
            exit()
        else:
            print('Invalid input!')
    else:
        print('Login failed. Please try again.')
def adminlog():
    import mysql
    import mysql.connector
    import getpass  # Import getpass module for secure password input

    print('--------------------------LOGIN------------------------------')
    db = None
    cursor = None
    max_attempts = 3  # Maximum number of login attempts
    attempts = 0  # Initialize the attempt counter

    while attempts < max_attempts:
        try:
            username = input("Enter your username: ")
            password = getpass.getpass("Enter your password: ")  # Use getpass to hide password input
            
            db = mysql.connector.connect(host="localhost", user="root", password="1234", database="alumni")
            cursor = db.cursor()
            
            query = "SELECT * FROM admin_login WHERE username=%s AND password=%s"
            cursor.execute(query, (username, password))
            
            login = cursor.fetchone()
            
            if login is not None:
                print("Login successful!")
                return True  # Exit the function on successful login
            else:
                attempts += 1  # Increment the attempt counter
                print(f"Invalid Login! Attempts remaining: {max_attempts - attempts}")
        
        except mysql.connector.Error as err:
            print("Error: {}".format(err))
        
        finally:
            if cursor:
                cursor.close()
            if db:
                db.close()
    
    print("Maximum login attempts exceeded. Exiting the program.")
    exit()  # Exit the program after three failed attempts
'''----------------------------------------------REGISTER STUDENT---------------------------------------------------'''
def register_stu():
    import datetime
    import mysql.connector

    Name = get_input("Enter the name of the student: ", is_name=True)
    M_Name = get_input("Enter the M_Name: ", is_name=True)
    F_Name = get_input("Enter the F_Name: ", is_name=True)
    Class = get_input("Enter the class: ")
    DoB = get_input("Enter the DOB (YYYY-MM-DD): ", is_date=True)

    # Calculate age
    try:
        dob_dt = datetime.datetime.strptime(DoB, '%Y-%m-%d')
        today = datetime.datetime.now()
        age = (today - dob_dt).days // 365
        
        if age < 14:
            raise ValueError("Student age is less than 14. Cannot register as an alumni.")
        
    except ValueError as e:
        print(e)
        return  # Exit the function if age is less than 14 or other error occurs

    Contact_Number = get_input("Enter the contact number: ")

    # Validate email and prompt again if invalid
    while True:
        email_input = get_input("Enter the email: ")
        if is_valid_email(email_input):
            Email_ID = email_input
            break
        else:
            print("Invalid email format. Please try again.")

    Passing_Year = get_input("Enter the passing year: ", is_int=True)
    Stream = get_input("Enter the stream taken: ")
    Current_Country = get_input("Enter the Current country of the student: ")
    Current_City = get_input("Enter the current city of the student: ")
    Employment_Status = get_input("Enter Employment status (e.g., Employed, Unemployed, etc.): ")
    E_Domain = get_input("Enter Domain of work (e.g., HR, Engineer, etc.): ")
    Company = get_input("Enter the company: ")

    # Connect to the database and insert the data
    db = mysql.connector.connect(host="localhost", user="root", password="1234", database="alumni")
    cursor = db.cursor()

    command = '''INSERT INTO students (Name, M_Name, F_Name, Class, DOB, Contact_Number, Email_ID, Passing_Year,
            Stream, Current_Country, Current_City, Employment_Status, E_Domain, Company) VALUES (%s, %s, %s, %s, %s, %s, 
            %s, %s, %s, %s, %s, %s, %s, %s)'''

    cursor.execute(command, (Name, M_Name, F_Name, Class, DoB, Contact_Number, Email_ID, Passing_Year,
                             Stream, Current_Country, Current_City, Employment_Status, E_Domain, Company))
    
    db.commit()
    cursor.close()
    db.close()
    print("Student registered successfully!")
'''----------------------------------------------SEARCH STUDENT-----------------------------------------------------'''
def search():
    from utils import get_user_input
    import mysql.connector

    # Connect to the database
    db = mysql.connector.connect(host="localhost", user="root", password="1234", database="alumni")
    cursor = db.cursor()

    # Base query
    query = "SELECT alumni_id, Name, F_Name, M_Name, Passing_Year, Stream, Employment_Status, Company, E_Domain, Email_ID FROM students WHERE 1=1"
    params = []

    # Get search criteria from the user with proper validation
    print("Enter the search criteria (press Enter to skip any filter):")
    name = get_user_input("Enter the student's name (or press Enter to skip): ", is_name=True)
    f_name = get_user_input("Enter the father's name (or press Enter to skip): ", is_name=True)
    m_name = get_user_input("Enter the mother's name (or press Enter to skip): ", is_name=True)
    passing_year = get_user_input("Enter the passing year (or press Enter to skip): ", is_int=True)
    stream = get_user_input("Enter the stream (or press Enter to skip): ")
    employment_status = get_user_input("Enter the employment status (or press Enter to skip): ")
    company = get_user_input("Enter the company (or press Enter to skip): ")
    domain = get_user_input("Enter the employment domain (or press Enter to skip): ")

    # Add conditions based on user input, if provided
    if name is not None:
        query += " AND Name = %s"
        params.append(name)
    if f_name is not None:
        query += " AND F_Name = %s"
        params.append(f_name)
    if m_name is not None:
        query += " AND M_Name = %s"
        params.append(m_name)
    if passing_year is not None:
        query += " AND Passing_Year = %s"
        params.append(passing_year)
    if stream is not None:
        query += " AND Stream = %s"
        params.append(stream)
    if employment_status is not None:
        query += " AND Employment_Status = %s"
        params.append(employment_status)
    if company is not None:
        query += " AND Company = %s"
        params.append(company)
    if domain is not None:
        query += " AND E_Domain = %s"
        params.append(domain)

    # Execute the query with or without filters
    cursor.execute(query, tuple(params))
    results = cursor.fetchall()
    print(results)
    cursor.close()
    db.close()

    return results  # Return the results for further processing
'''----------------------------------------------UPDATE STUDENT-----------------------------------------------------'''
def update_stu():
    import mysql
    import mysql.connector

    db = mysql.connector.connect(host="localhost", user="root", password="1234", database="alumni")
    cursor = db.cursor()

    stu_ids = search()  # Assuming this function returns a list of student IDs


    # Initialize stu_id
    stu_id = None

    # Check if stu_ids is a list and has at least one item
    if isinstance(stu_ids, list):
        if stu_ids:  # Check if the list is not empty
            stu_id = stu_ids[0]  # Get the first student ID

    # Check if a valid student ID was found 
        if stu_id is None:
            print("No valid student ID found.")
            db.close()
            cursor.close()
            return
    print("----------------Select option to update-----------------")
    print(
        "1: Class\n"
        "2: Contact Number\n"
        "3: Email_ID\n"
        "4: Stream\n"
        "5: Current Country\n"
        "6: Current City\n"
        "7: Employment Status\n"
        "8: Employment Domain\n"
        "9: Company\n"
    )
    
    option = get_input("Please enter your Option (1-9): ", is_int=True)
    
    if option == 1:
        # Class Updation
        while True:
            new_class = get_input("Enter the new class: ")
            command = "UPDATE students SET Class = %s WHERE Stu_Id = %s"
            cursor.execute(command, (new_class, stu_id))  # Use stu_id here
            db.commit()
            print("Class updated successfully!")
            break
            
    elif option == 2:
        # Contact Number Updation
        while True:
            new_contact = get_input("Enter the new contact number: ", is_int=True)
            command = "UPDATE students SET Contact_No = %s WHERE Stu_Id = %s"
            cursor.execute(command, (new_contact, stu_id))
            db.commit()
            print("Contact Number successfully updated!")
            break
            
    elif option == 3:
        # Email_ID Updation
        while True:
            new_email = input("Enter the new email ID: ")
            if is_valid_email(new_email):
                command = "UPDATE students SET Email_ID = %s WHERE Stu_Id = %s"
                cursor.execute(command, (new_email, stu_id))
                db.commit()
                print("Email ID updated successfully!")
                break
            else:
                print("Invalid email format. Please try again.")
            
    elif option == 4:
        # Stream Updation
        while True:
            new_stream = get_input("Enter the new stream: ", is_name=True)
            command = "UPDATE students SET Stream = %s WHERE Stu_Id = %s"
            cursor.execute(command, (new_stream, stu_id))
            db.commit()
            print("Stream updated successfully!")
            break
            
    elif option == 5:
        # Current Country Updation
        while True:
            new_country = get_input("Enter the new country: ", is_name=True)
            command = "UPDATE students SET Current_Country = %s WHERE Stu_Id = %s"
            cursor.execute(command, (new_country, stu_id))
            db.commit()
            print("Current Country updated successfully!")
            break
            
    elif option == 6:
        # Current City Updation
        while True:
            new_city = get_input("Enter the new city: ")
            command = "UPDATE students SET Current_City = %s WHERE Stu_Id = %s"
            cursor.execute(command, (new_city, stu_id))
            db.commit()
            print("Current City updated successfully!")
            break
            
    elif option == 7:
        # Employment Status Updation
        while True:
            new_employment_status = get_input("Enter the new employment status: ")
            command = "UPDATE students SET Employment_Status = %s WHERE Stu_Id = %s"
            cursor.execute(command, (new_employment_status, stu_id))
            db.commit()
            print("Employment Status updated successfully!")
            break
            
    elif option == 8:
        # Employment Domain
        while True:
            new_employment_domain = get_input("Enter the new employment domain: ")
            command = "UPDATE students SET Employment_Domain = %s WHERE Stu_Id = %s"
            cursor.execute(command, (new_employment_domain, stu_id))
            db.commit()
            print("Employment Domain updated successfully!")
            break
            
    elif option == 9:
        # Company Updation
        while True:
            new_company = get_input("Enter the new company: ")
            command = "UPDATE students SET Company = %s WHERE Stu_Id = %s"
            cursor.execute(command, (new_company, stu_id))
            db.commit()
            print("Company updated successfully!")
            break
            
    else:
        print('Invalid input. Please select a valid option (1-9).')

    db.close()
    cursor.close()
'''----------------------------------------------CREATE EVENT-------------------------------------------------------'''
def create_event():
    import mysql.connector
    from datetime import datetime, timedelta

    db = mysql.connector.connect(host='localhost', user='root', password='1234', database='alumni')
    cursor = db.cursor()

    # Create a new event table
    cursor.execute('''
    CREATE IF NOT EXISTS TABLE event (
        Event_ID INT AUTO_INCREMENT PRIMARY KEY,
        Event_Name VARCHAR(255),
        Event_Date DATE,
        Type VARCHAR(100),
        Venue VARCHAR(255),
        Total_Seats INT,
        Available_Seats INT,
        Status ENUM('Active', 'Cancelled', 'Postponed', 'Completed')
    )
    ''')

    event_name = input("Enter the Event Name: ")
    
    while True:
        event_date_input = input('Enter Date of Event (YYYY-MM-DD): ')
        try:
            event_date = datetime.strptime(event_date_input, '%Y-%m-%d').date()
            if event_date < datetime.now().date() + timedelta(weeks=2):  # Check for 2 weeks
                print("Event date must be at least 2 weeks from today's date. Please try again.")
            else:
                break
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")

    type_event = input("Enter the type of event (e.g., Seminar, Workshop, Conference): ")
    venue = input("Enter the venue: ")

    while True:
        try:
            total_seats = int(input("Enter the total number of seats: "))
            available_seats = int(input("Enter the seats available: "))
            if available_seats > total_seats:
                print("Available seats cannot exceed the total number of seats. Please enter again.")
            else:
                break
        except ValueError:
            print("Invalid input. Please enter a valid integer for the number of seats.")

    status = input("Enter the status (Active, Cancelled, Postponed, Completed): ")
    
    # Insert event data into the database
    command = '''INSERT INTO event (Event_Name, Event_Date, Type, Venue, Total_Seats, Available_Seats, Status)
                 VALUES (%s, %s, %s, %s, %s, %s, %s)'''
    
    try:
        cursor.execute(command, (event_name, event_date, type_event, venue, total_seats, available_seats, status))
        db.commit()
        print("Event created successfully.")
    except mysql.connector.Error as err:
        print("Error: {}".format(err))
    finally:
        cursor.close()
        db.close()
'''----------------------------------------------SEND MESSAGE-------------------------------------------------------'''
def send_email_message():
    import smtplib

    # Fetch the search result first
    student_data = search()

    if not student_data:  # If no students are found
        print("No students found to send emails.")
        return

    # Get the student ID to whom the email will be sent
    student_id = input("Enter the Student ID to send the email to: ")

    # Find the selected student's email and name using the ID
    recipient_email = None
    recipient_name = None

    for student in student_data:
        if str(student[0]) == student_id:  # Use the index for alumni_id
            recipient_email = student[9]  # Email_ID is at index 9
            recipient_name = student[1]  # Name is at index 1
            break

    if not recipient_email:
        print("Invalid Student ID. Email not sent.")
        return

    try:
        # Prepare the email
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        sender_email = "projects.euroschool@gmail.com"  # Use your sender's email here
        app_password = "nznx fzpw hvcp mgyd"  # App password for Gmail

        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, app_password)

        subject = "Important Update for Alumni"
        body = "Dear {},\n\nWe are reaching out to inform you about some exciting updates for alumni members.\n\nBest regards,\nAlumni Management Team".format(recipient_name)

        message = "Subject: {}\n\n{}".format(subject, body)

        # Send the email
        server.sendmail(sender_email, recipient_email, message)
        print("Email sent to {} at {}".format(recipient_name, recipient_email))

        server.quit()

    except Exception as e:
        print("Failed to send email: " + str(e))
'''----------------------------------------------UPDATE EVENT-------------------------------------------------------'''
def update_event():
    import mysql.connector
    from datetime import datetime

    db = mysql.connector.connect(host='localhost', user='root', password='1234', database='alumni')
    cursor = db.cursor()

    # Get the Event ID to update
    event_id = input("Enter the Event ID to update: ")

    # Check if the event exists
    cursor.execute("SELECT * FROM event WHERE Event_ID = %s", (event_id,))
    event = cursor.fetchone()

    if not event:
        print("Event not found.")
        cursor.close()
        db.close()
        return

    # Update status
    status = input("Enter the new status (Active, Cancelled, Postponed, Completed) or press Enter to keep current: ")
    if status.strip() == "":
        status = event[6]  # Keep the current status if no new input is provided

    # Update event date
    while True:
        event_date_input = input('Enter new Date of Event (YYYY-MM-DD) or press Enter to keep current: ')
        if event_date_input.strip() == "":
            event_date = event[2]  # Keep the current date if no new input is provided
            break
        try:
            event_date = datetime.strptime(event_date_input, '%Y-%m-%d').date()
            break
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")

    # Update venue
    venue = input("Enter the new venue or press Enter to keep current: ")
    if venue.strip() == "":
        venue = event[4]  # Keep the current venue if no new input is provided

    # Update the event in the database
    command = '''UPDATE event 
                 SET Status = %s, Event_Date = %s, Venue = %s 
                 WHERE Event_ID = %s'''
    
    try:
        cursor.execute(command, (status, event_date, venue, event_id))
        db.commit()
        print("Event updated successfully.")
    except mysql.connector.Error as err:
        print("Error: {}".format(err))
    finally:
        cursor.close()
        db.close()
       