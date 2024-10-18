# Alumni Management System

A Python-based system with MySQL integration to manage alumni and events. Alumni can register, view, and sign up for events, while admins handle data and event management. It features user authentication, input validation, and seamless database operations. Built using Python, MySQL, and MySQL Connector for efficient data handling.

## **Table of Contents**
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Features](#features)
- [Database](#database)
- [Contributing](#contributing)

## **Installation**
1. Clone the repository:
   ```bash
   git clone <repository_url>
   ```
2. Install the required dependencies:
   ```bash
   pip install mysql-connector-python
   ```
3. Set up the MySQL database:
   - Create a database named **alumni**.
   - Import relevant SQL scripts (if any) to set up tables.

## **Usage**
1. Run **computer_project.py** to start the system:
   ```bash
   python computer_project.py
   ```
2. Use the options to log in as an alumni or admin.
3. Perform operations like registering alumni, managing events, and more.

## **Project Structure**
```
├── alumni.py             # Alumni operations (registration, events)
├── admin.py              # Admin operations (event management, student data)
├── computer_project.py   # Entry point for the project
├── utils.py              # Helper functions (login, input validation)
└── README.md             # Documentation
```

## **Features**
- **Alumni Module:**  
  - Register alumni with validation against student data.
  - View upcoming, completed, and canceled events.
  - Register for events with real-time seat availability.

- **Admin Module:**  
  - Manage student records and event data.
  - Create, update, and monitor event status.

- **Utilities:**  
  - User authentication and input validation.
  - Helper functions to maintain clean and reusable code.

## **Database**
- **Tables:**
  - `students` : Stores student information for validation.
  - `alumni_students` : Holds registered alumni data.
  - `event` : Manages event details and availability.
  - `event_registration` : Tracks alumni event registrations.

## **Contributing**
Contributions are welcome! Please open issues or submit pull requests for improvements.

---

**Note:** Ensure MySQL is installed and running before starting the application.
