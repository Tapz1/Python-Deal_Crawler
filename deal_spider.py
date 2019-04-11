##########
# Programmer: Chris Tapia & Ehsun Farooq
# Program Description: Web Crawler to scrape the latest deals for those that are too busy, sends email of those deals
#       and can also send those emails at a more specific time.
# Date Modified: 12/06/18
##########

# if not yet done, need to "pip install bs4" and "pip install requests" from the command window
import os
import sys
import requests
from bs4 import BeautifulSoup
import send_email
import sched, time
from datetime import datetime
from threading import Timer


# displays the title and the price when ran


def ebay_spider():
    ebay_list = []  # list that we use to place into file

    url = "https://www.ebay.com/deals?_trkparms=%26clkid%3D8422823819386027280"
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, "html.parser") # parses through the content

    for item in soup.find_all('span', {'class': ['ebayui-ellipsis-3', 'ebayui-ellipsis-2', 'first', 'itemtile-price-bold']}):
        title = item.string # this grabs only the string
        print(title)
        ebay_list.append(str(title) + "\n") # creates list to put in a file

    message = '\n'.join([str(i) for i in ebay_list]) # formats the list for file
    file = open("C:\\ebay deals.txt", "w")
    file.write(message)
    file.close()
    filename = "C:\\ebay deals.txt"
    body = "Attached are the latest deals on Ebay."
    send_email.send_email("Ebay Deals", body, filename)


# look at ebay_spider comments for better understanding
def slickdeals_spider():
    slick_list = []

    url = "https://slickdeals.net"
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, "html.parser")

    for item in soup.find_all('a', {'class': 'itemTitle'}):
        title = item.string
        item_url = url + item.get('href')
        print(title)
        get_single_item(item_url)
        print(item_url)
        slick_list.append(str(title) + "\n" + str(get_single_item(item_url)) + "\n" + str(item_url) + "\n\n")

    message = '\n'.join([str(i) for i in slick_list])
    file = open("C:\\Slickdeals.txt", "w")
    file.write(message)
    file.close()
    filename = "C:\\Slickdeals.txt"
    body = "Attached are the latest deals across the web from Slickdeals.com"
    send_email.send_email("Slickdeals Deals!", body, filename)


def get_single_item(item_url):
    source_code = requests.get(item_url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, "html.parser")
    for item_price in soup.find_all('div', {'id': 'dealPrice'}):
        price = item_price.string
        print(str(price))


# here is the second menu
def menu():
    option = True
    while option:
        print ("""
        1. Deals on ebay
        2. Deals on Slickdeals
        3. Exit
        """)
        option = input("What would you like to do? ")
        if option == "1":
            print("\nHere are the current deals on ebay")
            ebay_spider()
        elif option == "2":
            print("\nHere are the deals on Slickdeals from across the web")
            slickdeals_spider()
        elif option == "3":
            raise SystemExit
        elif option != "":
            print("\n Not Valid Choice Try again")


# these automated functions send the email at a later time
# from which you choose
def ebay_automate(h, m):
    print("sending your email at: %s:%s" % (h, m))
    x = datetime.today()
    y = x.replace(day=x.day + 1, hour=h, minute=m, second=0, microsecond=0)
    delta_t = y - x

    secs = delta_t.seconds + 1

    t = Timer(secs, lambda: ebay_spider())  # lambda allows our function to be called separate from the Timer
    t.start()


def slickdeals_automate(h, m):
    print("sending your email at: %s:%s" % (h, m))
    x = datetime.today()
    y = x.replace(day=x.day + 1, hour=h, minute=m, second=0, microsecond=0)
    delta_t = y - x

    secs = delta_t.seconds + 1

    t = Timer(secs, lambda: slickdeals_spider())  # lambda allows our function to be called separate from the Timer
    t.start()


# starting menu
print("Which would you like to do?")
choice = input("""
    1. Run Menu
    2. Send me email of deals at a later time
    3. Exit
""")
if choice == "1":
    menu()
elif choice == "2":
    ebay_automate(15, 30)   # here you can put when to send the email
    slickdeals_automate(15, 30)
elif choice == "3":
    sys.exit
elif choice != "":
    print("\nNot a valid choice!")


## end code ##
