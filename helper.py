from bs4 import BeautifulSoup
import requests 

A_G = "http://www.upto75.com/Adventure_Gaming/145/Shopping_Deals.html"
main = "http://www.upto75.com/Adventure_Gaming/"
URL = "/Shopping_Deals.html"

Req = requests.get(A_G)
Soup = BeautifulSoup(Req.content)

id = Soup.find_all( "select", { "name":"src_category"} ,  {"id":"src_category"} ) 
id = id[0].find_all("option")
id.reverse()


CURLS = []
cfile = open("Cats.txt",'w')

for i in id :
	cat_ = i.text.encode('utf-8')
	CURLS.append(main+str(i.get("value")) + URL + "<=>"+cat_ )
	print "found  " + CURLS[-1]
	cfile.write(CURLS[-1]+"\n")

cfile.close()


open("processedURLS.txt",'a').close()
raw_input("\n\nPress Enter to close")

