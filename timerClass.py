'''imports'''
import datetime
from dateutil.relativedelta import relativedelta

'''timer class to be able to make countdown to periodicity'''
class Timer:
    def __init__(self, periodicity, dueDate=None):
        self.periodicity = periodicity
        self.dueDate = dueDate
        self.time = None
        self.timeDone = bool

    '''to know when the habit needs to be completed by.
    it automatically sets when the habit is created and repeats itself over and over when it ends.'''
    def timeLapse(self):
        firstDate = datetime.datetime.now()
        match self.periodicity:
            case "minute":
                self.dueDate = firstDate + datetime.timedelta(minutes= 1)
            case "daily":
                self.dueDate = firstDate + relativedelta(days=+1)
            case "weekly":
                self.dueDate = firstDate + relativedelta(weeks=+1)
            case "monthly":
                self.dueDate = firstDate + relativedelta(months=+1)
            case "yearly":
                self.dueDate = firstDate + relativedelta(years=+1)
        return self.dueDate

    '''to be called when the info table is displayed, to know the time remaining.'''
    def timeRemaining(self, dueDate):
        currentTime = datetime.datetime.now()
        remainingTime = dueDate - currentTime
        if remainingTime.total_seconds() <= 0:
            self.timeDone = True
            return self.timeDone
        else:
            return remainingTime

#main
def main():
    timer = Timer()
    print(timer.firstDate)
    timer.timeLapse()
    print(timer.dueDate)
    print(timer.timeRemaining())


if __name__ == "__main__":
    main()
