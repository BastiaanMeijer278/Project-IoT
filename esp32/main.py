# if __name__ == "__main__" IS COMMENTED OUT.
from machine import Pin
import socket
import time
import bluetooth    # Ubluetooth
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
        print('Connecting to network...')
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            pass
    print('Network config:', wlan.ifconfig())


class Bluetooth:
    def __init__(self):
        # self.bt = bluetooth.BLE(), vanzelfsprekend.
        self.bt = bluetooth.BLE()
        # Changes the active state of the ble radio. (turns it on.)
        self.bt.active(True)

        self.bt.irq(self.irq)   # Reference def irq().
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
        self.port = 8003
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
        # time.sleep(5)
        self.socket = socket.socket()
        # Make a connection with the host.
        self.socket.connect((self.host, self.port))
        # if s is empty we get a timeout error, so we add filler text before sending s.
        try:
            if s == '':
                self.green_led.value(1)
                s = 'No Devices Found.'
            else:
                self.green_led.value(0)
            # Send list of devices s to host.
            self.socket.send(bytes(s, 'utf-8'))
        except OSError:
            if s == '':
                self.green_led.value(1)
                s = 'No Devices Found.'
            else:
                self.green_led.value(0)
            # Send list of devices s to host.
            self.socket.send(bytes(s, 'utf-8'))
        # Closes the connection to the host.
        self.socket.close()
        self.list_of_devices = []
        print('Done!')

    # def receive(self):
    #     print('AAI')
    #     code = self.socket.recv(1024)
    #     code = code.decode('utf-8')
    #     if code == 'alarm':
    #         self.green_led.value(0)
    #         self.state = True
    #         self.alarm()
    #         self.socket.close()
    #     else:
    #         self.stop_alarm()
    #         self.socket.close()

    def start(self):
        while True:
            self.scan()
            time.sleep(10)
            self.send()
            time.sleep(1)
            # self.receive()

    def alarm(self):
        # Can get stuck in an endless loop, DO NOT USE YET.
        while self.state:
            self.red_led.value(1)
            time.sleep(0.5)
            self.red_led.value(0)
            time.sleep(0.5)
            # self.receive()
    
    def stop_alarm(self):
        # Used to stop the alarm by turning state to false, not added to alarm so DO NOT USE ALARM() YET.
        self.state = False
        self.green_led.value(1)


"""if __name__ == '__main__':
    # Make a wifi connection
    do_connect('ESPHotSpot', 'Welkom01!')
    # Create Detector1, a Detector Class thingy.
    Detector1 = Detector()
    # Run the start method of the Detector Class.
    Detector1.start()
"""
