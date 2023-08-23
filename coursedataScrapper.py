import requests
from bs4 import BeautifulSoup
import database


def searchSiteForPages():
    listOfPages = []
    URL = "https://webcs7.osss.uic.edu/schedule-of-classes/static/schedules/fall-2023/index.html"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    rows = soup.find("div", class_="row")
    columns = rows.find_all("div", class_="col")

    for column in columns:
        table = column.find("table", class_="table").find_all("tr")
        for subject in table:
            subjectInfo = subject.find("td")
            link = subjectInfo.find("a", href=True)
            listOfPages.append(link['href'])

    return listOfPages


def searchSiteForCourses(conn, page):
    URL = "https://webcs7.osss.uic.edu/schedule-of-classes/static/schedules/fall-2023/" + str(page)
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    container = soup.find("body", class_="container")
    subpage = container.find("main", class_="subpage")
    courseRows = subpage.find_all("div", class_="row course")

    for course in courseRows:
        courseNumber = course.find("h2").text.strip()
        courseSessionTable = ((course.find("div", class_="row")).find("div", class_="col")).find("table",
                                                                                                 class_="table")
        sessionsInCourse = courseSessionTable.find_all("tr")
        for session in sessionsInCourse:
            sessionInfo = session.find_all("td")

            # If the sessionInfo list is too short SKIP
            if len(sessionInfo) != 9:
                continue
            # If the sessionInfo time attribute is "ARRANGED" SKIP
            if sessionInfo[2].text.strip() == "ARRANGED":
                continue

            CRNOfSession = sessionInfo[0].text.strip()
            typeOfSession = sessionInfo[1].text.strip()
            timeOfSession = sessionInfo[2].text.strip()
            daysOfSession = sessionInfo[3].text.strip()
            roomOfSession = sessionInfo[4].text.strip()
            buildingOfSession = sessionInfo[5].text.strip()
            instructorOfSession = sessionInfo[6].text.strip()
            methodOfSession = sessionInfo[8].text.strip()
            database.addCourse(conn, courseNumber, CRNOfSession, typeOfSession, timeOfSession, daysOfSession,
                               roomOfSession, buildingOfSession, instructorOfSession, methodOfSession)
            # print(courseNumber, CRNOfSession, typeOfSession, timeOfSession, daysOfSession, roomOfSession,
            #      buildingOfSession, instructorOfSession, methodOfSession)

