import pickle
import threading

from gpiozero import DigitalInputDevice as IoIn
from gpiozero import DigitalOutputDevice as IoOut

import pinio

pins = {
    'master': {
        'in': IoIn(20),
        'out': IoOut(21)
    },
    'track_one': {
        'in': IoIn(17),
        'out': IoOut(14)
    },
    'track_two': {
        'in': IoIn(27),
        'out': IoOut(15)
    },
    'track_three': {
        'in': IoIn(22),
        'out': IoOut(18)
    }
}

if __name__ == '__main__':
    location = open("stations.p", "wb")
    pickle.dump({}, location)
    location.close()

    threads = [
        threading.Thread(
            target=pinio.listen_on_pin,
            args=[
                pins[pin]['in'],
                pins['master']['out'],
                [pins[p]['out'] for p in pins if p != 'master'],
                pins['master']['out']
            ]
        )
        for pin in pins
    ]

    for thread in threads:
        thread.start()
