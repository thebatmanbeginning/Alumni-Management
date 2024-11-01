# Alumni Management System

The Alumni Management System is a Python-based application integrated with a MySQL database to manage alumni and events. It enables alumni to register, view, and sign up for events, while allowing administrators to manage student data, alumni, and event information. This system offers user authentication, input validation, and efficient data handling with MySQL operations through MySQL Connector.

## **Table of Contents**
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Features](#features)
- [Database](#database)
- [Contributing](#contributing)

## **Installation**
1. **Clone the repository**:
   ```bash
   git clone <repository_url>
   ```
2. **Install the required dependencies**:
   ```bash
   pip install mysql-connector-python
   ```
3. **Set up the MySQL database**:
   - Ensure MySQL is installed and running on your system.
   - Log in to MySQL and create a database named **alumni**:
     ```sql
     CREATE DATABASE alumni;
     ```
   - **Run `create_db.py`** to initialize the database tables:
     ```bash
     python create_db.py
     ```
     This script will set up the following tables with the required structure for the system to operate: `admin_login`, `students`, `alumni_students`, `event`, and `event_registration`.

## **Usage**
1. **Run the Main Application**:
   - Start the application by running **`computer_project.py`**:
     ```bash
     python computer_project.py
     ```
   - This script will prompt for login as an Admin or Alumni and proceed based on the user role.

2. **Alumni Operations**:
   - **Register as an Alumni**: Alumni can register themselves in the system after verifying their details against the `students` table.
   - **View Events**: Alumni can browse events categorized by status (e.g., Active, Completed).
   - **Event Registration**: Alumni can register for available events, with real-time seat verification.

3. **Admin Operations**:
   - **Manage Student Data**: Admins can update or add records in the `students` table, which is used to validate alumni.
   - **Create and Manage Events**: Admins can add new events, update event details, or modify the status of an event (Active, Completed, Postponed, or Cancelled).

## **Project Structure**
```
├── alumni.py             # Alumni operations (registration, events, event registration)
├── admin.py              # Admin operations (student and event management)
├── computer_project.py   # Entry point of the application; initiates the login process
├── utils.py              # Utility functions for login, email validation, and input handling
├── create_db.py          # Script to initialize and configure the MySQL database
└── README.md             # Documentation
```

### File Descriptions:
- **`alumni.py`**: Contains functions for alumni to register, view available events, and register for events with seat availability.
- **`admin.py`**: Manages administrative functions like adding students to the `students` table and managing event details.
- **`computer_project.py`**: The main entry point that launches the system by prompting users to log in as Admin or Alumni.
- **`utils.py`**: Provides shared utility functions, including:
  - **`is_valid_email`**: Validates email format.
  - **`login`**: Guides user login by role.
  - **`get_user_input`** and **`get_input`**: Ensures valid inputs for integers, dates, and names.
- **`create_db.py`**: Initializes the database tables, allowing smooth database setup.

## **Features**
- **Alumni Module**:
  - **Register Alumni**: Alumni can register themselves by verifying their details against the existing `students` records.
  - **View Events**: Alumni can view all events, filtering by status (Active, Completed, etc.).
  - **Event Registration**: Alumni can register for upcoming events, ensuring availability through real-time seat tracking.

- **Admin Module**:
  - **Manage Student Records**: Admins can populate and manage the `students` table with records that alumni can use for registration.
  - **Event Management**: Admins have full control over events, including creating new events, updating details, and setting the event status.

- **Utility Functions**:
  - **Email Validation**: Ensures valid email format for alumni registration.
  - **Login System**: Simple user role-based access control.
  - **Data Input Validation**: Guarantees correct input formats for dates, names, and integers, contributing to a smooth user experience.

## **Database**
The MySQL database includes the following tables:

- **`admin_login`**: Stores admin credentials for secure access to administrative functions.
- **`students`**: Contains student records for validating alumni during registration.
- **`alumni_students`**: Maintains registered alumni profiles with personal and career information.
- **`event`**: Stores event details, including the event name, date, capacity, and status.
  - Status options include:
    - **Active**: Currently open for alumni registration.
    - **Completed**: Already conducted.
    - **Postponed**: Rescheduled for a future date.
    - **Cancelled**: No longer available.
- **`event_registration`**: Tracks event registrations by associating registered alumni with specific events, ensuring seat availability.

## **Contributing**
We welcome contributions to improve the system! Please follow these steps to contribute:
1. Fork the repository and create a new branch for your feature or bug fix.
2. Make your changes and test thoroughly.
3. Submit a pull request with a clear description of your changes.

---

**Note**: Ensure that the MySQL server is active and accessible before starting the application. Configure your MySQL connection parameters in `create_db.py` if necessary.
