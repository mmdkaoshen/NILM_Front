from PyQt5.QtCore import QDateTime
from PyQt5.QtWidgets import QDateTimeEdit


class TimeEdit(QDateTimeEdit):
    def __init__(self):
        super().__init__()
        self.setDateTime(QDateTime.currentDateTime())
        self.setDisplayFormat("yyyy-MM-dd HH:mm:ss")

    def getTime(self):
        date = self.date().toString('yyyy-MM-dd ')
        currentTime = self.time().toString()
        dateTime = date + currentTime

        return dateTime
