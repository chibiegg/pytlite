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

    def __init__(self, host, port=10000, proto="TCP"):
        """Connect to Patlite Signal Tower"""
        if proto.upper() == "TCP":
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            not NotImplementedError("Protocol '%s' is not supported." % proto)
        self.sock.connect((host, port))

    def close(self):
        """Close socket"""
        self.sock.close()

    def send_command(self):
        """Send change state command."""
        data = 0
        for i, status in enumerate(self._led):
            data |= (status << i)
        data |= self._buzzer
        self.sock.sendall(struct.pack("2B", 0x57, data))

    def set_led(self, led, value):
        """Change a LED state."""
        self._led[led] = value
        self.send_command()


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
        self.send_command()

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


    p = Patlite(host, port)

    print """For examples.
    p.red = p.ON
    p.yellow = p.BLINK
    p.green = p.OFF

    p.buzzer = p.SHORT
    """

    import code
    code.InteractiveConsole(globals()).interact()


