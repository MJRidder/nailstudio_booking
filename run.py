import gspread
from google.oauth2.service_account import Credentials
# import re

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
    Clears the screen from users inputs.
    """
    print("\033c", end="")


def main_menu():
    """
    Gives the user the initial options to make a booking, edit
    an existing booking or cancel.
    """

    print("$ *** Here comes the Nail studio logo ***\n")
    print("$ Welcome to Lou's nail studio!")
    print("$ Below you can find the menu options.")
    print("$ I am opening my doors from 2025 January 6th onwards.")
    print("$ Monday to Friday, mornings appointments only.\n")

    print("$ What would you like to do?")
    print("$ *  Type in 'A' to make a new appointment")
    print("$ *  Type in 'B' to update an existing appointment")
    print("$ *  Type in 'C' to cancel an existing appointment\n")
    print("$ *  Or type 'E' to exit this program\n")

    client_menu_choice()


def client_menu_choice():
    """
    Validate the data provided by the user. Transfer values into integers
    so that they can be used to navigate through the booking system. Making
    sure the right numbers are generated, only one answer is given and no
    letters are used.
    """
    data_str = input("Please provide your choice here (A, B, C or E): ")
    choice = data_str.strip().lower()

    if choice == "a":
        print("$ *** Book your next appointment ***\n")
        # clear_screen()
        book_appointment()
    elif choice == "b":
        print("$ *** Edit an existing appointment ***\n")
        # clear_screen()
        edit_appointment()
    elif choice == "c":
        print("$ *** Cancel an existing appointment ***\n")
        # clear_screen()
        cancel_appointment()
    elif choice == "e":
        print("$ Exiting program\n")
        # clear_screen()
        print("$ Thank you for visiting Lou's nail studio. Have a great day!")
        quit()
    else:
        print(
            f"\n$ Sorry, your answer '{choice}' is not one of the menu options.")
        print("$ *  Please review the suggested options and try again.\n")
        print("$ *  Please type in 'A' to make a new booking")
        print("$ *  Please type in 'B' to update an existing booking")
        print("$ *  Please type in 'C' to cancel an existing booking")
        print("$ *  Or type 'E' to exit this program.\n")
        client_menu_choice()


def date_choice():
    """
    Lets the client choose a date and checks if the date is available
    by checking the "string" to the 1st column of the
    available_dates_times google sheet. It then returns the cells of
    the day if it's available (every day has three matches, one  per
    time slot). If the day is not available it will notify the client
    and ask them  to try a different date. It also shows the client
    what format of date to use.
    """
    dates_times = SHEET.worksheet("available_dates_times")

    insert_date = input(
        "$ Please provide the desired date (in format: YYYY/MM/DD): ")
    print("\n$ Checking your chosen date...\n")

    match_date = dates_times.findall(insert_date, in_column=1)

    if match_date:
        print(f"$ The requested date is available.\n")
        return match_date, insert_date
    else:
        # clear_screen()
        print("$ The requested date does not seem to be available.")
        print("$ Did you book a weekday?")
        print("$ Did you use the correct format?: YYYY/MM/DD)?")
        print("$ Please follow the instructions and try again.\n")
        book_appointment()


def get_date_cell(choices):
    """
    strip cells of dates from context to then rebuild them with
    the context of the next columns cells (time). To ensure 
    that dates and times are available.
    """

    print("$ One moment, let's see what times are available...\n")
    # print(choices)
    # print(type(choices))
    time_cell = []
    for cell in choices:
        # print(cell.row)
        if cell != "":
            # print("this date is available")
            time_cell.append(cell.row)
        else:
            print("$ this date is not available")
            break
    # print(time_cell)

    available_times = [f"B{time_cell}" for time_cell in time_cell]
    # print(available_times)

    return(available_times)


# def time_choice(choice):
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
    # print("*** run get_time_cell\n")
    # print("Checking for available times...\n")
    # print(type(choice))
    # print(choice)

    available_time_value1 = ""
    available_time_value2 = ""
    available_time_value3 = ""

    dates_times = SHEET.worksheet("available_dates_times")

    try:
        available_time_value1 = SHEET.worksheet("available_dates_times").acell(choice[0]).value
        available_time_cell1 = SHEET.worksheet("available_dates_times").acell(choice[0]).row
    except Exception as e:
        print(str(e), " ")

    try:
        available_time_value2 = SHEET.worksheet("available_dates_times").acell(choice[1]).value
        available_time_cell2 = SHEET.worksheet("available_dates_times").acell(choice[1]).row
    except Exception as e:
        print(str(e), " ")

    try:
        available_time_value3 = SHEET.worksheet("available_dates_times").acell(choice[2]).value
        available_time_cell3 = SHEET.worksheet("available_dates_times").acell(choice[2]).row
    except Exception as e:
        print(str(e), " ")

    print("$ On your date we have availability at the following time(s): ")
    try:
        if available_time_value1 != "":
            print(f"\n{available_time_value1}")
        if available_time_value2 != "":
            print(f"{available_time_value2}")
        if available_time_value3 != "":
            print(f"{available_time_value3}")
    except Exception as e:
        print(str(e), "")

    print(
        "\n$ If your desired time is not available, type in 'r' to check for a different date.")

    while True:
        insert_time = input(
            "$ Please type in the desired time (exactly as the time is presented above): ")
        
        if insert_time == available_time_value1:
            chosen_time_cell = f"B{available_time_cell1}"
            # print(chosen_time_cell)
            # clear_screen()
            return chosen_time_cell
        elif insert_time == available_time_value2:
            chosen_time_cell = f"B{available_time_cell2}"
            # print(chosen_time_cell)
            # clear_screen()
            return chosen_time_cell
        elif insert_time == available_time_value3:
            chosen_time_cell = f"B{available_time_cell3}"
            # print(chosen_time_cell)
            # clear_screen()
            return chosen_time_cell
        elif insert_time == "r":
            print("$ OK, let's check for a different date")
            date_choice()
        
        else:
            print(
                "\n$ Please make sure you have chosen a correct time from the available time(s):")
            print(
                f"$ Available times: {available_time_value1} {available_time_value2} {available_time_value3}\n")
            print(
                "$ Is your desired time not available? type in 'r' to check for a different date.\n")


def provide_contact_name():
    """
    function to ask the client to enter their first and last name, results in a string.
    """
    insert_name = input("$ Please confirm your first and last name: ")
    return insert_name


def provide_contact_phone():
    """
    function to ask the client to enter their phone number, results in a string.
    """
    insert_phone = input("$ Please confirm your phone number: ")
    return insert_phone


def generate_booking_id():
    """
    Generates a new booking ID, looking at the highest current
    booking ID number in the confirmed_bookings sheet (column A).
    Taking this value and giving it a +1.
    """
    list_id = SHEET.worksheet("confirmed_bookings").col_values(1)[1:]
    # print(list_id)

    max_value = None
    for n in list_id:
        if max_value is None or int(n) > max_value: max_value = int(n)
    # print(max_value)

    new_booking_id = int(max_value) + 1
    # print(new_booking_id)

    return new_booking_id


def find_booking():
    """
    Ask user for the booking ID, check if it is indeed in
    the system and return the cell that the booking ID is
    in. Combined with the row number of that booking ID
    (so that the other information of the booking can be
    captured).
    """
    existing_booking = []

    print(
        "$ Your unique booking ID was provided at the time of your booking.")
    insert_booking_id = input(
        "$ What was the booking ID for your booking?: ")
    
    print("\n$ Please wait a moment while we fetch your booking...\n")
    # print(f"insert booking ID: {insert_booking_id}")
    # print(type(insert_booking_id))


    confirmed_bookings = SHEET.worksheet("confirmed_bookings")

    existing_booking = confirmed_bookings.findall(str(insert_booking_id), in_column=1)
    # print(f"existing booking ID: {existing_booking}")
    # print(type(existing_booking))

    if insert_booking_id == "r":
        # clear_screen()
        print("$ OK, you chose to cancel. Bringing you back to the main menu.")
        print("$ Let us bring you back to the main menu.")
        main_menu()
    else:
        if existing_booking != []:
            existing_booking = confirmed_bookings.findall(str(insert_booking_id), in_column=1)
            existing_booking_value = existing_booking[0].value
            # print(f"existing booking value: {existing_booking_value}")
            # print(type(existing_booking_value))
            existing_booking_row = existing_booking[0].row
            # print(f"existing booking row: {existing_booking_row}")
            # print(type(existing_booking_row))
            existing_booking.append(existing_booking_value)
            existing_booking.append(existing_booking_row)
            booking_return = existing_booking
            # print(f"booking return: {booking_return}")
            # print(type(booking_return))
            
            print("$ Great! we have been able to find your booking.")
            print("$ Retrieving the booking details now...\n")
            return booking_return
        else:
            # clear_screen()
            print(
                "$ We have not been able to match your booking number.")
            print(
                "$ Your unique booking ID was provided at the time of your booking.")
            print(
                "$ Your booking ID consists of numbers only.\n")
            while True:
                try_again = input("$ Would you like to try again? (y/n): ")
                try_again = try_again.strip().lower()
                if try_again == "y":
                    # clear_screen()
                    print("$ Great! let's try again.\n")
                    edit_appointment()
                elif try_again == "n":
                    # clear_screen()
                    print("\n$ Okido, let's bring you back to the main menu\n")
                    main_menu()
                else:
                    # clear_screen()
                    print(
                        "$ Apologies, it is not clear to us what you are trying to do.")
                    print(
                        "$ Please pay close attention to the instructions that are provided.")
                    print(
                        "$ For now, let us bring you back to the main menu.")
                    print(
                        "$ From here you can try again, exit the program.")
                    print(
                        "$ Apologies for any inconvenience.")
                    main_menu()
    

def booking_confirmation(booking_details):
    """
    Use booking details and confirm if the booking
    is indeed the correct booking that the user is 
    looking for. this function will run when an existing
    booking has been found.
    """
    confirmed_bookings = SHEET.worksheet("confirmed_bookings")

    # print("booking details print", booking_details)
    booking_row = booking_details[2]
    # print(booking_row)
    # print(type(booking_row))

    cell_booking_id = [f"A{booking_row}"]
    cell_booking_date = [f"B{booking_row}"]
    cell_booking_time = [f"C{booking_row}"]
    cell_booking_name = [f"D{booking_row}"]
    cell_booking_timestamp = [f"F{booking_row}"]
    cell_booking_confirmation = [f"G{booking_row}"]
    listing_booking_id = booking_details[0]

    value_booking_id = SHEET.worksheet(
        "confirmed_bookings").acell(cell_booking_id[0]).value
    value_booking_date = SHEET.worksheet(
        "confirmed_bookings").acell(cell_booking_date[0]).value
    value_booking_time = SHEET.worksheet(
        "confirmed_bookings").acell(cell_booking_time[0]).value
    value_booking_name = SHEET.worksheet(
        "confirmed_bookings").acell(cell_booking_name[0]).value
    value_booking_timestamp = SHEET.worksheet(
        "confirmed_bookings").acell(cell_booking_timestamp[0]).value
    value_booking_confirmation = SHEET.worksheet(
        "confirmed_bookings").acell(cell_booking_confirmation[0]).value

    booking_details = value_booking_id, value_booking_date, value_booking_time, value_booking_name, value_booking_timestamp, value_booking_confirmation, listing_booking_id
    # print("This is the booking details print", booking_details)

    if value_booking_confirmation == "cancelled":
        print(
            "$ We have found an old booking, but this was cancelled.")
        print(
            f"$ *   The provided booking ID was: {value_booking_id}.")
        print(
            f"$ *   The booking was made for {value_booking_time} on {value_booking_date}.")
        print(
            f"$ *   The booking was made by {value_booking_name}.\n")

        print(
            "$ would you like to try a different booking number? (y/n)")
        cancelled_booking = input(
            "$ or press 'r' to go back to the main menu: ")
        cancelled_booking = cancelled_booking.strip().lower()

        if cancelled_booking == "y":
            # clear_screen()
            print(f"$ OK, the booking with Booking ID {value_booking_id},")
            print("$ was cancelled, let's try another one.")
            find_booking()
        elif cancelled_booking == "n":
            # clear_screen()
            print("$ OK, let us bring you back to the main menu.")
            main_menu()
        elif cancelled_booking == "r":
            # clear_screen()
            print("$ OK, let us bring you back to the main menu.")
            main_menu()
        else:
            print("$ Sorry, we did not get that.")
            print("$ Please ensure that you use the suggested y or n format.")
            print("$ You are being sent back to the main menu.\n")
            main_menu()
    else:
        print("$ Please find below your booking details:")
        print(f"$ *   The provided booking ID was: {value_booking_id}.")
        print(f"$ *   The booking was made for {value_booking_time} on {value_booking_date}.")
        print(f"$ *   The booking was made by {value_booking_name}.\n")

        while True:
            client_confirmation = input("$ Is this the correct booking that you wanted to edit or cancel? (y/n): ")
            client_confirmation = client_confirmation.strip().lower()

            if client_confirmation == "y":
                # print("\nGreat!, let's fetch your booking for you now.\n")
                booking_details = value_booking_id, value_booking_date, value_booking_time, value_booking_name, value_booking_timestamp, value_booking_confirmation, listing_booking_id 
                # print("This is the booking details print in the if/else function", booking_details)
                return booking_details

            elif client_confirmation == "n":
                while True:
                    diff_book_id = input(
                    f"\n$ Would you like to try to find a different booking with a different booking number then {value_booking_id} (y/n): " #noqa
                    )
                    if diff_book_id == "y":
                        print("\n$ Okido, let's bring you back to the edit booking screen\n")
                        edit_appointment()
                    elif diff_book_id == "n":
                        # clear_screen()
                        print("$ OK, let us bring you back to the main menu.")
                        main_menu()
                    elif diff_book_id == "r":
                        # clear_screen()
                        print("$ OK, let us bring you back to the main menu.")
                        main_menu()
                    else:
                        print("\n$ Sorry, we did not get that.")
                        print("Please ensure that you use the suggested y or n format.")
                        print("\n$ Or press r to return to the main menu.\n")

            elif client_confirmation == "r":
                # clear_screen()
                print("$ OK, let us bring you back to the main menu.")
                main_menu()
            else:
                print("\n$ Sorry, we did not get that.")
                print("$ Please ensure that you use the suggested y or n format.")
                print("\n$ Or press r to return to the main menu.\n")


def remove_booked_availability(booking_details):
    """
    Updates the worksheet by removing/adding dates
    after a booking is made, edited or cancelled.
    """
    # print(booking_details)
    # print(type(booking_details))

    time_cell = booking_details[5]
    date_cell = booking_details[5].replace("B", "A")

    remove_time = SHEET.worksheet(
        "available_dates_times").update_acell(time_cell, "  ")
    # print("removed time")
    remove_date = SHEET.worksheet(
        "available_dates_times").update_acell(date_cell, "  ")
    # print("removed date")


def update_booking(correct_booking):
    """
    determine what the client would like to update of their existing booking. 
    """

    value_booking_id = correct_booking[0]
    value_booking_date = correct_booking[1]
    value_booking_time = correct_booking[2]
    value_booking_name = correct_booking[3]

    # clear_screen()
    print("\n$ To update your booking, please answer the following questions:\n")

    print("$ *   Type Y to confirm")
    print("$ *   Type N to decline")
    print("$ *   Type C to cancel your booking")
    print("$ *   Type R to stop editing and go return to the main menu\n")

    print(f"$ Your current appointment is on {value_booking_date},")
    print("$ would you like to change this?\n")
    change_date = input("$ change date? (y/n) or press c to cancel: ")
    change_date = change_date.strip().lower()
    if change_date == "y":
        print("\n$ OK, let's see if your desired date is available.")
        date_check = date_choice()
        time_cell_check = get_date_cell(date_check[0])
        # print("this is the value of time_cell_check in the update_booking function", time_cell_check)

        time_cell = get_time_cell(time_cell_check)
        # print("this is the value of time_cell - in the update booking function", time_cell)
        # print(type(time_cell))
        desired_date = date_check[1]
        # print("this is the value of desired date - in the update booking function", desired_date)
        # print(type(desired_date))

        booked_time = SHEET.worksheet("available_dates_times").acell(f"{time_cell}").value
        #The get_time_cell function provides a confirmmation of the chosen time.
        print(
            f"$ You have chosen {booked_time} as your desired time")
        print(f"$ on the date {desired_date}.\n")

        contact_name = provide_contact_name()
        print("Contact name provided\n")

        contact_phone = provide_contact_phone()
        print("Phone number name provided\n")

        booking_id = generate_booking_id()
        print("Unique booking ID created\n")

        print("confirm booking details...\n")
        booking_details = add_worksheet_confirmed(booking_id, desired_date, booked_time, contact_name, contact_phone, time_cell)

        print("Take out the dates and times...\n")
        remove_booked_availability(booking_details)
            
        print("cancel existing booking...\n")
        cancel_booking(correct_booking)

        print("reinstate old date and time...\n")
        reinstate_booking_slot(correct_booking)

        print("confirming new booking to the user...")
        confirm_to_user(correct_booking)

        back_to_menu()

    elif change_date == "n":
        print(f"\n$ Your booking on {value_booking_date} is at {value_booking_time},")
        print("$ would you like to change the time?\n")
        change_time = input("$ change? (y/n): ")
        change_time = change_time.strip().lower()
        
        if change_time == "y":
            dates_times = SHEET.worksheet("available_dates_times")
            check_time = dates_times.findall(str(correct_booking[1]), in_column=1)
            # print("check times print", check_time)
            print(
                "$ OK, let's see if there are other times available on your desired date.\n")
            time_cell_check = get_date_cell(check_time)
            # print("this is the time cell check value of when user wants to change time\n", )
            time_cell = get_time_cell(time_cell_check)
            # print("this is the time cell value of when user wants to change time\n", time_cell)

            desired_date = value_booking_date
            print("$ this is the value of desired date", desired_date)
            # print(type(desired_date))

            booked_time = SHEET.worksheet("available_dates_times").acell(f"{time_cell}").value
            # The get_time_cell function provides a confirmmation of the chosen time.
            print(
            f"$ You have chosen {booked_time} as your desired time")
            print(f"$ on the date {desired_date}.\n")

            contact_name = provide_contact_name()
            print("Contact name provided\n")

            contact_phone = provide_contact_phone()
            print("Phone number name provided\n")

            booking_id = generate_booking_id()
            print("Unique booking ID created\n")

            print("confirm booking details...")
            booking_details = add_worksheet_confirmed(booking_id, desired_date, booked_time, contact_name, contact_phone, time_cell)

            print("Take out the dates and times...")
            remove_booked_availability(booking_details)
                
            print("cancel existing booking...")
            cancel_booking(correct_booking)

            print("reinstate old date and time...")
            reinstate_booking_slot(correct_booking)

            print("confirming new booking to the user...")
            confirm_to_user(correct_booking)

            back_to_menu()

        elif change_time == "n":
            print(
                f"$ our booking on {value_booking_date} at {value_booking_time} was booked for")
            print(
                f"{contact_name}, with the phone number {contact_phone}.")
            change_contact = input(
                "$ Would you like to update these contact details? (y/n): ")
            change_contact = change_contact.strip().lower()

            if change_contact == "y":
                print(
                    "$ Great, please enter the contact name and phone number that you would like to use:")
                contact_name = provide_contact_name()
                contact_phone = provide_contact_phone()
                add_worksheet_confirmed(value_booking_id, value_booking_date, value_booking_time, contact_name, contact_phone, time_cell)

                confirm_to_user(booking_details)

                back_to_menu()
            elif change_contact == "n":
                # clear_screen()
                print("$ OK, as it seems that you do not want to change the details of your booking,")
                print("$ we will bring you back to the main menu.\n")
                main_menu()  
            else:
                print("$ Sorry, we did not understand what you meant")
                try_again = input("$ Would you like to try again? (y/n): ")
                if try_again == "y":
                    print("$ Great! let's try again.\n")
                    update_booking(correct_booking)
                elif try_again == "n":
                    print("\nOkido, let's bring you back to the main menu\n")
                    main_menu()
                else:
                    # clear_screen()
                    print("$ Apologies, it is not clear to us what you are trying to do.")
                    print("$ Please pay close attention to the instructions that are provided.")
                    print("$ For now, let us bring you back to the main menu.")
                    print("$ From here you can try again, or exit the program.")
                    print("$ Apologies for any inconvenience.")
                    main_menu()
        else:
            # clear_screen()
            print("$ Apologies, it is not clear to us what you are trying to do.")
            print("$ Please pay close attention to the instructions that are provided.")
            print("$ For now, let us bring you back to the main menu.")
            print("$ From here you can try again, or exit the program.")
            print("$ Apologies for any inconvenience.")
            main_menu()

    elif change_date == "c":
        # clear_screen()
        print("\n$ Are you sure you want to cancel the following booking?")
        print(f"$ Current booking is nn {value_booking_date} at {value_booking_time}.\n")

        confirm_cancellation = input("$ Answer (y/n): ")
        confirm_cancellation = confirm_cancellation.strip().lower()

        if confirm_cancellation == "y":

            print(
                f"\n$ cancelling booking of {value_booking_date} at {value_booking_time}...\n")
            cancel_booking(correct_booking)
            reinstate_booking_slot(correct_booking)

            print(
                f"\nYour booking of {correct_booking[2]}, on the {correct_booking[1]}, has now been cancelled.\n")

            print("$ If you have any further queries please let us know. You can do this via:")
            print("$ *  email: nailstudio@thebest.com")
            print("$ *  phone: +353 81 234 5678\n")

            print("$ We are here to help!\n")
            back_to_menu()

    elif change_date == "r":
        # clear_screen()
        print(
            "$ Editing your booking has been cancelled. Bringing you back to the main menu.")
        main_menu()
    else:
        print("$ Sorry, we did not understand what you meant")
        try_again = input("$ Would you like to try again? (y/n): ")
        if try_again == "y":
            print("$ Great! let's try again.\n")
            update_booking(correct_booking)
        elif try_again == "n":
            # clear_screen()
            print("\n$ Okido, let's bring you back to the main menu\n")
            main_menu()
        else:
            # clear_screen()
            print("$ Apologies, it is not clear to us what you are trying to do.")
            print("$ Please pay close attention to the instructions that are provided.")
            print("$ For now, let us bring you back to the main menu.")
            print("$ From here you can try again, or exit the program.")
            print("$ Apologies for any inconvenience.")
            main_menu()


def cancel_booking(correct_booking):
    """
    Find a booking based off the booking_id. confirm what 
    of the original booking needs to be edited. Confirm 
    availability to edit. Make new booking with a new 
    booking ID and booking data. Reinstate the original booking.
    """
    confirmed_bookings = SHEET.worksheet("confirmed_bookings")
    # print("correct_booking details (tuple)", correct_booking)
    # print(type(correct_booking))

    print("$ finding your old appointment...")

    find_old_id = confirmed_bookings.findall(str(correct_booking[0]), in_column=1)
    # print("find_old_id", find_old_id)
    # print(type(find_old_id))

    booking_row = find_old_id[0].row
    print(f"Booking row to be updated: {booking_row}")

    confirmation_cell = "G" + str(booking_row)
    print(confirmation_cell)

    print("Cancelling your old appointment")
    cancel_booking = SHEET.worksheet("confirmed_bookings").update_acell(confirmation_cell, "cancelled")

    print("old appointment cancelled\n")
    

    return correct_booking


def reinstate_booking_slot(correct_booking):
    """
    Receiving the timestamp of an old booking (which relates to the timeslot in the Google sheet). Using this
    value to reinstate date and time for future bookings.
    """
    dates_times = SHEET.worksheet("available_dates_times")

    print("correct booking details in reinstate function", correct_booking)

    print("reinstating old times...\n")

    date_truth_cell = correct_booking[4].replace("B","D")
    time_truth_cell = correct_booking[4].replace("B","E")

    reinstated_date = correct_booking[4].replace("B","A")

    print("date_truth_cell value", date_truth_cell)
    print("time_truth_cell value", time_truth_cell)

    date_truth_check = SHEET.worksheet("available_dates_times").acell(date_truth_cell).value
    time_truth_check = SHEET.worksheet("available_dates_times").acell(time_truth_cell).value

    reinstated_date_cell = SHEET.worksheet("available_dates_times").update_acell(str(date_truth_cell), date_truth_check)

    print("date_truth_check value", date_truth_check)
    print("time_truth_check value" , time_truth_check)

    reinstate_date = SHEET.worksheet("available_dates_times").update_acell(str(reinstated_date), date_truth_check)
    reinstate_time = SHEET.worksheet("available_dates_times").update_acell(str(correct_booking[4]), time_truth_check)
    print("* date reinstated", date_truth_check)
    print("* time reinstated", time_truth_check)
    return


def add_worksheet_confirmed(booking_id, desired_date, booked_time, contact_name, contact_phone, time_cell):
    """
    Receives the date of the booking, the time, first & last name and the phone number, 
    all in strings. Inserts these in their own columns in the worksheet, tab: confirmed_bookings.
    """
    print("confirming booking...")
    data = SHEET.worksheet("confirmed_bookings").get_all_values()

    print(f"Updating confirmed_bookings worksheet...\n")
    booking_data = [booking_id, desired_date, booked_time, contact_name, contact_phone, time_cell, "YES"]

    worksheet_to_update = SHEET.worksheet("confirmed_bookings")    
    worksheet_to_update.append_row(booking_data)
    print(f"Booking updated successfully\n")

    return booking_id, desired_date, booked_time, contact_name, contact_phone, time_cell


def back_to_menu():
    """
    Function to bring back the user back to the main menu.
    """
    back_to_menu = input("Would you like to go back to the main menu? y/n: ")
    choice = back_to_menu.strip().lower()

    if choice == "y":
        print("Bringing you back to the main menu.")
        #clear_screen()
        main_menu()
    elif choice == "n":
        print("Thank you for your time. Have a great day.")
        quit()
    else:
        print("Sorry, we did not quite catch that, could you please try again? Please say either y or n.")
        back_to_menu()


def confirm_to_user(booking_details):
    #clear_screen()
    print("Thank you for your booking! We appreciate your business. To confirm:\n")

    print(f"*  Your unique booking ID: {booking_details[0]}")
    print(f"*  The date of your booking: {booking_details[1]}")
    print(f"*  Your booking will be at: {booking_details[2]}")
    print(f"*  And your booking is for: {booking_details[3]}\n")
    print(f"*  We will send you a message on the following number to confirm: {booking_details[4]}\n")

    print("If you have any further queries please let us know. You can do this via:")
    print("*  email: nailstudio@thebest.com")
    print("*  phone: +353 81 234 5678\n")

    print("We are here to help!\n")

    return
    

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
    date_check = date_choice()
    #print("this is the value of date_check", date_check)

    time_cell_check = get_date_cell(date_check[0])
    #print("this is the value of time_cell_check", time_cell_check)

    time_cell = get_time_cell(time_cell_check)
    #print("this is the value of time_cell", time_cell)
    #print(type(time_cell))
    desired_date = date_check[1]
    #print("this is the value of desired date", desired_date)
    #print(type(desired_date))

    booked_time = SHEET.worksheet("available_dates_times").acell(f"{time_cell}").value

    #The get_time_cell function provides a confirmmation of the chosen time.
    print(f"You have chosen {booked_time} as your desired time on the date {desired_date}.\n\n")

    contact_name = provide_contact_name()
    print("Contact name provided\n")

    contact_phone = provide_contact_phone()
    print("Phone number name provided\n")

    booking_id = generate_booking_id()
    print("Unique booking ID created\n")

    booking_details = add_worksheet_confirmed(booking_id, desired_date, booked_time, contact_name, contact_phone, time_cell)

    remove_booked_availability(booking_details)

    confirm_to_user(booking_details)

    back_to_menu()


def edit_appointment():
    """
    This function will initialize the editing of an existing booking. It will call functions
    that will check the booking ID with the bookings made in the worksheet. It will then remove
    the booking if edits have been made and provide a new booking confirmation and booking ID.
    """
    print("Editing your nail appointment is quick and can be done via a few easy steps.\n")
    print("First, let's find your booking.\n")

    booking_details = find_booking()
    #print(find_booking)
    #print(type(find_booking))

    correct_booking = booking_confirmation(booking_details)
    print("print of correct booking", correct_booking)
    print("type of correct booking", type(correct_booking))

    update_booking(correct_booking)


def cancel_appointment():
    """
    one of the three main functions. Function to cancel an existing booking. User
    is asked for a booking ID and a confirmation if the right booking is approached.
    If yes, booking is cancelled and the time reinstated in the time overview.
    """
    print("Cancelling your nail appointment is quick and includes a few easy steps.")
    print("First, let's find your booking.\n")
    print("Or press r to return to the main menu.\n")

    booking_details = find_booking()
    print(find_booking)
    print(type(find_booking))

    correct_booking = booking_confirmation(booking_details)
    print("print of correct booking", correct_booking)
    print("type of correct booking", type(correct_booking))

    while True:
        
        print("Are you sure you would like to cancel the following booking?")
        print(f"current booking is on {correct_booking[1]} at {correct_booking[2]}.")
        confirm_cancellation = input("Answer (y/n): ")
        confirm_cancellation = confirm_cancellation.strip().lower()

        if confirm_cancellation == "y":
            print("printout booking details before it goes in", booking_details)
            print(type(booking_details))
            print("print of correct booking before cancelling", correct_booking)
            print(type(correct_booking))
            cancel_booking(correct_booking)
            print("print of correct booking after cancelling", correct_booking)
            print("type of correct booking after cancelling", type(correct_booking))

            reinstate_booking_slot(correct_booking)
            #clear_screen()
            print(f"\nYour booking of {correct_booking[2]}, on the {correct_booking[1]}, has now been cancelled.\n")

            print("If you have any further queries please let us know. You can do this via:")
            print("*  email: nailstudio@thebest.com")
            print("*  phone: +353 81 234 5678\n")

            print("We are here to help!\n")

            back_to_menu()
        elif confirm_cancellation == "n":
            #clear_screen()
            print("OK, we will not cancel your appointment. Bringing you back to the main menu")
            main_menu()
        else:
            print(f"\nPlease make sure you have chosen either y for yes or n for no:")

main_menu()