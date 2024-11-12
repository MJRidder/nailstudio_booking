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

    client_menu_choice()

def client_menu_choice():
    """
    Validate the data provided by the user. Transfer values into integers
    so that they can be used to navigate through the booking system. Making
    sure the right numbers are generated, only one answer is given and no
    letters are used.
    """
    data_str = input("Please provide your choice here (A, B or C): ")
    choice = data_str.strip().lower()

    if choice ==  "a":
        print("Book your appointment\n")
        book_appointment()
    elif choice == "b":
        print("Edit your appointment\n")
        edit_appointment()
    elif choice == "c":
        print("Cancel your appointment\n")
        cancel_appointment()
    else:
        print(
            f"\nUnfortunately your provided answer '{choice}' is not one of the menu options. Please review the suggested options and try again.\n"
            )
        print("Please type in 'A' to make a new booking")
        print("Please type in 'B' to update an existing booking")
        print("Please type in 'C' to cancel an existing booking\n")
        client_menu_choice()

def date_choice(date):
    """
    Lets the client choose a date and checks if the date is available by checking
    the "string" to the 1st column of the available_dates_times google sheet. It then
    returns the cells of the day if it's available (every day has three matches, one 
    per time slot). If the day is not available it will notify the client and ask them 
    to try a different date. It also shows the client what format of date to use.
    """
    print("*** run date_choice")

    dates_times = SHEET.worksheet("available_dates_times")

    match_date = dates_times.findall(date, in_column=1)
    #print(match_date)

    if match_date:
        print(f"The requested date is available.\n")
        return match_date
    else: #the else statement still breaks, gives the correct error, starts over the date_choice function, but then no longer recognizes the output
        print("The requested date does not seem to be available, please try again and choose a date that falls on a weekday. Please alsoe use the suggested format: YYYY/MM/DD.\n")
        date_choice()


def get_date_cell(choices):
    """
    strip cells of dates from context to then rebuild them with the context
    of the next columns cells (time). To ensure that dates and times are 
    available.
    """
    print("*** run get_date_cell\n")
    #print(choices)
    time_cell = []
    for cell in choices:
        #print(cell.row)
        if cell != "":
            #print("this date is available")
            time_cell.append(cell.row)
        else:
            print("this date is not available")
            break
    #print(time_cell)

    available_times = [f"B{time_cell}" for time_cell in time_cell]
    #print(available_times)

    return(available_times)


def time_choice(choice):
    """
    Converts the provided A / B or C into the actual time that can be
    matched with the worksheet.
    """
    print("*** run time_choice\n")
    choice = choice.strip().lower()

    if choice == "a":
        time = choice.replace("a", "9:00")
    elif choice == "b":
        time = choice.replace("b", "10:00")
    elif choice == "c":
        time = choice.replace("c", "11:00")
    else:
        print(
            f"Unfortunately your provided answer '{choice}' is not one of the menu options. Please review the suggested answers above"
            )

    return time


def get_time_cell(choice):
    """
    Converts the provided A / B or C into the actual time that can be
    matched with the worksheet.
    """
    print("*** run get_time_cell\n")
    dates_times = SHEET.worksheet("available_dates_times")

    available_time_value1 = SHEET.worksheet("available_dates_times").acell(choice[0]).value
    available_time_value2 = SHEET.worksheet("available_dates_times").acell(choice[1]).value
    available_time_value3 = SHEET.worksheet("available_dates_times").acell(choice[2]).value

    available_time_cell1 = SHEET.worksheet("available_dates_times").acell(choice[0]).row
    available_time_cell2 = SHEET.worksheet("available_dates_times").acell(choice[1]).row
    available_time_cell3 = SHEET.worksheet("available_dates_times").acell(choice[2]).row

    #print(f"{available_time_cell1} {available_time_cell2} {available_time_cell3}\n")

    print(f"Please choose below from the following available time(s) on that date: {available_time_value1} {available_time_value2} {available_time_value3}\n")

    insert_time = input("A = 9:00 | B = 10:00 | C = 11:00 : ") #if/else statement still needs to be added here to ensure the right input is given
    
    if insert_time == available_time_value1:
        chosen_time_cell = f"B{available_time_cell1}"
        #print(chosen_time_cell)
        return chosen_time_cell
    elif insert_time == available_time_value2:
        chosen_time_cell = f"B{available_time_cell2}"
        #print(chosen_time_cell)
        return chosen_time_cell
    elif insert_time == available_time_value3:
        chosen_time_cell = f"B{available_time_cell3}"
        #print(chosen_time_cell)
        return chosen_time_cell
    else:
        print(f"Please make sure you have chosen a correct time from the available time(s): {available_time_value1} {available_time_value2} {available_time_value3}\n")
        get_time_cell(choice) #function does not yet work corectly, is calling the function again the right move?


def provide_contact_name():
    """
    function to ask the client to enter their first and last name, results in a string.
    """
    insert_name = input("Please provide your first and last name: ")
    return insert_name


def provide_contact_phone():
    """
    function to ask the client to enter their phone number, results in a string.
    """
    insert_phone = input("Please provide your phone number: ")
    return insert_phone


def generate_booking_id():
    last_id = SHEET.worksheet("confirmed_bookings").col_values.max((1))
    print(last_id)

def complete_booking(insert_date, booked_time, contact_name, contact_phone):
    """
    Receives a the date of the booking, the time, first & last name and the phone number, 
    all in strings. Inserts these in their own columns in the worksheet, tab: confirmed_bookings.
    """
    data = SHEET.worksheet("confirmed_bookings").get_all_values()
    print(data)

    print(f"Updating confirmed_bookings worksheet...\n")
    booking_data = [insert_date, booked_time, contact_name, contact_phone]
    worksheet_to_update = SHEET.worksheet("confirmed_bookings")
    worksheet_to_update.append_row(booking_data)
    print(f"{worksheet_to_update} worksheet updated successfully\n")

def book_appointment():
    """
    Ensure that a correct format of date is given and entered by the client.
    Format being YYYY/MM/DD. Followed by choosing a time slot, which will be
    chosen from a 1/2/3 menu. 
    """
    print("Booking your nail appointment is quick and includes a few easy steps.")
    print("Please first provide us with the date you'd like to book using the following format: (YYYY/MM/DD).")
    print("If that date is available, you can then choose one of the available time slots.")
    print("Please share your name and your contact number in case we need to reach you.")
    print("After this your booking is complete and you will receive your unique booking number.\n")

    dates_times = SHEET.worksheet("available_dates_times")
    
    insert_date = input("Please provide the desired date (in format: YYYY/MM/DD): ")
    print("Checking if your chosen date is available...\n")
    date_check = date_choice(insert_date)
    #print(date_check)

    time_cell = get_date_cell(date_check)
    #print(time_cell)

    booked_time = get_time_cell(time_cell)
    val = SHEET.worksheet("available_dates_times").acell(f"{booked_time}").value
    # The get_time_cell function provides a confirmmation of the chosen time.
    print(f"You have chosen {val} as your desired time.")

    contact_name = provide_contact_name()

    contact_phone = provide_contact_phone()

    Booking_ID = generate_booking_id()

    complete_booking(insert_date, booked_time, contact_name, contact_phone)

def edit_appointment():
    print("This would start the editing process")
    """
    Ensure that a correct format of date is given and entered by the client.
    Format being YYYY/MM/DD. Followed by choosing a time slot, which will be
    chosen from a 1/2/3 menu. 
    """
    print("Editing your nail appointment is quick and includes a few easy steps.")
    print("Please first provide us with the date you'd like to book using the following format: (YYYY/MM/DD).")
    print("If that date is available, you can then choose one of the available time slots.")
    print("Please share your name and your contact number in case we need to reach you.")
    print("After this your booking is complete and you will receive your unique booking number.")

def cancel_appointment():
    print("This would start the cancellation process")
    """
    Ensure that a correct format of date is given and entered by the client.
    Format being YYYY/MM/DD. Followed by choosing a time slot, which will be
    chosen from a 1/2/3 menu. 
    """
    print("Cancelling your nail appointment is quick and includes a few easy steps.")
    print("Please first provide us with the date you'd like to book using the following format: (YYYY/MM/DD).")
    print("If that date is available, you can then choose one of the available time slots.")
    print("Please share your name and your contact number in case we need to reach you.")
    print("After this your booking is complete and you will receive your unique booking number.")

main_menu()