import coursedataScrapper
import database


databaseName = 'Fall2023'
conn = database.createDatabase(databaseName)

pageList = coursedataScrapper.searchSiteForPages()

for page in pageList:
    coursedataScrapper.searchSiteForCourses(conn, page)



