from websocket import create_connection
import time
import requests
import threading
import bs4 as bs
import urllib.request

#creating connection to blockchain info
ws = create_connection("wss://ws.blockchain.info/inv")
ws.send('{"op":"unconfirmed_sub"}')
price=requests.get("https://blockchain.info/q/24hrprice")


#thread creation
def txLookup(hash):
    time.sleep(0.5)

    url = "https://www.blockchain.com/btc/tx/"+hash
    sauce = urllib.request.urlopen(url).read()
    soup = bs.BeautifulSoup(sauce,"lxml")
    link = soup.findAll("div",{"class": "sc-8sty72-0 kcFwUU"})

    while(link[13].text == "0"):
        sauce = urllib.request.urlopen(url).read()
        soup = bs.BeautifulSoup(sauce,"lxml")
        link = soup.findAll("div",{"class": "sc-8sty72-0 kcFwUU"})

    print(hash+" HAS BEEN CONFIRMED")

def startTx(hash):
    txThread = threading.Thread(target= txLookup, args=(hash,))
    txThread.start()

#function to grab data
def grabbingData():
    #obtaining data
    result =  ws.recv()

    #finding hash and value locations in the JSON
    location = result.find('"hash":')
    location2 = result.find('"value":')
    hash=""
    value="";

    #modifying the locations
    location=location+8
    location2=location2+8
    b1=True
    b2=True

    #obtaining full strings and values
    while b1 or b2:
        if result[location] != "\"" and b1:
            hash = hash+result[location]
            location += 1
        elif result[location] == "\"":
            b1=False

        if result[location2]!="," and b2:
            value=value+result[location2]
            location2 += 1
        elif result[location2]==",":
            b2=False

    #editing values
    value = float(value)/100000000.0
    USD = value*float(price.text)

    #storing and returning list
    output=[hash,value,USD]
    return output

def scanner():
    #running data
    time1 = time.time()
    previousHash=""

    while True:
        output = grabbingData()

        #notify depending on the USD value
        if(output[2]>=50000 and (str(output[0])!=previousHash or firstRun)):
            print("{0:,} BTC transaction is on the network. USD value: {1:,.2f} Hash: {2}".format(output[1],output[2],str(output[0])))
            startTx(output[0])
            firstRun=False
        #counts to 10 seconds and updates the current BTC price
        end= time.time()
        if (end-time1)>10.0:
            price=requests.get("https://blockchain.info/q/24hrprice")
            time1=time.time()

        previousHash=output[0]

def main():
    scanner()


if __name__ == "__main__":
    main()
