import pickle
from multiprocessing import Process
from time import sleep

from gpiozero import DigitalInputDevice as IoIn
from gpiozero import DigitalOutputDevice as IoOut

import pinio

a = {
    "ryan": False,
    "alex": False,
    "peng": False,
    "matt": False
}
location = open("stations.p", "wb")
pickle.dump(a, location)
location.close()

b = ''
checking = open("checking.p", "wb")
pickle.dump(b, checking)
checking.close()

c = {
    "000": [],
    "001": [],
    "010": [],
    "011": []
}
connections = open("connections.p", "wb")
pickle.dump(c, connections)


def discover():
    for name in pinio.stations:
        print(f'Sending Discovery to {name}')
        ss = pinio.stations[name]
        pinio.discover(ss['out'], ss['id'], [])


if __name__ == '__main__':

    pin_pairs = {
        'ryan': {
            'out': IoOut(26),
            'in': IoIn(21)
        },
        'alex': {
            'out': IoOut(19),
            'in': IoIn(20),
        },
        'peng': {
            'out': IoOut(13),
            'in': IoIn(16),
        },
        'matt': {
            'out': IoOut(6),
            'in': IoIn(12),
        }
    }

    next_id = 0
    for s in pinio.stations:
        id_format = format(next_id, '03b')
        pinio.stations[s]['id'] = id_format
        print(f"Assigned {id_format} to {s}.")

        pinio.stations[s]['out'] = pin_pairs[s]['out']
        pinio.stations[s]['in'] = pin_pairs[s]['in']

        pinio.stations[s]['out'].off()  # make sure all pins are off
        next_id += 1

    threads = [
        Process(target=pinio.listen_on_pin, args=(pinio.stations[pin]['in'], pinio.stations[pin]['out'], [], []))
        for pin in pinio.stations
    ]

    for thread in threads:
        thread.start()

    print("\n================\n")

    discover()

    # hopefully everything has been discovered by now
    print("Waiting for discovery")
    sleep(5)
    location = open("stations.p", "rb")
    stations = pickle.load(location)

    print("Neighbour Discovery from active nodes")

    for st in stations:
        if stations[st]:
            # do neighbour check
            print(f"Checking Neighbours of {st}")

            checking = open("check.p", "wb")
            pickle.dump(st, checking)
            checking.close()

            pinio.neighbour_discover(pinio.stations[st]['out'], pinio.stations[st]['id'], [])
            sleep(3)
