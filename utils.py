def is_valid_email(email):
    import regex as re
    # Remove any leading or trailing whitespace
    email = email.strip()
    # Define the regex pattern for a valid email address
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    # Check if the email matches the pattern
    return re.match(pattern, email) is not None
def login():
    user = input("Enter A(Admin) or B(Alumni): ")
    
    # Delay imports to avoid circular import issues
    if user.upper() == "A":
        from admin import Admin  # Moved import inside the function
        Admin()
    elif user.upper() == "B":
        from alumni import Alumni  # Moved import inside the function
        Alumni()
    else:
        print("Invalid Input!")
def get_user_input(prompt, is_int=False, is_name=False, is_date=False):
    import datetime
    while True:
        value = input(prompt)
        # Allow blank input for optional fields
        if value.strip() == "":
            return None  # Return None if the input is empty

        if is_int:
            try:
                return int(value)
            except ValueError:
                print("Invalid input. Please enter a valid integer.")
        elif is_name:
            # Check if the value contains only letters and spaces
            if all(part.isalpha() for part in value.split()):
                return value
            print("Invalid input. Please enter a valid name (letters only).")
        elif is_date:
            try:
                datetime.datetime.strptime(value, '%Y-%m-%d')
                return value  # Return the valid date as a string
            except ValueError and TypeError:
                print("Invalid date format. Please use YYYY-MM-DD.")

        else:
            return value  # Allow any non-empty input
def get_input(prompt, is_int=False, is_name=False, is_date=False):
    import datetime
    while True:
        value = input(prompt)
        if is_int:
            try:
                return int(value)
            except ValueError:
                print("Invalid input. Please enter a valid integer.")
        elif is_name:
            if value.isalpha() or " " in value:  # Check if it's a valid name
                return value
            print("Invalid input. Please enter a valid name (letters only).")
        elif is_date:
            try:
                datetime.datetime.strptime(value, '%Y-%m-%d')
                return value  # Return the valid date as a string
            except ValueError:
                print("Invalid date format. Please use YYYY-MM-DD.")
        else:
            if value.strip(): 
                return value
            print("Invalid input. Please enter a valid value.")
