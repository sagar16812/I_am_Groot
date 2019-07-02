#the real working file
import network
import time
from umqtt.simple import MQTTClient
import os
import gc
import sys
from machine import ADC,Pin

adc = ADC(0)# To read the soil moisture sensor
p13 = Pin(13, Pin.OUT) # To actuate something on pin13

# the following function is the callback which is
# called when subscribed data is received
def cb(topic, msg):
    print('Subscribe:  Received Data:  Topic = {}, Msg = {}\n'.format(topic, msg))
    t=int(msg.decode("utf-8"))
    if t==1:#means the message is to turn on the pump
        p13.on()
        print('watered the plant')
        time.sleep(3)
        p13.off()
    else:
        pass

# WiFi connection information
WIFI_SSID = 'iot'
WIFI_PASSWORD = '9463758467'

# turn off the WiFi Access Point
ap_if = network.WLAN(network.AP_IF)
ap_if.active(False)

# connect the device to the WiFi network
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(WIFI_SSID, WIFI_PASSWORD)

# wait until the device is connected to the WiFi network
MAX_ATTEMPTS = 60
attempt_count = 0
while not wifi.isconnected() and attempt_count < MAX_ATTEMPTS:
    attempt_count += 1
    time.sleep(1)

if attempt_count == MAX_ATTEMPTS:
    print('could not connect to the WiFi network')
    sys.exit()

# create a random MQTT clientID
random_num = int.from_bytes(os.urandom(3), 'little')
mqtt_client_id = bytes('client_'+str(random_num), 'utf-8')

# connect to MQTT broker using unsecure TCP (port 1883)
#
# To use a secure connection (encrypted) with TLS:
#   set MQTTClient initializer parameter to "ssl=True"
#   Caveat: a secure connection uses about 9k bytes of the heap
#         (about 1/4 of the micropython heap on the ESP8266 platform)
URL = b'192.168.43.58'
USERNAME=b'sagar'

SOIL_FEED = b'soilmoisture'
RESPONSE_FEED=b'waterplant'

client = MQTTClient(client_id=mqtt_client_id,server=URL)

try:
    client.connect()
except Exception as e:
    print('could not connect to MQTT server {}{}'.format(type(e).__name__, e))
    sys.exit()



client.set_callback(cb)# To get the messages from broker
client.subscribe(RESPONSE_FEED)# Subscribe to the waterplant topic
PUBLISH_PERIOD_IN_SEC = 10
SUBSCRIBE_CHECK_PERIOD_IN_SEC = 0.5
accum_time = 0
while True:
    try:
        # Publish
        if accum_time >= PUBLISH_PERIOD_IN_SEC:
            sensor=adc.read()
            p=int((sensor*100)/1024)
            p=100-p
            dataToSend = p
            print('Publish:  Soil Moisture = {}'.format(dataToSend))
            msg=(b'{0},{1}'.format("sagar16812",p))
            client.publish(SOIL_FEED,msg)
            accum_time = 0

        # Subscribe.  Non-blocking check for a new message.
        client.check_msg()

        time.sleep(SUBSCRIBE_CHECK_PERIOD_IN_SEC)
        accum_time += SUBSCRIBE_CHECK_PERIOD_IN_SEC
    except KeyboardInterrupt:
        print('Ctrl-C pressed...exiting')
        client.disconnect()
        sys.exit()
