

from bs4 import BeautifulSoup as BS
import requests, csv, time, pickle

baseUrl = 'https://projects.propublica.org/nonprofits/'
searchUrl = "search?c_code%5Bid%5D=3&ntee%5Bid%5D=&page=%d&q=&state%5Bid%5D=MD"


def main():
	# Get ID and name info all 501(c)3 orgs
	for i in range(1,146):
		table = getPageOrgs(i)
		saveTable(table=table, pageNum=i)

	# Fill in data of each Organization

def getOrgUrls( pages ):
	orgTable = []
	for p in pages:
		orgTable.append(getSinglePageUrls(p))
	return orgTable


# Pull a table of the EIN, Name, City, State of each organization on the page
def getPageOrgs( pageNum ):
	searchUrl = 'search?c_code%%5Bid%%5D=3&ntee%%5Bid%%5D=&page=%d&q=&state%%5Bid%%5D=MD' % pageNum
	url = baseUrl + searchUrl
	r = requests.get(url)
	# Get tables from page
	data = r.text
	soup = BS(data, 'html5lib')
	siteTable = soup.find('body', class_='app old-page-new-wrapper').find('table').find('tbody')
	rows = siteTable.find_all('tr')

	# Convert tables
	orgTable = []
	for row in rows:
		a = row.find('a')
		city = row.find('td', class_='city').text.strip()
		state = row.find('td', class_='state').text.strip()
		name = a.contents[0]
		orgUrl = a['href']
		ein = orgUrl.split('/')[-1]
		orgTable.append([ein, name, city, state])
	return orgTable

# Save the table to the appropriate directory
def saveTable( pageNum, table, filePath='./Charities_MD/' ):
	fileName = 'charities_%03d' % pageNum
	with open(filePath+fileName+'.csv', 'w') as myfile:
	    #configure writer to write standard csv file
	    writer = csv.writer(myfile, quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
	    writer.writerow(['EIN', 'Name', 'City', 'State'])
	    for entry in table:
	        writer.writerow([entry[0], entry[1], entry[2], entry[3]])

tic = time.clock()
main()
toc = time.clock()
print('Processing Time: %2.3fsec' % (toc-tic))