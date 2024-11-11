import mysql.connector
import subprocess
import sys

def reset_and_create_database():
    # Connect to MySQL server (without specifying a database)
    db = mysql.connector.connect(host='localhost', user='root', password='1234')
    cursor = db.cursor()

    # Drop the alumni database if it exists, effectively clearing it
    cursor.execute("DROP DATABASE IF EXISTS alumni;")
    print("Dropped existing 'alumni' database (if it existed).")

    # Create the alumni database again
    cursor.execute("CREATE DATABASE alumni;")
    print("Created 'alumni' database.")

    # Use the alumni database
    cursor.execute("USE alumni;")

    # Recreate admin_login table for storing admin credentials
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS admin_login (
        admin_id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(50) NOT NULL,
        password VARCHAR(255) NOT NULL
    );
    ''')

    # Insert initial admin credentials
    insert_admin_credentials(cursor)

    # Recreate students table to store student information for validation
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        student_id INT AUTO_INCREMENT PRIMARY KEY,
        Name VARCHAR(255),
        F_Name VARCHAR(255),
        M_Name VARCHAR(255),
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
    ''')

    # Recreate alumni_students table for registered alumni data
    cursor.execute('''
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
    ''')

    # Recreate event table with Status as VARCHAR instead of ENUM
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS events (
        Event_ID INT AUTO_INCREMENT PRIMARY KEY,
        Event_Name VARCHAR(255),
        Event_Date DATE,
        Type VARCHAR(100),
        Venue VARCHAR(255),
        Total_Seats INT,
        Available_Seats INT,
        Status VARCHAR(20)  -- Now a VARCHAR instead of ENUM
    );
    ''')

    # Recreate event_registration table to track alumni event registrations
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS event_registration (
        registration_id INT AUTO_INCREMENT PRIMARY KEY,
        event_id INT NOT NULL,
        alumni_id INT NOT NULL,
        registration_date DATE NOT NULL,
        FOREIGN KEY (event_id) REFERENCES event(Event_ID),
        FOREIGN KEY (alumni_id) REFERENCES alumni_students(alumni_id)
    );
    ''')

    # Commit changes and close the database connection
    db.commit()
    cursor.close()
    db.close()
    print("Database and specified tables cleared and recreated successfully.")

def insert_admin_credentials(cursor):
    # SQL command to insert admin credentials
    insert_admin_query = """
    INSERT INTO admin_login (username, password) 
    VALUES (%s, %s);
    """
    # Values to insert for the admin
    admin_values = ("admin", "admin123@#")

    # Execute the query with the provided values
    cursor.execute(insert_admin_query, admin_values)

# Optional installation function for required libraries
def install_required_libraries():
    required_libraries = ['mysql','mysql-connector-python','regex','prettytable','sys','datetime','smtplib']
    for library in required_libraries:
        try:
            __import__(library)
        except ImportError:
            print("Installing", library, "...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', library])
            print(library, "installed successfully.")
        else:
            print(library, "is already installed.")

# Execute functions when the script runs
if __name__ == "__main__":
    install_required_libraries()
    reset_and_create_database()
