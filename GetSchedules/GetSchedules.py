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
&pageIndex=0\
&pageSize=10\
&sessionGUID={}"\
"&format=xml2\
&userHTTPStatusCodes=False".format(sessionGuid.text)

itemQuery = "http://api.larm.fm/v6/View/Get?\
view=Object\
&query={}\
&pageIndex=0\
&pageSize=20\
&sessionGUID={}\
&format=xml2\
&userHTTPStatusCodes=False"

#&filter=%28Type%3ASchedule%20OR%20Type%3AScheduleNote%29\


with urllib.request.urlopen(searchQuery) as searchResponse:
    data = searchResponse.read()
    soup = bs(data, "html.parser")
    ids = soup.findAll("id")

    for id in ids:
        with urllib.request.urlopen(itemQuery.format(id.text, sessionGuid.text)) as itemResponse:
            itemData = itemResponse.read()
            itemSoup = bs(itemData, "html.parser")
            #text = itemSoup.find("metadataxml")
            #text = itemSoup.find("filename")
            print (itemSoup.prettify())

print(sessionGuid.text)
