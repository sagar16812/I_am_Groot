I_am_Groot : A small project for automatic irrigation of the garden/field by using Esp8266 and MicroPython.

Requirement:-
   Hardware:- nodeMCU esp8266, any system with linux operating system (preferably ubuntu)
   Software:- mosquitto MQTT Broker, paho mqtt client, MicroPython, Python.

Files:-
Project/--|
          |--templates/-|
          |             |--result.html
          |
          |--adamqtt.py
          |--grootapi2.py
          |--twoway2.py
          |--sensorData.db
          |--sensordata.csv
          |--createtable.py
          |--References.txt


result.html - html page to show the results
adamqtt.py - MQTT client app, copied to the esp8266
grootapi2.py - Flask based app to insert the data to the database and to handle the request from the browser
twoway2.py - MQTT client's app
sensorData.db - database
 sensordata.csv - file used for classification
createtable.py - create a table with required fieldnames
References.txt - all the related useful links
