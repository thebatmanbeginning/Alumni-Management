import subprocess
import mysql.connector
import os

# MySQL connection details
source_user = "root"
source_host = "localhost"
source_db = "alumni"
destination_user = "root"
destination_host = "localhost"
destination_db = "alumni"
usb_path = r"C:\Users\Dark Isagi\Downloads"

# Path for the dump file
dump_file = os.path.join(usb_path, "alumni.sql")

# Step 1: Drop the existing database on the destination (but not on source)
dest_conn = mysql.connector.connect(
    host=destination_host,
    user=destination_user,
    password="1234"  # Password is 1234
)
dest_cursor = dest_conn.cursor()

# Drop the destination database if it exists and recreate it
dest_cursor.execute("DROP DATABASE IF EXISTS " + destination_db)
dest_cursor.execute("CREATE DATABASE " + destination_db)

# Close the destination database connection
dest_cursor.close()
dest_conn.close()

# Step 2: Export the source database to a SQL file using mysqldump (without affecting the source)
with open(dump_file, "w") as dump:
    subprocess.run([
        "mysqldump", 
        "-u", source_user, 
        "-p1234",  # Password is 1234
        source_db
    ], stdout=dump)

# Step 3: Import the SQL file into the destination database
with open(dump_file, "r") as dump:
    subprocess.run([
        "mysql", 
        "-u", destination_user, 
        "-p1234",  # Password is 1234
        destination_db
    ], stdin=dump)

print("Database migration completed successfully!")