# HABIT TRACKER OOP PROJECT

To run the code make sure the files are in the same directory together and just run the "main.py" file using the code "python main.py" in your termina window, first making sure you're in the correct directory. Everything will link together. The user interacts with the proagram via the terminal window. No code knowledge is needed; everything is explained with simple instructions. 
The database has already 5 habits with sample data for you to be able to test the program and see the functionality.  
For testing, there is also another periodicity (not written in the instructions) called "minute" which lasts only a minute, to be able to test the code faster and easier. 
If you want to use it, when the program asks you for a periodicity type: minute.


## INSTRUCTIONS TO OPEN

- Have a code editor like Visual Studio Code downloaded.
- Download the files from the github repository via this link: https://github.com/markslvk/habitTrackerAppPortfolio
- Make sure you're inside the folder where the files are. 
- Once inside the folder, run "pip install -r requirements.txt". You'll download all the needed packages to run the program.
- Once done, run "python main.py". 
- Once you run the file, the program will run with 5 habits already preinserted into the table for testing. Feel free to delete them if you want. 


## TESTING MODULE

There is a testing module. To run it type "python tests.py". It will run a few tests and help you determine if there is an error in the code. 


## FOR ADDITIONAL HELP

There are also docstrings all throughout the code, so if needed type __doc__ attribute or
help() function.

The database used is MySQL and is hosted online via the page "freeMySQLhosting.net". It may take a bit of time to load the program because of it. 
Here is relevant information from the database in case it is needed:
- host='aws.connect.psdb.cloud',
- user='sln71aslkpx045wosix0',
- password='pscale_pw_fmk299AAfR0dL6fV5OWjIxVakaBCcZFX4L0v0soZ6o9',
- database='habittrackerdb'



## It is divided into three documents:
- main.py
- habitClass.py
- timerClass.py



## main.py
Here is the main part of the code. It creates everuthing that the user will interact with. It's function is the infinite "while True" loop that displays a table with the current habits and prompts the user for different things, such as:
- Add new habit
- Mark habit as done
- View habit details
- View habits statistics
- Reload table
These options make the user be able to interact with the data. It used the "tabulate" module to display the information in a more pleasing way so that the user can more easily guide him or herself through using the app. 
### Inside the view habit details the user can:
- Simply view the data more in depth
- Edit a habit's name, description or periodicity
- Delete the habit and all its data



## habitClass.py
This document handles the logic of the entire operations. From creating the habits, changing them, adding them and modifiying the database, and the internal logic. The habit class has the following instances:
- id: which is only for the database
- name: which is given by the user
- periodicity: which is given by the user
- description: which is given by the user
- creationDate: which is set when teh habit is created
- streak: which updates every time the user marks a habit as complete or the time for completion is done.
- highestStreak: it stores the highest streak the user has reached with that habit
- logNum: saves the number of how many times the user has completed that habit
- checkLog: saves, in the form of a list, the dates in which the habit was completed
- timeDone: a boolean variable that indicates if the time is done for this period.
- did: a boolean variable that indicates if the user has done the habit in this current period.
- dueDate: a date variable that indicates when the next habit period finishes
- difficultyCount: a counter of how many times the user has failed to do the habit


## timerClass.py
This last file handles setting the due-date for each habit, resetting it when it is done, and making the calculations of how long until the due-date. The calculations for restingTime are not stored in the database, but are instead calculated when the method is called. 


For any doubts, comments or improvements please contact me via email: 
markslvk@gmail.com

Thank you for reading this and enjoy the program!


Mark Slovik Braun. 
04/07/2023