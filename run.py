import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('nailstudio_bookingsystem')

def clear_screen():
    """ 
    Clears the screen from users inputs 
    """
    print("\033c", end="")


def main_menu():
    """
    Gives the user the initial options to make a booking, edit
    an existing booking or cancel.
    """
    print("*** Here comes the Nail studio logo ***\n")
    print("Welcome to our nail studio. I am looking forward to be of assistance.")
    print("Please find below the option to make your booking or edit/cancel an existing one.\n")

    print("Please type in '1' to make a new booking")
    print("Please type in '2' to update an existing booking")
    print("Please type in '3' to cancel an existing booking\n")

    # options = [
    #    "[b] Book a class",
    #    "[e] Edit your booking",
    #    "[c] Cancel your booking"]

    data_str = input("Please provide your choice here (1, 2 or 3): ")

    menu_choice_client = data_str
    validate_choice_client(menu_choice_client)
    
def validate_choice_client(values):
    print(values)
    """
    Validate the data provided by the user. Transfer values into integers
    so that they can be used to navigate through the booking system. Making
    sure the right numbers are generated, only one answer is given and no
    letters are used.
    """
    try:

        if len(values) != 1 and int(values) > 3: # Still need to find a way to ensure a number is typed, not a letter
            raise ValueError(
                f"One number is required as an answer, you provided '{values}'. Please review the suggested answers above"
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")

main_menu()

def book_appointment(value=1):
    """
    Ensure that a correct format of date is given and entered by the client.
    Format being YEAR/MM/DD. Followed by choosing a time slot, which will be
    chosen from a 1/2/3 menu. 
    """
    print("Booking your nail appointment is quick and includes a few easy steps.")
    print("Please first provide us with the date you'd like to book using the following format: (YEAR/MM/DD).")
    print("If that date is available, you can then choose one of the available time slots.")
    print("Please share your name and your contact number in case we need to reach you.")
    print("After this your booking is complete and you will receive your unique booking number.")

    menu_choices()