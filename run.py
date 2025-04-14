import gspread
import colorama
from colorama import Fore, Style
from google.oauth2.service_account import Credentials
# import os

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('nailstudio_bookingsystem')

colorama.init(autoreset=True)


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

    print(f"{Style.BRIGHT}{Fore.YELLOW}$ *** Lou's Nail studio ***\n")
    print("$ Welcome to Lou's nail studio!")
    print("$ A place for all for your nail needs.\n")
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
        data_str = input(f"{Style.BRIGHT}$ Please provide your"
                         f" choice here (A, B, C or E): ")
        choice = data_str.strip().lower()

        if choice == "a":
            print("$ *** Book your next appointment ***\n")
            clear_screen()
            book_appointment()
        elif choice == "b":
            print("$ *** Edit an existing appointment ***\n")
            clear_screen()
            edit_appointment()
        elif choice == "c":
            print("$ *** Cancel an existing appointment ***\n")
            clear_screen()
            cancel_appointment()
        elif choice == "e":
            print("$ Exiting program\n")
            clear_screen()
            print("$ Thank you for visiting Lou's nail studio.")
            print("$ Have a great day!\n\n")
            quit()
        elif choice == "":
            clear_screen()
            print(
                f"{Fore.RED}\n$ Sorry, you did not seem to give an answer.")
            print(
                f"{Fore.RED}$ Please choose one"
                f" of the options: A, B, C or E.\n")
            print("$ *  Please review the suggested options and try again.\n")
            print("$ *  Please type in 'A' to make a new booking")
            print("$ *  Please type in 'B' to update an existing booking")
            print("$ *  Please type in 'C' to cancel an existing booking")
            print("$ *  Or type 'E' to exit this program.\n")
        else:
            clear_screen()
            print(
                f"{Fore.RED}\n$ Sorry, '{Fore.MAGENTA}{choice}'"
                f"{Fore.RED} is not one of the menu options.")
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
            f"{Style.BRIGHT}$ Please provide the desired"
            " date (in format: YYYY/MM/DD): ")
        insert_date = insert_date.strip().lower()

        if insert_date == "r":
            clear_screen()
            print("\n$ Okido, let's bring you back to the main menu\n")
            main_menu()
        elif insert_date == "":
            clear_screen()
            print("\n$ The chosen date cannot be empty. Please try again.\n")
            print("$ Example date: March 23rd, 2025 = 2025/03/23\n")
            print("$ Or press 'R' to go back to main menu.\n")
        else:
            print(f"{Fore.CYAN}\n$ Checking your chosen date...\n")
            match_date = dates_times.findall(insert_date, in_column=1)

            if match_date:
                print(
                    f"{Fore.GREEN}$ The requested date is available.\n")
                return match_date, insert_date
            else:
                clear_screen()
                print(
                    f"{Fore.RED}\n$ The requested date"
                    f" '{Fore.MAGENTA}{insert_date}'"
                    f" {Fore.WHITE}does not seem to be available.\n")
                print("$ Did you type in an actual date?")
                print("$ Did you use the correct format? = YYYY/MM/DD")
                print("$ Did you book a weekday?\n")
                print("$ Example date: March 23rd, 2025 = 2025/03/23\n")
                print("$ If the formatting is correct,"
                      " please try a different date.")
                print("$ As the available time slots will be fully booked.\n")
                print("$ Follow the instructions and try again.\n")


def get_date_cell(choices):
    """
    strip cells of dates from context to then rebuild them with
    the context of the next columns cells (time). To ensure
    that dates and times are available.
    """

    print(f"{Fore.CYAN}$ One moment, let's see what times are available...\n")
    time_cell = []
    for cell in choices:
        if cell != "":
            time_cell.append(cell.row)
        else:
            print(f"{Fore.Red}$ this date is not available")
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
            print(f"{Fore.GREEN}\n{available_time_value1}")
        if available_time_value2 != "":
            print(f"{Fore.GREEN}{available_time_value2}")
        if available_time_value3 != "":
            print(f"{Fore.GREEN}{available_time_value3}")
    except Exception as e:
        print(str(e), "")

    print(
        "\n$ Or type in 'R' to go back to main menu and start over.")

    while True:
        insert_time = input(
            f"{Style.BRIGHT}$ Type the desired time exactly"
            f" as the time is presented: ")
        if insert_time == "":
            clear_screen()
            print(
                f"{Fore.RED}\n$ The chosen time cannot be empty."
                f" Please try again.\n")
            print(
                "$ Type the desired time exactly as the time is presented")
            print("\n$ Available time(s):\n")
            print(f"{Fore.GREEN}{available_time_value1}")
            print(f"{Fore.GREEN}{available_time_value2}")
            print(f"{Fore.GREEN}{available_time_value3}\n")
            print("$ Or type in 'R' to go back to main menu and start over.\n")
        elif insert_time == "r":
            clear_screen()
            print("\n$ OK, let's bring you back.\n")
            main_menu()

        elif insert_time == available_time_value1:
            chosen_time_cell = f"B{available_time_cell1}"
            clear_screen()
            return chosen_time_cell
        elif insert_time == available_time_value2:
            chosen_time_cell = f"B{available_time_cell2}"
            clear_screen()
            return chosen_time_cell
        elif insert_time == available_time_value3:
            chosen_time_cell = f"B{available_time_cell3}"
            clear_screen()
            return chosen_time_cell
        else:
            clear_screen()
            print(f"\n$ You have chosen the time "
                  f"'{Fore.MAGENTA}{insert_time}'")
            print(f"{Fore.RED}$ Sorry, this time is not available,")
            print(f"{Fore.RED}$ or we did not recognise this as a valid time.")
            print(
                "\n$ Type the desired time exactly as the time is presented")
            print("$ And make sure to choose only from the available time(s).")
            print("\n$ Available time(s):\n")
            print(f"{Fore.GREEN}{available_time_value1}")
            print(f"{Fore.GREEN}{available_time_value2}")
            print(f"{Fore.GREEN}{available_time_value3}\n")
            print("$ Or type in 'R' to go back to main menu and start over.\n")


def provide_contact_name():
    """
    function to ask the client to enter their first and last name,
    results in a string.
    """

    while True:
        insert_name = input(
            f"{Style.BRIGHT}$ Please confirm your first and last name: ")

        if insert_name == "":
            print(
                f"{Fore.RED}\n$ Please provide a name.\n"
                f"$ This can not be left empty. Please try again.\n")
        else:
            return insert_name


def provide_contact_phone():
    """
    function to ask the client to enter their phone number,
    results in a string.
    """

    while True:
        print("* We use your phone number in case an appointment"
              " needs to be updated.")
        print("* It is therefore essential that you provide a"
              " valid phone number.\n")

        insert_phone = input(f"{Style.BRIGHT}$ Please confirm"
                             f" your phone number: ")

        if insert_phone == "":
            print(
                f"{Fore.RED}\n$ Please do provide a phone number.\n"
                f"$ This field can not be left empty. Please try again.\n")
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
        insert_booking_id = input(f"{Style.BRIGHT}$ Your booking ID: ")
        insert_booking_id = insert_booking_id.strip().lower()

        print(f"{Fore.CYAN}\n$ Please wait a moment while"
              f" we fetch your booking...\n")

        confirmed_bookings = SHEET.worksheet("confirmed_bookings")

        existing_booking = confirmed_bookings.findall(
            str(insert_booking_id), in_column=1)

        if insert_booking_id == "r":
            clear_screen()
            print("$ OK, you chose to stop this process.")
            print("$ Let us bring you back to the main menu.\n")
            main_menu()
        elif insert_booking_id == "":
            print(f"{Fore.RED}$ You have not entered a booking ID.")
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

            clear_screen()
            print(f"{Style.BRIGHT}{Fore.GREEN}$ Great! "
                  f"we have been able to find your booking.")
            print(f"{Fore.CYAN}$ Retrieving the booking details now.")
            print(f"{Fore.CYAN}$ This may take a few seconds...\n")

            return booking_return
        else:
            clear_screen()
            print(f"$ You provided {Fore.MAGENTA}{insert_booking_id}"
                  f"{Fore.WHITE} as your booking ID.")
            print(
                f"{Fore.RED}$ We have not been able to match"
                f" your booking number.\n")
            print(
                "$ Did you enter it correctly?")
            print(
                "$ Your booking ID was provided at the time of your booking.")
            print(
                "$ Your booking ID consists of numbers only.\n")
            print(
                "$ Please try again or press 'R' to go back to main menu.\n")
            
            # while True:
            #     try_again = input(f"{Style.BRIGHT}$ Would you like"
            #                       f" to try again? (y/n): ")
            #     try_again = try_again.strip().lower()
            #     if try_again == "y":
            #         clear_screen()
            #         print("$ Great! let's try again.\n")
            #         edit_appointment()
            #     elif try_again == "n":
            #         clear_screen()
            #         print(
            #             "\n$ Okido, let's bring you back to the main menu.\n")
            #         main_menu()
            #     elif try_again == "":
            #         clear_screen()
            #         print(f"{Fore.RED}$ The answer cannot be empty."
            #               f" Please try again.\n")
            #         print("$ Answer with either Y or N.")
            #         print("\n$ Or press 'R' to return to the main menu.\n")
            #     elif try_again == "r":
            #         clear_screen()
            #         print("$ OK, you chose to stop this process.")
            #         print("$ Let us bring you back to the main menu.\n")
            #         main_menu()
            #     else:
            #         clear_screen()
            #         print(
            #             f"\n$ You answered: '{Fore.MAGENTA}{try_again}'")
            #         print(
            #             f"{Fore.RED}$ Sorry, we did not recognise"
            #             " this as a valid answer.")
            #         print(
            #             "$ Or we have not been able to"
            #             " find a booking with that ID.")
            #         print("$ Your unique booking ID was"
            #               " provided at the time of your booking.\n")
            #         print(
            #             "$ Please follow the instructions that are provided.")
            #         print(
            #             "$ You can try again or press 'R'"
            #             " to return to main menu.\n")


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
            f"$ *   The provided booking ID was: "
            f"{Fore.MAGENTA}{value_booking_id}")
        print(
            f"$ *   The booking was made for "
            f"{Fore.MAGENTA}{value_booking_time}")
        print(
            f"$ *   On the date "
            f"{Fore.MAGENTA}{value_booking_date}")
        print(
            f"$ *   The booking was made by "
            f"{Fore.MAGENTA}{value_booking_name}\n")

        print(
            "$ would you like to try a different booking number? (y/n)")

        while True:
            cancelled_booking = input(
                f"{Style.BRIGHT}$ or press 'R' to go back to the main menu: ")
            cancelled_booking = cancelled_booking.strip().lower()

            if cancelled_booking == "y":
                clear_screen()
                print(f"$ OK, the booking with booking ID {value_booking_id},")
                print("$ was cancelled, let's try another one.\n")
                cancel_appointment()
            elif cancelled_booking == "n":
                clear_screen()
                print("$ OK, let us bring you back to the main menu.\n")
                main_menu()
            elif cancelled_booking == "r":
                clear_screen()
                print("$ OK, let us bring you back to the main menu.\n")
                main_menu()
            elif cancelled_booking == "":
                clear_screen()
                print(f"{Fore.RED}$ Sorry, you did not provide an answer.")
                print("$ Please answer with either Y or N.")
                print("$ Or press 'R' to return to the main menu.\n")
            else:
                clear_screen()
                print(f"\n$ You have chosen "
                      f"'{Fore.MAGENTA}{cancelled_booking}'")
                print(f"{Fore.RED}$ Sorry, we did not recognise"
                      f" this as a valid answer.")
                print("$ Please answer with either Y or N.")
                print("$ Or press 'R' to return to the main menu.\n")
    else:
        print(
            "$ Please find below the booking details.")
        print(
            f"$ *   The provided booking ID was: "
            f"{Fore.GREEN}{value_booking_id}")
        print(
            f"$ *   The booking was made for "
            f"{Fore.GREEN}{value_booking_time}")
        print(
            f"$ *   On the date "
            f"{Fore.GREEN}{value_booking_date}")
        print(
            f"$ *   The booking was made by "
            f"{Fore.GREEN}{value_booking_name}\n")

        while True:
            client_confirmation = input(
                f"{Style.BRIGHT}$ Is this the booking you want to"
                f" edit or cancel? (y/n): ")
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
                        f"$ The provided booking ID was:"
                        f" {Fore.MAGENTA}{value_booking_id}")
                    diff_book_id = input(
                        f"{Style.BRIGHT}\n$ Try a different booking? (y/n): ")
                    if diff_book_id == "y":
                        clear_screen()
                        print("\n$ Okido, let's bring you back to editing.\n")
                        edit_appointment()
                    elif diff_book_id == "n":
                        clear_screen()
                        print(f"{Fore.CYAN}$ OK, let us bring you back"
                              f" to the main menu.\n")
                        main_menu()
                    elif diff_book_id == "r":
                        clear_screen()
                        print(f"{Fore.CYAN}$ OK, let us bring you back"
                              " to the main menu.\n")
                        main_menu()
                    elif diff_book_id == "":
                        clear_screen()
                        print(f"{Fore.RED}$ Sorry, You did not"
                              " provide an answer.")
                        print("$ Answer with either Y or N")
                        print("\n$ Or press 'R' to return to the main menu.\n")
                        print(
                            "$ Please find below the booking details.")
                        print(
                            f"$ *   The provided booking ID was:"
                            f" {Fore.GREEN}{value_booking_id}")
                        print(
                            f"$ *   The booking was made for"
                            f" {Fore.GREEN}{value_booking_time}")
                        print(
                            f"$ *   On the date"
                            f" {Fore.GREEN}{value_booking_date}")
                        print(
                            f"$ *   The booking was made by"
                            f" {Fore.GREEN}{value_booking_name}\n")

                    else:
                        clear_screen()
                        print(
                            f"\nYou have entered "
                            f"'{Fore.MAGENTA}{diff_book_id}'")
                        print(
                            f"{Fore.RED}Sorry, we did not recognise"
                            f" this as a valid answer.")
                        print(
                            "$ Please answer with either Y or N.")
                        print(
                            "\n$ Or press 'R' to return to the main menu.\n")
                        print(
                            "$ Please find below the booking details.")
                        print(
                            f"$ *   The provided booking ID was:"
                            f" {Fore.GREEN}{value_booking_id}.")
                        print(
                            f"$ *   The booking was made for"
                            f" {Fore.GREEN}{value_booking_time}.")
                        print(
                            f"$ *   On the date"
                            f" {Fore.GREEN}{value_booking_date}.")
                        print(
                            f"$ *   The booking was made by"
                            f" {Fore.GREEN}{value_booking_name}.\n")

            elif client_confirmation == "r":
                clear_screen()
                print("$ OK, let us bring you back to the main menu.\n")
                main_menu()
            elif client_confirmation == "":
                clear_screen()
                print("\n$ The answer cannot be empty. Please try again.\n")
                print("$ Answer with either Y or N.")
                print("\n$ Or press 'R' to return to the main menu.\n")
                print(
                    f"$ *   The provided booking ID was:"
                    f" {Fore.GREEN}{value_booking_id}")
                print(
                    f"$ *   The booking was made for"
                    f" {Fore.GREEN}{value_booking_time}")
                print(
                    f"$ *   On the date"
                    f" {Fore.GREEN}{value_booking_date}")
                print(
                    f"$ *   The booking was made by"
                    f" {Fore.GREEN}{value_booking_name}\n")
            else:
                clear_screen()
                print(f"\nYou have entered "
                      f"'{Fore.MAGENTA}{client_confirmation}'")
                print(f"{Fore.RED}Sorry, we did not recognise"
                      f" this as a valid answer.")
                print("$ Please answer with either Y or N.")
                print("\n$ Or press 'R' to return to the main menu.\n")
                print(
                    f"$ *   The provided booking ID was:"
                    f" {Fore.GREEN}{value_booking_id}")
                print(
                    f"$ *   The booking was made for"
                    f" {Fore.GREEN}{value_booking_time}")
                print(
                    f"$ *   On the date"
                    f" {Fore.GREEN}{value_booking_date}")
                print(
                    f"$ *   The booking was made by"
                    f" {Fore.GREEN}{value_booking_name}\n")


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

    clear_screen()
    print("\n$ We can now update your booking.")
    print("$ Please use the following answer options:\n")

    print("$ *   Type 'Y' to confirm")
    print("$ *   Type 'N' to decline")
    print("$ *   Type 'C' to cancel your booking")
    print("$ *   Type 'R' to return to the main menu\n")

    print(
        f"\n$ Your booking on {Fore.GREEN}{value_booking_date}")
    print(
        f"$ Which was booked at {Fore.GREEN}{value_booking_time}")
    print(
        f"$ Was booked for {Fore.GREEN}{value_booking_name}\n")

    while True:
        change_date = input(
            f"{Style.BRIGHT}$ Would you like to change the date? (y/n): ")
        change_date = change_date.strip().lower()

        if change_date == "y":
            print("\n$ OK, let's see if your desired date is available.\n")
            date_check = date_choice()
            time_cell_check = get_date_cell(date_check[0])

            time_cell = get_time_cell(time_cell_check)

            desired_date = date_check[1]

            booked_time = SHEET.worksheet(
                "available_dates_times").acell(f"{time_cell}").value

            print(
                f"$ You have chosen {Fore.GREEN}{booked_time}"
                f"{Fore.WHITE} as your desired time,")
            print(f"$ on the date {Fore.GREEN}{desired_date}.\n")

            contact_name = provide_contact_name()
            print(f"{Fore.CYAN}$ Contact name provided.\n")

            contact_phone = provide_contact_phone()
            print(f"{Fore.CYAN}$ Phone number name provided.\n")

            booking_id = generate_booking_id()
            print(f"{Fore.CYAN}$ Unique booking ID created.\n")

            print(f"{Fore.CYAN}$ confirm booking details...\n")
            booking_details = add_worksheet_confirmed(
                booking_id,
                desired_date,
                booked_time,
                contact_name,
                contact_phone,
                time_cell
            )

            print(f"{Fore.CYAN}$ Take out the dates and times...\n")
            remove_booked_availability(booking_details)

            print(f"{Fore.CYAN}$ cancel existing booking...\n")
            cancel_booking(correct_booking)

            print(f"{Fore.CYAN}$ reinstate old date and time...\n")
            reinstate_booking_slot(correct_booking)

            print(f"{Fore.CYAN}$ confirming new booking to the user...\n")
            confirm_to_user(correct_booking)

            back_to_menu()

        elif change_date == "n":

            while True:
                change_time = input(
                    f"{Style.BRIGHT}\n$ Would you like to"
                    f" change the time? (y/n): ")
                change_time = change_time.strip().lower()

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
                    print(f"{Fore.CYAN}$ Contact name provided.\n")

                    contact_phone = provide_contact_phone()
                    print(f"{Fore.CYAN}$ Phone number name provided.\n")

                    booking_id = generate_booking_id()
                    print(f"{Fore.CYAN}$ Unique booking ID created.\n")

                    print(f"{Fore.CYAN}$ confirm booking details...\n")
                    booking_details = add_worksheet_confirmed(
                        booking_id,
                        desired_date,
                        booked_time,
                        contact_name,
                        contact_phone,
                        time_cell
                    )

                    print(f"{Fore.CYAN}$ Take out the dates and times...\n")
                    remove_booked_availability(booking_details)

                    print(f"{Fore.CYAN}$ cancel existing booking...\n")
                    cancel_booking(correct_booking)

                    print(f"{Fore.CYAN}$ reinstate old date and time...\n")
                    reinstate_booking_slot(correct_booking)

                    print(f"{Fore.CYAN}$ confirming"
                          f" new booking to the user...\n")
                    confirm_to_user(correct_booking)

                    back_to_menu()

                elif change_time == "n":
                    while True:
                        change_contact = input(
                            f"{Style.BRIGHT}\n$ Would you like to update"
                            " your contact details? (y/n): ")
                        change_contact = change_contact.strip().lower()
                        if change_contact == "y":
                            print(
                                "\n$ Great, please enter"
                                " your contact details:\n")
                            print("$ This will overwrite any"
                                  " old contact details.\n")

                            contact_name = provide_contact_name()
                            print(f"{Fore.CYAN}$ Contact name provided.\n")

                            contact_phone = provide_contact_phone()
                            print(f"{Fore.CYAN}$ Phone number provided.\n")

                            desired_date = value_booking_date
                            booked_time = value_booking_time
                            time_cell = correct_booking[4]

                            booking_id = generate_booking_id()
                            print(f"{Fore.CYAN}$ Unique booking ID created.\n")

                            print(f"{Fore.CYAN}$ confirm booking details...\n")
                            booking_details = add_worksheet_confirmed(
                                booking_id,
                                desired_date,
                                booked_time,
                                contact_name,
                                contact_phone,
                                time_cell
                            )

                            print(f"{Fore.CYAN}$ cancel existing booking...\n")
                            cancel_booking(correct_booking)

                            print(f"{Fore.CYAN}$ confirming new booking"
                                  f" to the user...\n")
                            confirm_to_user(correct_booking)

                            back_to_menu()
                        elif change_contact == "n":
                            clear_screen()
                            print(
                                "$ OK, as you are not looking"
                                " to change any details,")
                            print(
                                "$ we will bring you back to the main menu.\n")
                            main_menu()
                        elif change_contact == "r":
                            clear_screen()
                            print(
                                "$ OK, as you are not looking"
                                " to change any details,")
                            print(
                                "$ we will bring you back to the main menu.\n")
                            main_menu()
                        elif change_contact == "":
                            clear_screen()
                            print(f"{Fore.RED}$ Sorry, You did not provide"
                                  f" an answer. Please try again.\n")
                            print("$ Please answer with either Y or N.\n")
                            print("$ Or press 'R' to return"
                                " to the main menu.\n")
                            print(
                                f"\n$ Your booking on "
                                f"{Fore.GREEN}{value_booking_date}")
                            print(
                                f"$ Which was booked at "
                                f"{Fore.GREEN}{value_booking_time}")
                            print(
                                f"$ Was booked for "
                                f"{Fore.GREEN}{value_booking_name}\n")
                        else:
                            print(f"\n$ You answered: "
                                  f"{Fore.MAGENTA}{change_contact}")
                            print(f"{Fore.RED}$ Sorry, we did not recognise"
                                  f" this as a valid answer.")
                            print("$ Please answer with either Y or N.\n")
                            print("$ Or press 'R' to return"
                                  " to the main menu.\n")
                            print(
                                f"\n$ Your booking on "
                                f"{Fore.GREEN}{value_booking_date}")
                            print(
                                f"$ Which was booked at "
                                f"{Fore.GREEN}{value_booking_time}")
                            print(
                                f"$ Was booked for "
                                f"{Fore.GREEN}{value_booking_name}\n")
                elif change_time == "r":
                    clear_screen()
                    print("$ Editing your booking has been cancelled.")
                    print(f"{Fore.CYAN}$ Bringing you back to the main menu.\n")
                    main_menu()
                elif change_time == "":
                    print(f"{Fore.RED}$ Sorry, You did not provide"
                          f" an answer. Please try again.\n")
                    print("$ Please answer with either Y or N.\n")
                    print("$ Or press 'R' to return"
                          " to the main menu.\n")
                    print(
                        f"\n$ Your booking on "
                        f"{Fore.GREEN}{value_booking_date}")
                    print(
                        f"$ Which was booked at "
                        f"{Fore.GREEN}{value_booking_time}")
                    print(
                        f"$ Was booked for "
                        f"{Fore.GREEN}{value_booking_name}\n")

                else:
                    clear_screen()
                    print(
                        f"\n$ You answered: {Fore.MAGENTA}{change_time}")
                    print(
                        f"{Fore.RED}$ Sorry, it is not clear what you mean.")
                    print("$ Please answer with either Y or N.\n")
                    print("$ Or press 'R' to return"
                          " to the main menu.\n")
                    print(
                        f"\n$ Your booking on "
                        f"{Fore.GREEN}{value_booking_date}")
                    print(
                        f"$ Which was booked at "
                        f"{Fore.GREEN}{value_booking_time}")
                    print(
                        f"$ Was booked for "
                        f"{Fore.GREEN}{value_booking_name}\n")

        elif change_date == "c":
            print(
                "\n$ Are you sure you want to cancel the following booking?")
            print(
                f"$ {value_booking_date} at {value_booking_time}.\n")

            confirm_cancellation = input(f"{Style.BRIGHT}$ Answer (y/n): ")
            confirm_cancellation = confirm_cancellation.strip().lower()

            if confirm_cancellation == "y":
                clear_screen()
                print(f"{Fore.CYAN}\n$ cancelling your booking now...\n")
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
                print(f"{Fore.RED}$ Sorry, you did not provide"
                      f" an answer. Please try again.\n")
                print("$ Would you like to cancel your booking? (y/n): ")

        elif change_date == "r":
            clear_screen()
            print("$ Editing your booking has been cancelled.")
            print(f"{Fore.CYAN}$ Bringing you back to the main menu.\n")
            main_menu()
        elif change_date == "":
            clear_screen()
            print(f"{Fore.RED}$ Sorry, you did not provide"
                  f" an answer. Please try again.\n")
            print("$ Please answer with either Y or N.\n")
            print("$ Or press 'R' to return to the main menu.\n")
            print(f"$ Your booking on {Fore.GREEN}{value_booking_date}")
            print(f"$ Which was booked at {Fore.GREEN}{value_booking_time}")
            print(f"$ Was booked for {Fore.GREEN}{value_booking_name}\n")
        else:
            clear_screen()
            print(f"\n$ You answered: {Fore.MAGENTA}{change_date}")
            print(f"{Fore.RED}$ Sorry, we did not recognise"
                  f" this as a valid answer")
            print("$ Please answer with either Y or N.\n")
            print("$ Or press 'R' to return to the main menu.\n")
            print(f"$ Your booking on {Fore.GREEN}{value_booking_date}")
            print(f"$ Which was booked at {Fore.GREEN}{value_booking_time}")
            print(f"$ Was booked for {Fore.GREEN}{value_booking_name}\n")


def cancel_booking(correct_booking):
    """
    Find a booking based off the booking_id. confirm what
    of the original booking needs to be edited. Confirm
    availability to edit. Make new booking with a new
    booking ID and booking data. Reinstate the original booking.
    """
    confirmed_bookings = SHEET.worksheet("confirmed_bookings")

    print(f"{Fore.CYAN}$ finding your old appointment...\n")

    find_old_id = confirmed_bookings.findall(
        str(correct_booking[0]), in_column=1)

    booking_row = find_old_id[0].row
    # print(f"$ Booking row to be updated: {booking_row}")

    confirmation_cell = "G" + str(booking_row)

    print(f"{Fore.CYAN}$ Cancelling your old appointment...\n")
    # cancel_booking
    SHEET.worksheet(
        "confirmed_bookings").update_acell(confirmation_cell, "cancelled")

    print(f"{Fore.CYAN}$ old appointment cancelled\n")

    return correct_booking


def reinstate_booking_slot(correct_booking):
    """
    Receiving the timestamp of an old booking (which
    relates to the timeslot in the Google sheet). Using this
    value to reinstate date and time for future bookings.
    """
    # dates_times worksheet
    SHEET.worksheet("available_dates_times")

    print(f"{Fore.CYAN}reinstating old times...\n")

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

    print(f"{Fore.CYAN}$ confirming booking...\n")

    # confirmed booking sheet
    SHEET.worksheet("confirmed_bookings").get_all_values()

    # print("$ Updating confirmed_bookings worksheet...\n")
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
    print(f"{Fore.CYAN}$ Booking updated successfully\n")

    return booking_id, desired_date, booked_time, contact_name, contact_phone, time_cell # noqa


def back_to_menu():
    """
    Function to bring back the user back to the main menu.
    """

    while True:
        back_to_menu = input(
            f"{Style.BRIGHT}$ Would you like to go back"
            f" to the main menu? y/n: ")
        choice = back_to_menu.strip().lower()

        if choice == "y":
            clear_screen()
            print(f"{Fore.CYAN}$ Bringing you back to the main menu.\n")
            main_menu()
        elif choice == "n":
            clear_screen()
            print(f"{Style.BRIGHT}$ Thank you for visiting Lou's nail studio.")
            print(f"{Style.BRIGHT}$ Have a great day.\n\n")
            quit()
        elif choice == "":
            # clear_screen()
            print(
                "\n$ The answer cannot be empty. Please try again.\n")
            print("$ Answer with either Y or N.")
        else:
            # clear_screen()
            print(
                f"\n$ You entered: {Fore.MAGENTA}{choice}.")
            print(
                f"{Fore.RED}$ Sorry, that is not a valid option.")
            print(
                "$ could you please try again? Please use either Y or N.\n")


def confirm_to_user(booking_details):
    """
    Function that reads back the finalised booking to the user.
    """

    clear_screen()
    print(
        f"{Style.BRIGHT}{Fore.GREEN}$ Thank you for your booking!"
        f" We appreciate your business.\n")
    print(
        "To confirm:")

    print(
        f"{Style.BRIGHT}$ *  "
        f"Your unique booking ID: {Fore.GREEN}{booking_details[0]}")
    print(
        f"{Style.BRIGHT}$ *  "
        f"The date of your booking: {Fore.GREEN}{booking_details[1]}")
    print(
        f"{Style.BRIGHT}$ *  "
        f"Your booking will be at: {Fore.GREEN}{booking_details[2]}")
    print(
        f"{Style.BRIGHT}$ *  "
        f"And your booking is for: {Fore.GREEN}{booking_details[3]}\n")
    print(
        f"{Style.BRIGHT}$ To confirm, We will send you a message on")
    print(
        f"{Style.BRIGHT}$ "
        f"the following number: {Fore.GREEN}{booking_details[4]}\n")

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
    print(f"{Style.BRIGHT}{Fore.YELLOW}$*** Book your next appointment ***\n")
    print(
        "$ Booking a nail appointment is quick and takes a few easy steps.")
    print(
        "$ First provide the desired date using the format: (YYYY/MM/DD).")
    print(
        "$ If that date is available, choose from the available time slots.")
    print("$ Monday to Friday, mornings appointments only.\n")
    print(
        "$ Or press 'R' if you want to return to the main menu.\n")

    SHEET.worksheet("available_dates_times")
    date_check = date_choice()

    time_cell_check = get_date_cell(date_check[0])

    time_cell = get_time_cell(time_cell_check)

    desired_date = date_check[1]

    booked_time = SHEET.worksheet(
        "available_dates_times").acell(f"{time_cell}").value

    # The get_time_cell function provides a confirmmation of the chosen time.
    print(
        f"$ You have chosen {booked_time} as your desired time")
    print(
        f"on the date {desired_date}.\n")

    contact_name = provide_contact_name()
    print(f"{Fore.CYAN}\n$ Contact name has been provided.\n")

    contact_phone = provide_contact_phone()
    print(f"{Fore.CYAN}\n$ Phone number has been provided.\n")

    booking_id = generate_booking_id()
    print(f"{Fore.CYAN}$ Unique booking ID created.\n")

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
    print(f"{Style.BRIGHT}{Fore.YELLOW}$*** Editing an appointment ***\n")
    print(
        "$ Editing a nail appointment is quick and takes a few easy steps.")
    print("$ Remember: Monday to Friday, mornings appointments only.\n")
    print("$ First, let's find your booking.")

    booking_details = find_booking()

    correct_booking = booking_confirmation(booking_details)

    update_booking(correct_booking)


def cancel_appointment():
    """
    one of the three main functions. Function to cancel an existing booking.
    User is asked for a booking ID and a confirmation if the right booking
    is approached. If yes, booking is cancelled and the time reinstated in
    the time overview.
    """
    print(f"{Style.BRIGHT}{Fore.YELLOW}$*** Cancelling an appointment ***\n")
    print(
        "$ Cancelling a nail appointment is quick and takes a few easy steps.")
    print("$ First, let's find your booking.")
    print("$ Or press 'R' to return to the main menu.\n")

    booking_details = find_booking()

    correct_booking = booking_confirmation(booking_details)

    while True:

        print(
            f"{Style.BRIGHT}$ Are you sure you would like to"
            f" cancel the following booking?")
        print(f"$ current booking is on the date {correct_booking[1]}.")
        print(f"$ Time of your booking is {correct_booking[2]}.\n")
        confirm_cancellation = input(f"{Style.BRIGHT}Answer (y/n): ")
        confirm_cancellation = confirm_cancellation.strip().lower()

        if confirm_cancellation == "y":

            cancel_booking(correct_booking)

            reinstate_booking_slot(correct_booking)
            clear_screen()
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
            clear_screen()
            print("$ OK, we will not cancel your appointment.\n")
            print(f"{Fore.CYAN}$ Bringing you back to the main menu.\n")
            main_menu()
        elif confirm_cancellation == "":
            print(f"{Fore.RED}$ Sorr, You did not enter an answer,"
                  f" please answer with y or n.")
            print(
                "$ Or press 'R' to return to the main menu.\n")
        elif confirm_cancellation == "r":
            clear_screen()
            print(
                "$ OK, we will not cancel your appointment.")
            print(f"{Fore.CYAN}$ Bringing you back to the main menu.\n")
            main_menu()
        else:
            print("$ Sorry. We did not get that.")
            print("$ Please ensure that you use the suggested y or n format.")


main_menu()
