'''imports'''
import mysql.connector
from datetime import date, datetime
import mysql.connector.pooling
from dotenv import load_dotenv
import os
import re
from habitClass import Habit

#environment variables for DB
load_dotenv()
db_user = os.getenv("HABITDB_USER")
db_password = os.getenv("HABITDB_PASS")

#function to create the habits database
def create_database():
    conn = mysql.connector.connect(
        host='aws.connect.psdb.cloud',
        user=db_user,
        password=db_password,
    )

    #establish the connection to the habits database
    conn = mysql.connector.connect(
        host='aws.connect.psdb.cloud',
        user=db_user,
        password=db_password,
        database='habittrackerdb'
    )
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS habits (
            id INT AUTO_INCREMENT PRIMARY KEY,
            reload
        )
    ''')
    conn.commit()
    cursor.close()
    conn.close()

#function to save habits to the database
def save_to_database(habits):
    conn = mysql.connector.connect(
        host='aws.connect.psdb.cloud',
        user=db_user,
        password=db_password,
        database='habittrackerdb'
    )
    cursor = conn.cursor()

    cursor.execute("TRUNCATE TABLE habits")

    for habit in habits:
        cursor.execute('''
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
            habit.name, habit.periodicity, habit.description, habit.creation_date, habit.streak, habit.highest_streak,
            habit.log_num, ' | '.join(map(str, habit.check_log)), int(habit.time_done), int(habit.did),
            habit.due_date, habit.difficulty_count
        ))

    conn.commit()
    cursor.close()
    conn.close()

#function to load habits from the database
def load_from_database():
    conn = mysql.connector.connect(
        host='aws.connect.psdb.cloud',
        user=db_user,
        password=db_password,
        database='habittrackerdb'
    )
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM habits")
    habits = []
    for row in cursor:
        habit = Habit(row[1], row[2], row[3], row[11])
        habit.id = row[0]
        habit.creation_date = row[4]
        habit.streak = row[5]
        habit.highest_streak = row[6]
        habit.log_num = row[7]

        #convert check_log from string to list of dates
        check_log_str = row[8]
        if check_log_str:
            date_pattern = r'\d{4}-\d{2}-\d{2}'
            check_log_dates = [datetime.strptime(dateStr, '%Y-%m-%d').date() for dateStr in re.findall(date_pattern, check_log_str)]
        else:
            check_log_dates = []
        habit.check_log = check_log_dates

        #set the due_date using timer.time_lapse() if it is not already set
        if not habit.due_date:
            habit.due_date = habit.timer.time_lapse()

        habits.append(habit)

    cursor.close()
    conn.close()

    return habits