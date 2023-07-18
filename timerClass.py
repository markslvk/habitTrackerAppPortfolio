'''imports'''
import datetime
from dateutil.relativedelta import relativedelta

'''timer class to be able to make countdown to periodicity'''
class Timer:
    def __init__(self, periodicity, due_date=None):
        self.periodicity = periodicity
        self.due_date = due_date
        self.time = None
        self.time_done = bool

    '''to know when the habit needs to be completed by.
    it automatically sets when the habit is created and repeats itself over and over when it ends.'''
    def time_lapse(self):
        first_date = datetime.datetime.now()
        match self.periodicity:
            case "minute":
                self.due_date = first_date + datetime.timedelta(minutes= 1)
            case "daily":
                self.due_date = first_date + relativedelta(days=+1)
            case "weekly":
                self.due_date = first_date + relativedelta(weeks=+1)
            case "monthly":
                self.due_date = first_date + relativedelta(months=+1)
            case "yearly":
                self.due_date = first_date + relativedelta(years=+1)
        return self.due_date

    '''to be called when the info table is displayed, to know the time remaining.'''
    def time_remaining(self, due_date):
        current_time = datetime.datetime.now()
        remaining_time = due_date - current_time
        if remaining_time.total_seconds() <= 0:
            self.time_done = True
            return True
        else:
            self.time_done = False
            return remaining_time

#main
def main():
    timer = Timer()
    print(timer.first_date)
    timer.time_lapse()
    print(timer.due_date)
    print(timer.time_remaining())


if __name__ == "__main__":
    main()
