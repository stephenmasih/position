import sys
import serial
import time
import paho.mqtt.client as mqtt

DWM = serial.Serial(port="/dev/ttyACM0", baudrate=115200)
serialString = ""
DWM.write("\r\r".encode())
time.sleep(1)
DWM.write("lep\r".encode())
time.sleep(1)
try:
    def on_publish(client, userdata, result):
        print("data published \n")
    if __name__ == "__main__":
        mqttc = mqtt.Client()
        mqttc.on_publish = on_publish
        hostname = "tailor.cloudmqtt.com"
        username = "maudksix"
        password = "7mTysv3OWj96"
        topic = "data"
        port = "16136"

        # Connect
        mqttc.username_pw_set(username, password)
        mqttc.connect(hostname, int(port))
        rc = 0
        while rc == 0:
            rc = mqttc.loop()
            while 1:
                if DWM.in_waiting > 0:
                    try:
                        serialString = DWM.readline()
                        # print(serialString)
                        if serialString:
                            parse = serialString.decode().split(",")
                            if parse[0] == "POS":
                                tag = parse[parse.index("POS") + 2]
                                x = parse[parse.index("POS") + 3]
                                y = parse[parse.index("POS") + 4]

                                data = tag +"," + x + "," + y
                                print(data)
                                mqttc.publish("data", data)
                            else:
                                print("Fail")
                    except Exception as ex:
                        print(ex)
                        break

except KeyboardInterrupt as ex:
    DWM.write("\r".encode())
    print('keyboard interrupt')
    sys.exit(0)
