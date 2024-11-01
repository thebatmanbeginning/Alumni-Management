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
    from prettytable import PrettyTable  # Import PrettyTable

    # Establish a database connection
    db = mysql.connector.connect(host="localhost", user="root", password="1234", database="alumni")
    cursor = db.cursor()

    # Base query for searching students, using student_id as the primary key
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

    # Add conditions based on user input, if provided
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
    else:
        print("Search Results:")
        print(table)  # Print the PrettyTable

    # Close the connection
    cursor.close()
    db.close()

    return results
'''----------------------------------------------UPDATE STUDENT-----------------------------------------------------'''
def update_stu():
    from utils import get_user_input
    import mysql.connector

    db = mysql.connector.connect(host="localhost", user="root", password="1234", database="alumni")
    cursor = db.cursor()

    # Search for students and get results
    students = search()
    if not students:
        print("No students found for the given criteria.")
        return

    # Choose a student to update if multiple results were returned
    if len(students) > 1:
        print("Multiple students found. Select a student to update:")
        for i in range(len(students)):
            print(i + 1, ":", students[i])
        choice = get_user_input("Select a student by number to update: ", is_int=True)
        student_id = students[choice - 1][0]  # Get student_id from the selected result
    else:
        student_id = students[0][0]  # Use the first result's student_id if only one result

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

    # Define field updates based on the selected option
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

    # Execute the update command
    cursor.execute(command, (new_value, student_id))
    db.commit()
    print("Update successful.")

    # Close database resources
    cursor.close()
    db.close()
'''----------------------------------------------CREATE EVENT-------------------------------------------------------'''
def create_event():
    import mysql.connector
    from datetime import datetime, timedelta

    db = mysql.connector.connect(host='localhost', user='root', password='1234', database='alumni')
    cursor = db.cursor()

    # Create a new event table

    event_name = input("Enter the Event Name: ")
    
    while True:
        event_date_input = get_input('Enter Date of Event (YYYY-MM-DD): ',is_date=True)
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

    while True:
        # Fetch the search result
        student_data = search()

        if not student_data:  # If no students are found
            print("No students found to send emails.")
            return

        # Display search results and collect email addresses and names
        recipients = []
        for student in student_data:
            student_id = student[0]
            recipient_name = student[1]
            recipient_email = student[9]
            print("ID:", student_id, "Name:", recipient_name, "Email:", recipient_email)
            recipients.append((recipient_name, recipient_email))

        # Confirm sending email to all recipients
        send_to_all = input("Send email to all listed students? (Y/N): ").strip().upper()
        if send_to_all == "Y":
            try:
                # Email server setup
                smtp_server = "smtp.gmail.com"
                smtp_port = 587
                sender_email = "projects.euroschool@gmail.com"  # Sender's email
                app_password = "nznx fzpw hvcp mgyd"  # App password for Gmail

                server = smtplib.SMTP(smtp_server, smtp_port)
                server.starttls()
                server.login(sender_email, app_password)

                # Email content
                subject = "Important Update for Alumni"
                body_template = (
                    "Dear {},\n\n"
                    "We are reaching out to inform you about some exciting updates for alumni members.\n\n"
                    "Best regards,\nAlumni Management Team"
                )

                for recipient_name, recipient_email in recipients:
                    body = body_template.replace("{}", recipient_name)
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
'''----------------------------------------------UPDATE EVENT-------------------------------------------------------'''
def update_event():
    import mysql.connector
    from datetime import datetime

    db = mysql.connector.connect(host='localhost', user='root', password='1234', database='alumni')
    cursor = db.cursor()

    event_id = input("Enter the Event ID to update: ")
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
    finally:
        cursor.close()
        db.close()