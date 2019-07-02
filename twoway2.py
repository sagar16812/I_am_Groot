import paho.mqtt.client as mqtt
import json
from time import sleep
import pyowm
import requests
import datetime
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier

state=0


# This is the Subscriber
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("soilmoisture")

#This function is responsible for displaying the recieved data
def on_message(client, userdata, msg):
    url="http://192.168.43.58:5000/"
    #instantiating the weather api object
    owm = pyowm.OWM('1564849dab31cdfad3ab802cf5cfe045')
    observation = owm.weather_at_place("Puducherry,india")
    w = observation.get_weather()
    print(w)
    global state
    print("the data recieved")
    print(msg.payload.decode("utf-8"))
    t,h=msg.payload.decode("utf-8").split(",")
    d=int(h)

    currentDT = datetime.datetime.now()
    hr=currentDT.hour   #getting the current hour from time
    #getting the weather details
    temperature = w.get_temperature('celsius')
    humidity = w.get_humidity()
    pressure = w.get_pressure()
    status = w.get_status()
    status=status.lower()

    if hr <=24:  #if it is day

        if status=='sunny':
            status=1
        elif status=='rain':
            status=2
        elif status=='clouds':
            status=3
        elif status=='clear':
            status=4
        else:
            pass
        print(temperature['temp'],pressure['press'],humidity,status,h)
        # Assign colum names to the dataset
        names = ['soilmoisture','temp','press','hum','status','class']

        # Read dataset to pandas dataframe
        dataset = pd.read_csv('/home/sagar/vir-envprog/sensordata.csv', names=names)
        # print(dataset.head())
        # print(dataset.describe())

        X = dataset.iloc[:, :-1].values
        y = dataset.iloc[:, 5].values
        X_train=X
        y_train=y
        X_test =[[100,temperature['temp'],pressure['press'],humidity,status]]#this is the data to be tested
        print(X_test)
        scaler = StandardScaler()
        scaler.fit(X_train)

        X_train = scaler.transform(X_train)
        X_test = scaler.transform(X_test)



        classifier = KNeighborsClassifier(n_neighbors=3)
        classifier.fit(X_train, y_train)

        y_pred = classifier.predict(X_test)
        y_test_for_yes=['yes']#give to different values for y_test
        print(np.mean(y_pred==y_test_for_yes))
        result_yes=np.mean(y_pred==y_test_for_yes)
        y_test_for_no=['no']#give to different values for y_test
        print(np.mean(y_pred==y_test_for_no))
        result_no=np.mean(y_pred==y_test_for_no)
        if result_no < result_yes:
            state=1
        else:
            state=0
    res = requests.post(url, json={'Temperature': str(temperature['temp']),
                                   'Pressure': str(pressure['press']),
                                   'Humidity': str(humidity),
                                   'Status': status,
                                   'Time': currentDT.strftime("%Y-%m-%d %H:%M:%S"),
                                   'SoilMoisture': h,
                                   'Username': t
                                   })

def on_publish(mosq, obj, mid):
    print("mid: " + str(mid))

def main():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("192.168.43.58", 1883, 60)
    client.loop_start()


    while True:
        dataToSend=state
        print("publishing Response:" +str(dataToSend))
        client.publish('waterplant',str(dataToSend))
        sleep(4)
main()
