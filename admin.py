from utils import login
from utils import is_valid_email
from utils import get_input
def Admin():
    login_successful = adminlog()
    
    if login_successful:   
        print('-------WELCOME----------')
        print('''Please Select an Option
              \n1. Student Registration
              \n2. Update Student Data
              \n3. Create Event
              \n4. Update Event
              \n5. Send Mail
              \n6. Search Students
              \n7. Main Menu
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
    import getpass  

    print('--------------------------LOGIN------------------------------')
    db = None
    cursor = None
    max_attempts = 3  
    attempts = 0  

    while attempts < max_attempts:
        try:
            username = input("Enter your username: ")
            password = getpass.getpass("Enter your password: ")
            
            db = mysql.connector.connect(host="localhost", user="root", password="1234", database="alumni")
            cursor = db.cursor()
            
            query = "SELECT * FROM admin_login WHERE username=%s AND password=%s"
            cursor.execute(query, (username, password))
            
            login = cursor.fetchone()
            
            if login is not None:
                print("Login successful!")
                return True 
            else:
                attempts += 1 
                print(f"Invalid Login! Attempts remaining: {max_attempts - attempts}")
        
        except mysql.connector.Error as err:
            print("Error: ",err)
        
        finally:
            if cursor:
                cursor.close()
            if db:
                db.close()
    
    print("Maximum login attempts exceeded. Exiting the program.")
    exit()  
def register_stu():
    import datetime
    import mysql.connector
    from prettytable import PrettyTable

    Name = get_input("Enter the name of the student: ", is_name=True)
    M_Name = get_input("Enter the M_Name: ", is_name=True)
    F_Name = get_input("Enter the F_Name: ", is_name=True)
    Class = get_input("Enter the class: ")
    DoB = get_input("Enter the DOB (YYYY-MM-DD): ", is_date=True)

    try:
        dob_dt = datetime.datetime.strptime(DoB, '%Y-%m-%d')
        today = datetime.datetime.now()
        age = (today - dob_dt).days // 365
        if age < 14:
            raise ValueError("Student age is less than 14. Cannot register as an alumni.")
    except ValueError as e:
        print(e)
        return

    Contact_Number = get_input("Enter the contact number: ")

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
    E_Domain = get_input("Enter Domain of work (e.g., HR, Engineer, etc. OR N/A): ")
    Company = get_input("Enter the company OR N/A: ")

    db = mysql.connector.connect(host="localhost", user="root", password="1234", database="alumni")
    cursor = db.cursor()

    command = '''INSERT INTO students (Name, M_Name, F_Name, Class, DOB, Contact_Number, Email_ID, Passing_Year,
            Stream, Current_Country, Current_City, Employment_Status, E_Domain, Company) VALUES (%s, %s, %s, %s, %s, %s, 
            %s, %s, %s, %s, %s, %s, %s, %s)'''

    cursor.execute(command, (Name, M_Name, F_Name, Class, DoB, Contact_Number, Email_ID, Passing_Year,
                             Stream, Current_Country, Current_City, Employment_Status, E_Domain, Company))
    
    db.commit()

    cursor.execute("SELECT * FROM students WHERE Email_ID = %s", (Email_ID,))
    result = cursor.fetchone()

    table = PrettyTable()
    table.field_names = ["ID", "Name", "M_Name", "F_Name", "Class", "DOB", "Contact_Number", "Email_ID", "Passing_Year", 
                         "Stream", "Current_Country", "Current_City", "Employment_Status", "E_Domain", "Company"]
    table.add_row(result)

    print("Student registered successfully!")
    print(table)

    cursor.close()
    db.close()
def update_stu():
    from utils import get_user_input
    import mysql.connector
    from prettytable import PrettyTable

    db = mysql.connector.connect(host="localhost", user="root", password="1234", database="alumni")
    cursor = db.cursor()

    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    if not students:
        print("No students found.")
        cursor.close()
        db.close()
        return

    table = PrettyTable()
    table.field_names = [desc[0] for desc in cursor.description]
    for student in students:
        table.add_row(student)
    
    print("Students List:")
    print(table)

    choice = get_user_input("Select a student by number to update: ", is_int=True)
    student_id = students[choice - 1][0]

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

    option = get_user_input("Please enter your Option (1-9): ", is_int=True)

    if option == 1:
        new_value = get_user_input("Enter the new class: ")
        command = "UPDATE students SET Class = %s WHERE student_id = %s"
    elif option == 2:
        new_value = get_user_input("Enter the new contact number: ", is_int=True)
        command = "UPDATE students SET Contact_Number = %s WHERE student_id = %s"
    elif option == 3:
        new_value = input("Enter the new email ID: ")
        if not is_valid_email(new_value):
            print("Invalid email format. Please try again.")
            cursor.close()
            db.close()
            return
        command = "UPDATE students SET Email_ID = %s WHERE student_id = %s"
    elif option == 4:
        new_value = get_user_input("Enter the new stream: ")
        command = "UPDATE students SET Stream = %s WHERE student_id = %s"
    elif option == 5:
        new_value = get_user_input("Enter the new current country: ")
        command = "UPDATE students SET Current_Country = %s WHERE student_id = %s"
    elif option == 6:
        new_value = get_user_input("Enter the new current city: ")
        command = "UPDATE students SET Current_City = %s WHERE student_id = %s"
    elif option == 7:
        new_value = get_user_input("Enter the new employment status: ")
        command = "UPDATE students SET Employment_Status = %s WHERE student_id = %s"
    elif option == 8:
        new_value = get_user_input("Enter the new employment domain: ")
        command = "UPDATE students SET E_Domain = %s WHERE student_id = %s"
    elif option == 9:
        new_value = get_user_input("Enter the new company: ")
        command = "UPDATE students SET Company = %s WHERE student_id = %s"
    else:
        print("Invalid option.")
        cursor.close()
        db.close()
        return

    cursor.execute(command, (new_value, student_id))
    db.commit()

    cursor.execute("SELECT * FROM students WHERE student_id = %s", (student_id,))
    updated_student = cursor.fetchone()
    table = PrettyTable()
    table.field_names = [desc[0] for desc in cursor.description]
    table.add_row(updated_student)
    print(table)

    cursor.close()
    db.close()
    print("Student data updated successfully.")
def create_event():
    import mysql.connector
    from datetime import datetime, timedelta
    from prettytable import PrettyTable

    db = mysql.connector.connect(host='localhost', user='root', password='1234', database='alumni')
    cursor = db.cursor()

    event_name = input("Enter the Event Name: ")
    
    while True:
        event_date_input = get_input('Enter Date of Event (YYYY-MM-DD): ', is_date=True)
        try:
            event_date = datetime.strptime(event_date_input, '%Y-%m-%d').date()
            if event_date < datetime.now().date() + timedelta(weeks=2):
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
    
    command = '''INSERT INTO event (Event_Name, Event_Date, Type, Venue, Total_Seats, Available_Seats, Status)
                 VALUES (%s, %s, %s, %s, %s, %s, %s)'''
    
    try:
        cursor.execute(command, (event_name, event_date, type_event, venue, total_seats, available_seats, status))
        db.commit()
        
        cursor.execute("SELECT * FROM event WHERE Event_Name = %s AND Event_Date = %s", (event_name, event_date))
        created_event = cursor.fetchone()
        
        table = PrettyTable()
        table.field_names = [desc[0] for desc in cursor.description]
        table.add_row(created_event)
        
        print("Event created successfully.")
        print(table)
    except mysql.connector.Error as err:
        print("Error: ",err)
    finally:
        cursor.close()
        db.close()
def update_event():
    import mysql.connector
    from datetime import datetime
    from prettytable import PrettyTable

    db = mysql.connector.connect(host='localhost', user='root', password='1234', database='alumni')
    cursor = db.cursor()

    cursor.execute("SELECT * FROM event")
    all_events = cursor.fetchall()

    if all_events:
        table = PrettyTable()
        table.field_names = [desc[0] for desc in cursor.description]
        for event in all_events:
            table.add_row(event)
        print("Existing Events:")
        print(table)
    else:
        print("No events found.")
        cursor.close()
        db.close()
        return

    event_id = input("\nEnter the Event ID to update: ")
    cursor.execute("SELECT * FROM event WHERE Event_ID = %s", (event_id,))
    event = cursor.fetchone()

    if not event:
        print("Event not found.")
        cursor.close()
        db.close()
        return

    valid_statuses = ["Active", "Cancelled", "Postponed", "Completed"]

    status = input("Enter the new status (Active, Cancelled, Postponed, Completed) or press Enter to keep current: ")
    if status.strip() == "":
        status = event[7]
    elif status not in valid_statuses:
        print("Invalid status. Please enter one of the following: Active, Cancelled, Postponed, Completed.")
        cursor.close()
        db.close()
        return

    while True:
        event_date_input = input("Enter new Date of Event (YYYY-MM-DD) or press Enter to keep current: ")
        if event_date_input.strip() == "":
            event_date = event[2]
            break
        try:
            event_date = datetime.strptime(event_date_input, '%Y-%m-%d').date()
            break
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")

    venue = input("Enter the new venue or press Enter to keep current: ")
    if venue.strip() == "":
        venue = event[4]

    command = '''UPDATE event 
                 SET Status = %s, Event_Date = %s, Venue = %s 
                 WHERE Event_ID = %s'''
    
    try:
        cursor.execute(command, (status, event_date, venue, event_id))
        db.commit()
        print("Event updated successfully.")
    except mysql.connector.Error as err:
        print("Error:", err)
        cursor.close()
        db.close()
        return
    
    cursor.execute("SELECT * FROM event WHERE Event_ID = %s", (event_id,))
    updated_event = cursor.fetchone()

    table = PrettyTable()
    table.field_names = ["Event ID", "Event Name", "Event Date", "Type", "Venue", "Total Seats", "Available Seats", "Status"]
    table.add_row(updated_event)

    print("\nUpdated Event Details:")
    print(table)

    cursor.close()
    db.close()
def send_email_message():
    import smtplib
    from prettytable import PrettyTable
    import mysql.connector

    # Connect to the database
    db = mysql.connector.connect(host="localhost", user="root", password="1234", database="alumni")
    cursor = db.cursor()

    # Fetch active events
    cursor.execute("SELECT Event_ID, Event_Name, Event_Date, Venue FROM event WHERE Status = 'Active'")
    active_events = cursor.fetchall()

    if not active_events:
        print("No active events found.")
        cursor.close()
        db.close()
        return

    # Display active events in a table
    event_table = PrettyTable()
    event_table.field_names = ["Event ID", "Event Name", "Event Date", "Venue"]
    for event in active_events:
        event_table.add_row(event)

    print("\nActive Events:")
    print(event_table)

    send_to_all = input("Do you want to send details of these active events to the alumni? (Y/N): ").strip().upper()
    if send_to_all != "Y":
        print("Aborting email sending process.")
        cursor.close()
        db.close()
        return

    # Fetch selected students (alumni) details
    student_data = search()  # Assuming `search` function fetches a list of alumni to whom emails will be sent.

    if not student_data:
        print("No students found to send emails.")
        cursor.close()
        db.close()
        return

    recipients = []
    student_table = PrettyTable()
    student_table.field_names = ["ID", "Name", "Email"]

    for student in student_data:
        student_id = student[0]
        recipient_name = student[1]
        recipient_email = student[9]
        student_table.add_row([student_id, recipient_name, recipient_email])
        recipients.append((recipient_name, recipient_email))

    print("\nSelected Alumni:")
    print(student_table)

    try:
        # Set up email server
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        sender_email = "projects.euroschool@gmail.com"
        app_password = "nznx fzpw hvcp mgyd"

        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, app_password)

        # Email content
        subject = "Exciting New Events for Alumni"
        events_info = ""
        for event in active_events:
            events_info += event[1] + " on " + str(event[2]) + " at " + event[3] + "\n"
        body_template = (
            "Dear {},\n\n"
            "We are thrilled to inform you of some new and exciting events for our alumni community:\n\n"
            "{}\n\n"
            "We would love for you to join us!\n\n"
            "Best regards,\nAlumni Management Team"
        )

        # Send email to each recipient
        for recipient_name, recipient_email in recipients:
            body = body_template.format(recipient_name, events_info)
            message = ("Subject: ",subject,"\n\n",body)

            server.sendmail(sender_email, recipient_email, message)
            print("Email sent to", recipient_name, "at", recipient_email)

        server.quit()

    except Exception as e:
        print("Failed to send emails:", str(e))

    # Close database connection
    cursor.close()
    db.close()
def search():
    from utils import get_user_input
    import mysql.connector
    from prettytable import PrettyTable  

  
    db = mysql.connector.connect(host="localhost", user="root", password="1234", database="alumni")
    cursor = db.cursor()

   
    query = "SELECT student_id, Name, F_Name, M_Name, Passing_Year, Stream, Employment_Status, Company, E_Domain, Email_ID FROM students WHERE 1=1"
    params = []


    print("Enter the search criteria (press Enter to skip any filter):")
    name = get_user_input("Enter the student's name (or press Enter to skip): ", is_name=True)
    f_name = get_user_input("Enter the father's name (or press Enter to skip): ", is_name=True)
    m_name = get_user_input("Enter the mother's name (or press Enter to skip): ", is_name=True)
    passing_year = get_user_input("Enter the passing year (or press Enter to skip): ", is_int=True)
    stream = get_user_input("Enter the stream (or press Enter to skip): ")
    employment_status = get_user_input("Enter the employment status (or press Enter to skip): ")
    company = get_user_input("Enter the company (or press Enter to skip): ")
    domain = get_user_input("Enter the employment domain (or press Enter to skip): ")

    if name:
        query += " AND Name = %s"
        params.append(name)
    if f_name:
        query += " AND F_Name = %s"
        params.append(f_name)
    if m_name:
        query += " AND M_Name = %s"
        params.append(m_name)
    if passing_year:
        query += " AND Passing_Year = %s"
        params.append(passing_year)
    if stream:
        query += " AND Stream = %s"
        params.append(stream)
    if employment_status:
        query += " AND Employment_Status = %s"
        params.append(employment_status)
    if company:
        query += " AND Company = %s"
        params.append(company)
    if domain:
        query += " AND E_Domain = %s"
        params.append(domain)

    cursor.execute(query, tuple(params))
    results = cursor.fetchall()

    table = PrettyTable()
    table.field_names = ["Student ID", "Name", "Father's Name", "Mother's Name", "Passing Year", 
                         "Stream", "Employment Status", "Company", "Employment Domain", "Email ID"]

    for result in results:
        table.add_row(result)
    if not results:
        print("No results found.")
    else:
        print("Search Results:")
        print(table)  
    cursor.close()
    db.close()

    return results
