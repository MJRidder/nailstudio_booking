import gspread
from google.oauth2.service_account import Credentials
import re
import run.py

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('nailstudio_bookingsystem')


def reinstate_booking():
    """
    Receiving the date and time of an old booking that was cancelled, reinstating the date and time back into
    the Google sheet database.
    """
    dates_times = SHEET.worksheet("available_dates_times")
    
    old_id = 16
    date = "2025/01/07"
    time = "11:00"
    name = "Ash Ketchum"
    timestamp = B5

    print("correct booking details in reinstate function", correct_booking)



    print("reinstating old times, making them available for new clients...")
    find_old_date = dates_times.findall(str(correct_booking[1]), in_column=4)
    print("find_old_date", find_old_date)
    print(type(find_old_date))

    reinstate_date_row = find_old_date[0].row
    print(f"Booking row to be updated: {reinstate_date_row}")
    reinstate_date_cell = "A" + str(reinstate_date_row)
    print(reinstate_date_cell)  

    date_truth_cell = "D" + str(reinstate_date_row)
    time_truth_cell = "E" + str(reinstate_date_row)

    date_truth_check = SHEET.worksheet("available_dates_times").acell(date_truth_cell).value
    time_truth_check = SHEET.worksheet("available_dates_times").acell(time_truth_cell).value

    print("date_truth_cell value", date_truth_cell)
    print("time_truth_cell value", time_truth_cell)
    print("date_truth_check value", date_truth_check)
    print("time_truth_check" , value)
    print(type(date_truth_cell, time_truth_cell, date_truth_check, time_truth_check))

    if date_truth_check.value == correct_booking[1] and time_truth_check.value == correct_booking[2]:
        reinstate_date = SHEET.worksheet("available_dates_times").update_acell(reinstate_date_cell, correct_booking[1])
        print("reinstate_date details", reinstate_date, reinstate_date_cell, correct_booking[1])
    else:
        print("an error occured, please try again.")
        find_booking()


reinstate_booking()



# This is the booking details print ('16', '2025/01/07', '9:00', 'Ash Ketchum', 'B5')