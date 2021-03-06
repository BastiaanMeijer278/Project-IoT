from machine import Pin
import socket
import time
import bluetooth
from micropython import const
import ubinascii

# const(5) is het ID voor _IRQ_SCAN_RESULT, const(6) is het ID voor SCAN_DONE.
_IRQ_SCAN_RESULT = const(5)
_IRQ_SCAN_DONE = const(6)


def do_connect(ssid, password):
    """ do_connect connects to a wifi network. """
    import network
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())


class Bluetooth:
    def __init__(self):
        # self.bt = bluetooth.BLE(), vanzelfsprekend.
        self.bt = bluetooth.BLE()
        # Changes the active state of the ble radio. (turns it on.)
        self.bt.active(True)
        # Reference def irq().
        self.bt.irq(self.irq)
        # List of detected bluetooth devices.
        self.list_of_devices = []
        # Pin of the green led, D33
        self.green_led = Pin(33, Pin.OUT)
        # Pin of the red led, D32
        self.red_led = Pin(32, Pin.OUT)

    def irq(self, event, data):
        """" IRQ stands for Interrupt Request, sends interrupts to the system so the system can resolve the data
             gotten with the request(?) """
        # A single scan result:
        if event == _IRQ_SCAN_RESULT:
            # addr_type = indicates public (0x00) or random (0x01) address.
            # addr      = address of the device result. (ip or bluetooth address, no clue...)
            # adv_type  = values corresponding to the Bluetooth Specifications:
            #           0x00 - ADV_IND - connectable and scannable undirected advertising.
            #           0x01 - ADV_DIRECT_IND - connectable directed advertising.
            #           0x02 - ADV_SCAN_IND - scannable undirected advertising.
            #           0x03 - ADV_NONCONN_IND - non-connectable undirected advertising.
            #           0x04 - SCAN_RSP - scan response.
            # rssi      = Received Signal Strength Indication.
            # adv_data  = unknown, data of ADVertising device?
            addr_type, addr, adv_type, rssi, adv_data = data
            # NO CLUE WAT DIT DOET.
            self.list_of_devices.append((ubinascii.hexlify(addr)).decode('utf-8'))

        # Scan duration finished or manually stopped.
        elif event == _IRQ_SCAN_DONE:
            # if scan done, pin 33 light off.
            self.red_led.value(0)
    
    def scan(self):
        """ scan Scans for bluetooth devices."""
        # If scanning: pin 33 (red light) on.
        self.red_led.value(1)
        # Run a bluetooth scan for 10000 miliseconds (10 seconds),
        # every scan result raises an _IRQ_SCAN_RESULT event,
        # When the scanning is done, an _IRQ_SCAN_DONE event is raised instead.
        self.bt.gap_scan(10000)


class Detector:
    def __init__(self):
        self.bt = Bluetooth()
        self.list_of_devices = self.bt.list_of_devices
        self.green_led = Pin(33, Pin.OUT)
        self.red_led = Pin(32, Pin.OUT)
        self.host = '192.168.137.1'
        self.port = 7002
        self.state = False

    def scan(self):
        """Performs bt.scan(), a gap_scan to scan for devices."""
        print('Scannen...')
        self.bt.scan()

    def send(self):
        """" Sends the found devices to the server, run this after a scan unless you already have the devices."""
        # s is the list for devices.
        s = ''
        # s does not always get populated with devices,
        # bluetooth not finding devices for some reason?
        for device in self.list_of_devices:
            s += str(device)
        print(s)
        print(self.list_of_devices)
        # Gives an error if put in __init__, so its here.
        self.socket = socket.socket()
        # Make a connection with the host.
        self.socket.connect((self.host, self.port))
        # if s is empty we get a timeout error, so we add filler text before sending s.
        try:
            if s == '':
                s = 'No Devices Found.'
            # Send list of devices s to host, needs to be a string, not a list.
            self.socket.send(bytes(s, 'utf-8'))
        except OSError:
            if s == '':
                # self.green_led.value(1)
                s = 'No Devices Found.'
            # Send list of devices s to host, needs to be a string, not a list.
            self.socket.send(bytes(s, 'utf-8'))
        # Socket needs to be closed and reopened for it to receive/send data again.
        self.socket.close()
        # Empty list_of_devices so it can be filled by the scan again.
        self.list_of_devices = []
        print('Done!')

    def start(self):
        self.scan()
        time.sleep(10)
        self.send()
        time.sleep(1)


def main():
    do_connect('ESPHotSpot', 'Welkom01!')
    while True:
        Detector1 = Detector()
        Detector1.start()
