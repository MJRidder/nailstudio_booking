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
    # Have to insert a while loop still to avoid clients having to start over each time
    print("*** Here comes the Nail studio logo ***\n")
    print("Welcome to our nail studio. I am looking forward to be of assistance.")
    print("Please find below the option to make your booking or edit/cancel an existing one.\n")

    print("Please type in 'A' to make a new booking")
    print("Please type in 'B' to update an existing booking")
    print("Please type in 'C' to cancel an existing booking\n")

    data_str = input("Please provide your choice here (A, B or C): ")

    validate_choice_client(data_str)

def validate_choice_client(choice):
    choice = choice.strip().lower()
    """
    Validate the data provided by the user. Transfer values into integers
    so that they can be used to navigate through the booking system. Making
    sure the right numbers are generated, only one answer is given and no
    letters are used.
    """
    if choice ==  "a":
        print("Book your appointment")
        book_appointment()
    elif choice == "b":
        print("Edit your appointment")
        edit_appointment()
    elif choice == "c":
        print("Cancel your appointment")
        cancel_appointment()
    else:
        print(
            f"Unfortunately your provided answer '{choice}' is not one of the menu options. Please review the suggested answers above"
            )

def date_choice():
    """
    Uses the provided preferred date of the client and checks if this is available. 
    """
    dates_times = SHEET.worksheet("available_dates_times")

    insert_date = input("Please provide the desired date (in format: YEAR/MM/DD): ")

    print("Checking if your chosen date is available...\n")

    match_date = dates_times.findall(insert_date, in_column=1)

    while match_date != "":

        print(f"The requested date is available.\n")
        #print(match_date)
        return match_date
        break
    
    print("The requested date is not availble, please choose again a date that falls in a week day.")
    date_choice()



def get_date_rows(choices):
    """
    strip cells of dates from context to then rebuild them with the context
    of the next columns cells (time). To ensure that dates and times are 
    available.
    """
    #print(choices)
    time_cells = []
    for cell in choices:
        #print(cell.row)
        if cell != "":
            #print("this date is available")
            time_cells.append(cell.row)
        else:
            print("this date is not available")
            break
    #print(time_cells)

    available_times = [f"B{time_cell}" for time_cell in time_cells]
    #print(available_times)

    return(available_times)


def time_choice(choice):
    choice = choice.strip().lower()
    """
    Converts the provided A / B or C into the actual time that can be
    matched with the worksheet.
    """
    if choice == "a":
        time = choice.replace("a", "09:00")
    elif choice == "b":
        time = choice.replace("b", "10:00")
    elif choice == "c":
        time = choice.replace("c", "11:00")
    else:
        print(
            f"Unfortunately your provided answer '{choice}' is not one of the menu options. Please review the suggested answers above"
            )

    return time

def time_availability(choice):
    """
    Converts the provided A / B or C into the actual time that can be
    matched with the worksheet.
    """
    dates_times = SHEET.worksheet("available_dates_times")

    available_time1 = SHEET.worksheet("available_dates_times").acell(choice[0]).value
    available_time2 = SHEET.worksheet("available_dates_times").acell(choice[1]).value
    available_time3 = SHEET.worksheet("available_dates_times").acell(choice[2]).value

    print(f"Please choose below from the following available time(s) on that date: {available_time1} {available_time2} {available_time3}\n")

    insert_time = input("A = 09:00 | B = 10:00 | C = 11:00 : ")

    time_choice(insert_time)
    print(f"You have chosen {time_choice} as your desired time.")

def book_appointment():
    """
    Ensure that a correct format of date is given and entered by the client.
    Format being YEAR/MM/DD. Followed by choosing a time slot, which will be
    chosen from a 1/2/3 menu. 
    """
    print("Booking your nail appointment is quick and includes a few easy steps.")
    print("Please first provide us with the date you'd like to book using the following format: (YEAR/MM/DD).")
    print("If that date is available, you can then choose one of the available time slots.")
    print("Please share your name and your contact number in case we need to reach you.")
    print("After this your booking is complete and you will receive your unique booking number.\n")

    dates_times = SHEET.worksheet("available_dates_times")
    
#    insert_date = input("Please provide the desired date (in format: YEAR/MM/DD): ")
#
#    print("Checking if your chosen date is available...\n")
#
    date_check = date_choice()
    #print(date_check)

    time_cells = get_date_rows(date_check)
    #print(time_cells)

    time_availability(time_cells)

    time_availability()




def edit_appointment():
    print("This would start the editing process")
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

def cancel_appointment():
    print("This would start the cancellation process")
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