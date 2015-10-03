

#!/usr/bin/env python
# -*- coding: utf-8 -*-

from BeautifulSoup import BeautifulSoup as bs
import urllib

file = open('actors', 'w')

for letterIndex in range(0,28):
    url = "http://danskefilm.dk/navngroup/"+ (chr(ord('A')+letterIndex)) +".html"
    soup = bs(urllib.urlopen(url))

    names = soup.findAll('a')

    for name in names:
        if name is None:
            continue

        nameText = name.text
        nameText = nameText.strip()
        nameText = nameText.encode('UTF-8', 'ignore')

        if len(nameText)>0:
            print nameText
            file.write(nameText + "\n")

file.close()
