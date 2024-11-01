def is_valid_email(email):
    import re
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
    value = input(prompt)
    
    # Accept and return empty input as None (optional fields)
    if value.strip() == "":
        return None

    # Validate integer input if is_int is True
    if is_int:
        try:
            return int(value)
        except ValueError:
            print("Invalid input. Please enter a valid integer.")
            return get_user_input(prompt, is_int=True)  # Retry the prompt

    # Validate name input if is_name is True
    elif is_name:
        # Ensure the value contains only letters and spaces
        if all(part.isalpha() for part in value.split()):
            return value
        print("Invalid input. Please enter a valid name (letters only).")
        return get_user_input(prompt, is_name=True)  # Retry the prompt

    # Validate date input if is_date is True
    elif is_date:
        try:
            datetime.datetime.strptime(value, '%Y-%m-%d')
            return value  # Return the valid date as a string
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")
            return get_user_input(prompt, is_date=True)  # Retry the prompt

    # For general input without specific validation
    return value
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
