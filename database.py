import sqlite3
from datetime import *
import os

def createDatabase(database):

    if os.path.isfile(database+".db"):
        conn = sqlite3.connect(str(database) + '.db')
    else:
        conn = sqlite3.connect(str(database) + '.db')
        c = conn.cursor()
        c.execute(""" CREATE TABLE courses (
                        class text,
                        crn text,
                        classtype text,
                        startTime TIME,
                        endTime TIME,
                        meetingday text,
                        room text,
                        building text,
                        instructor text,
                        method text
          )""")
        conn.commit()
    conn.commit()
    return conn


def addCourse(conn, classNumber, crn, type, timeframe, days, room, building, instructor, method):
    c = conn.cursor()
    for day in days:
        stime, etime = tuple(timeframe.split(' - '))  # Time split into start and end times
        StartTime = datetime.strptime(stime, '%I:%M  %p') # Convert from hour hr format to 24 hour format
        EndTime = datetime.strptime(etime, '%I:%M  %p')
        print(end="")
        c.execute("INSERT INTO courses VALUES (?,?,?,?,?,?,?,?,?,?) ", [classNumber, crn, type, datetime.strftime(StartTime, "%H:%M"), datetime.strftime(EndTime, "%H:%M"), day, room, building, instructor, method])

    conn.commit()



