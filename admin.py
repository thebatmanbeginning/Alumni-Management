from utils import login
from utils import is_valid_email
from utils import get_input
def Admin():
    login_successful = adminlog()  # Getting the result(True or False)
    
    if login_successful:  # Only runs when the login_successful is True 
        while True:
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

def Admin2():
    login_successful = True  # Assuming this always succeeds for this example
    
    if login_successful:  # Only runs when the login_successful is True 
        while True:
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
                search()  # Same here
                continue  # Go back to the menu
            elif choice == 7:
                login()
            elif choice == 8:
                exit()
            else:
                print('Invalid input!')

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
                print("Invalid Login! Attempts remaining:", max_attempts - attempts)
        
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
    # Localize imports inside the function
    import datetime
    import mysql.connector
    from prettytable import PrettyTable
    from utils import get_input, is_valid_email

    # Get student details from the admin
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
    Employment_Status = get_input("Enter Employment status (e.g., Employed, Unemployed OR N/A): ")
    E_Domain = get_input("Enter Domain of work (e.g., HR, Engineer,etc. OR N/A): ")
    Company = get_input("Enter the company: ")

    # Connect to the database and insert the data
    db = mysql.connector.connect(host="localhost", user="root", password="1234", database="alumni")
    cursor = db.cursor()

    command = '''INSERT INTO students (Name, M_Name, F_Name, Class, DOB, Contact_Number, Email_ID, Passing_Year,
            Stream, Current_Country, Current_City, Employment_Status, E_Domain, Company) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''

    cursor.execute(command, (Name, M_Name, F_Name, Class, DoB, Contact_Number, Email_ID, Passing_Year,
                             Stream, Current_Country, Current_City, Employment_Status, E_Domain, Company))
    
    db.commit()

    # Fetch the newly registered student's details
    cursor.execute("SELECT * FROM students WHERE Email_ID = %s", (Email_ID,))
    registered_student = cursor.fetchone()

    # Create and display the newly registered student's data in PrettyTable format
    table = PrettyTable()
    table.field_names = ["Student ID", "Name", "Class", "DOB", "Contact Number", "Email ID", "Passing Year",
                         "Stream", "Current Country", "Current City", "Employment Status", "Employment Domain", "Company"]
    table.add_row(registered_student)

    print("\nStudent Registered Successfully!")
    print("\nRegistered Student Details:")
    print(table)

    # Close cursor and database connection
    cursor.close()
    db.close()
    Admin2()
'''----------------------------------------------SEARCH STUDENT-----------------------------------------------------'''
def search():
    from utils import get_user_input
    import mysql.connector
    from prettytable import PrettyTable

    # Establish a database connection
    db = mysql.connector.connect(host="localhost", user="root", password="1234", database="alumni")
    cursor = db.cursor()

    # Base query for searching students
    query = "SELECT student_id, Name, F_Name, M_Name, Passing_Year, Stream, Employment_Status, Company, E_Domain, Email_ID FROM students WHERE 1=1"
    params = []

    # Prompt for search criteria
    print("Enter the search criteria (press Enter to skip any filter):")
    name = get_user_input("Enter the student's name (or press Enter to skip): ", is_name=True)
    f_name = get_user_input("Enter the father's name (or press Enter to skip): ", is_name=True)
    m_name = get_user_input("Enter the mother's name (or press Enter to skip): ", is_name=True)
    passing_year = get_user_input("Enter the passing year (or press Enter to skip): ", is_int=True)
    stream = get_user_input("Enter the stream (or press Enter to skip): ")
    employment_status = get_user_input("Enter the employment status (or press Enter to skip): ")
    company = get_user_input("Enter the company (or press Enter to skip): ")
    domain = get_user_input("Enter the employment domain (or press Enter to skip): ")

    # Add conditions based on user input
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

    # Execute the query with filters if provided
    cursor.execute(query, tuple(params))
    results = cursor.fetchall()

    # Create a PrettyTable object for displaying results
    table = PrettyTable()
    table.field_names = ["Student ID", "Name", "Father's Name", "Mother's Name", "Passing Year", 
                         "Stream", "Employment Status", "Company", "Employment Domain", "Email ID"]

    # Add rows to the table
    for result in results:
        table.add_row(result)

    # Display results in a table format
    if not results:
        print("No results found.")
        return [], []  # Return empty lists if no results found
    else:
        print("Search Results:")
        print(table)  # Print the PrettyTable

    # Close the connection
    cursor.close()
    db.close()

    # Create a list of emails
    email_list = [result[9] for result in results]  # Email_ID is the last column
    return results, email_list  # Return student data and list of emails
'''----------------------------------------------UPDATE STUDENT-----------------------------------------------------'''
def update_stu():
    # Localize imports inside the function
    from prettytable import PrettyTable
    from utils import get_user_input
    import mysql.connector

    # Connect to the database
    db = mysql.connector.connect(host="localhost", user="root", password="1234", database="alumni")
    cursor = db.cursor()

    # Fetch all students
    cursor.execute("SELECT student_id, name FROM students")
    students = cursor.fetchall()

    if not students:
        print("No students found in the database.")
        return

    # Create a PrettyTable instance for displaying student data
    table = PrettyTable()
    table.field_names = ["Student ID", "Name"]  # Set column headers

    # Add each student to the table
    for student in students:
        table.add_row([student[0], student[1]])

    # Display the table
    print("All Students:")
    print(table)

    # Ask the admin to select a student ID
    student_id_input = get_user_input("Enter the student ID you want to update: ").strip()

    try:
        # Convert user input to an integer
        student_id = int(student_id_input)
    except ValueError:
        print("Invalid student ID format. Please enter a valid numeric student ID.")
        return

    # Check if the student ID exists in the database
    if not any(student[0] == student_id for student in students):
        print("Invalid student ID. Please try again.")
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

    # Ask for update option
    option = get_user_input("Please enter your Option (1-9): ", is_int=True)

    # Handle the update based on the selected option
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
            return
        command = "UPDATE students SET Email_ID = %s WHERE student_id = %s"
    elif option == 4:
        new_value = get_user_input("Enter the new stream: ", is_name=True)
        command = "UPDATE students SET Stream = %s WHERE student_id = %s"
    elif option == 5:
        new_value = get_user_input("Enter the new country: ", is_name=True)
        command = "UPDATE students SET Current_Country = %s WHERE student_id = %s"
    elif option == 6:
        new_value = get_user_input("Enter the new city: ")
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
        print("Invalid option selected.")
        return

    # Execute the update command for the selected student
    cursor.execute(command, (new_value, student_id))

    # Commit the changes to the database
    db.commit()

    print("Update successful.")

    # Fetch the updated student's details
    cursor.execute("SELECT * FROM students WHERE student_id = %s", (student_id,))
    updated_student = cursor.fetchone()

    # Create and display the updated student's data in PrettyTable format
    table = PrettyTable()
    table.field_names = ["Student ID", "Name", "Class", "DOB", "Contact Number", "Email ID", "Passing Year",
                         "Stream", "Current Country", "Current City", "Employment Status", "Employment Domain", "Company"]
    table.add_row(updated_student)

    print("\nUpdated Student Details:")
    print(table)

    # Close cursor and database connection
    cursor.close()
    db.close()
    Admin2()
'''----------------------------------------------CREATE EVENT-------------------------------------------------------'''
def create_event():
    # Localize imports inside the function
    from prettytable import PrettyTable
    import mysql.connector
    from datetime import datetime, timedelta

    # Connect to the database
    db = mysql.connector.connect(host='localhost', user='root', password='1234', database='alumni')
    cursor = db.cursor()

    # Gather event information from the user
    event_name = input("Enter the Event Name: ")

    while True:
        event_date_input = get_input('Enter Date of Event (YYYY-MM-DD): ', is_date=True)
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
        return
    finally:
        cursor.close()

    # Fetch the most recently created event (assuming events are inserted in order)
    cursor = db.cursor()
    cursor.execute("SELECT * FROM event WHERE Event_Name = %s AND Event_Date = %s ORDER BY Event_ID DESC LIMIT 1", 
                   (event_name, event_date))
    event = cursor.fetchone()

    # Display the event details using PrettyTable
    if event:
        table = PrettyTable()
        table.field_names = ["Event ID", "Event Name", "Event Date", "Type", "Venue", "Total Seats", "Available Seats", "Status"]
        table.add_row(event)
        print("\nRegistered Event:")
        print(table)
    else:
        print("Error: Unable to fetch the created event details.")
    
    # Close the database connection
    db.close()
    Admin2()
'''----------------------------------------------SEND MESSAGE-------------------------------------------------------'''
def send_email_message():
    # Localizing imports inside the function
    import smtplib
    import mysql.connector
    from prettytable import PrettyTable

    # Step 1: Connect to the database
    db = mysql.connector.connect(host="localhost", user="root", password="1234", database="alumni")
    cursor = db.cursor()

    # Step 2: Fetch all active events (no year restriction)
    cursor.execute('''
        SELECT Event_ID, Event_Name, Event_Date, Venue, Status
        FROM event
        WHERE Status = 'Active'
        ORDER BY Event_Date
    ''')

    active_events = cursor.fetchall()

    if not active_events:
        print("No active events found.")
        return

    # Step 3: Display events in a PrettyTable
    print("\nActive Events:")
    events_table = PrettyTable()
    events_table.field_names = ["Event ID", "Event Name", "Event Date", "Venue", "Status"]
    
    for event in active_events:
        events_table.add_row(event)
    
    print(events_table)

    # Step 4: Allow admin to select event(s) to send email for
    selected_event_ids = input("\nEnter the Event IDs you want to send emails for (comma-separated): ").strip()

    # Convert to list of event IDs
    try:
        selected_event_ids = [int(event_id.strip()) for event_id in selected_event_ids.split(",")]
    except ValueError:
        print("Invalid input. Please enter valid Event IDs.")
        return

    # Check if the selected event IDs are valid
    valid_event_ids = [event[0] for event in active_events]
    invalid_ids = [event_id for event_id in selected_event_ids if event_id not in valid_event_ids]

    if invalid_ids:
        print("Invalid Event IDs: " + ", ".join(map(str, invalid_ids)) + ". Please try again.")
        return

    # Step 5: Create the email body for the selected events
    event_details = "Upcoming Active Events:\n\n"
    
    for event_id in selected_event_ids:
        event = next((e for e in active_events if e[0] == event_id), None)
        if event:
            event_details += (
                "Event ID: " + str(event[0]) + "\n"
                "Event Name: " + event[1] + "\n"
                "Event Date: " + str(event[2]) + "\n"
                "Venue: " + event[3] + "\n"
                "Status: " + event[4] + "\n\n"  # Ensure proper new line after each event
            )

    # Step 6: Perform the search and get recipients (alumni) for the email
    while True:
        recipients, emails = search()  # Perform the search and get recipients and emails
        if not recipients:
            print("No students found to send emails.")
            return

        # Confirm sending email to all recipients
        send_to_all = input("Send email to all listed students for " + str(len(selected_event_ids)) + " event(s)? (Y/N): ").strip().upper()
        if send_to_all == "Y":
            try:
                # Step 7: Email server setup
                smtp_server = "smtp.gmail.com"
                smtp_port = 587
                sender_email = "projects.euroschool@gmail.com"  # Sender's email
                app_password = "nznx fzpw hvcp mgyd"  # App password for Gmail

                server = smtplib.SMTP(smtp_server, smtp_port)
                server.starttls()
                server.login(sender_email, app_password)

                # Email content
                subject = "Upcoming Active Events for Alumni"
                body_template = (
                    "Dear {},\n\n"
                    "We are excited to share the following upcoming active events for you to attend:\n\n"
                    "{event_details}"  # Add the event details here
                    "Best regards,\nAlumni Management Team"
                )

                # Loop through recipients and emails
                for (student_id, recipient_name, *other_info, recipient_email) in recipients:
                    body = body_template.format(recipient_name, event_details=event_details)
                    message = "Subject: " + subject + "\n\n" + body

                    # Send the email to the current recipient
                    server.sendmail(sender_email, recipient_email, message)
                    print("Email sent to", recipient_name, "at", recipient_email)

                server.quit()
                break

            except Exception as e:
                print("Failed to send emails:", str(e))
                break

        elif send_to_all == "N":
            print("Restarting search.")
            continue

        else:
            print("Invalid input. Please enter 'Y' or 'N'.")
    Admin2()
'''----------------------------------------------UPDATE EVENT-------------------------------------------------------'''
def update_event():
    # Localize imports inside the function
    import mysql.connector
    from datetime import datetime
    from prettytable import PrettyTable

    # Connect to the database
    db = mysql.connector.connect(host='localhost', user='root', password='1234', database='alumni')
    cursor = db.cursor()

    try:
        # Prompt for Event ID
        event_id = input("Enter the Event ID to update: ")
        cursor.execute("SELECT * FROM event WHERE Event_ID = %s", (event_id,))
        event = cursor.fetchone()

        if not event:
            print("Event not found.")
            return

        valid_statuses = ["Active", "Cancelled", "Postponed", "Completed"]

        # Update event status
        status = input("Enter the new status (Active, Cancelled, Postponed, Completed) or press Enter to keep current: ")
        if status.strip() == "":
            status = event[7]  # Keep the current status
        elif status not in valid_statuses:
            print("Invalid status. Please enter one of the following: Active, Cancelled, Postponed, Completed.")
            return

        # Update event date
        while True:
            event_date_input = input("Enter new Date of Event (YYYY-MM-DD) or press Enter to keep current: ")
            if event_date_input.strip() == "":
                event_date = event[2]  # Keep the current date
                break
            try:
                event_date = datetime.strptime(event_date_input, '%Y-%m-%d').date()
                break
            except ValueError:
                print("Invalid date format. Please use YYYY-MM-DD.")

        # Update venue
        venue = input("Enter the new venue or press Enter to keep current: ")
        if venue.strip() == "":
            venue = event[4]  # Keep the current venue

        # SQL command to update the event
        command = '''UPDATE event 
                     SET Status = %s, Event_Date = %s, Venue = %s 
                     WHERE Event_ID = %s'''
        
        cursor.execute(command, (status, event_date, venue, event_id))
        db.commit()
        print("Event updated successfully.")

        # Fetch the updated event details
        cursor.execute("SELECT * FROM event WHERE Event_ID = %s", (event_id,))
        updated_event = cursor.fetchone()

        # Create and display the updated event in PrettyTable format
        table = PrettyTable()
        table.field_names = ["Event ID", "Event Name", "Event Date", "Venue", "Status"]
        table.add_row(updated_event)

        print("\nUpdated Event Details:")
        print(table)

    except mysql.connector.Error as err:
        print("Error:", err)

    finally:
        cursor.close()
        db.close()
        Admin2()
