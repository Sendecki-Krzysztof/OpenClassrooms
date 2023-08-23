import sqlite3
from datetime import *
import os

def createDatabase(database):

    if os.path.isfile(database+".db"):
        conn = sqlite3.connect(str(database) + '.db')
    else:
        conn = sqlite3.connect(str(database) + '.db')
        c = conn.cursor()
        createCourseLocation(c)
        createCourseTable(c)
        createCourseTimeTable(c)
    conn.commit()
    return conn

def createCourseLocation(c):
    c.execute(""" Create Table location(
                    LID INTEGER PRIMARY KEY autoincrement,
                    building text,
                    room text,
                    UNIQUE (building, room)
        )""")
def createCourseTable(c):
    c.execute(""" Create Table course(
                    crn text primary key,
                    title text,
                    classtype text,
                    instructor text
                    
        )""")
def createCourseTimeTable(c):
    c.execute(""" Create Table coursetime(
                    crn text,
                    LID int,
                    weekday text,
                    startTime TIME,
                    endTime TIME,
                    primary key (crn, weekday),
                    foreign key (LID) references location(LID)
        )""")


def addToCourseTable(conn, crn, title, type, instructor):
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO course VALUES (?,?,?,?)", [crn, title, type, instructor])

def addToCourseTimeTable(conn, crn, LID, day, timeframe):
    c = conn.cursor()
    stime, etime = tuple(timeframe.split(' - '))  # Time split into start and end times
    StartTime = datetime.strptime(stime, '%I:%M  %p')  # Convert from hour hr format to 24 hour format
    EndTime = datetime.strptime(etime, '%I:%M  %p')

    c.execute("INSERT OR IGNORE into courseTime VALUES (?,?,?,?,?)", [crn, LID, day, datetime.strftime(StartTime, "%H:%M"),  datetime.strftime(EndTime, "%H:%M")])

def addToLocationTable(conn, building, room):
    c = conn.cursor()
    c.execute("INSERT OR IGNORE into location (building, room) VALUES (?,?)", [building, room])
    c.execute("Select LID from location where building = ? and room = ?", [building, room])
    value = c.fetchone()
    return value[0]


def addCourse(conn, title, crn, type, timeframe, days, room, building, instructor, method):
    c = conn.cursor()
    for day in days:

        LID = addToLocationTable(conn, building, room)
        addToCourseTable(conn, crn, title, type, instructor)
        addToCourseTimeTable(conn, crn, LID, day, timeframe)
    conn.commit()



