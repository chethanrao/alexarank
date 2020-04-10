import csv
import urllib.request
import xml.etree.ElementTree as ET
import ssl
def getMapFromCSV(file):
	f=open(file)
	map=dict()
	for row in csv.reader(f):
		map[row[0]]=row[1]
		
	return map	
	
map=getMapFromCSV("stocksweburl.csv")
stock=input('Enter the stock\n')
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
if len(stock)>1:
	url=map[stock.lower()]
	alexaurl="http://data.alexa.com/data?cli=10&url="+url
	response=urllib.request.urlopen(alexaurl,context=ctx)
	if response.getcode()==200:
		tree=ET.fromstring(response.read().decode())
		rank=tree.find('.//RANK')
		if int(rank.get('DELTA'))>0:
			print("buy")
		else if int(rank.get('DELTA'))==0:
			print("no recommendation at this point of time")
		else:
			print("do not buy")
	else:
		print("wrong response code expected 200 found:"+response.getcode())
else:
	print("stock not found")
