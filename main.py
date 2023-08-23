import coursedataScrapper
import database


databaseName = 'Fall2023'
conn = database.createDatabase(databaseName)

pageList = coursedataScrapper.searchSiteForPages()

print("Scrapping site to populate", databaseName, "database")
for page in pageList:
    coursedataScrapper.searchSiteForCourses(conn, page)

print("Finished populating", databaseName, "database")


