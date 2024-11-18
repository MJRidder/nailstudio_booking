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


def cancel_booking(correct_booking):
    """
    Find a booking based off the booking_id. confirm what of the original booking needs to be
    edited. Confirm availability to edit. Make new booking with a new booking ID and booking 
    data. Reinstate the original booking.
    """
    confirmed_bookings = SHEET.worksheet("confirmed_bookings")
    print("correct_booking details (tuple)", correct_booking)
    print(type(correct_booking))

    print("finding your old appointment...")

    find_old_id = confirmed_bookings.findall(str(correct_booking[0]), in_column=1)
    print("find_old_id", find_old_id)
    print(type(find_old_id))

    booking_row = find_old_id[0].row
    #print(f"Booking row to be updated: {booking_row}")

    confirmation_cell = "G" + str(booking_row)
    #print(confirmation_cell)

    print("Cancelling your old appointment")
    cancel_booking = SHEET.worksheet("confirmed_bookings").update_acell(confirmation_cell, "cancelled")

    #print(cancel_booking, date, time)
    print("old appointment cancelled")

cancel_booking()



# This is the booking details print ('16', '2025/01/07', '9:00', 'Ash Ketchum', 'B5')