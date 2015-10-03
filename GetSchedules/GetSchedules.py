import datetime
import re
import sqlite3 as lite
import urllib.request
from bs4 import BeautifulSoup as bs

with urllib.request.urlopen("http://api.larm.fm/v6/Session/Create") as session:
    data = session.read()
    soup = bs(data, "html.parser")
    sessionGuid = soup.find("guid")

searchQuery = "http://api.larm.fm/v6/View/Get?\
view=Search\
&sort=PubStartDate%2Bdesc\
&filter=Type%3ASchedule\
&pageIndex={}\
&pageSize={}\
&sessionGUID={}"\
"&format=xml2\
&userHTTPStatusCodes=False"

itemQuery = "http://api.larm.fm/v6/View/Get?\
view=Object\
&query={}\
&pageIndex=0\
&pageSize=20\
&sessionGUID={}\
&format=xml2\
&userHTTPStatusCodes=False"

#&filter=%28Type%3ASchedule%20OR%20Type%3AScheduleNote%29\
con = lite.connect('../hack4dk.sqlite')
regex = "\d{4}-\d{2}-\d{2}"

with con:
    cur = con.cursor()
    cur.execute("DELETE FROM schedules")

pageSize = 2000
totalcount = pageSize
itemsloaded = 0
currentpage = 0
currentid = 0

while itemsloaded < totalcount:
    print ("Loading page {}".format(currentpage))
    with urllib.request.urlopen(searchQuery.format(str(currentpage), str(pageSize), sessionGuid.text)) as searchResponse:
        data = searchResponse.read()
        soup = bs(data, "html.parser")
        ids = soup.findAll("id")
        totalcount = int(soup.find("totalcount").text)

        for id in ids:
            with urllib.request.urlopen(itemQuery.format(id.text, sessionGuid.text)) as itemResponse:
                #convert to soup
                itemData = itemResponse.read()
                itemSoup = bs(itemData, "html.parser")

                # the actual text description
                description = itemSoup.find("metadataxml")
                if description is None:
                    continue;

                #Fetch date from filename
                filename = itemSoup.find("filename")
                if filename is None:
                    continue;

                dateStr = re.search(regex, filename.text)
                date = datetime.datetime.strptime(dateStr.group(0), "%Y-%m-%d").date()

                #insert into db
                with con:
                    cur = con.cursor()
                    sqlQuery = "INSERT INTO Schedules VALUES(?, ?, ?)"
                    cur.execute(sqlQuery, (currentid, date, description.text))

            currentid = currentid + 1
            if currentid % 100 == 0:
                print("Loaded {} out of {}".format(str(currentid), str(totalcount)))

        # We loaded the items on this page
        itemsloaded = itemsloaded + pageSize
        currentpage = currentpage + 1
