'''imports'''
from tabulate import tabulate
from habitClass import Habit
import time

habits = []

def main():
    global habits

    habits = Habit.load_from_database()


    '''infinite main loop'''
    while True:
        print_habit_table()
        print_instructions()
        '''promt user for next action'''
        prompt = input("What do you want to do? ")
        prompt = prompt.lower()

        '''choose to add habit, mark habit as complete, watch habit details or view stats.'''
        check_prompt(prompt)


        '''time delay for design and usex experience purposes'''
        time.sleep(0.5)
        print("returning to main menu...")
        time.sleep(1)

        Habit.save_to_database(habits)



def print_instructions():
    print(
        "Instruction list: \n -For creating a new habit type: new\n -For marking a habit as ready type: mark\n -For seeing habit details type: details\n -For stats type: stats\n -To reload type: reload"
    )

'''to know which function to call after the user input'''
def check_prompt(prompt):
    match prompt:
        case "new":
            add_habit()
        case "mark":
            mark_habit()
        case "details":
            habit_name = input("Type the name of the habit you want to see details of: ")
            habitName = habit_name.lower()
            see_details(habit_name)
        case "stats":
            watch_stats()
        case "reload":
            return
        case other:
            print("Not a valid input")
            prompt = input("What do you want to do? ")
            check_prompt(prompt)
    return

'''printing the main habit table. This is the main menu'''
def print_habit_table():
    table = []
    for habit in habits:
        if habit.timer.time_remaining(habit.due_date) == True:
            habit.timeout()
            Habit.save_to_database(habits)
        if habit.did == False:
            table.append([habit.name, habit.description, habit.periodicity, habit.streak, habit.timer.time_remaining(habit.due_date)])
        else:
            table.append([habit.name, habit.description, habit.periodicity, habit.streak, "habit completed"])
    print("\n\n\n HABITS TABLE")
    print(tabulate(table, headers=["Name", "Description", "Periodicity", "Streak", "Time left"], tablefmt="pretty"))

'''function to ad a habit into the database'''
def add_habit():
    habit = Habit.get()
    habit.original_due_date = habit.due_date
    habits.append(habit)
    print("New habit created!")
    return

'''function to mark a habit as complete'''
def mark_habit():
    habit_name = input("Type the name of the habit you want to mark as complete: ")
    habit_name = habit_name.lower()
    for habit in habits:
        if habit.name == habit_name:
            habit.log()
    return


'''function to see all of the habit information and to be able to edit it'''
def see_details(habit_name):
    for habit in habits:
        if habit.timer.time_remaining(habit.due_date) == True:
            habit.timeout()
            Habit.save_to_database(habits)
        if habit.name == habit_name:
            details = [
                [habit.name, habit.description, habit.periodicity, habit.streak, habit.highest_streak, habit.did, habit.timer.time_remaining(habit.due_date),
                 habit.creation_date, habit.log_num]
            ]
            print(f"\n\n\n   Habit '{habit.name}' details:")
            print(tabulate(details, headers=["Name", "Description", "Periodicity", "Streak", "Highest Streak", "Completed?", "Time Left",
                                              "Creation Date", "Log Number"], tablefmt="pretty"))
            print(" -To delete the current habit, type: 'delete'")
            print(" -To edit the current habit, type: 'edit'")
            print(" -To go back to the main menu, type: 'return'")

            prompt = input("What do you want to do? ")
            if prompt == "delete":
                delete_habit(habit)
            elif prompt == "edit":
                edit_habit(habit)
            elif prompt == "return":
                return
            else:
                print("Not a valid prompt")
                see_details(habit_name)
            return

'''function to delete habit'''
def delete_habit(habit):
    print(f"Your '{habit.name}' habit has been deleted successfully!")
    habits.remove(habit)
    Habit.save_to_database(habits)
    return

'''function to edit habit name, description or periodicity'''
def edit_habit(habit):
    print(" -To edit the name, type: 'name'")
    print(" -To edit the description, type: 'description'")
    print(" -To edit the periodicity, type: 'periodicity'")

    choice = input("Select an option: ")

    match choice:
        case "name":
            new_name = input("New Name: ")
            habit.name = new_name
        case "description":
            new_description = input("New Description: ")
            habit.description = new_description
        case "periodicity":
            new_periodicity = input("New Periodicity: ")
            habit.periodicity = new_periodicity
        case other:
            print("Invalid choice!")
            return
        
    Habit.save_to_database(habits)
    print(f"Your '{habit.name}' habit has been edited successfully!")
    return


'''function to watch general user statistics'''
def watch_stats():
    print("\n\n\n   STATS:\n")
    
    '''find the longest habit streak'''
    longest_streak = max(habit.highest_streak for habit in habits)
    print("Longest Streak:", longest_streak)
    longest_current_streak = max(habit.streak for habit in habits)
    print("Longest current streak:", longest_current_streak)

    '''the habit with the most failed times'''
    worst_habit = max(habits, key=lambda habit: habit.difficulty_count)
    print(f"\nThe habit you've strugled the most with is {worst_habit.name}. Make sure you don't forget to do it!\n")


    '''find the number of habits by periodicity'''
    daily_habits = [habit.name for habit in habits if habit.periodicity == "daily"]
    print("Current daily habits:", daily_habits)
    weekly_habits = [habit.name for habit in habits if habit.periodicity == "weekly"]
    print("Current weekly habits:", weekly_habits)
    monthly_habits = [habit.name for habit in habits if habit.periodicity == "monthly"]
    print("Current monthly habits:", monthly_habits)
    yearly_habits = [habit.name for habit in habits if habit.periodicity == "yearly"]
    print("Current yearly habits:", yearly_habits)

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
                habits.sort(key=lambda x: x.creation_date)
            case "due":
                habits.sort(key=lambda x: x.due_date)
            case "streak":
                habits.sort(key=lambda x: x.streak)
            case other:
                print("Not a valid option")
        return 
    else:
        return


main()
