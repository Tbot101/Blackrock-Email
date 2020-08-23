import time
from datetime import datetime as dt
import pandas as pd
import requests
from bs4 import BeautifulSoup
import smtplib

URL = 'http://www.aastocks.com/en/funds/quote/quote.aspx?funds=1430'
price = 0
date = 0


def check_price():
    page = requests.get(URL)
    soup1 = BeautifulSoup(page.content, 'html.parser')
    soup2 = BeautifulSoup(soup1.prettify(), 'html.parser')
    global price
    price = soup2.find(attrs={'class': 'font26 bold'}).get_text()
    global date
    date = soup2.find(attrs={'class': 'rmk2 greya'}).get_text()
    print(price+" "+date)


check_price()

price1 = price.strip()
price2 = float(price1)
date1 = (date.strip())[15:25]
print(price1+" "+date1)


# analysis
sb = 1000  # stocks bought
pb = 10  # price bought
tav = int(sb*pb)  # total asset value
ttav = int(price2*sb)  # total asset value
pl = int(ttav) - int(tav)  # profit loss


def send_mail():

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login('SENDER EMAIL', 'EMAIL PASSWORD')
    subject = 'Blackrock World Energy Fund'
    body = '''Hello,
Today's data is from {0}
Today's Blackrock stock price is: {1}$
Today's profit/loss is: {2}$'''.format(date1, price2, pl)

    msg = f"Subject: {subject}\n\n{body}"

    server.sendmail(
        'SENDER EMAIL',
        ('RECEIVER EMAIL', 'RECEIVER EMAIL'),
        msg
    )
    print('Hey EMAIL has been sent!')
    server.quit()


send_mail()
