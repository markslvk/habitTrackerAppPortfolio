'''imports'''
from datetime import date, datetime
from timerClass import Timer
import time
import mysql.connector
import mysql.connector.pooling


'''main Habit class'''
class Habit:

    conn = None  # Class variable to hold the database connection

    '''initializing the habit object when created'''
    def __init__(self, name, periodicity, description=None, dueDate=None):

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
        self.creationDate = date.today()
        self.streak = 0
        self.logNum = 0
        self.checkLog = []
        self.timeDone = False
        self.did = False
        self.timer = Timer(self.periodicity)
        self.originalDueDate = dueDate
        self.highestStreak = 0
        self.difficultyCount = 0

        '''setting timer'''
        if dueDate:
            self.dueDate = datetime
        else:
            self.dueDate = self.timer.timeLapse()

        '''create a new database connection'''
        self.conn = mysql.connector.connect(
            host='sql7.freemysqlhosting.net	',
            user='sql7630486',
            password='eUXLRyhGwG',
            database='sql7630486'
        )

        '''create db cursor'''
        self.cursor = self.conn.cursor()

        '''insert habit data into the database'''
        self.insertIntoDb()

    
    '''this method is called at the beginning of main to see if the db has not been created'''
    @staticmethod
    def createDatabase():
        conn = mysql.connector.connect(
            host='sql7.freemysqlhosting.net	',
            user='sql7630486',
            password='eUXLRyhGwG'
        )

        cursor = conn.cursor()
        cursor.execute('''
            CREATE DATABASE IF NOT EXISTS sql7630486
        ''')
        cursor.close()
        conn.close()

        '''establish the connection to the habits database'''
        conn = mysql.connector.connect(
            host='sql7.freemysqlhosting.net	',
            user='sql7630486',
            password='eUXLRyhGwG',
            database='sql7630486'
        )
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS habits (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                periodicity VARCHAR(10) NOT NULL,
                description TEXT,
                creationDate DATE NOT NULL,
                streak INT NOT NULL,
                highestStreak INT NOT NULL,
                logNum INT NOT NULL,
                checkLog TEXT,
                timeDone TINYINT(1) NOT NULL,
                did TINYINT(1) NOT NULL,
                dueDate DATETIME NOT NULL,
                difficultyCount INT NOT NULL
            )
        ''')
        conn.commit()
        cursor.close()
        conn.close()


    '''this method handles saving every change to the database so that each function 
    or method doesn't have to deal with it. 
    It is called inside the object and outside'''
    @staticmethod
    def saveToDatabase(habits):
        conn = mysql.connector.connect(
            host='sql7.freemysqlhosting.net	',
            user='sql7630486',
            password='eUXLRyhGwG',
            database='sql7630486'
        )
        cursor = conn.cursor()

        '''clear the existing data in the table'''
        cursor.execute("TRUNCATE TABLE habits")

        '''insert the habit data into the database'''
        for habit in habits:
            cursor.execute('''
                INSERT INTO habits (
                    name, 
                    periodicity, 
                    description, 
                    creationDate, 
                    streak,
                    highestStreak,
                    logNum, 
                    checkLog, 
                    timeDone, 
                    did, 
                    dueDate,
                    difficultyCount)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', (
                habit.name, habit.periodicity, habit.description, habit.creationDate, habit.streak, habit.highestStreak,
                habit.logNum, ' | '.join(map(str, habit.checkLog)), int(habit.timeDone), int(habit.did),
                habit.dueDate, habit.difficultyCount
            ))

        conn.commit()
        cursor.close()
        conn.close()


    '''this loads all rows of the database and turns them into a new object to be able to manipulate.
    It makes sure that the object isn't duplicated in the database and is just a temporary object.'''
    @staticmethod
    def loadFromDatabase():
        '''create a new database connection'''
        conn = mysql.connector.connect(
            host='sql7.freemysqlhosting.net	',
            user='sql7630486',
            password='eUXLRyhGwG',
            database='sql7630486'
        )
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM habits")
        habits = []
        for row in cursor:
            habit = Habit(row[1], row[2], row[3], row[11])
            habit.id = row[0]
            habit.creationDate = row[4]
            habit.streak = row[5]
            habit.highestStreak = row[6]
            habit.logNum = row[7]

            '''convert checkLog from string to list of dates'''
            checkLogStr = row[8]
            if checkLogStr:
                checkLogDates = [datetime.strptime(dateStr, '%Y-%m-%d').date() for dateStr in checkLogStr.split(" | ")]
            else:
                checkLogDates = []
            habit.checkLog = checkLogDates

            habit.timeDone = bool(row[9])
            habit.did = bool(row[10])
            habit.dueDate = row[11]
            habit.difficultyCount = row[12]

            '''set the dueDate using timer.timeLapse() if it is not already set'''
            if not habit.dueDate:
                habit.dueDate = habit.timer.timeLapse()

            habits.append(habit)

        cursor.close()
        conn.close()

        return habits
    
    '''for when a new habit is created, this method inserts it into the database.
    It first checks there aren't any habits called the same'''
    def insertIntoDb(self):
        self.cursor.execute('SELECT * FROM habits WHERE name = %s', (self.name,))
        existing_habit = self.cursor.fetchone()
        if existing_habit is None:
            '''only set the creationDate for new habits'''
            if not self.did:  
                self.creationDate = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            if self.originalDueDate:
                '''use the originalDueDate if available'''
                self.dueDate = self.originalDueDate.strftime('%Y-%m-%d %H:%M:%S')
            elif not self.dueDate:
                '''set the dueDate to the current time'''
                self.dueDate = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            self.cursor.execute('''
                INSERT INTO habits (
                    name, 
                    periodicity, 
                    description, 
                    creationDate, 
                    streak, 
                    highestStreak,
                    logNum, 
                    checkLog, 
                    timeDone, 
                    did, 
                    dueDate,
                    difficultyCount)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', (
                self.name, self.periodicity, self.description, self.creationDate, self.streak, self.highestStreak,
                self.logNum, ' | '.join(map(str, self.checkLog)), int(self.timeDone), int(self.did),
                self.dueDate, self.difficultyCount
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
            host='sql7.freemysqlhosting.net	',
            user='sql7630486',
            password='eUXLRyhGwG',
            database='sql7630486'
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
    def fetchAll(cls):
        return cls.loadFromDatabase()
    
    
    '''logging activity. This method is called when the user selects to mark a habit.'''
    def log(self):

        '''connect to database'''
        conn = mysql.connector.connect(
            host='sql7.freemysqlhosting.net	',
            user='sql7630486',
            password='eUXLRyhGwG',
            database='sql7630486'
        )
        cursor = conn.cursor()

        self.did = True
        self.logNum += 1
        self.checkLog.append(date.today())
        self.streak, self.highestStreak = self.updateStreak()

        '''edit database'''
        cursor.execute(
            """
            UPDATE habits SET logNum = %s, checkLog = %s, streak = %s, highestStreak = %s, did = %s, dueDate = %s, dificultyCount = %s
            WHERE id = %s
            """,
            (
                self.logNum,
                "|".join(map(str, self.checkLog)),
                self.streak,
                self.highestStreak,
                int(self.did),
                self.dueDate,
                self.difficultyCount,
                self.id,
            ),
        )
        conn.commit()
        cursor.close()
        conn.close()

    
    '''update streak for when a habit is marked or when the periodicity is done'''
    def updateStreak(self):
        '''checks if the habit is completed'''
        if self.did == True:
            self.streak += 1
            print(f"Congrats! Your streak for {self.name} is now {self.streak}")
            if self.streak > self.highestStreak:
                self.highestStreak = self.streak
        else: 
            '''checks if the habit wasn't complete by the time the periodicity was done'''
            self.streak = 0
            print(f"😢, you just lost your {self.name} streak. Remember to keep doing your habits!")
            self.difficultyCount += 1
            time.sleep(1)
        return self.streak, self.highestStreak

    
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
            

    '''when periodicity is up call updateStreak and reset timer and variables.'''
    def timeout(self):
        self.timeDone = True
        if self.did == False:
            self.updateStreak()
        self.did = False
        self.timeDone = False
        self.dueDate = self.timer.timeLapse()
        return


#main
def main():
    habit1 = Habit.get()
    print(f"{habit1.creationDate}")
    habit1.log()


if __name__ == "__main__":
    main()


