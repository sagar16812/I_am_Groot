<h1> <b>I_am_Groot</b> : A small project to automatically irrigate the garden/field by using Esp8266 and MicroPython.</h1>

<h2>Requirement:-</h2><br />
Please make sure all the requirements satisfied.
   <h3>Hardware:-</h3> nodeMCU esp8266, any system with linux operating system (preferably ubuntu)<br /> 
   <h3>Software:-</h3> mosquitto MQTT Broker, paho mqtt client, MicroPython, Python.<br /> 


<h2> ***Files Description*** </h2>
result.html - html page to show the results. <br /> 
adamqtt.py - MQTT client app, copied to the esp8266. <br /> 
grootapi2.py - Flask based app to insert the data to the database and to handle the request from the browser. <br /> 
twoway2.py - MQTT client's app. <br /> 
sensorData.db - database. <br /> 
 sensordata.csv - file used for classification. <br /> 
createtable.py - create a table with required fieldnames. <br /> 
References.txt - all the related useful lin. <br /> 
