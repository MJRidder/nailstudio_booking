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
        clear_screen()
        book_appointment()
    elif choice == "b":
        print("Edit your appointment\n")
        clear_screen()
        edit_appointment()
    elif choice == "c":
        print("Cancel your appointment\n")
        clear_screen()
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
    #print("*** run date_choice\n")

    dates_times = SHEET.worksheet("available_dates_times")

    match_date = dates_times.findall(date, in_column=1)
    #print(match_date)

    if match_date:
        print(f"The requested date is available.\n")
        return match_date
    else:
        clear_screen()
        print("The requested date does not seem to be available or perhaps we did not understand the date as it was typed.")
        print("Please try again and choose a date that falls on a weekday. Please use the suggested format: YYYY/MM/DD.\n\n")
        book_appointment()


def get_date_cell(choices):
    """
    strip cells of dates from context to then rebuild them with the context
    of the next columns cells (time). To ensure that dates and times are 
    available.
    """
    #print("*** run get_date_cell\n")
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


#def time_choice(choice):
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
    Takes the cell values provided in choices (the available booking times) and translates these
    to available times for a client to book. Times are only shown if they are available in the 
    dates_times worksheet. Otherwise it will be populated by a <space>, which will still hold a
    string value, but will not show as an actual time for the client.
    """
    #print("*** run get_time_cell\n")
    #print("Checking for available times...\n")
    #print(type(choice))
    #print(choice)

    available_time_value1 = ""
    available_time_value2 = ""
    available_time_value3 = ""

    dates_times = SHEET.worksheet("available_dates_times")

    try:
        available_time_value1 = SHEET.worksheet("available_dates_times").acell(choice[0]).value
        available_time_cell1 = SHEET.worksheet("available_dates_times").acell(choice[0]).row
    except Exception as e:
        print(str(e), "")

    try:
        available_time_value2 = SHEET.worksheet("available_dates_times").acell(choice[1]).value
        available_time_cell2 = SHEET.worksheet("available_dates_times").acell(choice[1]).row
    except Exception as e:
        print(str(e), "")

    try:
        available_time_value3 = SHEET.worksheet("available_dates_times").acell(choice[2]).value
        available_time_cell3 = SHEET.worksheet("available_dates_times").acell(choice[2]).row
    except Exception as e:
        print(str(e), "")

    #print(f"{available_time_cell1} {available_time_cell2} {available_time_cell3}\n")

    print("On your date we have availability at the following time(s): ")
    try:
        if available_time_value1 != "":
            print(f"{available_time_value1}")
        if available_time_value2 != "":
            print(f"{available_time_value2}")
        if available_time_value3 != "":
            print(f"{available_time_value3}")
    except Exception as e:
        print(str(e), "")

    insert_time = input("Please type in the desired time (exactly as the time is presented above): ") #if/else statement not working for the "else piece" yet.
    
    if insert_time == available_time_value1:
        chosen_time_cell = f"B{available_time_cell1}"
        #print(chosen_time_cell)
        clear_screen()
        return chosen_time_cell
    elif insert_time == available_time_value2:
        chosen_time_cell = f"B{available_time_cell2}"
        #print(chosen_time_cell)
        clear_screen()
        return chosen_time_cell
    elif insert_time == available_time_value3:
        chosen_time_cell = f"B{available_time_cell3}"
        #print(chosen_time_cell)
        clear_screen()
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
    """
    Generates a new booking ID, looking at the highest current booking ID
    number in the confirmed_bookings sheet (column A). Taking this value
    and giving it a +1.
    """
    list_id = SHEET.worksheet("confirmed_bookings").col_values(1)[1:]
    print(list_id)

    max_value = None
    for n in list_id:
        if max_value is None or int(n) > max_value: max_value = int(n)
    print(max_value)

    new_booking_id = int(max_value) + 1
    print(new_booking_id)

    return new_booking_id


#def find_booking():
    """
    funtion to find the booking, based on booking ID.
    """

    booking_id = ['7']
    print(type(booking_id))
    dates_times = SHEET.worksheet("confirmed_bookings")

    if existing_booking:
        existing_booking = dates_times.findall(str(booking_id[0]), in_column=1)
        print(existing_booking, f"An existing booking with the booking ID {booking_id} has been found, fetching data...")

        booking_row = existing_booking.row

        date_booking = SHEET.worksheet("confirmed_bookings").acell(choice[1]).value
        time_booking = SHEET.worksheet("confirmed_bookings").acell(choice[1]).value
        name_booking = SHEET.worksheet("confirmed_bookings").acell(choice[1]).value

        return existing_booking
    else: 
        print(f"No existing booking with the booking ID {booking_id} has been found. please review")


def remove_booked_availability(booking_id, time_cell, booked_time):
    """
    Updates the worksheet by removing/adding dates after a booking is made, edited or cancelled.
    """
    date_cell = time_cell.replace("B", "A")

    remove_time = SHEET.worksheet("available_dates_times").update_acell(time_cell, "  ")
    #print("removed time")
    remove_date = SHEET.worksheet("available_dates_times").update_acell(date_cell, "  ")
    #print("removed date")


def reinstate_booking():
    """
    Find a booking based off the booking_id. confirm what of the original booking needs to be
    edited. Confirm availability to edit. Make new booking with a new booking ID and booking 
    data. Reinstate the original booking.
    """
    dates_times = SHEET.worksheet("confirmed_bookings")

    find_booking_id = dates_times.findall(str(booking_id[0]), in_column=1)
    #print(remove_booking_cells)

    booking_row = find_booking_id[0].row
    #print(f"Booking row to be updated: {booking_row}")

    confirmation_cell = "F" + str(booking_row)
    #print(confirmation_cell)

    cancel_booking = SHEET.worksheet("confirmed_bookings").update_acell(confirmation_cell, "cancelled")

    return remove_time, remove_date, cancel_booking


def confirm_booking(booking_id, insert_date, booked_time, contact_name, contact_phone):
    """
    Receives a the date of the booking, the time, first & last name and the phone number, 
    all in strings. Inserts these in their own columns in the worksheet, tab: confirmed_bookings.
    """
    print("confirming booking...")
    data = SHEET.worksheet("confirmed_bookings").get_all_values()

    print(f"Updating confirmed_bookings worksheet...\n")
    booking_data = [booking_id, insert_date, booked_time, contact_name, contact_phone, "YES"]
    worksheet_to_update = SHEET.worksheet("confirmed_bookings")
    worksheet_to_update.append_row(booking_data)
    print(f"Booking updated successfully\n")


def back_to_menu():
        back_to_menu = input("Would you like to go back to the main menu? y/n: ")
        choice = back_to_menu.strip().lower()

        if choice == "y":
            print("Bringing you back to the main menu.")
            clear_screen()
            main_menu()
        else:
            clear_screen()
            print("Thank you for your time. Have a great day.")


def book_appointment():
    """
    Ensure that a correct format of date is given and entered by the client.
    Format being YYYY/MM/DD. Followed by choosing a time slot, which will be
    chosen from a 1/2/3 menu. 
    """
    print("Booking your nail appointment is quick and includes a few easy steps.")
    print("Please first provide us with the date you'd like to book using the following format: (YYYY/MM/DD).")
    print("If that date is available, you can then choose one of the available time slots.")
    print("Please share your name and your contact number in case we need to reach you.\n")
    print("After this your booking is complete and you will receive your unique booking number.\n")

    dates_times = SHEET.worksheet("available_dates_times")
    
    insert_date = input("Please provide the desired date (in format: YYYY/MM/DD): ")
    print("Checking if your chosen date is available...\n")
    date_check = date_choice(insert_date)
    #print(date_check)

    time_cell_check = get_date_cell(date_check)
    #print(time_cell_check)

    time_cell = get_time_cell(time_cell_check)
    booked_time = SHEET.worksheet("available_dates_times").acell(f"{time_cell}").value
    # The get_time_cell function provides a confirmmation of the chosen time.
    print(f"You have chosen {booked_time} as your desired time on the date {insert_date}.\n\n")

    contact_name = provide_contact_name()
    print("Contact name provided\n")

    contact_phone = provide_contact_phone()
    print("Phone number name provided\n")

    booking_id = generate_booking_id()
    print("Unique booking ID created\n")

    confirm_booking(booking_id, insert_date, booked_time, contact_name, contact_phone)

    remove_booked_availability(booking_id, time_cell, booked_time)
    
    clear_screen()
    print("Thank you for your booking! We appreciate your business. To confirm:\n")

    print(f"*  Your unique booking ID: {booking_id}")
    print(f"*  The date of your booking: {insert_date}")
    print(f"*  Your booking will be at: {booked_time}")
    print(f"*  And your booking is for: {contact_name}\n")
    print(f"*  We will send you a message on the following number to confirm: {contact_phone}\n")

    print("If you have any further queries please let us know. You can do this via:")
    print("*  email: nailstudio@thebest.com")
    print("*  phone: +353 81 234 5678\n")

    print("We are here to help!\n")

    back_to_menu()


def edit_appointment():
    print("This would start the editing process")
    """
    This function will initialize the editing of an existing booking. It will call functions
    that will check the booking ID with the bookings made in the worksheet. It will then remove
    the booking if edits have been made and provide a new booking confirmation and booking ID.
    """
    print("Editing your nail appointment is quick and includes a few easy steps.\n")

    insert_booking_id = input("What was the booking ID for your booking?: ")
    find_booking(insert_booking_id)


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