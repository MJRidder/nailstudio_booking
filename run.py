import gspread
from google.oauth2.service_account import Credentials

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

    print("$ *** Lou's Nail studio ***\n")
    print("$ Welcome to Lou's nail studio!")
    print("$ Below you can find the menu options.")
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

    while True:
        data_str = input("$ Please provide your choice here (A, B, C or E): ")
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
            print("$ Thank you for visiting Lou's nail studio.")
            print("$ Have a great day!\n\n")
            quit()
        elif choice == "":
            # clear_screen()
            print(
                "\n$ Sorry, you did not seem to give an answer. "
                "Please choose one of the options: A, B, C or E.\n")
            print("$ *  Please review the suggested options and try again.\n")
            print("$ *  Please type in 'A' to make a new booking")
            print("$ *  Please type in 'B' to update an existing booking")
            print("$ *  Please type in 'C' to cancel an existing booking")
            print("$ *  Or type 'E' to exit this program.\n")
        else:
            # clear_screen()
            print(
                f"\n$ Sorry, '{choice}' is not one of the menu options.")
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

    while True:
        insert_date = input(
            "$ Please provide the desired date (in format: YYYY/MM/DD): ")
        insert_date = insert_date.strip().lower()

        if insert_date == "r":
            # clear_screen()
            print("\n$ Okido, let's bring you back to the main menu\n")
            main_menu()
        elif insert_date == "":
            # clear_screen()
            print("$ The chosen date cannot be empty. Please try again.\n")
            print("$ Or press 'R' to go back to main menu.\n")
        else:
            print("\n$ Checking your chosen date...\n")
            match_date = dates_times.findall(insert_date, in_column=1)
            # check_date = dates_times.findall(insert_date, in_column=4)

            if match_date:
                print(
                    "$ The requested date is available.\n")
                # print("XXX dataprint XXX - match_date", match_date)
                # print("XXX dataprint XXX - insert_date", insert_date)
                # print("XXX dataprint XXX - check_date", check_date)
                return match_date, insert_date
            # , check_date
            else:
                # clear_screen()
                print(
                    f"$ The requested date '{insert_date}' "
                    "does not seem to be available.\n")
                print("$ Did you type in an actual date?")
                print("$ Did you use the correct format? = YYYY/MM/DD")
                print("$ Did you book a weekday?\n")
                print("$ Example date: March 23rd, 2025 = 2025/03/23\n")
                print("$ if the formatting is correct,"
                      " please try a different date.")
                print("$ As the available time slots will be fully booked.\n")
                print("$ Follow the instructions and try again.\n")


def get_date_cell(choices):
    """
    strip cells of dates from context to then rebuild them with
    the context of the next columns cells (time). To ensure
    that dates and times are available.
    """

    print("$ One moment, let's see what times are available...\n")
    time_cell = []
    for cell in choices:
        if cell != "":
            time_cell.append(cell.row)
        else:
            print("$ this date is not available")
            break

    available_times = [f"B{time_cell}" for time_cell in time_cell]

    return available_times


def get_time_cell(choice):
    """
    Takes the cell values provided in choices (the available booking times)
    and translates these to available times for a client to book. Times are
    only shown if they are available in the dates_times worksheet. Otherwise
    it will be populated by a <space>, which will still hold a string value,
    but will not show as an actual time for the client.
    """

    available_time_value1 = ""
    available_time_value2 = ""
    available_time_value3 = ""

    available_time_cell1 = ""
    available_time_cell2 = ""
    available_time_cell3 = ""

    SHEET.worksheet("available_dates_times")

    print("XXX dataprint XXX - choice", choice)

    try:
        available_time_value1 = SHEET.worksheet(
            "available_dates_times").acell(choice[0]).value
        available_time_cell1 = SHEET.worksheet(
            "available_dates_times").acell(choice[0]).row
    except Exception:
        pass

    try:
        available_time_value2 = SHEET.worksheet(
            "available_dates_times").acell(choice[1]).value
        available_time_cell2 = SHEET.worksheet(
            "available_dates_times").acell(choice[1]).row
    except Exception:
        pass
    try:
        available_time_value3 = SHEET.worksheet(
            "available_dates_times").acell(choice[2]).value
        available_time_cell3 = SHEET.worksheet(
            "available_dates_times").acell(choice[2]).row
    except Exception:
        pass

    print("$ We have availability at the following time(s): ")
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
        "\n$ Or type in 'R' to go back to main menu and start over.")

    while True:
        insert_time = input(
            "$ Type the desired time exactly as the time is presented: ")
        if insert_time == "":
            print(
                "\n$ The chosen time cannot be empty. Please try again.\n")
            print(
                "\n$ Type the desired time exactly as the time is presented:")
            print("\n$ Available time(s):\n")
            print(f"{available_time_value1}")
            print(f"{available_time_value2}")
            print(f"{available_time_value3}\n")
            print("$ Or type in 'R' to go back to main menu and start over.\n")
        elif insert_time == "r":
            # clear_screen()
            print("\n$ OK, let's bring you back.\n")
            main_menu()

        elif insert_time == available_time_value1:
            chosen_time_cell = f"B{available_time_cell1}"
            # clear_screen()
            return chosen_time_cell
        elif insert_time == available_time_value2:
            chosen_time_cell = f"B{available_time_cell2}"
            # clear_screen()
            return chosen_time_cell
        elif insert_time == available_time_value3:
            chosen_time_cell = f"B{available_time_cell3}"
            # clear_screen()
            return chosen_time_cell
        else:
            # clear_screen()
            print(f"\n$ You have chosen '{insert_time}'")
            print("$ Sorry, this time is not available,")
            print("or we did not recognise this as a valid time.")
            print(
                "\n$ Type the desired time exactly as the time is presented:")
            print("$ And make sure to type only the available time(s).")
            print("\n$ Available time(s):\n")
            print(f"{available_time_value1}")
            print(f"{available_time_value2}")
            print(f"{available_time_value3}\n")
            print("$ Or type in 'R' to go back to main menu and start over.\n")


def provide_contact_name():
    """
    function to ask the client to enter their first and last name,
    results in a string.
    """

    while True:
        insert_name = input(
            "$ Please confirm your first and last name: ")

        if insert_name == "":
            print(
                "\n$ Please provide a name.\n"
                "$ This can not be left empty. Please try again.\n")
        else:
            return insert_name


def provide_contact_phone():
    """
    function to ask the client to enter their phone number,
    results in a string.
    """

    while True:
        print("$ * We use your phone number in case an appointment"
              " needs to be cancelled or changed.")
        print("$ It is therefore essential that you provide a"
              " valid phone number.\n")

        insert_phone = input("$ Please confirm your phone number: ")

        if insert_phone == "":
            print(
                "\n$ Please do provide a phone number.\n"
                "$ This field can not be left empty. Please try again.\n")
        else:
            return insert_phone


def generate_booking_id():
    """
    Generates a new booking ID, looking at the highest current
    booking ID number in the confirmed_bookings sheet (column A).
    Taking this value and giving it a +1.
    """
    list_id = SHEET.worksheet("confirmed_bookings").col_values(1)[1:]

    max_value = None
    for n in list_id:
        if max_value is None or int(n) > max_value:
            max_value = int(n)

    new_booking_id = int(max_value) + 1

    return new_booking_id


def find_booking():
    """
    Ask user for the booking ID, check if it is indeed in
    the system and return the cell that the booking ID is
    in. Combined with the row number of that booking ID
    (so that the other information of the booking can be
    captured).
    """

    print(
        "$ Your unique booking ID was provided at the time of your booking.")
    print("$ Please provide below your booking ID.")
    print("$ Or press 'R' to return to the main menu.\n")

    existing_booking = []

    while True:
        insert_booking_id = input("$ Your booking ID: ")
        insert_booking_id = insert_booking_id.strip().lower()

        print("\n$ Please wait a moment while we fetch your booking...\n")

        confirmed_bookings = SHEET.worksheet("confirmed_bookings")

        existing_booking = confirmed_bookings.findall(
            str(insert_booking_id), in_column=1)

        if insert_booking_id == "r":
            # clear_screen()
            print("$ OK, you chose to stop this process.")
            print("$ Let us bring you back to the main menu.\n")
            main_menu()
        elif insert_booking_id == "":
            print("$ You have not entered a booking ID.")
            print(
                "$ Please try again or press 'R' to go back to main menu.\n")
        elif existing_booking != []:
            existing_booking = confirmed_bookings.findall(
                    str(insert_booking_id), in_column=1)

            existing_booking_value = existing_booking[0].value

            existing_booking_row = existing_booking[0].row

            existing_booking.append(existing_booking_value)

            existing_booking.append(existing_booking_row)

            booking_return = existing_booking

            # clear_screen()
            print("$ Great! we have been able to find your booking.")
            print("$ Retrieving the booking details now...\n")

            return booking_return
        else:
            # clear_screen()
            print(
                "$ We have not been able to match your booking number.\n")
            print(
                "$ Did you enter it correctly?")
            print(
                "$ Your booking ID was provided at the time of your booking.")
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
                    print(
                        "\n$ Okido, let's bring you back to the main menu.\n")
                    main_menu()
                elif try_again == "":
                    # clear_screen()
                    print("$ The answer cannot be empty. Please try again.\n")
                    print("$ Answer with either y or n.")
                    print("\n$ Or press 'R' to return to the main menu.\n")
                elif try_again == "r":
                    # clear_screen()
                    print("$ OK, you chose to stop this process.")
                    print("$ Let us bring you back to the main menu.\n")
                    main_menu()
                else:
                    # clear_screen()
                    print(
                        f"\n$ Apologies, '{try_again}' is not a valid answer.")
                    print(
                        "Or we have not been able to"
                        " find a booking with that ID.")
                    print(
                        "$ Please follow the instructions that are provided.")
                    print(
                        "$ You can try again or press 'r'"
                        " to return to main menu.\n")


def booking_confirmation(booking_details):
    """
    Use booking details and confirm if the booking
    is indeed the correct booking that the user is
    looking for. this function will run when an existing
    booking has been found.
    """
    # confirmed_bookings worksheet
    SHEET.worksheet("confirmed_bookings")
    booking_row = booking_details[2]

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

    booking_details = [
        value_booking_id,
        value_booking_date,
        value_booking_time,
        value_booking_name,
        value_booking_timestamp,
        value_booking_confirmation,
        listing_booking_id]

    if value_booking_confirmation == "cancelled":
        print(
            "$ We have found an old booking, but this was cancelled.")
        print(
            f"$ *   The provided booking ID was: {value_booking_id}.")
        print(
            f"$ *   The booking was made for {value_booking_time}.")
        print(
            f"$ *   On the date {value_booking_date}.")
        print(
            f"$ *   The booking was made by {value_booking_name}.\n")

        print(
            "$ would you like to try a different booking number? (y/n)")

        while True:
            cancelled_booking = input(
                "$ or press 'R' to go back to the main menu: ")
            cancelled_booking = cancelled_booking.strip().lower()

            if cancelled_booking == "y":
                # clear_screen()
                print(f"$ OK, the booking with booking ID {value_booking_id},")
                print("$ was cancelled, let's try another one.\n")
                cancel_appointment()
            elif cancelled_booking == "n":
                # clear_screen()
                print("$ OK, let us bring you back to the main menu.")
                main_menu()
            elif cancelled_booking == "r":
                # clear_screen()
                print("$ OK, let us bring you back to the main menu.")
                main_menu()
            elif cancelled_booking == "":
                # clear_screen()
                print("$ Sorry, you did not provide an answer.")
                print("$ Please answer with either y or n.")
                print("$ Or press 'R' to return to the main menu.\n")
            else:
                # clear_screen()
                print(f"\n$ You have chosen '{cancelled_booking}'")
                print("$ Sorry, we did not recognise this as a valid answer.")
                print("$ Please answer with either y or n.")
                print("$ Or press 'R' to return to the main menu.\n")
    else:
        print(
            "$ Please find below the booking details.")
        print(
            f"$ *   The provided booking ID was: {value_booking_id}.")
        print(
            f"$ *   The booking was made for {value_booking_time}.")
        print(
            f"$ *   On the date {value_booking_date}.")
        print(
            f"$ *   The booking was made by {value_booking_name}.\n")

        while True:
            client_confirmation = input(
                "$ Is this the booking you want to edit or cancel? (y/n): ")
            client_confirmation = client_confirmation.strip().lower()

            if client_confirmation == "y":

                booking_details = [
                    value_booking_id,
                    value_booking_date,
                    value_booking_time,
                    value_booking_name,
                    value_booking_timestamp,
                    value_booking_confirmation,
                    listing_booking_id]

                return booking_details

            elif client_confirmation == "n":
                while True:
                    print(
                        f"$ The provided booking ID was: {value_booking_id}")
                    diff_book_id = input(
                        "\n$ Try a different booking? (y/n): ")
                    if diff_book_id == "y":
                        print("\n$ Okido, let's bring you back to editing.\n")
                        edit_appointment()
                    elif diff_book_id == "n":
                        # clear_screen()
                        print("$ OK, let us bring you back to the main menu.")
                        main_menu()
                    elif diff_book_id == "r":
                        # clear_screen()
                        print("$ OK, let us bring you back to the main menu.")
                        main_menu()
                    elif diff_book_id == "":
                        print("$ You did not provide an answer.")
                        print("$ Answer with either y or n.")
                        print("\n$ Or press 'R' to return to the main menu.\n")
                    else:
                        print(
                            f"\nYou have entered '{diff_book_id}'")
                        print(
                            "Sorry, we did not recognise"
                            " this as a valid answer.")
                        print(
                            "$ Please answer with either y or n.")
                        print(
                            "\n$ Or press 'R' to return to the main menu.\n")

            elif client_confirmation == "r":
                # clear_screen()
                print("$ OK, let us bring you back to the main menu.")
                main_menu()
            elif client_confirmation == "":
                print("\n$ The answer cannot be empty. Please try again.\n")
                print("$ Answer with either y or n.")
                print("\n$ Or press 'R' to return to the main menu.\n")
            else:
                print(f"\nYou have entered '{client_confirmation}'")
                print("Sorry, we did not recognise this as a valid answer.")
                print("$ Please answer with either y or n.")
                print("\n$ Or press 'R' to return to the main menu.\n")


def remove_booked_availability(booking_details):
    """
    Updates the worksheet by removing/adding dates
    after a booking is made, edited or cancelled.
    """

    time_cell = booking_details[5]
    date_cell = booking_details[5].replace("B", "A")

    # remove old time from worksheet
    SHEET.worksheet(
        "available_dates_times").update_acell(time_cell, "  ")

    # remove old date from worksheet
    SHEET.worksheet(
        "available_dates_times").update_acell(date_cell, "  ")


def update_booking(correct_booking):
    """
    determine what the client would like to update
    of their existing booking.
    """

    value_booking_date = correct_booking[1]
    value_booking_time = correct_booking[2]
    value_booking_name = correct_booking[3]

    # clear_screen()
    print("\n$ We can now update your booking.")
    print("$ Please use the following answer options:\n")

    print("$ *   Type 'Y' to confirm")
    print("$ *   Type 'N' to decline")
    print("$ *   Type 'C' to cancel your booking")
    print("$ *   Type 'R' to return to the main menu\n")

    print(
        f"\n$ Your booking on {value_booking_date},")
    print(
        f"$ Which was booked at {value_booking_time},")
    print(
        f"$ Was booked for {value_booking_name}.\n")

    while True:
        change_date = input(
            "$ Would you like to change the date? (y/n): ")
        change_date = change_date.strip().lower()

        if change_date == "y":
            print("\n$ OK, let's see if your desired date is available.")
            date_check = date_choice()
            time_cell_check = get_date_cell(date_check[0])

            time_cell = get_time_cell(time_cell_check)

            desired_date = date_check[1]

            booked_time = SHEET.worksheet(
                "available_dates_times").acell(f"{time_cell}").value

            print(
                f"$ You have chosen {booked_time} as your desired time")
            print(f"$ on the date {desired_date}.\n")

            contact_name = provide_contact_name()
            print("$ Contact name provided.\n")

            contact_phone = provide_contact_phone()
            print("$ Phone number name provided.\n")

            booking_id = generate_booking_id()
            print("$ Unique booking ID created.\n")

            print("$ confirm booking details...\n")
            booking_details = add_worksheet_confirmed(
                booking_id,
                desired_date,
                booked_time,
                contact_name,
                contact_phone,
                time_cell
            )

            print("$ Take out the dates and times...\n")
            remove_booked_availability(booking_details)

            print("$ cancel existing booking...\n")
            cancel_booking(correct_booking)

            print("$ reinstate old date and time...\n")
            reinstate_booking_slot(correct_booking)

            print("$ confirming new booking to the user...\n")
            confirm_to_user(correct_booking)

            back_to_menu()

        elif change_date == "n":
            change_time = input(
                "\n$ Would you like to change the time? (y/n): ")
            change_time = change_time.strip().lower()

            while True:
                if change_time == "y":
                    dates_times = SHEET.worksheet("available_dates_times")
                    check_time = dates_times.findall(
                        str(correct_booking[1]), in_column=1)

                    print(
                        "$ OK, let's see if there"
                        " are other times available.\n")
                    time_cell_check = get_date_cell(check_time)

                    time_cell = get_time_cell(time_cell_check)

                    desired_date = value_booking_date

                    booked_time = SHEET.worksheet(
                        "available_dates_times").acell(f"{time_cell}").value

                    print(
                        f"$ You have chosen {booked_time}"
                        " as your desired time")
                    print(f"$ on the date {desired_date}.\n")

                    contact_name = provide_contact_name()
                    print("$ Contact name provided.\n")

                    contact_phone = provide_contact_phone()
                    print("$ Phone number name provided.\n")

                    booking_id = generate_booking_id()
                    print("$ Unique booking ID created.\n")

                    print("$ confirm booking details...\n")
                    booking_details = add_worksheet_confirmed(
                        booking_id,
                        desired_date,
                        booked_time,
                        contact_name,
                        contact_phone,
                        time_cell
                    )

                    print("$ Take out the dates and times...\n")
                    remove_booked_availability(booking_details)

                    print("$ cancel existing booking...\n")
                    cancel_booking(correct_booking)

                    print("$ reinstate old date and time...\n")
                    reinstate_booking_slot(correct_booking)

                    print("$ confirming new booking to the user...\n")
                    confirm_to_user(correct_booking)

                    back_to_menu()

                elif change_time == "n":
                    change_contact = input(
                        "\n$ Would you like to update"
                        " your contact details? (y/n): ")
                    change_contact = change_contact.strip().lower()
                    while True:
                        if change_contact == "y":
                            print(
                                "\n$ Great, please enter"
                                " your contact details:\n")
                            print("$ This will overwrite any"
                                  " old contact details.\n")

                            contact_name = provide_contact_name()
                            print("$ Contact name provided.\n")

                            contact_phone = provide_contact_phone()
                            print("$ Phone number name provided.\n")

                            desired_date = value_booking_date
                            booked_time = value_booking_time
                            time_cell = correct_booking[4]

                            booking_id = generate_booking_id()
                            print("$ Unique booking ID created.\n")

                            print("$ confirm booking details...\n")
                            booking_details = add_worksheet_confirmed(
                                booking_id,
                                desired_date,
                                booked_time,
                                contact_name,
                                contact_phone,
                                time_cell
                            )

                            print("$ cancel existing booking...\n")
                            cancel_booking(correct_booking)

                            print("$ confirming new booking to the user...\n")
                            confirm_to_user(correct_booking)

                            back_to_menu()
                        elif change_contact == "n":
                            # clear_screen()
                            print(
                                "$ OK, as you are not looking"
                                " to change any details,")
                            print(
                                "$ we will bring you back to the main menu.\n")
                            main_menu()
                        elif change_contact == "":
                            # clear_screen()
                            print(
                                "$ You did not enter a choice."
                                " Please try again.\n")
                            print(
                                "$ Would you like to update your"
                                " contact details? (y/n): ")
                        else:
                            print(
                                "$ Sorry, we did not understand"
                                " what you meant")
                            try_again = input("$ Would you like to"
                                              " try again? (y/n): ")
                            while True:
                                if try_again == "y":
                                    print("$ Great! let's try again.\n")
                                    update_booking(correct_booking)
                                elif try_again == "n":
                                    print("\nOkido, let's bring you back"
                                          " to the main menu\n")
                                    main_menu()
                                elif try_again == "":
                                    print("\n$ You did not enter a choice."
                                          " Please try again.")
                                    print("$ Would you like to"
                                          " try again? (y/n): \n")
                                else:
                                    # clear_screen()
                                    print(
                                        "$ Sorry, it is not clear"
                                        " what you mean.")
                                    print(
                                        "$ Please follow the instructions"
                                        " that are provided.")
                                    print(
                                        "$ For now, let us bring you back"
                                        " to the main menu.")
                                    print(
                                        "$ From here you can try again,"
                                        " or exit the program.")
                                    print(
                                        "$ Apologies for any inconvenience.")
                                    main_menu()
                else:
                    # clear_screen()
                    print(
                        "$ Sorry, it is not clear what you mean.")
                    print(
                        "$ Please follow the instructions"
                        " that are provided.")
                    print(
                        "$ For now, let us bring you back"
                        " to the main menu.")
                    print(
                        "$ From here you can try again,"
                        " or exit the program.")
                    print(
                        "$ Apologies for any inconvenience.")
                    main_menu()

        elif change_date == "c":
            # clear_screen()
            print(
                "\n$ Are you sure you want to cancel the following booking?")
            print(
                f"$ {value_booking_date} at {value_booking_time}.\n")

            confirm_cancellation = input("$ Answer (y/n): ")
            confirm_cancellation = confirm_cancellation.strip().lower()

            if confirm_cancellation == "y":

                print("\n$ cancelling your booking booking now...\n")
                cancel_booking(correct_booking)
                reinstate_booking_slot(correct_booking)

                print(f"\n$ The booking at {correct_booking[2]}")
                print(f"$ on {correct_booking[1]}\n")
                print("$ Has now been cancelled")

                print("$ If you have any further queries"
                      " please let us know.\n")
                print("$ You can do this via:")
                print("$ *  email: nailstudio@thebest.com")
                print("$ *  phone: +353 81 234 5678\n")

                print("$ We are here to help!\n")
                back_to_menu()
            elif confirm_cancellation == "n":
                print("$ OK, let's bring you back to the main menu.\n")
                main_menu()
            elif confirm_cancellation == "":
                print("$ You did not provide an answer. Please try again.\n")
                print("$ Would you like to cancel your booking? (y/n): ")

        elif change_date == "r":
            # clear_screen()
            print("$ Editing your booking has been cancelled.")
            print("$ Bringing you back to the main menu.")
            main_menu()
        elif change_date == "":
            print("$ You did not provide an answer Please try again.\n")
            print("$ Please answer with either y or n.\n")
            print("$ Or press 'R' to return to the main menu.\n")
        else:
            print(f"\n$ You answered: {change_date}")
            print("$ Sorry, we did not recognise this as a valid answer")
            print("$ Please answer with either y or n.\n")
            print("$ Or press 'R' to return to the main menu.\n")

            # try_again = input("$ Would you like to try again? (y/n): ")
            # if try_again == "y":
            #     print("$ Great! let's try again.\n")
            #     update_booking(correct_booking)
            # elif try_again == "n":
            #     # clear_screen()
            #     print(
            #         "\n$ Okido, let's bring you back to the main menu\n")
            #     main_menu()
            # elif try_again == "":
            #     print(
            #         "\n$ You did not enter a choice. Please try again.")
            # else:
            #     # clear_screen()
            #     print(
            #         "$ Sorry, it is not clear what you mean.")
            #     print(
            #         "$ Please follow the instructions that are provided.")
            #     print(
            #         "$ For now, let us bring you back to the main menu.")
            #     print(
            #         "$ From here you can try again, or exit the program.")
            #     print(
            #         "$ Apologies for any inconvenience.")
            #     main_menu()


def cancel_booking(correct_booking):
    """
    Find a booking based off the booking_id. confirm what
    of the original booking needs to be edited. Confirm
    availability to edit. Make new booking with a new
    booking ID and booking data. Reinstate the original booking.
    """
    confirmed_bookings = SHEET.worksheet("confirmed_bookings")

    print("$ finding your old appointment...\n")

    find_old_id = confirmed_bookings.findall(
        str(correct_booking[0]), in_column=1)

    booking_row = find_old_id[0].row
    print(f"$ Booking row to be updated: {booking_row}")

    confirmation_cell = "G" + str(booking_row)

    print("$ Cancelling your old appointment...\n")
    # cancel_booking
    SHEET.worksheet(
        "confirmed_bookings").update_acell(confirmation_cell, "cancelled")

    print("$ old appointment cancelled\n")

    return correct_booking


def reinstate_booking_slot(correct_booking):
    """
    Receiving the timestamp of an old booking (which
    relates to the timeslot in the Google sheet). Using this
    value to reinstate date and time for future bookings.
    """
    # dates_times worksheet
    SHEET.worksheet("available_dates_times")

    print("reinstating old times...\n")

    date_truth_cell = correct_booking[4].replace("B", "D")
    time_truth_cell = correct_booking[4].replace("B", "E")

    reinstated_date = correct_booking[4].replace("B", "A")

    date_truth_check = SHEET.worksheet(
        "available_dates_times").acell(date_truth_cell).value
    time_truth_check = SHEET.worksheet(
        "available_dates_times").acell(time_truth_cell).value

    # reinstated_date_cell
    SHEET.worksheet(
        "available_dates_times").update_acell(
            str(date_truth_cell), date_truth_check)

    # reinstate_date
    SHEET.worksheet(
        "available_dates_times").update_acell(
            str(reinstated_date), date_truth_check)

    # reinstate_time
    SHEET.worksheet(
        "available_dates_times").update_acell(
            str(correct_booking[4]), time_truth_check)
    return


def add_worksheet_confirmed(booking_id, desired_date, booked_time, contact_name, contact_phone, time_cell): # noqa
    """
    Receives the date of the booking, the time, first &
    last name and the phone number, all in strings. Inserts
    these in their own columns in the worksheet,
    tab: confirmed_bookings.
    """

    print("$ confirming booking...\n")

    # confirmed booking sheet
    SHEET.worksheet("confirmed_bookings").get_all_values()

    print("$ Updating confirmed_bookings worksheet...\n")
    booking_data = [
        booking_id,
        desired_date,
        booked_time,
        contact_name,
        contact_phone,
        time_cell,
        "YES"]

    worksheet_to_update = SHEET.worksheet("confirmed_bookings")
    worksheet_to_update.append_row(booking_data)
    print("$ Booking updated successfully\n")

    return booking_id, desired_date, booked_time, contact_name, contact_phone, time_cell # noqa


def back_to_menu():
    """
    Function to bring back the user back to the main menu.
    """

    while True:
        back_to_menu = input(
            "$ Would you like to go back to the main menu? y/n: ")
        choice = back_to_menu.strip().lower()

        if choice == "y":
            print("$ Bringing you back to the main menu.")
            # clear_screen()
            main_menu()
        elif choice == "n":
            print("$ Thank you for your time. Have a great day.\n\n")
            quit()
        elif choice == "":
            print(
                "$ The answer cannot be empty. Please try again.\n")
            print("$ Answer with either y or n.")
        else:
            # clear_screen()
            print(
                f"$ You entered: {choice}.")
            print(
                "$ Sorry, that is not a valid option.")
            print(
                "$ could you please try again? Please use either y or n.\n")


def confirm_to_user(booking_details):
    """
    Function that reads back the finalised booking to the user.
    """

    # clear_screen()
    print(
        "$ Thank you for your booking! We appreciate your business.\n")
    print(
        "To confirm:")

    print(
        f"$ *  Your unique booking ID: {booking_details[0]}")
    print(
        f"$ *  The date of your booking: {booking_details[1]}")
    print(
        f"$ *  Your booking will be at: {booking_details[2]}")
    print(
        f"$ *  And your booking is for: {booking_details[3]}\n")
    print(
        "$ To confirm, We will send you a message on")
    print(
        f"$ the following number: {booking_details[4]}\n")

    print("$ If you have any further queries please let us know.\n")
    print("$ You can do this via:")
    print("$ *  email: nailstudio@thebest.com")
    print("$ *  phone: +353 81 234 5678\n")

    print("$ We are here to help!\n")

    return


def book_appointment():
    """
    One of the three main functions. This is the main booking
    function that will run through relevant functions to
    ensure the booking can be completed.
    """
    print("*** Book your next appointment ***\n")
    print(
        "$ Booking a nail appointment is quick and takes a few easy steps.")
    print(
        "$ First provide the desired date using the format: (YYYY/MM/DD).")
    print(
        "$ If that date is available, choose from the available time slots.\n")
    print(
        "$ Or press 'R' if you want to return to the main menu.\n")

    SHEET.worksheet("available_dates_times")
    date_check = date_choice()
    print("XXX dataprint XXX - date_check", date_check)

    time_cell_check = get_date_cell(date_check[0])
    print("XXX dataprint XXX - time_cell_check", time_cell_check)

    time_cell = get_time_cell(time_cell_check)
    print("XXX dataprint XXX - time_cell", time_cell)

    desired_date = date_check[1]
    print("XXX dataprint XXX - desired_date", desired_date)

    booked_time = SHEET.worksheet(
        "available_dates_times").acell(f"{time_cell}").value

    # The get_time_cell function provides a confirmmation of the chosen time.
    print(
        f"$ You have chosen {booked_time} as your desired time")
    print(
        f"on the date {desired_date}.\n")

    contact_name = provide_contact_name()
    print("\n$ Contact name has been provided.\n")

    contact_phone = provide_contact_phone()
    print("\n$ Phone number has been provided.\n")

    booking_id = generate_booking_id()
    print("$ Unique booking ID created.\n")

    booking_details = add_worksheet_confirmed(
        booking_id,
        desired_date,
        booked_time,
        contact_name,
        contact_phone,
        time_cell
    )

    remove_booked_availability(booking_details)

    confirm_to_user(booking_details)

    back_to_menu()


def edit_appointment():
    """
    One of the three main functions. This is the main editing function.
    Running the user through the relavant functions to complete their
    editing (or also cancellation of their booking.
    """
    print("*** Editing an appointment ***\n")
    print(
        "$ Editing a nail appointment is quick and takes a few easy steps.")
    print("$ First, let's find your booking.")

    booking_details = find_booking()
    # print("XXX dataprint XXX - booking details for editing", booking_details)

    correct_booking = booking_confirmation(booking_details)

    update_booking(correct_booking)


def cancel_appointment():
    """
    one of the three main functions. Function to cancel an existing booking.
    User is asked for a booking ID and a confirmation if the right booking
    is approached. If yes, booking is cancelled and the time reinstated in
    the time overview.
    """
    print("*** Cancelling an appointment ***\n")
    print(
        "$ Cancelling a nail appointment is quick and takes a few easy steps.")
    print("$ First, let's find your booking.")
    print("$ Or press 'R' to return to the main menu.\n")

    booking_details = find_booking()

    correct_booking = booking_confirmation(booking_details)

    while True:

        print(
            "$ Are you sure you would like to cancel the following booking?")
        print(f"$ current booking is on the date {correct_booking[1]}.")
        print(f"$ Time of your booking is {correct_booking[2]}.\n")
        confirm_cancellation = input("Answer (y/n): ")
        confirm_cancellation = confirm_cancellation.strip().lower()

        if confirm_cancellation == "y":

            cancel_booking(correct_booking)

            reinstate_booking_slot(correct_booking)
            # clear_screen()
            print(f"\n$ The booking at {correct_booking[2]}")
            print(f"$ on {correct_booking[1]}\n")
            print("$ Has now been cancelled")

            print("$ If you have any further queries please let us know.\n")
            print("$ You can do this via:")
            print("$ *  email: nailstudio@thebest.com")
            print("$ *  phone: +353 81 234 5678\n")

            print("$ We are here to help!\n")

            back_to_menu()
        elif confirm_cancellation == "n":
            # clear_screen()
            print("$ OK, we will not cancel your appointment.\n")
            print("$ Bringing you back to the main menu.")
            main_menu()
        elif confirm_cancellation == "":
            print("$ You did not enter an answer, please answer with y or n.")
            print(
                "$ Or press 'R' to return to the main menu.\n")
        elif confirm_cancellation == "r":
            # clear_screen()
            print(
                "$ OK, we will not cancel your appointment.")
            print("$ Bringing you back to the main menu.")
            main_menu()
        else:
            print("$ Sorry. We did not get that.")
            print("$ Please ensure that you use the suggested y or n format.")


main_menu()
