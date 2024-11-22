![CI logo](https://codeinstitute.s3.amazonaws.com/fullstack/ci_logo_small.png)

Welcome,

This is the Code Institute student template for deploying your third portfolio project, the Python command-line project. The last update to this file was: **May 14, 2024**

## Reminders

- Your code must be placed in the `run.py` file
- Your dependencies must be placed in the `requirements.txt` file
- Do not edit any of the other files or your code may not deploy properly

## Creating the Heroku app

When you create the app, you will need to add two buildpacks from the _Settings_ tab. The ordering is as follows:

1. `heroku/python`
2. `heroku/nodejs`

You must then create a _Config Var_ called `PORT`. Set this to `8000`

If you have credentials, such as in the Love Sandwiches project, you must create another _Config Var_ called `CREDS` and paste the JSON into the value field.

Connect your GitHub repository and deploy as normal.

## Constraints

The deployment terminal is set to 80 columns by 24 rows. That means that each line of text needs to be 80 characters or less otherwise it will be wrapped onto a second line.

---

Happy coding!
#############################################################################################

# Lou's nail studio - about the page
This project is a simple booking system for a fictional nail studio called "Lou's nail studio." The aim of the system is to allow for bookings to be made, existing bookings being edited and existing bookings being cancelled. All tracked and updated in a Google Sheet database. The tool and database is accessable online, so can be viewed when on the move and is not bound to a specific machine. By using Google sheets, the user will have several options to extend it's functionalities. For example linking it to their Gmail or Google calendar.

The project is hosted on Github and deployed on Heroku for easy access, sharing an collaboration. 

[Live site](https://lous-nailstudio-booking-system-72021c02bd05.herokuapp.com/)

[Repository link](https://github.com/MJRidder/nailstudio_booking)

![Am I responsive? view](./Readme/Am-I-Responsive-visual.png)

## Table of Contents

1. [User Experience](#user_experience)
2. [Design](#design)
3. [Features](#features)
4. [Technologies Used](#technologies_used)
5. [Creating a Google Spreadsheet and Integrating it using API](#creating_a_google_spreadsheet_and_integrating_it_using_api)
6. [Google Sheets](#google_sheets)
7. [Deployment](#deployment)
8. [Browser Capability](#browser_capability)
9. [Testing](#testing)
10. [Bugs](#bugs)
11. [Credits](#credits)

## User experience

### Business goals
* Have an online tool that allows for:
    - business to be generated (bookings) at any given time of the day
    - existing bookings to be updated as per clients preference
    - tracking of all upcoming bookings (dates & times)
    - an overview of all cancelled bookings
    - integration with a back end database (Google Sheets)
* Clients to book/edit/cancel bookings without human interaction
* Have a tool that integrates easily with a front-end website
* Have a tool that can be used in collaboration with other functions (email/calendar planning)

### User goals
* Quick and easy booking of nail appointments
* Quick and easy editing/cancelling of existing bookings
* Quick and easy way to check availability for a nail appointment
* Ability to make a booking at any given moment in time

## Design
The design has purposefully kept simple and to the point. Not asking the user for extensive answers, but navigating through the system by answering with 2-4 option buttons (letter or times). Formatting of how an answer is expected is clarified before each question. It is also repeated where this is needed.

Every step in the process has been reviewed for the users best experience. Ensuring they have options to go back to the main menu with every question. Giving them the ability to go back and not get stuck in the system.

Flowchart of making a booking 
![making a booking ](./Readme//flowchart-make-a-booking.png)

Flowchart of editing a booking
![editing a booking](./Readme/flowchart-edit-a-booking.png)

Flowchart of canceling a booking
![canceling a booking](./Readme/flowchart-cancel-a-booking.png)

There has been made a concideration up front as well as to how the different flowcharts could make use of the same functions to avoid duplication

Alignment of all flowcharts
![Alignment of all flowcharts](./Readme/flowchart-all-combined.png)

Every line of printed text is preceeded with the " $ " symbol to help destinguish the text from the side of the screen. The " $ " was used to copy the formatting of the love-sandwitches example from the CI course.

### User stories
This Nail studio booking system has been developed to allow for clients of "Lou's nail studio" to check for availability, review their own bookings and to make/edit bookings at any point in time that they desire. Allowing for flexibility and on online option for such adjustments. Which is especially relevant today where people are less likely to pick up the phone. Or at the very least, less enjoy doing so.

## Features

### Welcome message + navigation menu
The user is welcomed to the booking system with a simple message. Providing information about Lou's Nail studio, specifically about it's opening days. It also provides the user with the initial options. Keeping it clean and tight as this system is only used to navigate bookings. It is expected that further information is presented on the front-end webiste.

Initial menu + navigation (SCREENSHOT TO BE ADDED)
![Alignment of all flowcharts](./Readme/flowchart-all-combined.png)

### Make a booking
It is quick and easy to make a booking through this system. This feature takes you through the process, step-for-step.

Make a booking feature (SCREENSHOTS TO BE ADDED)
![Alignment of all flowcharts](./Readme/flowchart-all-combined.png)

User facing:
* 1) First helping you by picking a date,
* 2) Checking it's availability (moves to the next step if it is, otherwise brings you back to step 1.)
* 3) Gives the available times on the desired date
* 4) Asks user to provide their first and last name
* 5) Asks user to provide their contact phone number
* 6) Creates a unique booking ID for the user to keep in case of questions or desire to edit at a later stage
* 7) Confirms all booking details back to the user

Back-end facing:
While the user is making it's booking, the following steps are taken when a booking is comopleted
* 1) All booking data is added to a confirmed booking sheet: 
    - date
    - time
    - name
    - phone number
    - timestamp
    - booking confirmation
* 2) Chosen date & time are removed from the available dates & times sheet

This results in the chosen time no longer being available for the next users.

### Edit a booking
Allows the user to edit existing bookings. Users can edit the date, time and contact details of their booking. The steps are similar to making a booking, but are preceeded by a Booking ID check to ensure that the original booking is cancelled. All edits will then be saved for the user with a new booking number. 

By providing a new booking ID, there is no confusion on what booking is the most up-to-date. Old booking ID and their bookings are still viewable by Lou's nail studio however. This way they can track past bookings.

Edit a booking feature (SCREENSHOT TO BE ADDED)
![Alignment of all flowcharts](./Readme/flowchart-all-combined.png)

### Cancel a booking
This feature is purposefully also similar to the booking and editing feature. Asking the user for their booking ID, confirming that the right booking is being reviewed, before asking the user if sure that they are looking to cancel the booking. All with the intend of the user in mind. Avoiding cancellations to happen by accident.

Cancel a booking feature (SCREENSHOT TO BE ADDED)
![Alignment of all flowcharts](./Readme/flowchart-all-combined.png)

### Booking ID
Each booking and each followed iteration will receive a unique booking number. This booking number is unique generated with each completed action (booking or editing) by the user and is created by looking at the highest (last) booking number and adding 1. 

Booking ID's allow for the user to always have a clear reference for their booking when they reach out to Lou's nail studio. This to avoid confusion and to ensure any edits made, are made to the correct booking.

The booking ID's allow also for Lou's nail studio, to track their users activity and when a client reaches out to them (online or over the phone) to ensure that the correct booking is reviewed. This to avoid mistakes and confusion.

### Exit and Return options
Each page also has Exit or Return options. Users can make mistakes, or simply change their minds. These menu options allow users to step back from their current path in the navigation. Without having to quit (or 'kill') the booking system all together.

exit or cancel options feature (SCREENSHOTS TO BE ADDED)
![Alignment of all flowcharts](./Readme/flowchart-all-combined.png)

### Google sheets database
(more on this later) The G suite database allows for the tracking of appointments. Also where days are removed or added back in again manually, the booking system takes this into account automatically.

## Creating a Google Spreadsheet and Integrating it using API

### Creating the Google Spreadsheet:

1. Log in: (or sign up) to your Google Account.
2. Access Google Spreadsheet: Navigate to Google Sheets.
3. Create a new spreadsheet: and give it a descriptive name, e.g., 'flexibook' like the name of the application.
4. Rename the worksheet: (e.g., 'confirmation') and add, if necessary, additional worksheets.
5. Add headings: (Confirmation code, day, time and name).

### Setting up the APIs:

1. **Navigate to the Google Cloud Platform:**
   - Create a new project by clicking the button "Select a project" and then selecting "New project."
   - Give the project a descriptive and meaningful name, e.g., flexibook, and click on the "CREATE" button.
   - In the Notifications pop-up, click on "SELECT PROJECT."
   
2. **On the project page:**
   - Go to the menu (click the burger icon in the top-left corner of the page), click on "APIs and services," and then select "Library."
   - In the search bar, search for "Google Drive" and enable it.
   - Click on "Credentials" in the sidebar and then select "+ CREATE CREDENTIALS > Help me choose."
   
3. **Credential setup:**
   - Select "Google Drive API" and "Application Data" in the Credential Type section and click on the "NEXT" button.
   - Enter a custom service name and click the "CREATE AND CONTINUE" button.
   - Select "Editor" as the role in the Quick access section Basic and press the "CONTINUE" button.
   - Leave the form fields in the next question blank and click on "DONE."
   - Click on the email from the newly created Service Account.
   - Click on the Tab "KEYS" and then select "Create new key" from the dropdown menu of the "ADD KEY" button.
   - Keep the key type as JSON and click the "CREATE" button. Download the JSON file to your local machine.

4. **Enable Google Sheets API:**
   - Go back to the library again, search for "Google Sheets API," and enable it.

5. **Drag and drop credential-json file:**
   - Drag and drop the credential JSON file (downloaded after step 3) into the workspace and rename it as "creds.json" for simplicity.

6. **Sharing the Spreadsheet:**
   - Open the JSON file in the workspace, copy the client email (without the quotes).
   - Go to the created Google Spreadsheet, click the "Share" button.
   - Paste in the email address (from step 6), select "Editor," and then click "Share."

### Connecting the APIs to Python:

1. **Install dependencies:**
   - In the workspace terminal, run the command 'pip3 install gspread google-auth'.
   
2. **Import libraries:**
   - Import the gspread library at the top of the Python file in the workspace.
   - Import the Credentials from the Google Auth Account (google.oauth2.service_account).
   
3. **Set SCOPE and create CREDS:**
   - Set the SCOPE, listing the APIs the program needs to access to run.
   - Create CREDS using the gspread authorise method to access the created worksheet data.

**Note:** Ensure the JSON file is never committed to GitHub as it contains sensitive information. Create a .gitignore file in the workspace and add the name of the JSON file to it.

## Google Sheets

[Link to the Google sheets database](https://docs.google.com/spreadsheets/d/1gYfWLpP4dIJ-gYyem_8ing6lhQcKknn0aqblNaNz888/edit?gid=0#gid=0)

Google sheets is used to act as a database for "Lou's Nail Studio" booking system. It provides the following benefits:

* 1) Tracking of available dates & times
* 2) Overview of confirmed bookings
* 3) Automatic updating of dates/times when they are booked/edited/cancelled
* 4) Provides an overview of clients and their contact details
* 5) Historical overview of bookings (and cancellations)

I used the CI course example "love-sandwiches" asgu



## Future features

### Add colors and other formatting
Adding color and additional formatting to the booking system will help with making it easer to read and with that, navigate.

### Add specific nail services to the booking system
Depending on the available nails services (these are not clear at this point), specific nail services could be added to the booking system. Making it possible for users to book a specific service. This will help with preparation and planning. However as it is currently unclear what services will be proviced. The booking system itself is now focusing on blocking of time slots.

### Linking Google sheets database with Gmail
Be able to auto email clients from the system.

### Linking Google sheets database with Google calendar
Auto add/remove and update bookings in Google calendar based on client input in the system,

### Linking Google sheets database with Analytics
Track which days/times (in future: services) are most popular, should the offer of days be expanded?

### Saving Google sheets data separately to create user profiles
With the information present in Google sheets, user profiles and history can be build.

## Testing * TO BE UPDATED
Testing of the booking system has been an ongoing process. It has also been extensive. Expanding features with multiple choice options and linking features at different stages of the process. Initial testing took place in Gitpod. When the MVP was ready however, testing in Gitpod was combined with testing in Heroku to ensure the actual user experience was taken into account when making adjustments.

### Python validator test
The Python code itself has been reviewed with the "flake8" command in Gitpod. Removing all errors shown in the "run.py" file. Errors however in other files (e.g. .vscode) have gone untouched as these were part of the Code Institute template and were not used/touched by me in the process of building the booking system.

Next to "flake8" the code was also checked with the suggested CI Python Linter. On both tools the initial issues that were shown were about:
    - Using too many charactars in a line (79+), which I then adjusted
    - Unused variables (which I have removed, adjusted or hashtagged out)
    - Whitelines (which were removed)
    - Incorrect indentations (which were updated)

Flake8 review
[flake8](./Readme/flake8-python-linter.png)

CI Python Linter
[CI Python Linter](./Readme/CI-python-linter.png)

CI Python Linter in Gitpod Code
[CI Python Linter code](./Readme//CI-python-linter-error-code.png)

The two lines of code in the error messages have not been touched (# noqa) as they are an essential part of that function.

## (Un)fixed bugs

### bug 1


## Deployment

The site was deployed to GitHub Pages. The steps to deploy are as follows:

- In the [GitHub repository](https://github.com/MJRidder/nailstudio_booking), navigate to the Settings tab
- From the source section drop-down menu, select the Main Branch, then click "Save".
- The page will be automatically refreshed with a detailed ribbon display to indicate the successful deployment.

The live link on Heroku can be found [here](https://lous-nailstudio-booking-system-72021c02bd05.herokuapp.com/)

### Local Deployment
This project can be cloned or forked in order to make a local copy on your own system.

### Cloning
You can clone the repository by following these steps:

1. Go to the [GitHub repository](https://github.com/MJRidder/nailstudio_booking)
2. Locate the Code button above the list of files and click it
3. Select if you prefer to clone using HTTPS, SSH, or GitHub CLI and click the copy button to copy the URL to your clipboard
4. Open Git Bash or Terminal
5. Change the current working directory to the one where you want the cloned directory
6. In your IDE Terminal, type the following command to clone my repository:
- git clone https://github.com/MJRidder/nailstudio_booking
7. Press Enter to create your local clone.
Alternatively, if using Gitpod, you can click below to create your own workspace using this repository.

Please note that in order to directly open the project in Gitpod, you need to have the browser extension installed. A tutorial on how to do that can be found [here](https://www.gitpod.io/docs/configure/user-settings/browser-extension).

### Forking
By forking the GitHub Repository, we make a copy of the original repository on our GitHub account to view and/or make changes without affecting the original owner's repository. You can fork this repository by using the following steps:

1. Log in to GitHub and locate the [GitHub repository](https://github.com/MJRidder/nailstudio_booking)
2. At the top of the Repository (not top of page) just above the "Settings" Button on the menu, locate the "Fork" Button.
3. Once clicked, you should now have a copy of the original repository in your own GitHub account!

## Heroku deployment

1. Go to the Heroku dashboard.
2. Click on the "Create new app" button.
3. Name the app uniquely (e.g., "love-sandwiches").
4. Select the appropriate region.
5. Click on "Create app".
6. Navigate to the "Settings" tab.
7. Under "Config Vars", add a new config var with the key "CREDS" and copy the contents of the creds.json file from your workspace into the value field.
8. Click on "Add".
9. Add two buildpacks: Python and node.js. Ensure Python is on top.
10. Navigate to the "Deploy" section.
11. Choose the deployment method (e.g., Github).
12. Connect to your Github repository.
13. Select the repository name.
14. Click on "Connect".
15. Choose either automatic deploys or manual deploys.
16. If manual, select the branch to deploy.
17. Wait for the deployment process to complete.
18. Check the deployment logs for any errors.
19. Test the deployed application to ensure it works correctly.
20. Verify functionality with both correct and incorrect data inputs.

Project deployed!

## Credits

### Tools Used

| Source | Location | Notes |
| --- | --- | --- |
| [Github](https://github.com/j) | Site creation | Website building |
| [ChatGPT](https://openai.com/index/chatgpt/) | JS/CSS/HTML | Code review/adjustments |

### Resources Used

| Source | Location | Notes |
| --- | --- | --- |
| [W3schools](https://www.youtube.com/watch?v=riDzcEQbX6k) | Quizprep | HTML/CSS coding |

Special shout outs:
1. First to my mentor [Sheryl Goldberg](https://github.com/sherylg343) 

### Content/Media Used

| Source | Location | Notes |
| --- | --- | --- |
| [Variety](https://variety.com/) | Quizpage | Images |
