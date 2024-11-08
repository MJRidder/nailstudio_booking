import gspread
from google.oauth2.service_account import Credentials
import re

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
    if values == ("A") or ("a"):
        print("Book your appiontment")
        book_appointment()
    elif values == ("B") or ("b"):
        print("Edit your appiontment")
        edit_appointment()
    elif values == ("C") or ("c"):
        print("cancel your appiontment")
    else:
        print(
            f"Unfortunately your provided answer '{values}' is not one of the menu options. Please review the suggested answers above"
            )

main_menu()

def book_appointment(values):
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

def edit_appointment(values):
    """
    Ensure that a correct format of date is given and entered by the client.
    Format being YEAR/MM/DD. Followed by choosing a time slot, which will be
    chosen from a 1/2/3 menu. 
    """
    print("Editing your nail appointment is quick and includes a few easy steps.")
    print("Please first provide us with the date you'd like to book using the following format: (YEAR/MM/DD).")
    print("If that date is available, you can then choose one of the available time slots.")
    print("Please share your name and your contact number in case we need to reach you.")
    print("After this your booking is complete and you will receive your unique booking number.")

def cancel_appointment(values):
    """
    Ensure that a correct format of date is given and entered by the client.
    Format being YEAR/MM/DD. Followed by choosing a time slot, which will be
    chosen from a 1/2/3 menu. 
    """
    print("Cancelling your nail appointment is quick and includes a few easy steps.")
    print("Please first provide us with the date you'd like to book using the following format: (YEAR/MM/DD).")
    print("If that date is available, you can then choose one of the available time slots.")
    print("Please share your name and your contact number in case we need to reach you.")
    print("After this your booking is complete and you will receive your unique booking number.")

main_menu()