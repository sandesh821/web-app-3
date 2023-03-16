import requests #allows you to send HTTP requests
import pandas as pd
import smtplib
from flask import Flask,render_template,request,url_for,redirect

name=""
email=""
country=""
query=""


def fetchNews(name,country,query):
    Api_key="5210b1f82708404e851c6342df71b5ad"
    
    url = f"https://newsapi.org/v2/top-headlines?q={query}&country={country}&apiKey={Api_key}"

    main_page=requests.get(url).json()  

    articles=main_page["articles"]

    newsTitles=[]
    newsLinks=[]
    author=[]

    body=f"Hello {name}\n\nYour News is:\n"


    for a in articles:
        newsTitles.append(a["title"])
        newsLinks.append(a["url"])
        author.append(a["author"])
    
    noOfnews=5
    if(len(newsTitles) < 5):
         noOfnews=len(newsTitles)

    for i in range (noOfnews):
        print(f"{i+1} {newsTitles[i]}\n")
        body=body+newsTitles[i]+"\n\n"

    return body

def sendemail(MailId,body):

    sender='pranjalpjjain666@gmail.com'
    password="fxonczrqzsbfccfl"
    receiver=MailId
    subject='Daily News'
    
    connect= smtplib.SMTP_SSL("smtp.gmail.com",465)
    connect.login(user=sender,password=password)
    message=f"Subject :{subject}\n\n{body}"
    connect.sendmail(from_addr=sender,to_addrs=receiver,msg=message)
    print("E-mail sent Sucessfully")
    connect.close()
    return 



app=Flask(__name__)
@app.route("/",methods=["GET","POST"])
def getvalue():
    global name
    global email
    global country
    global query
    if request.method=="POST":
        name=request.form.get('Name')
        MailId=request.form.get("mail")
        country=request.form.get("Country")
        query=request.form.get("query")
        body=fetchNews(name,country,query)
        sendemail(MailId,body)
        return render_template("index.html",n=name,e=MailId)
    return render_template("mynews.html")

    
if __name__=='__main__':
        app.run(port=5500)
        

        



