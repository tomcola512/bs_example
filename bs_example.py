from BeautifulSoup import BeautifulSoup
import urllib2
import codecs 
import pprint
import unicode_magic as um

url = "http://en.wikipedia.org/wiki/Chinese_language"
page = urllib2.urlopen(url)
soup = BeautifulSoup(page.read())

table = soup.findAll(name = "table", attrs = {"class": "wikitable"}, limit = 3)[-1]
rows = table.findAll("tr")

table = []
keys = [header.text for header in rows[0].findAll("th")]
table.append(keys)

for i in range(len(rows)-1):
    table.append([rows[i+1].findAll("td")[j].text for j in range(len(keys))])

table = [[um.fix_bad_unicode(table[i][j]) for j in range(len(table[0]))] for i in range(len(table))]
    
def dump(o):
    with codecs.open("output.txt", "w", "utf-8") as f:
        f.write(o)

def pad(str):
    gap = 25 - len(str)
    tabs = gap/4
    spaces = gap - tabs*4
    return str+' '*spaces+'\t'*tabs
        
blob = '\n'.join([' '.join(table[i]) for i in range(len(table)-1)])

dump(blob)

def in_ipynb():
    try:
        cfg = get_ipython().config
        if cfg['IPKernelApp']['parent_appname'] == 'ipython-notebook':
            return True
        else:
            return False
    except NameError:
        return False
        
if in_ipynb:
    def table_print():
        for i in range(len(table)):
            for j in range(len(table[0])):
                print table[i][j],
            print
    table_print()
else:
    print "Unicode output suppressed when not in IPython Notebook"