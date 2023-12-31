'''imports'''
from datetime import date, datetime
from timerClass import Timer
import time
import mysql.connector
import mysql.connector.pooling
from dotenv import load_dotenv
import os
import re


'''main Habit class'''
class Habit:

    '''environment variables for DB'''
    load_dotenv()
    db_user = os.getenv("HABITDB_USER")
    db_password = os.getenv("HABITDB_PASS")

    conn = None  

    '''initializing the habit object when created'''
    def __init__(self, name, periodicity, description=None, due_date=None):

        self.conn = None
        self.cursor = None

        '''checking for that none of the obligatory fields is empty:'''
        if not name or not periodicity:
            raise ValueError("Missing info.")

        '''setting all instances given by user'''
        self.name = name
        self.periodicity = periodicity
        self.description = description

        '''setting automatic instances'''
        self.id = None  
        self.creation_date = date.today()
        self.streak = 0
        self.log_num = 0
        self.check_log = []
        self.time_done = False
        self.did = False
        self.timer = Timer(self.periodicity)
        self.original_due_date = due_date
        self.highest_streak = 0
        self.difficulty_count = 0

        '''setting timer'''
        if due_date:
            self.due_date = due_date
        else:
            self.due_date = self.timer.time_lapse()

        '''create a new database connection'''
        self.conn = mysql.connector.connect(
            host='aws.connect.psdb.cloud',
            user=Habit.db_user,
            password=Habit.db_password,
            database='habittrackerdb'
        )

        '''create db cursor'''
        self.cursor = self.conn.cursor()

        '''insert habit data into the database'''
        self.insert_into_db()

    
    '''for when a new habit is created, this method inserts it into the database.
    It first checks there aren't any habits called the same'''
    def insert_into_db(self):
        self.cursor.execute('SELECT * FROM habits WHERE name = %s', (self.name,))
        existing_habit = self.cursor.fetchone()
        if existing_habit is None:
            '''only set the creationDate for new habits'''
            if not self.did:  
                self.creation_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            if self.original_due_date:
                '''use the originalDueDate if available'''
                self.due_date = self.original_due_date.strftime('%Y-%m-%d %H:%M:%S')
            elif not self.due_date:
                '''set the dueDate to the current time'''
                self.due_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            self.cursor.execute('''
                INSERT INTO habits (
                    name, 
                    periodicity, 
                    description, 
                    creation_date, 
                    streak, 
                    highest_streak,
                    log_num, 
                    check_log, 
                    time_done, 
                    did, 
                    due_date,
                    difficulty_count)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', (
                self.name, self.periodicity, self.description, self.creation_date, self.streak, self.highest_streak,
                self.log_num, ' | '.join(map(str, self.check_log)), int(self.time_done), int(self.did),
                self.due_date, self.difficulty_count
            ))

        self.id = self.cursor.lastrowid
        self.conn.commit()
        self.conn.close()
        self.cursor.close()


    '''class method get to be able to create a new object by prompting the user. 
    This is called in the addHabit function in the main.py file'''
    @classmethod
    def get(cls):
        name = input("Name: ")
        print("Periodicity options: daily, weekly, monthly, yearly.")
        periodicity = input("Periodicity: ")
        description = input("Description: ")

        '''create a new database connection'''
        conn = mysql.connector.connect(
            host='aws.connect.psdb.cloud',
            user=Habit.db_user,
            password=Habit.db_password,
            database='habittrackerdb'
        )
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM habits WHERE name = %s", (name,))
        row = cursor.fetchall()

        cursor.close()
        conn.close()

        if row:
            '''habit already exists, retrieve the streak count'''
            streak = row[0][5]
        else:
            streak = 0

        '''create the habit instance'''
        habit = cls(name, periodicity, description)
        habit.streak = streak
        return habit
    

    @classmethod
    def fetch_all(cls):
        return cls.load_from_database()
    
    
    '''logging activity. This method is called when the user selects to mark a habit.'''
    def log(self):

        '''connect to database'''
        conn = mysql.connector.connect(
            host='aws.connect.psdb.cloud',
            user=Habit.db_user,
            password=Habit.db_password,
            database='habittrackerdb'
        )
        cursor = conn.cursor()

        self.did = True
        self.log_num += 1
        self.check_log.append(date.today())
        self.streak, self.highest_streak = self.update_streak()

        '''edit database'''
        cursor.execute(
            """
            UPDATE habits SET log_num = %s, check_log = %s, streak = %s, highest_streak = %s, did = %s, due_date = %s, difficulty_count = %s
            WHERE id = %s
            """,
            (
                self.log_num,
                "|".join(map(str, self.check_log)),
                self.streak,
                self.highest_streak,
                int(self.did),
                self.due_date,
                self.difficulty_count,
                self.id,
            ),
        )
        conn.commit()
        cursor.close()
        conn.close()

    
    '''update streak for when a habit is marked or when the periodicity is done'''
    def update_streak(self):
        '''checks if the habit is completed'''
        if self.did == True:
            self.streak += 1
            print(f"Congrats! Your streak for {self.name} is now {self.streak}")
            if self.streak > self.highest_streak:
                self.highest_streak = self.streak
        else: 
            '''checks if the habit wasn't complete by the time the periodicity was done'''
            self.streak = 0
            print(f"😢, you just lost your {self.name} streak. Remember to keep doing your habits!")
            self.difficulty_count += 1
            time.sleep(1)
        return self.streak, self.highest_streak

    
    '''getter for feature'''
    @property
    def periodicity(self):
        return self._periodicity
    
    '''setter for feature'''
    @periodicity.setter
    def periodicity(self, periodicity):
        if periodicity not in ["minute", "daily", "weekly", "monthly", "yearly"]:
            raise ValueError("Invalid periodicity")
        self._periodicity = periodicity
            

    '''when periodicity is up call update_streak and reset timer and variables.'''
    def timeout(self):
        self.time_done = True
        if self.did == False:
            self.update_streak()
        self.did = False
        self.time_done = False
        self.due_date = self.timer.time_lapse()
        return


#main
def main():
    habit1 = Habit.get()
    print(f"{habit1.creation_date}")
    habit1.log()


if __name__ == "__main__":
    main()


