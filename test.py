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

    date = "2025/01/07"
    time = "11:00"

    print("date and time", date, time)
    #print(type(date, time))

    find_old_date = dates_times.findall(str(date), in_column=4)
    print("find_old_date", find_old_date)
    print(type(find_old_date))

    find_old_time = dates_times.findall(str(time), in_column=5)
    #print("find_old_time", find_old_time)
    print(type(find_old_time)) 

    cells = get_date_cell(find_old_date)
    print("find_old_date cells", cells)
    print(type(cells))

    #if find_old_date == str(date) and find_old_time == str(time):
    #    print("this is what will be captured", find_old_date, find_old_time) 


    #reinstate_date_row = find_old_date[0].row
    #print(f"Booking row to be updated: {reinstate_date_row}")
    #reinstate_date_cell = "A" + str(reinstate_date_row)
    #print(reinstate_date_cell)

    #reinstate_date = SHEET.worksheet("available_dates_times").update_acell(reinstate_date_cell, date)
    #print(reinstate_date)


reinstate_booking()



    #find_old_time = dates_times.findall(str(date), in_column=5)
   # print("find_old_time", find_old_time)
   # print(type(find_old_time))