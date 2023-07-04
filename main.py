'''imports'''
from tabulate import tabulate
from datetime import datetime
from habitClass import Habit
import time
from dateutil.relativedelta import relativedelta

habits = []

def main():
    global habits
    '''create database and table if they don't exist'''
    Habit.createDatabase()  

    habits = Habit.loadFromDatabase()


    '''infinite main loop'''
    while True:
        printHabitTable()
        printInstructions()
        '''promt user for next action'''
        prompt = input("What do you want to do? ")
        prompt = prompt.lower()

        '''choose to add habit, mark habit as complete, watch habit details or view stats.'''
        checkPrompt(prompt)


        '''time delay for design and usex experience purposes'''
        time.sleep(0.5)
        print("returning to main menu...")
        time.sleep(1)

        Habit.saveToDatabase(habits)



def printInstructions():
    print(
        "Instruction list: \n -For creating a new habit type: new\n -For marking a habit as ready type: mark\n -For seeing habit details type: details\n -For stats type: stats\n -To reload type: reload"
    )

'''to know which function to call after the user input'''
def checkPrompt(prompt):
    match prompt:
        case "new":
            addHabit()
        case "mark":
            markHabit()
        case "details":
            habitName = input("Type the name of the habit you want to see details of: ")
            habitName = habitName.lower()
            seeDetails(habitName)
        case "stats":
            watchStats()
        case "reload":
            return
        case other:
            print("Not a valid input")
            prompt = input("What do you want to do? ")
            checkPrompt(prompt)
    return

'''printing the main habit table. This is the main menu'''
def printHabitTable():
    table = []
    for habit in habits:
        if habit.timer.timeRemaining(habit.dueDate) == True:
            habit.timeout()
            Habit.saveToDatabase(habits)
        if habit.did == False:
            table.append([habit.name, habit.description, habit.periodicity, habit.streak, habit.timer.timeRemaining(habit.dueDate)])
        else:
            table.append([habit.name, habit.description, habit.periodicity, habit.streak, "habit completed"])
    print("\n\n\n HABITS TABLE")
    print(tabulate(table, headers=["Name", "Description", "Periodicity", "Streak", "Time left"], tablefmt="pretty"))

'''function to ad a habit into the database'''
def addHabit():
    habit = Habit.get()
    habit.originalDueDate = habit.dueDate
    habits.append(habit)
    print("New habit created!")
    return

'''function to mark a habit as complete'''
def markHabit():
    habitName = input("Type the name of the habit you want to mark as complete: ")
    habitName = habitName.lower()
    for habit in habits:
        if habit.name == habitName:
            habit.log()
    return


'''function to see all of the habit information and to be able to edit it'''
def seeDetails(habitName):
    for habit in habits:
        if habit.timer.timeRemaining(habit.dueDate) == True:
            habit.timeout()
            Habit.saveToDatabase(habits)
        if habit.name == habitName:
            details = [
                [habit.name, habit.description, habit.periodicity, habit.streak, habit.highestStreak, habit.did, habit.timer.timeRemaining(habit.dueDate),
                 habit.creationDate, habit.logNum]
            ]
            print(f"\n\n\n   Habit '{habit.name}' details:")
            print(tabulate(details, headers=["Name", "Description", "Periodicity", "Streak", "Highest Streak", "Completed?", "Time Left",
                                              "Creation Date", "Log Number"], tablefmt="pretty"))
            print(" -To delete the current habit, type: 'delete'")
            print(" -To edit the current habit, type: 'edit'")
            print(" -To go back to the main menu, type: 'return'")

            prompt = input("What do you want to do? ")
            if prompt == "delete":
                deleteHabit(habit)
            elif prompt == "edit":
                editHabit(habit)
            elif prompt == "return":
                return
            else:
                print("Not a valid prompt")
                seeDetails(habitName)
            return

'''function to delete habit'''
def deleteHabit(habit):
    print(f"Your '{habit.name}' habit has been deleted successfully!")
    habits.remove(habit)
    Habit.saveToDatabase(habits)
    return

'''function to edit habit name, description or periodicity'''
def editHabit(habit):
    print(" -To edit the name, type: 'name'")
    print(" -To edit the description, type: 'description'")
    print(" -To edit the periodicity, type: 'periodicity'")

    choice = input("Select an option: ")

    match choice:
        case "name":
            newName = input("New Name: ")
            habit.name = newName
        case "description":
            newDescription = input("New Description: ")
            habit.description = newDescription
        case "periodicity":
            newPeriodicity = input("New Periodicity: ")
            habit.periodicity = newPeriodicity
        case other:
            print("Invalid choice!")
            return
        
    Habit.saveToDatabase(habits)
    print(f"Your '{habit.name}' habit has been edited successfully!")
    return


'''function to watch general user statistics'''
def watchStats():
    print("\n\n\n   STATS:\n")
    
    '''find the longest habit streak'''
    longestStreak = max(habit.highestStreak for habit in habits)
    print("Longest Streak:", longestStreak)
    longestCurrentStreak = max(habit.streak for habit in habits)
    print("Longest current streak:", longestCurrentStreak)

    '''the habit with the most failed times'''
    worstHabit = max(habits, key=lambda habit: habit.difficultyCount)
    print(f"\nThe habit you've strugled the most with is {worstHabit.name}. Make sure you don't forget to do it!\n")


    '''find the number of habits by periodicity'''
    dailyHabits = [habit.name for habit in habits if habit.periodicity == "daily"]
    print("Current daily habits:", dailyHabits)
    weeklyHabits = [habit.name for habit in habits if habit.periodicity == "weekly"]
    print("Current weekly habits:", weeklyHabits)
    monthlyHabits = [habit.name for habit in habits if habit.periodicity == "monthly"]
    print("Current monthly habits:", monthlyHabits)
    yearlyHabits = [habit.name for habit in habits if habit.periodicity == "yearly"]
    print("Current yearly habits:", yearlyHabits)

    '''to change the order habits are displayed in the main menu'''
    time.sleep(1)
    want = input("\nDo you want to rearrange how the habits are displayed? (y/n): ")
    if want == "y":
        print(" -To arrange habits by periodicity type: periodicity")
        print(" -To arrange habits by date of creation type: date")
        print(" -To arrange habits by due-date type: due")
        print(" -To arrange habits by streak type: streak")
        arrange = input("How do you want to arrange the habits? ")
        match arrange:
            case "periodicity":
                habits.sort(key=lambda x: x.periodicity)
            case "date":
                habits.sort(key=lambda x: x.creationDate)
            case "due":
                habits.sort(key=lambda x: x.dueDate)
            case "streak":
                habits.sort(key=lambda x: x.streak)
            case other:
                print("Not a valid option")
        return 
    else:
        return


main()
