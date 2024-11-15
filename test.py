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
    Via the provided booking ID it is determined if there is an existing booking. The 
    Details are shared and it is confirmed that the right booking is approached. from
    there the client can determine if they want to edit/cancel or stop editing.
    """
    existing_booking = []

    insert_booking_id = input("What was the booking ID for your booking?: ")
    print("Please wait a moment while we fetch your booking...\n")
    print(f"insert booking ID: {insert_booking_id}")
    #print(type(insert_booking_id))


    dates_times = SHEET.worksheet("confirmed_bookings")

    existing_booking = dates_times.findall(str(insert_booking_id), in_column=1)
    #print(f"existing booking ID: {existing_booking}")
    #print(type(existing_booking))


    if existing_booking != []:
        existing_booking = dates_times.findall(str(insert_booking_id), in_column=1)
        existing_booking_value = existing_booking[0].value
        #print(f"existing booking value: {existing_booking_value}")
        #print(type(existing_booking_value))
        existing_booking.append(existing_booking_value)
        booking_return = existing_booking
        #print(f"booking return: {booking_return}")
        #print(type(booking_return))
        print("Great! we have been able to find your booking.\n")
        print(f"(to be removed) The finding booking function has ended, return = {booking_return}\n")
        return booking_return
    else:
        print("We have not been able to match your booking number.")
        try_again = input("Would you like to try again? (y/n): ")
        if try_again == "y":
            print("Great! let's try again.\n")
            find_booking()
        elif try_again == "n":
            print("Okido, let's bring you back to the main menu\n")
            main_menu()
        else:
            print("Sorry, we did not get that. We'll sent you back to the main menu so that you can try again.\n")
            main_menu()

find_booking()