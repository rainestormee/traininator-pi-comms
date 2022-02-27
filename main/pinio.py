import pickle
from time import sleep

baud_rate = 0.1

my_id = ""


def listen_on_pin(in_pin, out_pin, child_pins, master_pin):
    while True:
        byte = read_byte(in_pin)
        operator = ''.join(str(x) for x in byte[1:4])
        operand = byte[4:-1]
        instr = instructions
        print(byte)
        if operator in instr:
            # print(instr[operator]['name'])
            entry = instr[operator]
            if operator == '100':
                entry['handle'](master_pin, operand, child_pins)
            else:
                entry['handle'](out_pin, operand, child_pins)


def send_byte(pin, byte):
    # print("Sending: " + str(byte))
    pin.on()
    for x in byte:
        x = int(x)
        sleep(baud_rate)
        if x == 1:
            pin.on()
        else:
            pin.off()
    sleep(baud_rate)
    pin.off()


def discover(pin, node_id, _):
    send_byte(pin, [0, 0, 1] + [int(x) for x in node_id])


def discover_resp(pin, node_id, _):
    # respond to discovery request with id
    global my_id
    my_id = node_id
    send_byte(pin, [0, 1, 0] + [int(x) for x in node_id])


def discover_confirm(_, node_id, __):
    location = open("stations.p", "rb")
    a = pickle.load(location)
    location.close()

    for station in stations:
        if ''.join([str(x) for x in node_id]) == stations[station]['id']:
            a[station] = True
            stations[station]['online'] = True

    location = open("stations.p", "wb")
    pickle.dump(a, location)
    location.close()


def neighbour_discover(pin, node_id, _):
    send_byte(pin, [0, 1, 1] + [int(x) for x in node_id])


def neighbour_discover_resp(_, neighbour_id, pins):
    for pin in pins:
        send_byte(pin, [1, 0, 0] + [int(x) for x in neighbour_id])


def neighbour_discover_confirm(pin, neighbour_id, _):
    # print(f"{neighbour_id} -> {my_id}")

    send_byte(pin, [1, 0, 1] + [int(x) for x in my_id])


def neighbour_discover_firm(_, neighbour_id, __):
    checking = open("check.p", "rb")
    name = pickle.load(checking)
    print(f"{name} is connected to {neighbour_id}")


def read_byte(pin):
    byte = []
    while not pin.is_active:
        sleep(baud_rate)
    for i in range(0, 7):
        sleep(baud_rate)
        if pin.is_active:
            byte.append(1)
        else:
            byte.append(0)
    byte = [1] + byte
    # print("Received: " + ''.join(str(b) for b in byte))
    return byte


stations = {
    'ryan': {
        'online': False,
        'id': 0,
        'in': '',
        'out': '',
        'connections': [

        ]
    },
    'alex': {
        'online': False,
        'id': 0,
        'in': '',
        'out': '',
        'connections': []
    },
    'peng': {
        'online': False,
        'id': 0,
        'in': '',
        'out': '',
        'connections': []
    },
    'matt': {
        'online': False,
        'id': 0,
        'in': '',
        'out': '',
        'connections': []
    }
}

instructions = {
    '001': {
        'name': 'discovery',
        'function': discover,
        'handle': discover_resp,
    },
    '010': {
        'name': 'discovery_resp',
        'function': discover_resp,
        'handle': discover_confirm
    },
    '011': {
        'name': 'neighbour_discovery',
        'function': neighbour_discover,
        'handle': neighbour_discover_resp
    },
    '100': {
        'name': 'neighbour_discovery_resp',
        'handle': neighbour_discover_confirm
    },
    '101': {
        'name': 'neighbour_discovery_firm',
        'handle': neighbour_discover_firm
    }
}
