from kafka import KafkaProducer
import time
import serial
import sys
import json

p = KafkaProducer(bootstrap_servers="pkc-43n10.us-central1.gcp.confluent.cloud:9092",
                  security_protocol="SASL_SSL",
                  sasl_mechanism="PLAIN",
                  sasl_plain_username="LWREB5JKVOY24U4O",
                  sasl_plain_password="HGVeVIlZQTMuAvMeZXpOhmXpiVwoA77uGlV10kptwtJLrbPxpenbT3MPmYNxmSPi"
                  )

DWM = serial.Serial(port="/dev/ttyACM0", baudrate=115200)
value = ""
try:
    while True:
        if DWM.in_waiting > 0:
            value = DWM.readline()
            if value:
                data = value.decode(errors='ignore').split(",")
                if len(data) == 5:
                    k = str.encode(data[0])
                    value = str.encode(json.dumps({"UID" : data[0],"FLOOR" : data[1],"X" : float(data[2]),"Y" : float(data[3]),"Z" : float(data[4])}))
                    p.send("data", key=k, value=value)
                    print(k)
                    print(value)
                    #time.sleep(0.2)

except KeyboardInterrupt as ex:
    #DWM.write("\r".encode())
    print('keyboard interrupt')
    sys.exit(0)
