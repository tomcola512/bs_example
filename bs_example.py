from BeautifulSoup import BeautifulSoup
import urllib2
import codecs 
import pprint

url = "http://en.wikipedia.org/wiki/Chinese_language"
page = urllib2.urlopen(url)
soup = BeautifulSoup(page.read())

#Select the 3rd wikitable table in the page
table = soup.findAll(name = "table", attrs = {"class": "wikitable"}, limit = 3)[-1]
rows = table.findAll("tr")

table = []
keys = [header.text for header in rows[0].findAll("th")]
table.append(keys)

for i in range(len(rows)-1):
    table.append([rows[i+1].findAll("td")[j].text for j in range(len(keys))])
    
def dump(o):
    with codecs.open("output.txt", "w", "utf-8") as f:
        f.write(o)

def pad(str):
    #assume 4 space tab
    gap = 20 - len(str)
    tabs = gap/4
    spaces = gap - tabs*4
    return str+' '*spaces+'\t'*tabs
        
blob = '\n'.join(['\t'.join(map(pad, table[i])) for i in range(len(table)-1)])
dump(blob)