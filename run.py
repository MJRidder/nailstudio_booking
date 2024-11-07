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

print("Here comes the Nail studio logo")
print("Welcome to my nail studio. I")

def menu_choices():
    """
    Gives the user the initial options to make a booking, edit
    an existing booking or cancel.
    """
    print("*** Here comes the Nail studio logo ***\n")
    print("Welcome to my nail studio. I am looking forward to be of assistance")
    print("Please find below the option to make your booking or edit/cancel an existing one\n")

    print("Please type in '1' to make a new booking")
    print("Please type in '2' to update an existing booking")
    print("Please type in '3' to cancel an existing booking\n")

    data_str = input("Please provide your choice here (1, 2 or 3): ")

    menu_choice_client = data_str.split(",")
    validate_choice_client(menu_choice_client)
    
def validate_choice_client(values):
    print(values)

menu_choices()
