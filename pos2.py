import paho.mqtt.client as mqtt
import json
from scipy.optimize import minimize
import numpy as np

anchor_position = np.zeros((1, 3))

def initializeJson():
    global anchor_position
    with open('sample.json', 'r') as openfile:
    # Reading from json file
        json_object = json.load(openfile)
        for (i, j) in json_object.items():
            new_row = [i, j["pos"][0], j["pos"][1]]
            anchor_position = np.vstack([anchor_position, new_row])
    #print(str(anchor_position))

def gps_solve(distances_to_station, stations_coordinates):
    def error(x, c, r):
        return sum([(np.linalg.norm(x - c[i]) - r[i]) ** 2 for i in range(len(c))])

    l = len(stations_coordinates)
    S = sum(distances_to_station)
    # compute weight vector for initial guess
    W = [((l - 1) * S) / (S - w) for w in distances_to_station]
    # get initial guess of point location
    x0 = sum([W[i] * stations_coordinates[i] for i in range(l)])
    # optimize distance from signal origin to border of spheres
    return minimize(error, x0, args=(stations_coordinates, distances_to_station), method='Nelder-Mead').x


def on_connect(client, userdata, flags, rc):
    print("connected")


def on_message(client, obj, msg):
    #print("message recieved")
    parser(msg.payload)


def parser(payload):
    payload = json.loads(payload)
    #print(payload)
    if len(payload["nrng"]["uid"])<3:
        print("calculation aborted")
    else:
        coordinates = []
        for uid in payload["nrng"]["uid"]:
            i = 0
            for anchor in anchor_position[:, 0]:
                # print(anchor)
                if anchor == uid:
                    new_coordinate = [float(anchor_position[i, 1]), float(anchor_position[i, 2])]
                    coordinates.append(new_coordinate)
                    break
                i = i + 1
        # print(coordinates)
        rng = []
        for i, val in enumerate(payload["nrng"]["rng"]):
            rng.append(float(val))
        print(payload["euid"])
        res = gps_solve(rng, list(np.array(coordinates)))
        print(res)


def on_publish(client, obj, mid):
    print("mid: " + str(mid))


def on_subscribe(client, obj, mid, granted_qos):
    print("Subscribed")


def on_log(client, obj, level, string):
    print(string)

if __name__ == "__main__":
    initializeJson()
    mqttc = mqtt.Client()
    # Assign event callbacks
    mqttc.on_message = on_message
    mqttc.on_connect = on_connect
    mqttc.on_publish = on_publish
    mqttc.on_subscribe = on_subscribe

    # Uncomment to enable debug messages
    # mqttc.on_log = on_log

    hostname = "tailor.cloudmqtt.com"
    username = "maudksix"
    password = "7mTysv3OWj96"
    topic = "data"
    port = "16136"

    # Connect
    mqttc.username_pw_set(username, password)
    mqttc.connect(hostname, int(port))

    # Start subscribe, with QoS level 0
    mqttc.subscribe(topic, 0)

    rc = 0
    while rc == 0:
        rc = mqttc.loop()
