#the real flask api file
from flask import Flask, jsonify, request, redirect, render_template, url_for
import sqlite3 as lite
import sys
app = Flask(__name__)
@app.route('/result/')
def result():
   con2 = lite.connect("sensorsData.db")
   con2.row_factory = lite.Row

   cur = con2.cursor()
   cur.execute("Select * from sms_data Where id >5 order by id DESC Limit 5")

   rows = cur.fetchall();
   print(type(rows))
   return render_template('result.html',title='result',rows = rows)


@app.route('/',methods=['GET','POST'])
def index():
    con = lite.connect('sensorsData.db',check_same_thread=False)#database connection
    content=request.json
    print(content)
    soilmoisture = content['SoilMoisture']
    temp = content['Temperature']
    press = content['Pressure']
    hum = content['Humidity']
    readtime = content['Time']
    status = content['Status']
    username = content['Username']
    with con:
        cur = con.cursor()
        cur.execute("INSERT INTO sms_data (readtime,username,soilmoisture,temp,press,hum,status) VALUES (?,?,?,?,?,?,?)",(readtime,username,soilmoisture,temp,press,hum,status))
        con.commit()
        msg = "Record successfully added"
        
    return msg
if __name__=='__main__':
    app.run(host="--your system's ip address--",debug=False)
