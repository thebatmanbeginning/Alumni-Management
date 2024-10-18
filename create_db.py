def create_database_and_tables():
    import mysql.connector
    # Connect to MySQL server (without specifying a database)
    conn = mysql.connector.connect(host='localhost', user='root', password='1234')
    cursor = conn.cursor()
    
    # Create the alumni database if it does not exist
    cursor.execute("CREATE DATABASE IF NOT EXISTS alumni;")
    
    # Use the alumni database
    cursor.execute("USE alumni;")
    
    # Create alumni_students table
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

    # Create event table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS event (
        event_id INT AUTO_INCREMENT PRIMARY KEY,
        event_name VARCHAR(255) NOT NULL,
        event_date DATE NOT NULL,
        status VARCHAR(50) DEFAULT 'Active',
        total_seats INT NOT NULL
    );
    ''')

    # Create event_registration table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS event_registration (
        registration_id INT AUTO_INCREMENT PRIMARY KEY,
        event_id INT NOT NULL,
        alumni_id INT NOT NULL,
        registration_date DATE NOT NULL,
        FOREIGN KEY (event_id) REFERENCES event(event_id),
        FOREIGN KEY (alumni_id) REFERENCES alumni_students(alumni_id)
    );
    ''')

    # Create admin_login table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS admin_login (
        admin_id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(50) NOT NULL,
        password VARCHAR(255) NOT NULL
    );
    ''')

    # Create students table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        student_id INT AUTO_INCREMENT PRIMARY KEY,
        Name VARCHAR(255),
        Email_ID VARCHAR(255),
        F_Name VARCHAR(255),
        Passing_Year INT
    );
    ''')

    # Commit changes and close connection
    conn.commit()
    cursor.close()
    conn.close()
    print("Database and tables created successfully (if they didn't already exist).")

create_database_and_tables()

import subprocess
import sys

def install_required_libraries():
    # List of required libraries
    required_libraries = [
        'mysql-connector-python',  # For MySQL database connectivity
        'datetime',
        'regex',  # Comma added here
        'smtplib'  # For date handling (part of the standard library, no installation needed)
        # Add other libraries as needed
    ]

    for library in required_libraries:
        try:
            # Check if the library is already installed
            __import__(library)
        except ImportError:
            # If not installed, run pip to install it
            print("Installing " + library + "...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', library])
            print(library + " installed successfully.")
        else:
            print(library + " is already installed.")

# Call the function when this script is executed
if __name__ == "__main__":
    install_required_libraries()
