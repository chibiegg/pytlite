import socket
import struct

class Patlite(object):

    OFF = 0
    BLINK = 0x20
    ON = 0x01

    SHORT = 0x08
    LONG = 0x10

    RED = 0
    YELLOW = 1
    GREEN = 2

    _led = [0, 0, 0]
    _buzzer = 0

    send = None
    
    class NAKError(Exception):
        pass

    def __init__(self, host, port=10000, proto="TCP", timeout=2):
        """Connect to Patlite Signal Tower"""

        self.host = host
        self.port = port
        self.timeout = timeout

        if proto.upper() == "TCP":
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((host, port))
            self.send = self._send_tcp
        elif proto.upper() == "UDP":
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.send = self._send_udp
        else:
            not NotImplementedError("Protocol '%s' is not supported." % proto)
        self.sock.settimeout(timeout)

        # Get curernt status
        self.get_status()

    # Implementation of Send
    def _send_tcp(self, data):
        """Send implementation for TCP"""
        self.sock.sendall(data)

    def _send_udp(self, data):
        """Send implementation for UDP"""
        self.sock.sendto(data, (self.host, self.port))

    def close(self):
        """Close Socket"""
        self.sock.close()

    def send_status(self):
        """Send change state command."""
        data = 0
        for i, status in enumerate(self._led):
            data |= (status << i)
        data |= self._buzzer
        self.send(struct.pack("2B", 0x57, data))
        # Recv ACK
        data, addr = self.sock.recvfrom(10)
        if not data[:3] == "ACK":
            raise self.NAKError()
    
    def get_status(self):
        """Get current status from Patlite"""
        self.send("\x52")
        data, addr = self.sock.recvfrom(10)
        if not data[0] == "R":
            raise self.NAKError()
        data = struct.unpack("B", data[1])[0]

        # Parse LED statuses.
        for i in xrange(3):
            led = self.OFF
            if (data & (self.ON << i)):
                led = self.ON
            elif (data & (self.BLINK << i)):
                led = self.BLINK
            self._led[i] = led

        # Parse the buzzer status.
        buzzer = self.OFF
        if (data & (self.LONG)):
            buzzer = self.LONG
        elif (data & (self.LONG)):
            buzzer = self.SHORT
        self._buzzer = buzzer


    def set_led(self, led, value):
        """Change a LED state."""
        self._led[led] = value
        self.send_status()


    # LED propertiess
    red = property(lambda self:self._led[self.RED],
                   lambda self, value:self.set_led(self.RED, value))

    green = property(lambda self:self._led[self.GREEN],
                     lambda self, value:self.set_led(self.GREEN, value))

    yellow = property(lambda self:self._led[self.YELLOW],
                      lambda self, value:self.set_led(self.YELLOW, value))


    def set_buzzer(self, value):
        """Change the buzzer state."""
        self._buzzer = value
        self.send_status()

    # Buzzer property
    buzzer = property(lambda self:self._buzzer,
                      lambda self, value:self.set_buzzer(value))


if __name__ == "__main__":
    # For testing
    import sys

    host = sys.argv[1]

    if len(sys.argv) >= 3:
        port = int(sys.argv[2])
    else:
        port = 10000

    if len(sys.argv) >= 4:
        proto = sys.argv[3].upper()
    else:
        proto = "TCP"

    p = Patlite(host, port, proto)

    print """For examples.
    p.red = p.ON
    p.yellow = p.BLINK
    p.green = p.OFF

    p.buzzer = p.SHORT
    """

    import code
    code.InteractiveConsole(globals()).interact()


