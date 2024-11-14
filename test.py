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


def find_booking():
    """
    funtion to find the booking, based on booking ID.
    """
    booking_id = [99]

    dates_times = SHEET.worksheet("confirmed_bookings")

    existing_booking = dates_times.findall(str(booking_id[0]), in_column=1)
    if existing_booking == dates_times.findall(str(booking_id[0]), in_column=1):
        print(existing_booking)
        if existing_booking:
            cell = existing_booking[0]
            row_number = cell.row
    else:
        print("Sorry, we did not get that. Please ensure that you use the suggested y or n format.")
        find_booking()
    

find_booking()


