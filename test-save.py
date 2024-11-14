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


#def generate_booking_id():
  #  last_id = SHEET.worksheet("confirmed_bookings").col_values(1)[1:]
  #  print(last_id)
#
 #   high_id = max(last_id)
  #  new_booking_id = int(high_id) + 1
   # return new_booking_id

#print(generate_booking_id())

def update_worksheet_availability():
    """
    Updates the worksheet by removing/adding dates after a booking is made, edited or cancelled.
    """
    booking_id = ["7"]
    print(type(booking_id))
    time_cell = "B4"
    booked_time = "11:00"

    date_cell = time_cell.replace("B", "A")

    remove_time = SHEET.worksheet("available_dates_times").update_acell(time_cell, " ")
    #print("removed time")
    remove_date = SHEET.worksheet("available_dates_times").update_acell(date_cell, " ")
    #print("removed date")

    dates_times = SHEET.worksheet("confirmed_bookings")

    remove_booking_cells = dates_times.findall(booking_id[0], in_column=1)
    #print(remove_booking_cells)

    booking_row = remove_booking_cells[0].row
    #print(f"Booking row to be updated: {booking_row}")

    confirmation_cell = "F" + str(booking_row)
    #print(confirmation_cell)

    cancel_booking = SHEET.worksheet("confirmed_bookings").update_acell(confirmation_cell, "cancelled")


print(update_worksheet_availability())
