import sqlite3
import string
from datetime import *

databaseName = 'Fall2023'


def FindTime(database, room, building, meetingDay):
    conn = sqlite3.connect(str(database) + '.db')
    c = conn.cursor()
    c.execute("Select * from courses where room = ? and building = ? and meetingday = ? order by startTime", [room, building, meetingDay])

    return c.fetchall()


results = FindTime(databaseName, 240, '2ARC', 'M')
idNum = 0
for r in results:
    idNum = idNum + 1
    stime = datetime.strptime(r[3], "%H:%M")
    etime = datetime.strptime(r[4], "%H:%M")
    #print(r[0], '-', r[7], r[6], '---', stime.strftime("%I:%M %p") + ' - ' + etime.strftime("%I:%M %p"), r[5])
    timeFrame = str(stime.strftime("%I:%M %p") + ' - ' + etime.strftime("%I:%M %p"));

    print('{')
    print(""" id: {}, \n text: "{} \\n {}",\n start: "2023-10-02T{}:00",\n end: "2023-10-02T{}:00"\n""".format(idNum, r[0], timeFrame, r[3], r[4]), end='')
    print('},')

