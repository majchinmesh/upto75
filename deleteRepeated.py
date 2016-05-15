from bs4 import BeautifulSoup
import requests 

def compare(O , Offers):
	for Offer in Offers :
		if O.offer_link == Offer.offer_link :
			return 1 
	return 0 


maindealf = open("finaldealf.xml","r")
ContenT = maindealf.read()
maindealf.close()

soup = BeautifulSoup(ContenT)

unicon = []

count = 0

all_offers = soup.find_all("offer") 


for offr in all_offers:
	count +=1
	if compare(offr , unicon ) == 0:
		print offr.offer_link.text.encode('utf-8')
		unicon.append(offr)


ContenT = ""


print "initially " + str(len(all_offers)) + " offers were there."

for offr in unicon:
	ContenT += str(offr)

print "finally " + str(len(unicon)) + " offers are present after deleting the repaeted ones."


maindealf = open("finaldealf.xml","w")
maindealf.write('<?xml version="1.0" encoding="ISO-8859-1" ?> \n\n <all_offers>')

maindealf.write(ContenT)

maindealf.write("\n</all_offers>")
maindealf.close()

raw_input("\n\nPress Enter to close")