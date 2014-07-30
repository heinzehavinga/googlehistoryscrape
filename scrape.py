from bs4 import BeautifulSoup
import unicodecsv, re, urlparse, os

def checkDiv(div):
	
	if div.find_all('h1') is None:
		return False
	else:
		return True

datetimeString = ""
search = ""
desturl = ""
destFound = False

writer = unicodecsv.writer(open('history.csv', 'wb'), encoding='utf-8',delimiter=';', dialect='excel',quotechar='"')
writer.writerow([
			        				"Search words",
			        				"Choosen result",
			        				"Result domain",
			        				"Date",
			        			])

for file in os.listdir("."):
	if file.endswith(".html"):
		
		soup = BeautifulSoup(open(file))

		for header in soup.find_all('h1'):
			# print header.text
			datetimeString = ""

			go = True
			nextOne = header.parent.nextSibling
			while go is True:
				
				destFound = False
				
				if nextOne is not None:
					for td in nextOne.find_all('td'):
						regexp = re.compile(r'^[0-9]{2}:[0-9]{2}$')
						if regexp.search(td.text) is not None:
							datetimeString = header.text+" "+td.text

					
					for table in nextOne.find_all('table'):
						for a in table.find_all('a', {'href':re.compile('.+')}):		
							if "www.google.com/search?q=" in a['href']:
								search = a.text
							else:
								destFound = True
								desturl = str(a.get('href'))
								parsed = urlparse.urlparse(desturl)
								p =  urlparse.parse_qs(parsed.query)
								
								if 'q' in p.keys():
									desturl = str(p['q'])
								netloc = parsed.netloc
								writer.writerow([
			        				search,
			        				desturl[2:-2],
			        				netloc,
			        				datetimeString,
			        			])
			        	if destFound is False:
			        		writer.writerow([
			        				search,
			        				"","",
			        				datetimeString,
			        			])

					nextOne = nextOne.nextSibling
					if nextOne is not None:
						go = checkDiv(nextOne)
					else:
						go = False
print("all done!")
