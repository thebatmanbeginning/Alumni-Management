'''
Make sure mysql is installed with the correct path! 
1."C:\Program Files\MySQL\MySQL Server 8.0\bin" copy this path
2. Press Win + R on your keyboard to open the Run and enter sysdm.cpl
3. Under the system properties window go to Advanced and Click on Environment Variables
4. Click new and Paste the copied path
5. Click on okay to exit out
6. Open CMD and enter "mysql --version"
7. If you get a similar output then your MySQL is fixed!
 "mysql  Ver 8.0.20 for Win64 on x86_64 (MySQL Community Server - GPL)"
'''
import subprocess
import mysql.connector
import os

# Prompt user to select S (Source) or D (Destination)
db_choice = input("Enter 'S' for Source Computer or 'D' for Destination Computer: ").strip().upper()

# MySQL connection details
source_user = "root"
source_host = "localhost"
source_db = "alumni"
destination_user = "root"
destination_host = "localhost"
destination_db = "alumni"
usb_path = r"D:\SQL Backup"

# Path for the dump file
dump_file = os.path.join(usb_path, "alumni.sql")

# Function to reset a database (drop and recreate)
def reset_database(host, user, password, database_name):
    conn = mysql.connector.connect(
        host=host,
        user=user,
        password=password
    )
    cursor = conn.cursor()
    cursor.execute("DROP DATABASE IF EXISTS " + database_name)
    cursor.execute("CREATE DATABASE " + database_name)
    cursor.close()
    conn.close()

# Step 1: Reset the destination database if the user chooses 'D'
if db_choice == 'D':
    print("Resetting Destination Database...")
    reset_database(destination_host, destination_user, "1234", destination_db)
elif db_choice == 'S':
    print("Source Computer selected. No reset will be performed.")
else:
    print("Invalid choice. Exiting the script.")
    exit()

# Step 2: Export the source database to a SQL file using mysqldump (this does not affect the source)
with open(dump_file, "w") as dump:
    subprocess.run([
        r"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysqldump.exe", 
        "-u", source_user, 
        "-p1234",  # Password is 1234
        source_db
    ], stdout=dump)

# Step 3: Import the SQL file into the destination database
with open(dump_file, "r") as dump:
    subprocess.run([
        r"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe", 
        "-u", destination_user, 
        "-p1234",  # Password is 1234
        destination_db
    ], stdin=dump)

print("Database migration completed successfully!")

