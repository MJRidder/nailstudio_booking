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

def generate_booking_id():
    list_id = SHEET.worksheet("confirmed_bookings").col_values(1)[1:]
    print(list_id)

    max_value = None
    for n in list_id:
        if max_value is None or int(n) > max_value: max_value = int(n)
    print(max_value)

    new_booking_id = int(max_value) + 1
    print(new_booking_id)

generate_booking_id()
