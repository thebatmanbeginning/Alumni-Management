def create_database_and_tables():
    import mysql.connector

    # Connect to MySQL server (without specifying a database)
    db= mysql.connector.connect(host='localhost', user='root', password='1234')
    cursor = db.cursor()

    # Drop the alumni database if it exists
    cursor.execute("DROP DATABASE IF EXISTS alumni;")
    print("Dropped existing 'alumni' database (if it existed).")

    # Create the alumni database again
    cursor.execute("CREATE DATABASE alumni;")
    print("Created 'alumni' database.")

    # Use the alumni database
    cursor.execute("USE alumni;")

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
        F_Name VARCHAR(255),
        M_Name VARCHAR(255),
        Email_ID VARCHAR(255),
        Class VARCHAR(50),
        DOB DATE,
        Passing_Year INT,
        Stream VARCHAR(100),
        Current_Country VARCHAR(100),
        Current_City VARCHAR(100),
        Employment_Status VARCHAR(50),
        E_Domain VARCHAR(100),
        Company VARCHAR(255)
    );
    ''')

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
        type VARCHAR(100),
        venue VARCHAR(255),
        total_seats INT NOT NULL,
        available_seats INT NOT NULL,
        status ENUM('Active', 'Cancelled', 'Postponed', 'Completed') DEFAULT 'Active'
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

    # Create messages table for admin messaging functionality
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS messages (
        message_id INT AUTO_INCREMENT PRIMARY KEY,
        sender_id INT NOT NULL,
        recipient_email VARCHAR(255) NOT NULL,
        subject VARCHAR(255) NOT NULL,
        body TEXT,
        sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (sender_id) REFERENCES admin_login(admin_id)
    );
    ''')

    # Create announcements table for storing admin announcements
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS announcements (
        announcement_id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        content TEXT NOT NULL,
        posted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    ''')

    # Create admin_events_log table to track admin actions on events
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS admin_events_log (
        log_id INT AUTO_INCREMENT PRIMARY KEY,
        admin_id INT NOT NULL,
        event_id INT NOT NULL,
        action VARCHAR(100) NOT NULL,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (admin_id) REFERENCES admin_login(admin_id),
        FOREIGN KEY (event_id) REFERENCES event(event_id)
    );
    ''')

    # Commit changes and close connection
    db.commit()
    cursor.close()
    db.close()
    print("Database and all tables created successfully from scratch.")

# Installation logic for required libraries
import subprocess
import sys

def install_required_libraries():
    required_libraries = [
        'mysql-connector-python',  # For MySQL connectivity
        'datetime',  # Standard library for date handling
        'regex',  # Regex for data validation
        'smtplib'  # Email handling (standard library)
    ]

    for library in required_libraries:
        try:
            __import__(library)
        except ImportError:
            print(f"Installing {library}...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', library])
            print(f"{library} installed successfully.")
        else:
            print(f"{library} is already installed.")

# Execute functions when the script runs
if __name__ == "__main__":
    install_required_libraries()
    create_database_and_tables()
