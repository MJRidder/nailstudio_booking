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
    last_id = SHEET.worksheet("confirmed_bookings").col_values(1)[1:]
    print(last_id)

    high_id = max(last_id)
    new_booking_id = int(high_id) + 1
    return new_booking_id

print(generate_booking_id())