import datetime

import requests
import json
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import passes


def getNewResp(login, apikey):
    resp = requests.get(
        "https://isod.ee.pw.edu.pl/isod-portal/wapi?q=mynewsfull&username={0}&apikey={1}&from=0&to=10".format(
            login, apikey))
    return resp


def getOldJson():
    f = open("last_news.isod", "r")
    try:
        last_resp = json.loads(f.read())
    except:
        last_resp = json.loads("""{"items":[{"hash":""}]}""")
    f.close()
    return last_resp


def writeToFile(resp: requests.Response):
    f = open("last_news.isod", "w")
    f.write(resp.text)
    f.close()


def sendUpdates(news: json, rec_email: str):
    global number_message
    news_block = str()
    smtp_server = "smtp.gmail.com"
    port = 587  # For starttls
    sender_email = passes.getFromEmail()
    password = passes.getPass()
    message = MIMEMultipart("alternative")
    if len(news) > 1:
        message["Subject"] = "{0} nowych powiadomień ISOD".format(len(news))
        number_message = "{0} powiadomień".format(len(news))
    else:
        message["Subject"] = "Nowe powiadomienie ISOD"
        number_message = "nowe powiadomienie"

    message["From"] = "Powiadomienia ISOD"
    message["To"] = rec_email

    for i in range(0, len(news)):
        news_block += """\
        <span>  
	    <p class="subject" style="font-weight: bold;">{0}</p>
	    <p class="not-significant-text">
			Data publikacji: <span class="date">{1}</span>, przez  <span class="date">{2}</span>
		</p>
		
	    <div class="noreset news-content">
	    	<p>{3}</p><br>
	    	
	    </div>
    
</span>
""".format(news[i]["subject"], news[i]["modifiedDate"], news[i]["modifiedBy"], news[i]["content"])

    html = """\
    <html>

      <body>
        <h2>Dodano {0} do ISOD:
        </h2>
        {1}
        
        <br><br><span style="font-style: italic">Wysłano automatycznie. Grzegorz Jewusiak {2} - <a href="https://jewusiak.pl">jewusiak.pl</a></span>
      </body>
    </html>
    """.format(number_message, news_block,datetime.date.today().year)

    # Turn these into plain/html MIMEText objects
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part2)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, rec_email, message.as_string()
        )
