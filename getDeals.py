from bs4 import BeautifulSoup
import requests 

purlsf = open("processedURLS.txt",'r')
prcdURLS = purlsf.read().split("\n")
purlsf.close()





rc =0 

def getTitle(soup): # works
	try :
		id = soup.find_all("div" , {"id":"srch-results"})[0]
		return str(id.find_all("h1")[0].text)
	except:
		return "NA"

def getDate(soup): # works
	try :
		id = soup.find_all("span" , {"style":"padding-right:30px"})[0]
	except:
		return "Limited period offer"
	return str(id.text)

def getDesOld(soup):
	id = soup.find_all("div" , {"class":"bnr-left"},{"style":"padding-top:0"})[0]
	id = id.find_all("div", {"class":"discount-coupon-code"})[1]
	id = id.find_all("p")[0]
	try :
		return str(id.text)
	except:
		return (id.text).encode('utf-8') 



def getDes(soup):
	try : 
		id = soup.find_all("div", {"class":"bnr-text1"})[0]
		id = id.find_all("strong")[0]
		try :
			return str(id.text)
		except:
			return (id.text).encode('utf-8') 
	except:
		return "NA"

def getTandC(soup):
	try :
		id = soup.find_all("div" , {"class":"bnr-left"},{"style":"padding-top:0"})[0]
		id = id.find_all("div", {"class":"discount-coupon-code"})	 

		for i in id : 
			if len( i.find_all("h3") ) != 0 :
				if i.find_all("h3")[0].text == "Terms and Conditions" :
					return (i.find_all("p")[0].text).encode('utf-8')

		return "NA"

	except :
		return "NA"


def getCats(soup):
	try :
		id = soup.find_all("div" , {"class":"bnr-left"},{"style":"padding-top:0"})[0]
		id = id.find_all("div", {"class":"discount-coupon-code"})	 
		temp = []
		cats = "" 
		for i in id : 
			if len( i.find_all("h4") ) != 0 :
				if i.find_all("h4")[0].text == "Check Latest Discount Coupons in these Related Categories" :
					temp = i.find_all("a")
					for a in temp :
						cats = cats+", " + (a.text).encode('utf-8') 

					return cats[2:-1]

		return "NA"

	except:
		return "NA"





def getMerchant(soup):
	try :
		id = soup.find_all("div" ,{ "class":"coupon-logo" }, { "style":"border-bottom:0" } )
		id = id[0].find_all("img")[0]
		return str(id.get("title"))
	except:
		return "NA"
def getImageUrl(soup):
	try :
		id = soup.find_all("div" , {"class":"offer-image"} )[0]
		return str(id.find_all("img")[0].get("src")) 
	except :
		return "NA"

def getPages(soup):
	try :
		id = soup.find_all("td" , { "height":"8" } ,{"align":"right" } )
		return int(id[0].text.split(" ")[3])
	except:
		try :
			return int(id[0].text.split(" ")[4]) 
		except:

			return 1 

def getAddress(soup):
	addr = ""
	id = soup.find_all("span" ,  {"class":"text1" }, {"style":"line-height:20px;font-size:12px" } )
	
	try :
		id = id[0].find_all("div")
	except :
		return "NA"

	for div in id :
		addr+= (div.text).encode('utf-8')
	
	if len(addr) > 0 :
		return addr	
	else :
		return "NA"

def getPin(soup):
	addr = ""
	id = soup.find_all("span" ,  {"class":"text1" }, {"style":"line-height:20px;font-size:12px" } )
	try :
		id = id[0].find_all("div")
	except :
		return "NA"
	for div in id :
		addr+= (div.text).encode('utf-8')
		if ", India " in (div.text).encode('utf-8'):  ###  bug fixed
			break
	if len(addr) > 0 :
		return addr.split(" ")[-1]	
	else :
		return "NA"


def getCity(soup):
	addr = ""
	id = soup.find_all("span" ,  {"class":"text1" }, {"style":"line-height:20px;font-size:12px" } )
	try :
		id = id[0].find_all("div")
	except :
		return "NA"
	for div in id :
		addr+= (div.text).encode('utf-8')
		if ", India " in (div.text).encode('utf-8'):  ###  bug fixed 
			break
	if len(addr) > 0 :
		return (addr.split(" ")[-3])[0:-1]	
	else :
		return "NA"



def getArea(soup):
	area = ""
	id = soup.find_all("span" ,  {"class":"text1" }, {"style":"line-height:20px;font-size:12px" } )
	try :
		id = id[0].find_all("div")
		area = str(id[0]).split("<br")[0][5:-1]
	except :
		return "NA" 

	if len(area) > 0 :
		return area
	else :
		return "NA"


def getURLS(cat):
	global rc
	global currentPrcdURLS 
	urls = []
	temp = ""
	req = requests.get(cat)
	sop = BeautifulSoup(req.content)
	id = sop.find_all("div", { "class":"deal-1" })
	for i in id :
		u = str( i.find_all("a")[0].get("href")) 
		print"found : "+ u 
		urls.append(u)
		#print urls[-1]
	pages = getPages(sop)
	for page in range(1,pages):
		temp = cat + "?start=" + str(20*page)
		req = requests.get(temp)
		sop = BeautifulSoup(req.content)
		id = sop.find_all("div", { "class":"deal-1" })
		for i in id :
			u = str( i.find_all("a")[0].get("href")) 
			print"found : "+ u 
			urls.append(u)
			#print urls[-1]


	for u in urls:
		if u in prcdURLS :
			rc+=1
			print "=========================repetead==============================="
			urls.remove(u)

		else :
			prcdURLS.append(u)
			currentPrcdURLS.append(u)
	return urls



currentPrcdURLS = []

cfileaddr = "Cats.txt" 

CURLS = []

cfile = open(cfileaddr,"r")
for c in cfile.read().split("\n")[0:-1]:
	CURLS.append(c)

cfile.close()


dealf = open("dealf.txt","w")
maindealf = open("finaldealf.xml","a")

counter = 1 

for CURL in CURLS[:] :
	currentPrcdURLS = []
	CAT_ = CURL.split("<=>")[1]
	_CURL = CURL.split("<=>")[0]

	if CAT_ == " Select Category" :
		CAT_ = "Other"

	allUrls = getURLS(_CURL)
	
	print "###"*40
	print CURL
	print "###"*40
	
	for url in allUrls :
		
		try :
			Req = requests.get(url)
		except requests.exceptions.MissingSchema :
			break
		Soup = BeautifulSoup(Req.content)
		if len ( Soup.find_all("img", {"src":"http://discount-coupon-codes.upto75.com/coupon-ends.png"}) ) == 0 :
			dealf.write("\n\n<Offer>\n")
			flag = 0
			print "Deal : "+str(counter)+"	"+url 
			counter+=1
			dealf.write("\n <OFFER_LINK>\n"+url+"\n </OFFER_LINK>\n")
			
			dealf.write("\n <OFFER_TITLE>\n"+getTitle(Soup) + "\n </OFFER_TITLE>\n")
			
			dealf.write("\n <OFFER_MERCHANT>\n"+getMerchant(Soup) + "\n </OFFER_MERCHANT>\n")
			
			dealf.write("\n <OFFER_START_DATE>\n"+"NA" + "\n </OFFER_START_DATE>\n")
			
			dealf.write("\n <OFFER_END_DATE>\n"+getDate(Soup) + "\n </OFFER_END_DATE>\n")
			
			dealf.write("\n <OFFER_DESCRIPTION>\n"+getDes(Soup) + "\n </OFFER_DESCRIPTION>\n")
			
			dealf.write("\n <OFFER_IMAGE_URL>\n"+getImageUrl(Soup) + "\n </OFFER_IMAGE_URL>\n")
			
			dealf.write("\n <OFFER_CATEGORY>\n"+CAT_ + "\n </OFFER_CATEGORY>\n")
			
			dealf.write("\n <OFFER_SIMILAR_CATEGORIES>\n"+getCats(Soup) + "\n </OFFER_SIMILAR_CATEGORIES>\n")
			
			dealf.write("\n <OFFER_TERMS_AND_CONDITIONS>\n"+getTandC(Soup) + "\n </OFFER_TERMS_AND_CONDITIONS>\n")
			
			dealf.write("\n <OFFER_ADDRESS>\n"+getAddress(Soup) + "\n </OFFER_ADDRESS>\n")
			
			dealf.write("\n <OFFER_PINCODE>\n"+getPin(Soup) + "\n </OFFER_PINCODE>\n")
			
			dealf.write("\n <OFFER_CITY>\n"+getCity(Soup) + "\n </OFFER_CITY>\n")
			
			dealf.write("\n <OFFER_AREA>\n"+getArea(Soup) + "\n</OFFER_AREA>\n")
			
			print "\n\n"
			print "__"*40
			print "\n\n"
			
			dealf.write("\n\n")
			dealf.write("</Offer>")
			dealf.write("\n\n")


		elif flag == 3 :
			break 

		else :
			flag +=1

	dealf.close()
	
	ContenT = open("dealf.txt",'r').read()
	ContenT = ContenT.split('&')
	ContenT = 'and'.join(ContenT)
	maindealf.write(ContenT)

	dealf = open("dealf.txt",'w')

	CURLS.remove(CURL)
	cfile = open(cfileaddr,"w")
	for c in CURLS:
		cfile.write(c+"\n") 

	purlsf = open("processedURLS.txt",'a')

	for pu in currentPrcdURLS :
		purlsf.write(pu+"\n")

	purlsf.close()

	cfile.close()

dealf.close()


maindealf = open("finaldealf.xml","r")
ContenT = maindealf.read()
maindealf.close()

maindealf = open("finaldealf.xml","w")
maindealf.write('<?xml version="1.0" encoding="ISO-8859-1" ?> \n\n <all_offers>')
maindealf.write(ContenT)
maindealf.write("\n</all_offers>")
maindealf.close()


print "There were " +str(rc)+ " repeated offers."
purlsf.close()