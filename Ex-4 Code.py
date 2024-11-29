from machine import Pin, I2C
import network
import utime
import bme280
from umqtt.simple import MQTTClient

ssid = ""
password = ""

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.config(pm=0xa11140)  # Disable powersave mode
wlan.connect(ssid, password)

max_wait = 10
while max_wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    max_wait -= 1
    print('waiting for connection...')
    utime.sleep(1)

# Handle connection error
if wlan.status() != 3:
    raise RuntimeError('wifi connection failed')
else:
    print('connected')
    status = wlan.ifconfig()
    print('ip = ' + status[0])
#initialise I2C
i2c=I2C(0,sda=Pin(0), scl=Pin(1), freq=100000)
led_pin = Pin('LED', Pin.OUT)
def connectMQTT():
  client = MQTTClient(client_id=b"",
                      server=b"",
                      port=8883,
                      user=b"",
                      password=b"",
                      keepalive=7200,
                      ssl=True,
                      ssl_params={'server_hostname':''})
  client.connect()
  return client
client = connectMQTT()
def publish(topic, value):
    print(topic)
    print(value)
    client.publish(topic, value)
    print("publish Done")
def on_message(topic, msg):
    print(f"Received message: {msg} on topic: {topic}")
    if msg == b"ON":
        led_pin.on()  # Turn on the LED
        print("LED ON")
    elif msg == b"OFF":
        led_pin.off()  # Turn off the LED
        print("LED OFF")
client.set_callback(on_message)
client.subscribe(b"picow/control")
while True:
    # Read sensor data
    sensor_reading = bme280.BME280(i2c=i2c)
    temperature = sensor_reading.values[0]
    pressure = sensor_reading.values[1]
    #humidity = sensor_reading.values[2]

    print(sensor_reading)

    # Publish as MQTT payload
    publish('picow/temperature', temperature)
    publish('picow/pressure', pressure)
    #publish('picow/humidity', humidity)
    client.check_msg()

    # Delay 5 seconds
    utime.sleep(5)
