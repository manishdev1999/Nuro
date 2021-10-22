from flask import Flask, request, render_template, redirect, session, url_for
from urllib.parse import quote
from requests import check_compatibility
from selenium import webdriver
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
import pyrebase
import urllib, hashlib
from flask_session import Session
from datetime import date
import csv
import os.path
import sys
import os
import shutil
import pandas as pd
import xlsxwriter
import random
import xlrd as xl 
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import requests 
from requests.structures import CaseInsensitiveDict
import json
import webbrowser
from threading import Timer
from textblob import TextBlob



app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
application_path = os.path.dirname(sys.executable)


config = {
"apiKey": "AIzaSyARJHP1fE9QkiPzk8NGzll-jh9mvbQc2IM",
  "authDomain": "whato-7a8ed.firebaseapp.com",
  "projectId": "whato-7a8ed",
  "storageBucket": "whato-7a8ed.appspot.com",
  "messagingSenderId": "918836431687",
  "appId": "1:918836431687:web:11cd51524b100085939a62",
  "measurementId": "G-LW200LFV7E",
  "databaseURL": "https://whato-7a8ed-default-rtdb.asia-southeast1.firebasedatabase.app/",

}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

@app.route('/')
def home():
    if not os.path.exists("C:/Whato"):
        os.mkdir("C:/Whato/")
        os.mkdir("C:/Whato/documents/")
        os.mkdir("C:/Whato/documents/data")
        os.mkdir("C:/Whato/images/")
        os.mkdir("C:/Whato/images/data")
        os.mkdir("C:/Whato/message/")
        os.mkdir("C:/Whato/message/data")
        os.mkdir("C:/Whato/pdf/")
        os.mkdir("C:/Whato/pdf/data")
        os.mkdir("C:/Whato/video/")
        os.mkdir("C:/Whato/video/data")
        os.mkdir("C:/Whato/dynamic/")
        os.mkdir("C:/Whato/dynamic/imagedynamic")  
        os.mkdir("C:/Whato/dynamic/imagedynamic/data")  
        os.mkdir("C:/Whato/dynamic/videodynamic")  
        os.mkdir("C:/Whato/dynamic/videodynamic/data") 
        os.mkdir("C:/Whato/dynamic/docdynamic")  
        os.mkdir("C:/Whato/dynamic/docdynamic/data")  
        os.mkdir("C:/Whato/dynamic/messagedynamic")  
        os.mkdir("C:/Whato/dynamic/messagedynamic/data")        
    
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if not session.get("user"):
        if (request.method == 'POST'):
                email = request.form['username']
                password = request.form['password']
                
                try:
                    user = auth.sign_in_with_email_and_password(email, password)
                    cc = auth.get_account_info(user['idToken'])
                    usr  = cc['users'][0]['localId']
                    session["user"] = usr
                    return redirect('/dashboard')
                    # return render_template('dashboard.html')
                except:
                    unsuccessful = 'Please check your credentials'
                    return render_template('login.html', umessage=unsuccessful)
        return render_template('login.html')
    else:

        return redirect('/dashboard')

@app.route('/forgotpassword', methods=['GET', 'POST'])
def forgotpassword():
    if (request.method == 'POST'):
            email = request.form['username']
            auth.send_password_reset_email(email)
            return render_template('login.html')
          
    return render_template('forgot.html')

@app.route('/contactus', methods=['GET', 'POST'])
def contactus():
    if (request.method == 'POST'):
            name = request.form['name']
            email = request.form['email']
            phone = request.form['phone']
            look = request.form['look']
            message = 'Hey,\nI am' + str(name) + '\n*My Email* : '  + str(email) + '\nMy Phone : ' + str(phone) + '\nI am here for : ' + str(look) + '\nThanks.'
            message = quote(message)
            url = 'https://web.whatsapp.com/send?phone=+917598308018&text=' + message
            return redirect(url, code=302)
           
    return render_template('contact.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if (request.method == 'POST'):
            name = request.form['name']
            email = request.form['email']
            phone = request.form['phone']
            password = request.form['password']
            today = date.today()
            today = str(today)
            user = auth.create_user_with_email_and_password(email, password)
            cc = auth.get_account_info(user['idToken'])
            ukey = cc['users'][0]['localId']
            result = hashlib.md5(email.encode("utf-8")).hexdigest()
            gravatar_url = "https://www.gravatar.com/avatar/" + str(result)
            number = random.randint(1000,9999)
            data = {
                "name": name,
                "email": email,
                "phone": phone,
                "profileURL" : gravatar_url,
                "pack" : "100",
                "date" : today,
                "cardid": number

                }

            
            db.child("users").child(ukey).set(data)
            db.child("users").child(ukey).child("campaigns")


           
    return render_template('register.html')

@app.route("/refferal")
def refer():
    if not session.get("user"):
        return redirect("/login")
    else:
        onUser = session['user']
        onUser = str(onUser)
        userData = db.child("users").child(onUser).get()
        userKey = db.child("users").child(onUser).get()
        userData = userData.val()
        key = userKey.key()
        referal = "Hey, I would love to introduce you to WHATO .WHATO enables you with the new power of supremacy through enhanced campaigns on WhatsApp" + "\n" + "Please Use my Refferal during Sign Up  :  " + key
    return render_template("refferal.html", currentUser=userData, key=key, referal = referal)


@app.route("/logout")
def logout():
    session["user"] = None
    return redirect("/dashboard")

    
@app.route("/dashboard")
def dashboard():
    if not session.get("user"):
        return redirect("/login")
    else:
        onUser = session['user']
        onUser = str(onUser)
        userData = db.child("users").child(onUser).get()
        userKey = db.child("users").child(onUser).get()
        userData = userData.val()
        key = userKey.key()
        return  render_template('dashboard.html' , currentUser=userData, key=key)

    return render_template('dashboard.html' , currentUser=userData)

@app.route('/connect', methods=['GET', 'POST'])
def connect():
    if not session.get("user"):
        return redirect("/login")
    else:
        onUser = session['user']
        onUser = str(onUser)
        userData = db.child("users").child(onUser).get()
        userData = userData.key()
        if (request.method == 'POST'):
            balance = request.form['balance']
        message = "Recharge   " + userData + "  for   " + balance
        url = "https://web.whatsapp.com/send?phone=917598308018""&text=" + message
    return redirect(url)



@app.route('/recharge/manishdev1999@gmail.com/5FC8ED73E38FDCCD961CFE322CE9D/<id>/<amount>')
def rechargecard(id,amount):
    if not session.get("user"):
        return redirect("/login")
    else:
        onUser = session['user']
        onUser = str(onUser)
        userData = db.child("users").child(id).get()
        userData = userData.val()
        currentamount = userData['pack']
        currentamount = int(currentamount)
        amount = int(amount)
        credits = amount * 4
        updatedamount = currentamount + credits
        data = {
            "pack" : updatedamount
        }
        userData = db.child("users").child(id).update(data)

        return "successfully recharged"

    return render_template('messagecampaign.html' , currentUser=userData)
#campaigns 

@app.route('/messagecampaign' , methods=['GET', 'POST'])
def messagecampaign():
    if not session.get("user"):
        return redirect("/login")
    else:
        today = date.today()
        today = str(today)
        onUser = session['user']
        onUser = str(onUser)
        userData = db.child("users").child(onUser).get()
        userData = userData.val()
        if (request.method == 'POST'):
            name = request.form['name']
            tagline = request.form['tagline']
            message = request.form['message']
            edu = TextBlob(message)
            print(edu)
            number = edu.sentiment.polarity
            number = number * 100
            if(number<0):
                number = 100 + number
            else:
                number = number
            save_path = 'C:/Whato/message/data'
            completeName = os.path.join(save_path, name+".txt")         
            file1 = open(completeName, "w")
            file1.close()
            datas = {
               
                    "name": name,
                    "location": name,
                    "date": today,
                    "tagline" : tagline,
                    "analysis" : number,
                    "status"    : "Active",
                    "number"    : "",
                    "success"   : "",
                    "failed"    : "",
                    "type"      : "message",
                    "message"   : message,
                    "path"      : "/message",
                    "sp"   : "0",
                    "fp"      : "0",
                    "op"    : "0"
                
                }      

            print(datas)
        
            db.child("users").child(onUser).child("campaign").push(datas)
            return redirect("/dashboard")
        
        return  render_template('messagecampaign.html', currentUser=userData)

    return render_template('messagecampaign.html' , currentUser=userData)

@app.route('/mediacampaign' , methods=['GET', 'POST'])
def mediacampaign():
    if not session.get("user"):
        return redirect("/login")
    else:
        today = date.today()
        today = str(today)
        onUser = session['user']
        onUser = str(onUser)
        userData = db.child("users").child(onUser).get()
        userData = userData.val()
        if (request.method == 'POST'):
            name = request.form['name']
            tagline = request.form['tagline']
            filename = request.form['filename']
            message = request.form['message']
            edu = TextBlob(message)
            print(edu)
            number = edu.sentiment.polarity
            number = number * 100
            if(number<0):
                number = 100 + number
            else:
                number = number
            save_path = 'C:/Whato/images/data'
            completeName = os.path.join(save_path, name+".txt")         
            file1 = open(completeName, "w")
            file1.close()
            datas = {
               
                    "name": name,
                    "location": name,
                    "date": today,
                    "tagline" : tagline,
                    "analysis" : number,
                    "status"    : "Active",
                    "number"    : "",
                    "success"   : "",
                    "failed"    : "",
                    "type"      : "images",
                    "message"   : message,
                    "path"      : "/message",
                    "sp"   : "",
                    "fp"      : "",
                    "op"    : "",
                    "mediaurl" : filename
                
                }        
        
            db.child("users").child(onUser).child("campaign").push(datas)
            return redirect("/dashboard")

        return  render_template('mediacampaign.html', currentUser=userData)

    return render_template('mediacampaign.html' , currentUser=userData)

@app.route('/videocampaign', methods=['GET', 'POST'])
def videocampaign():
    if not session.get("user"):
        return redirect("/login")
    else:
        today = date.today()
        today = str(today)
        onUser = session['user']
        onUser = str(onUser)
        userData = db.child("users").child(onUser).get()
        userData = userData.val()
        if (request.method == 'POST'):
            name = request.form['name']
            tagline = request.form['tagline']
            filename = request.form['filename']
            message = request.form['message']
            edu = TextBlob(message)
            print(edu)
            number = edu.sentiment.polarity
            number = number * 100
            if(number<0):
                number = 100 + number
            else:
                number = number
            save_path = 'C:/Whato/video/data'
            completeName = os.path.join(save_path, name+".txt")         
            file1 = open(completeName, "w")
            file1.close()
            datas = {
               
                    "name": name,
                    "location": name,
                    "date": today,
                    "tagline" : tagline,
                    "analysis" : number,
                    "status"    : "Active",
                    "number"    : "",
                    "success"   : "",
                    "failed"    : "",
                    "type"      : "video",
                    "message"   : message,
                    "path"      : "/message",
                    "sp"   : "",
                    "fp"      : "",
                    "op"    : "",
                    "mediaurl" : filename
                
                }        
        
            db.child("users").child(onUser).child("campaign").push(datas)
            return redirect("/dashboard")

        return  render_template('videocampaign.html', currentUser=userData)

    return render_template('videocampaign.html' , currentUser=userData)

@app.route('/documentcampaign' , methods=['GET', 'POST'])
def reportcampaign():
    if not session.get("user"):
        return redirect("/login")
    else:
        today = date.today()
        today = str(today)
        onUser = session['user']
        onUser = str(onUser)
        userData = db.child("users").child(onUser).get()
        userData = userData.val()
        if (request.method == 'POST'):
            name = request.form['name']
            tagline = request.form['tagline']
            filename = request.form['filename']
            save_path = 'C:/Whato/documents/data'
            completeName = os.path.join(save_path, name+".txt") 
            print(completeName)        
            file1 = open(completeName, "w")
            file1.close()
            datas = {
               
                    "name": name,
                    "location": name,
                    "date": today,
                    "tagline" : tagline,
                    "analysis" : "0",
                    "status"    : "Active",
                    "number"    : "",
                    "success"   : "",
                    "failed"    : "",
                    "type"      : "documents",
                    "path"      : "/documents",
                    "sp"   : "",
                    "fp"      : "",
                    "op"    : "",
                    "mediaurl" : filename
                
                }        
        
            db.child("users").child(onUser).child("campaign").push(datas)
            return redirect("/dashboard")

        return  render_template('documentcampaign.html', currentUser=userData)

    return render_template('reportcampaign.html' , currentUser=userData)

@app.route('/imagedynamiccampaign', methods=['GET', 'POST'])
def imagedynamiccampaign():
    if not session.get("user"):
        return redirect("/login")
    else:
        today = date.today()
        today = str(today)
        onUser = session['user']
        onUser = str(onUser)
        userData = db.child("users").child(onUser).get()
        userData = userData.val()
        if (request.method == 'POST'):
            name = request.form['name']
            tagline = request.form['tagline']
            message = request.form['message']
            edu = TextBlob(message)
            print(edu)
            number = edu.sentiment.polarity
            number = number * 100
            if(number<0):
                number = 100 + number
            else:
                number = number
            save_path = 'C:/Whato/dynamic/imagedynamic/data'
            completeName = os.path.join(save_path, name+".xlsx")  
            workbook = xlsxwriter.Workbook(completeName)
            worksheet = workbook.add_worksheet()
            worksheet.write('A1', 'name')
            worksheet.write('B1', 'phone')
            worksheet.write('C1', 'amt1')
            worksheet.write('D1', 'amt2')
            worksheet.write('E1', 'amt3')
            worksheet.write('F1', 'mark1')
            worksheet.write('G1', 'mark2')
            worksheet.write('H1', 'mark3')
            worksheet.write('I1', 'mark4')
            worksheet.write('J1', 'mark5')
            worksheet.write('K1', 'total')
            worksheet.write('L1', 'orderid')
            worksheet.write('M1', 'ordername')
            worksheet.write('N1', 'status')
            worksheet.write('O1', 'file')
            workbook.close()

            # file1 = open(completeName, "w", header=headerList)
            # file1.close()
            datas = {
               
                    "name": name,
                    "location": name,
                    "date": today,
                    "tagline" : tagline,
                    "analysis" : number,
                    "status"    : "Active",
                    "number"    : "",
                    "success"   : "",
                    "failed"    : "",
                    "type"      : "imagedynamic",
                    "message"   : message,
                    "path"      : "/imagedynamiccampaign",
                    "sp"   : "",
                    "fp"      : "",
                    "op"    : "",
                
                }        
        
            db.child("users").child(onUser).child("campaign").push(datas)
            return redirect("/dashboard")

        return  render_template('dynamiccampaign.html', currentUser=userData)

@app.route('/videodynamiccampaign', methods=['GET', 'POST'])
def videodynamiccampaign():
    if not session.get("user"):
        return redirect("/login")
    else:
        today = date.today()
        today = str(today)
        onUser = session['user']
        onUser = str(onUser)
        userData = db.child("users").child(onUser).get()
        userData = userData.val()
        if (request.method == 'POST'):
            name = request.form['name']
            tagline = request.form['tagline']
            message = request.form['message']
            edu = TextBlob(message)
            print(edu)
            number = edu.sentiment.polarity
            number = number * 100
            if(number<0):
                number = 100 + number
            else:
                number = number
            save_path = 'C:/Whato/dynamic/videodynamic/data'
            completeName = os.path.join(save_path, name+".xlsx")  
            workbook = xlsxwriter.Workbook(completeName)
            worksheet = workbook.add_worksheet()
            worksheet.write('A1', 'name')
            worksheet.write('B1', 'phone')
            worksheet.write('C1', 'amt1')
            worksheet.write('D1', 'amt2')
            worksheet.write('E1', 'amt3')
            worksheet.write('F1', 'mark1')
            worksheet.write('G1', 'mark2')
            worksheet.write('H1', 'mark3')
            worksheet.write('I1', 'mark4')
            worksheet.write('J1', 'mark5')
            worksheet.write('K1', 'total')
            worksheet.write('L1', 'orderid')
            worksheet.write('M1', 'ordername')
            worksheet.write('N1', 'status')
            worksheet.write('O1', 'file')
            workbook.close()

            # file1 = open(completeName, "w", header=headerList)
            # file1.close()
            datas = {
               
                    "name": name,
                    "location": name,
                    "date": today,
                    "tagline" : tagline,
                    "analysis" : number,
                    "status"    : "Active",
                    "number"    : "",
                    "success"   : "",
                    "failed"    : "",
                    "type"      : "videodynamic",
                    "message"   : message,
                    "path"      : "/videodynamiccampaign",
                    "sp"   : "",
                    "fp"      : "",
                    "op"    : "",
                
                }        
        
            db.child("users").child(onUser).child("campaign").push(datas)
            return redirect("/dashboard")

        return  render_template('videodynamiccampaign.html', currentUser=userData)

@app.route('/docdynamiccampaign', methods=['GET', 'POST'])
def docdynamiccampaign():
    if not session.get("user"):
        return redirect("/login")
    else:
        today = date.today()
        today = str(today)
        onUser = session['user']
        onUser = str(onUser)
        userData = db.child("users").child(onUser).get()
        userData = userData.val()
        if (request.method == 'POST'):
            name = request.form['name']
            tagline = request.form['tagline']
            message = request.form['message']
            edu = TextBlob(message)
            print(edu)
            number = edu.sentiment.polarity
            number = number * 100
            if(number<0):
                number = 100 + number
            else:
                number = number

            save_path = 'C:/Whato/dynamic/docdynamic/data'
            completeName = os.path.join(save_path, name+".xlsx")  
            workbook = xlsxwriter.Workbook(completeName)
            worksheet = workbook.add_worksheet()
            worksheet.write('A1', 'name')
            worksheet.write('B1', 'phone')
            worksheet.write('C1', 'amt1')
            worksheet.write('D1', 'amt2')
            worksheet.write('E1', 'amt3')
            worksheet.write('F1', 'mark1')
            worksheet.write('G1', 'mark2')
            worksheet.write('H1', 'mark3')
            worksheet.write('I1', 'mark4')
            worksheet.write('J1', 'mark5')
            worksheet.write('K1', 'total')
            worksheet.write('L1', 'orderid')
            worksheet.write('M1', 'ordername')
            worksheet.write('N1', 'status')
            worksheet.write('O1', 'file')
            workbook.close()

            # file1 = open(completeName, "w", header=headerList)
            # file1.close()
            datas = {
               
                    "name": name,
                    "location": name,
                    "date": today,
                    "tagline" : tagline,
                    "analysis" : number,
                    "status"    : "Active",
                    "number"    : "",
                    "success"   : "",
                    "failed"    : "",
                    "type"      : "docdynamic",
                    "message"   : message,
                    "path"      : "/docdynamiccampaign",
                    "sp"   : "",
                    "fp"      : "",
                    "op"    : "",
                
                }        
        
            db.child("users").child(onUser).child("campaign").push(datas)
            return redirect("/dashboard")

        return  render_template('docdynamiccampaign.html', currentUser=userData)

@app.route('/messagedynamiccampaign', methods=['GET', 'POST'])
def messagedynamiccampaign():
    if not session.get("user"):
        return redirect("/login")
    else:
        today = date.today()
        today = str(today)
        onUser = session['user']
        onUser = str(onUser)
        userData = db.child("users").child(onUser).get()
        userData = userData.val()
        if (request.method == 'POST'):
            name = request.form['name']
            tagline = request.form['tagline']
            message = request.form['message']
            edu = TextBlob(message)
            print(edu)
            number = edu.sentiment.polarity
            number = number * 100
            if(number<0):
                number = 100 + number
            else:
                number = number
            save_path = 'C:/Whato/dynamic/messagedynamic/data'
            completeName = os.path.join(save_path, name+".xlsx")  
            workbook = xlsxwriter.Workbook(completeName)
            worksheet = workbook.add_worksheet()
            worksheet.write('A1', 'name')
            worksheet.write('B1', 'phone')
            worksheet.write('C1', 'amt1')
            worksheet.write('D1', 'amt2')
            worksheet.write('E1', 'amt3')
            worksheet.write('F1', 'mark1')
            worksheet.write('G1', 'mark2')
            worksheet.write('H1', 'mark3')
            worksheet.write('I1', 'mark4')
            worksheet.write('J1', 'mark5')
            worksheet.write('K1', 'total')
            worksheet.write('L1', 'orderid')
            worksheet.write('M1', 'ordername')
            worksheet.write('N1', 'status')
            worksheet.write('O1', 'file')
            workbook.close()

            # file1 = open(completeName, "w", header=headerList)
            # file1.close()
            datas = {
               
                    "name": name,
                    "location": name,
                    "date": today,
                    "tagline" : tagline,
                    "analysis" : number,
                    "status"    : "Active",
                    "number"    : "",
                    "success"   : "",
                    "failed"    : "",
                    "type"      : "messagedynamic",
                    "message"   : message,
                    "path"      : "/messagedynamiccampaign",
                    "sp"   : "",
                    "fp"      : "",
                    "op"    : "",
                
                }        
        
            db.child("users").child(onUser).child("campaign").push(datas)
            return redirect("/dashboard")

        return  render_template('messagedynamiccampaign.html', currentUser=userData)

@app.route('/insights/<id>')
def insights(id):
    if not session.get("user"):
        return redirect("/login")
    else:
     
        onUser = session['user']
        onUser = str(onUser)
        loginData = db.child("users").child(onUser).get()
        loginData = loginData.val()
        userData = db.child("users").child(onUser).child("campaign").child(id).get()
        userData = userData.val()
        typeof = userData['type']
        typeof = str(typeof)
        path = userData['location']
        numbers = []
        if (typeof == "messagedynamic" or typeof == "imagedynamic" or typeof == "videodynamic" or typeof == "docdynamic"):
            location = "C:/Whato/dynamic/"+ str(typeof) +"/data/" + str(path) + ".xlsx"
            xls = pd.ExcelFile(location)  
            sheetX = xls.parse(0) 
            i = 0
            count = 0
            for i,row in sheetX.iterrows():
                    count = count + 1
            total_number = count
      
        else:
            location = "C:/Whato/"+ str(typeof) +"/data/" + str(path) + ".txt"
            location = str(location)
            print(location)
            f = open(location, "r")
            for line in f.read().splitlines():
                if line != "":
                    numbers.append(line)
            f.close()
            total_number=len(numbers)
            total_number = str(total_number)

        update = {
                 
                 "number"    : total_number,

        }
        userData = db.child("users").child(onUser).child("campaign").child(id).update(update)
        userData = db.child("users").child(onUser).child("campaign").child(id).get()
        userData = userData.val()
        return  render_template('graphs.html' , currentUser=userData, loginData = loginData, id=id)
    
    return render_template('graphs.html')


@app.route('/insights/message/<id>')
def message(id):
    onUser = session['user']
    onUser = str(onUser)
    userData = db.child("users").child(onUser).child("campaign").child(id).get()
    userData = userData.val()
    message = userData['message']
    message = str(message)
    path = userData['location']
    path = str(path)
    packdetails = db.child("users").child(onUser).get()
    packdetails = packdetails.val()
    pack = packdetails['pack']
    pack = int(pack)
    numbers = []
    location = "C:/Whato/message/data/" + path + ".txt"
    errlocation = "C:/Whato/message/data/" + path + "error.txt"
    f = open(location, "r")
    for line in f.read().splitlines():
        if line != "":
            numbers.append(line)
    f.close()
    total_number=len(numbers)
    total_number = int(total_number)
    pointreq = total_number * 1
    pointreq = int(pointreq)
    if(int(pack) < int(pointreq)):
        return redirect('/error/Please Recharge your Credit ')
    else:
        updatedamount = pack - pointreq
        updatedamount = int(updatedamount)
        uppack = {
            "pack" : updatedamount,
        }
        db.child("users").child(onUser).update(uppack)
        count = 1
        success = 0
        failed = 0
        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.get('https://web.whatsapp.com/')
        sleep(20)
        for idx, number in enumerate(numbers):
            number = number.strip()
            if number == "":
                    continue
            try:
                    url = "https://web.whatsapp.com/send?phone=" + number + "&text=" + message
                    driver.get(url)
                    sleep(5)
                    button = driver.find_element_by_class_name('_4sWnG')
                    button.click()
                    sleep(5)

                    success = success + 1
            except Exception as e:
                    f = open(errlocation, "a")
                    f.write('Failed to send message to ' + number + '\n')
                    failed = failed + 1

        sp = (success/total_number)*100
        fp = (failed/total_number)*100
        op = ((success-failed)/total_number)*100
        op = abs(op)
        
        update = {
                    
                "success"    : success,
                "failed"    :  failed,
                "status"    : "Completed",
                "sp"    : sp,
                "fp"    : fp,
                "op"    : op
                

            }
        userData = db.child("users").child(onUser).child("campaign").child(id).update(update)
        driver.quit()
    return redirect('/insights/'+id)

@app.route('/insights/images/<id>')
def images(id):
    onUser = session['user']
    onUser = str(onUser)
    userData = db.child("users").child(onUser).child("campaign").child(id).get()
    userData = userData.val()
    message = userData['message']
    message = str(message)
    path = userData['location']
    path = str(path)
    packdetails = db.child("users").child(onUser).get()
    packdetails = packdetails.val()
    pack = packdetails['pack']
    pack = int(pack)
    mediaurl = userData['mediaurl']
    mediaurl = str(mediaurl)
    numbers = []
    location = "C:/Whato/images/data/" + path + ".txt"
    errlocation = "C:/Whato/images/data/" + path + "error.txt"
    f = open(location, "r")
    for line in f.read().splitlines():
        if line != "":
            numbers.append(line)
    f.close()
    total_number=len(numbers)
    total_number = int(total_number)
    pointreq = total_number * 2
    pointreq = int(pointreq)

    if(int(pack) < int(pointreq)):
        return redirect('/error/Please Recharge your Credit ')
    else:
        updatedamount = pack - pointreq
        updatedamount = int(updatedamount)
        uppack = {
            "pack" : updatedamount,
        }
        db.child("users").child(onUser).update(uppack)
        count = 1
        success = 0
        failed = 0
        driver = webdriver.Chrome(ChromeDriverManager().install())
        # driver = webdriver.Chrome('C:/Whato/chromedriver')
        driver.get('https://web.whatsapp.com/')
        sleep(20)
        for idx, number in enumerate(numbers):
            number = number.strip()
            if number == "":
                    continue
            try:
                    url = "https://web.whatsapp.com/send?phone=" + number + "&text=" + message
                    driver.get(url)
                    sleep(5)
                    button = driver.find_element_by_class_name('_2jitM')
                    button.click()
                    sleep(1)
                    doc = driver.find_element_by_xpath('//input[@accept="image/*,video/mp4,video/3gpp,video/quicktime"]')
                    doc.send_keys("C:/Whato/images/"+ mediaurl)
                    sleep(7)
                    final = driver.find_element_by_class_name('_1w1m1')
                    final.click()
                    sleep(7)
                    success = success + 1
            except Exception as e:
                    f = open(errlocation, "a")
                    f.write('Failed to send message to ' + number + '\n')
                    failed = failed + 1

    sp = (success/total_number)*100
    fp = (failed/total_number)*100
    op = ((success-failed)/total_number)*100
    op = abs(op)
    update = {
                 
            "success"    : success,
            "failed"    :  failed,
            "status"    : "Completed",
            "sp"    : sp,
            "fp"    : fp,
            "op"    : op
            

        }
    userData = db.child("users").child(onUser).child("campaign").child(id).update(update)
    driver.quit()
    return redirect('/insights/'+id)


@app.route('/insights/imagedynamic/<id>')
def dynamicimages(id):
    onUser = session['user']
    onUser = str(onUser)
    userData = db.child("users").child(onUser).child("campaign").child(id).get()
    userData = userData.val()
    message = userData['message']
    path = userData['location']
    total_number = userData['number']
    packdetails = db.child("users").child(onUser).get()
    packdetails = packdetails.val()
    pack = packdetails['pack']
    pack = int(pack)
    total_number = int(total_number)
    pointreq = total_number * 4
    pointreq = int(pointreq)
    if(int(pack) < int(pointreq)):
        return redirect('/error/Please Recharge your Credit ')
    else:
        updatedamount = pack - pointreq
        updatedamount = int(updatedamount)
        uppack = {
            "pack" : updatedamount,
        }
        db.child("users").child(onUser).update(uppack)
        print("i am up")
        location = "C:/Whato/dynamic/imagedynamic/data/"+ path +".xlsx"
        errlocation = "C:/Whato/dynamic/imagedynamic/data/" + path + "error.txt"
        print("i am up 1")
        xls = pd.ExcelFile(location)  
        print("i am up 2")
        sheetX = xls.parse(0) 
        name = sheetX['name']
        amt1 = sheetX['amt1']
        amt2 = sheetX['amt2']
        amt3 = sheetX['amt3']
        mark1 = sheetX['mark1']
        mark2 = sheetX['mark2']
        mark3 = sheetX['mark3']
        mark4 = sheetX['mark4']
        mark5 = sheetX['mark5']
        total = sheetX['total']
        orderid = sheetX['orderid']
        ordername = sheetX['ordername']
        status = sheetX['status']
        phone = sheetX['phone']
        file = sheetX['file']
        i = 0
        check = message
        success = 0
        failed = 0
        driver = webdriver.Chrome(ChromeDriverManager().install())
        # driver = webdriver.Chrome('C:/Whato/chromedriver')
        driver.get('https://web.whatsapp.com/')
        sleep(10)
        count = 0
        for i,row in sheetX.iterrows():
                count = count + 1
                try:    
                        message = check
                        message = message.replace('+ name', str(name[i]))
                        message = message.replace('+ amt1', str(amt1[i]))
                        message = message.replace('+ amt2',str(amt2[i]))
                        message = message.replace('+ amt3',str(amt3[i]))
                        message = message.replace('+ mark1',str(mark1[i]))
                        message = message.replace('+ mark2',str(mark2[i]))
                        message = message.replace('+ mark3',str(mark3[i]))
                        message = message.replace('+ mark4',str(mark4[i]))
                        message = message.replace('+ mark5',str(mark5[i]))
                        message = message.replace('+ total',str(total[i]))
                        message = message.replace('+ orderid',str(orderid[i]))
                        message = message.replace('+ ordername',str(ordername[i]))
                        message = message.replace('+ status',str(status[i]))
                        finalurl = "https://web.whatsapp.com/send?phone=" + str(phone[i]) + "&text=" + message
                        print(finalurl)  
                        driver.get(finalurl)
                        sleep(7)
                        button = driver.find_element_by_class_name('_2jitM')
                        button.click()
                        sleep(1)
                        doc = driver.find_element_by_xpath('//input[@accept ="image/*,video/mp4,video/3gpp,video/quicktime"]')
                        doc.send_keys("C:/Whato/dynamic/imagedynamic/"+ str(file[i]))
                        sleep(7)
                        final = driver.find_element_by_class_name('_1w1m1')
                        final.click()
                        sleep(7)
                        success = success + 1
                except Exception as e:
                        f = open(errlocation, "a")
                        f.write('Failed to send message to ' + str(phone[i]) + '\n')
                        failed = failed + 1

    sp = (success/count)*100
    fp = (failed/count)*100
    op = ((success-failed)/count)*100
    if(op == 0):
        op = 100
    op = abs(op)

    update = {
                 
            "success"    : success,
            "failed"    :  failed,
            "status"    : "Completed",
            "sp"    : sp,
            "fp"    : fp,
            "op"    : op

        }
    userData = db.child("users").child(onUser).child("campaign").child(id).update(update)
    driver.quit()
    return redirect('/insights/'+id)

@app.route('/error/<error>')
def exeception(error):
    if not session.get("user"):
        return redirect("/login")
    else:
     
        onUser = session['user']
        onUser = str(onUser)
        loginData = db.child("users").child(onUser).get()
        loginData = loginData.val()
        userData = db.child("users").child(onUser).child("campaign").child(id).get()
        userData = userData.val()
    return render_template("errors.html", currentUser=userData, loginData = loginData, id=id, error=error)

@app.route('/insights/videodynamic/<id>')
def videodynamicimages(id):
    onUser = session['user']
    onUser = str(onUser)
    userData = db.child("users").child(onUser).child("campaign").child(id).get()
    userData = userData.val()
    message = userData['message']
    path = userData['location']
    total_number = userData['number']
    packdetails = db.child("users").child(onUser).get()
    packdetails = packdetails.val()
    pack = packdetails['pack']
    pack = int(pack)
    total_number = int(total_number)
    pointreq = total_number * 4
    pointreq = int(pointreq)
    if(int(pack) < int(pointreq)):
        return redirect('/error/Please Recharge your Credit ')
    else:
        updatedamount = pack - pointreq
        updatedamount = int(updatedamount)
        uppack = {
            "pack" : updatedamount,
        }
        db.child("users").child(onUser).update(uppack)
        location = "C:/Whato/dynamic/videodynamic/data/"+ path +".xlsx"
        errlocation = "C:/Whato/dynamic/videodynamic/data/" + path + "error.txt"
        xls = pd.ExcelFile(location)  
        sheetX = xls.parse(0) 
        name = sheetX['name']
        amt1 = sheetX['amt1']
        amt2 = sheetX['amt2']
        amt3 = sheetX['amt3']
        mark1 = sheetX['mark1']
        mark2 = sheetX['mark2']
        mark3 = sheetX['mark3']
        mark4 = sheetX['mark4']
        mark5 = sheetX['mark5']
        total = sheetX['total']
        orderid = sheetX['orderid']
        ordername = sheetX['ordername']
        status = sheetX['status']
        phone = sheetX['phone']
        file = sheetX['file']
        i = 0
        check = message
        success = 0
        failed = 0
        driver = webdriver.Chrome(ChromeDriverManager().install())
        # driver = webdriver.Chrome('C:/Whato/chromedriver')
        driver.get('https://web.whatsapp.com/')
        sleep(10)
        count = 0
        for i,row in sheetX.iterrows():
                count = count + 1
                try:    
                        message = check
                        message = message.replace('+ name', str(name[i]))
                        message = message.replace('+ amt1', str(amt1[i]))
                        message = message.replace('+ amt2',str(amt2[i]))
                        message = message.replace('+ amt3',str(amt3[i]))
                        message = message.replace('+ mark1',str(mark1[i]))
                        message = message.replace('+ mark2',str(mark2[i]))
                        message = message.replace('+ mark3',str(mark3[i]))
                        message = message.replace('+ mark4',str(mark4[i]))
                        message = message.replace('+ mark5',str(mark5[i]))
                        message = message.replace('+ total',str(total[i]))
                        message = message.replace('+ orderid',str(orderid[i]))
                        message = message.replace('+ ordername',str(ordername[i]))
                        message = message.replace('+ status',str(status[i]))
                        finalurl = "https://web.whatsapp.com/send?phone=" + str(phone[i]) + "&text=" + message
                        print(finalurl)  
                        driver.get(finalurl)
                        sleep(5)
                        button = driver.find_element_by_class_name('_2jitM')
                        button.click()
                        sleep(1)
                        doc = driver.find_element_by_xpath('//input[@accept ="image/*,video/mp4,video/3gpp,video/quicktime"]')
                        doc.send_keys("C:/Whato/dynamic/videodynamic/"+ str(file[i]))
                        sleep(10)
                        final = driver.find_element_by_class_name('_1w1m1')
                        final.click()
                        sleep(10)
                        success = success + 1
                except Exception as e:
                        f = open(errlocation, "a")
                        f.write('Failed to send message to ' + str(phone[i]) + '\n')
                        failed = failed + 1

    sp = (success/count)*100
    fp = (failed/count)*100
    op = ((success-failed)/count)*100
    if(op == 0):
        op = 100
    op = abs(op)
    update = {
                 
            "success"    : success,
            "failed"    :  failed,
            "status"    : "Completed",
            "sp"    : sp,
            "fp"    : fp,
            "op"    : op
            

        }
    userData = db.child("users").child(onUser).child("campaign").child(id).update(update)
    driver.quit()
    return redirect('/insights/'+id)

@app.route('/insights/messagedynamic/<id>')
def messagedynamic(id):
    onUser = session['user']
    onUser = str(onUser)
    userData = db.child("users").child(onUser).child("campaign").child(id).get()
    userData = userData.val()
    message = userData['message']
    path = userData['location']
    total_number = userData['number']
    packdetails = db.child("users").child(onUser).get()
    packdetails = packdetails.val()
    pack = packdetails['pack']
    pack = int(pack)
    total_number = int(total_number)
    pointreq = total_number * 2
    pointreq = int(pointreq)
    if(int(pack) < int(pointreq)):
        return redirect('/error/Please Recharge your Credit ')
    else:
        updatedamount = pack - pointreq
        updatedamount = int(updatedamount)
        uppack = {
            "pack" : updatedamount,
        }
        db.child("users").child(onUser).update(uppack)
        location = "C:/Whato/dynamic/messagedynamic/data/"+ path +".xlsx"
        errlocation = "C:/Whato/dynamic/messagedynamic/data/" + path + "error.txt"        
        xls = pd.ExcelFile(location)  
        sheetX = xls.parse(0) 
        name = sheetX['name']
        amt1 = sheetX['amt1']
        amt2 = sheetX['amt2']
        amt3 = sheetX['amt3']
        mark1 = sheetX['mark1']
        mark2 = sheetX['mark2']
        mark3 = sheetX['mark3']
        mark4 = sheetX['mark4']
        mark5 = sheetX['mark5']
        total = sheetX['total']
        orderid = sheetX['orderid']
        ordername = sheetX['ordername']
        status = sheetX['status']
        phone = sheetX['phone']
        file = sheetX['file']
        i = 0
        check = message
        success = 0
        failed = 0
        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.get('https://web.whatsapp.com/')
        sleep(10)
        count = 0
        for i,row in sheetX.iterrows():
                count = count + 1
                try:    
                        message = check
                        message = message.replace('"', '')
                        message = message.replace('+ name', str(name[i]))
                        message = message.replace('+ amt1', str(amt1[i]))
                        message = message.replace('+ amt2',str(amt2[i]))
                        message = message.replace('+ amt3',str(amt3[i]))
                        message = message.replace('+ mark1',str(mark1[i]))
                        message = message.replace('+ mark2',str(mark2[i]))
                        message = message.replace('+ mark3',str(mark3[i]))
                        message = message.replace('+ mark4',str(mark4[i]))
                        message = message.replace('+ mark5',str(mark5[i]))
                        message = message.replace('+ total',str(total[i]))
                        message = message.replace('+ orderid',str(orderid[i]))
                        message = message.replace('+ ordername',str(ordername[i]))
                        message = message.replace('+ status',str(status[i]))
                        finalurl = "https://web.whatsapp.com/send?phone=" + str(phone[i]) + "&text=" + message
                        driver.get(finalurl)
                        sleep(7)
                        button = driver.find_element_by_class_name('_4sWnG')
                        button.click()
                        sleep(7)
                        success = success + 1
                except Exception as e:
                        f = open(errlocation, "a")
                        f.write('Failed to send message to ' + str(phone[i]) + '\n')
                        failed = failed + 1

    sp = (success/count)*100
    fp = (failed/count)*100
    op = ((success-failed)/count)*100
    if(op == 0):
        op = 100
    op = abs(op)
    update = {
                 
            "success"    : success,
            "failed"    :  failed,
            "status"    : "Completed",
            "sp"    : sp,
            "fp"    : fp,
            "op"    : op
            

        }
    userData = db.child("users").child(onUser).child("campaign").child(id).update(update)
    driver.quit()
    return redirect('/insights/'+id)

@app.route('/insights/docdynamic/<id>')
def docudynamic(id):
    onUser = session['user']
    onUser = str(onUser)
    userData = db.child("users").child(onUser).child("campaign").child(id).get()
    userData = userData.val()
    message = userData['message']
    path = userData['location']
    total_number = userData['number']
    packdetails = db.child("users").child(onUser).get()
    packdetails = packdetails.val()
    pack = packdetails['pack']
    pack = int(pack)
    total_number = int(total_number)
    pointreq = total_number * 5
    pointreq = int(pointreq)
    if(int(pack) < int(pointreq)):
        return redirect('/error/Please Recharge your Credit ')
    else:
        updatedamount = pack - pointreq
        updatedamount = int(updatedamount)
        uppack = {
            "pack" : updatedamount,
        }
        db.child("users").child(onUser).update(uppack)
        location = "C:/Whato/dynamic/docdynamic/data/"+ path +".xlsx"
        errlocation = "C:/Whato/dynamic/imagedynamic/data/" + path + "error.txt"
        xls = pd.ExcelFile(location)  
        sheetX = xls.parse(0) 
        name = sheetX['name']
        amt1 = sheetX['amt1']
        amt2 = sheetX['amt2']
        amt3 = sheetX['amt3']
        mark1 = sheetX['mark1']
        mark2 = sheetX['mark2']
        mark3 = sheetX['mark3']
        mark4 = sheetX['mark4']
        mark5 = sheetX['mark5']
        total = sheetX['total']
        orderid = sheetX['orderid']
        ordername = sheetX['ordername']
        status = sheetX['status']
        phone = sheetX['phone']
        file = sheetX['file']
        i = 0
        check = message
        success = 0
        failed = 0
        count = 0
        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.get('https://web.whatsapp.com/')
        sleep(10)
        for i,row in sheetX.iterrows():
                count = count + 1
                try:    
                        message = check
                        message = message.replace('+ name', str(name[i]))
                        message = message.replace('+ amt1', str(amt1[i]))
                        message = message.replace('+ amt2',str(amt2[i]))
                        message = message.replace('+ amt3',str(amt3[i]))
                        message = message.replace('+ mark1',str(mark1[i]))
                        message = message.replace('+ mark2',str(mark2[i]))
                        message = message.replace('+ mark3',str(mark3[i]))
                        message = message.replace('+ mark4',str(mark4[i]))
                        message = message.replace('+ mark5',str(mark5[i]))
                        message = message.replace('+ total',str(total[i]))
                        message = message.replace('+ orderid',str(orderid[i]))
                        message = message.replace('+ ordername',str(ordername[i]))
                        message = message.replace('+ status',str(status[i]))

                        finalurl = "https://web.whatsapp.com/send?phone=" + str(phone[i]) + "&text=" + message
                        driver.get(finalurl)
                        sleep(5)
                        button = driver.find_element_by_class_name('_4sWnG')
                        button.click()
                        sleep(5)
                        url = "https://web.whatsapp.com/send?phone=" + str(phone[i]) 
                        driver.get(url)
                        sleep(5)
                        button = driver.find_element_by_class_name('_2jitM')
                        button.click()
                        sleep(5)
                        doc = driver.find_element_by_xpath('//input[@accept="*"]')
                        doc.send_keys("C:/Whato/dynamic/docdynamic/"+ str(file[i]))
                        sleep(7)
                        final = driver.find_element_by_class_name('_1w1m1')
                        final.click()
                        sleep(7)
                        success = success + 1
                except Exception as e:
                        f = open(errlocation, "a")
                        f.write('Failed to send message to ' + str(phone[i]) + '\n')
                        failed = failed + 1


    sp = (success/count)*100
    fp = (failed/count)*100
    op = ((success-failed)/count)*100
    if(op == 0):
        op = 100
    op = abs(op)

    update = {
                 
            "success"    : success,
            "failed"    :  failed,
            "status"    : "Completed",
            "sp"    : sp,
            "fp"    : fp,
            "op"    : op

        }
    userData = db.child("users").child(onUser).child("campaign").child(id).update(update)
    driver.quit()
    return redirect('/insights/'+id)

@app.route('/delete/<id>')
def delete(id):
    onUser = session['user']
    onUser = str(onUser)
    db.child("users").child(onUser).child("campaign").child(id).remove()
    return redirect('/dashboard')

@app.route('/reset/<id>')
def reset(id):
    onUser = session['user']
    onUser = str(onUser)
    update = {
                 
            "success"    : 0,
            "failed"    :  0,
            "status"    : "Active",
            "sp"    : 0,
            "fp"    : 0,
            "op"    : 0

    }
    db.child("users").child(onUser).child("campaign").child(id).update(update)
    return redirect('/insights/'+id)
 
@app.route('/insights/video/<id>')
def video(id):
    onUser = session['user']
    onUser = str(onUser)
    userData = db.child("users").child(onUser).child("campaign").child(id).get()
    userData = userData.val()
    message = userData['message']
    message = str(message)
    path = userData['location']
    path = str(path)
    packdetails = db.child("users").child(onUser).get()
    packdetails = packdetails.val()
    pack = packdetails['pack']
    pack = int(pack)
    mediaurl = userData['mediaurl']
    mediaurl = str(mediaurl)
    numbers = []
    location = "C:/Whato/video/data/" + path + ".txt"
    errlocation = "C:/Whato/message/data/" + path + "error.txt"

    f = open(location, "r")
    for line in f.read().splitlines():
        if line != "":
            numbers.append(line)
    f.close()
    total_number=len(numbers)
    total_number = int(total_number)
    pointreq = total_number * 2
    pointreq = int(pointreq)
    if(int(pack) < int(pointreq)):
        return redirect('/error/Please Recharge your Credit ')
    else:
        updatedamount = pack - pointreq
        updatedamount = int(updatedamount)
        uppack = {
            "pack" : updatedamount,
        }
        db.child("users").child(onUser).update(uppack)
        count = 0
        success = 0
        failed = 0
        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.get('https://web.whatsapp.com/')
        sleep(20)
        
        for idx, number in enumerate(numbers):
            count = count + 1 
            number = number.strip()
            if number == "":
                    continue
            try:
                    url = "https://web.whatsapp.com/send?phone=" + number + "&text=" + message
                    driver.get(url)
                    sleep(5)
                    button = driver.find_element_by_class_name('_2jitM')
                    button.click()
                    sleep(1)
                    doc = driver.find_element_by_xpath('//input[@accept="image/*,video/mp4,video/3gpp,video/quicktime"]')
                    doc.send_keys("C:/Whato/video/"+ mediaurl)
                    sleep(7)
                    final = driver.find_element_by_class_name('_1w1m1')
                    final.click()
                    sleep(10)
                    success = success + 1
            except Exception as e:
                    f = open(errlocation, "a")
                    f.write('Failed to send message to ' + number + '\n')
                    failed = failed + 1


    sp = (success/count)*100
    fp = (failed/count)*100
    op = ((success-failed)/count)*100
    if(op == 0):
        op = 100
    op = abs(op)

    update = {
                 
            "success"    : success,
            "failed"    :  failed,
            "status"    : "Completed",
            "sp"    : sp,
            "fp"    : fp,
            "op"    : op
            

        }
    userData = db.child("users").child(onUser).child("campaign").child(id).update(update)
    driver.quit()
    return redirect('/insights/'+id)



@app.route('/insights/documents/<id>')
def documents(id):
    onUser = session['user']
    onUser = str(onUser)
    userData = db.child("users").child(onUser).child("campaign").child(id).get()
    userData = userData.val()
    path = userData['location']
    path = str(path)
    packdetails = db.child("users").child(onUser).get()
    packdetails = packdetails.val()
    pack = packdetails['pack']
    pack = int(pack)
    mediaurl = userData['mediaurl']
    mediaurl = str(mediaurl)
    numbers = []
    location = "C:/Whato/documents/data/" + path + ".txt"
    errlocation = "C:/Whato/documents/data/" + path + "error.txt"
    f = open(location, "r")
    for line in f.read().splitlines():
        if line != "":
            numbers.append(line)
    f.close()
    total_number=len(numbers)
    total_number = int(total_number)
    pointreq = total_number * 2
    pointreq = int(pointreq)
    if(int(pack) < int(pointreq)):
        return redirect('/error/Please Recharge your Credit ')
    else:
        updatedamount = pack - pointreq
        updatedamount = int(updatedamount)
        uppack = {
            "pack" : updatedamount,
        }
        db.child("users").child(onUser).update(uppack)
        count = 0
        success = 0
        failed = 0
        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.get('https://web.whatsapp.com/')
        sleep(10)
        
        for idx, number in enumerate(numbers):
            count = count + 1
            number = number.strip()
            if number == "":
                    continue
            try:
                    url = "https://web.whatsapp.com/send?phone=" + number
                    driver.get(url)
                    sleep(5)
                    button = driver.find_element_by_class_name('_2jitM')
                    button.click()
                    sleep(7)
                    doc = driver.find_element_by_xpath('//input[@accept="*"]')
                    doc.send_keys("C:/Whato/documents/"+ mediaurl)
                    sleep(7)
                    final = driver.find_element_by_class_name('_1w1m1')
                    final.click()
                    sleep(7)
                    success = success + 1
            except Exception as e:
                    f = open(errlocation, "a")
                    f.write('Failed to send message to ' + str(number) + '\n')
                    failed = failed + 1
    sp = (success/count)*100
    fp = (failed/count)*100
    op = ((success-failed)/count)*100
    if(op == 0):
        op = 100
    op = abs(op)

    update = {
                 
            "success"    : success,
            "failed"    :  failed,
            "status"    : "Completed",
            "sp"    : sp,
            "fp"    : fp,
            "op"    : op
            

        }
    userData = db.child("users").child(onUser).child("campaign").child(id).update(update)
    driver.quit()
    return redirect('/insights/'+id)



if __name__ == '__main__':
      app.run(debug=True, port=5002)