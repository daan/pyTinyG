import sys
import glob
import serial

# based on solution provided by Stackoverflow user Thomas
# http://stackoverflow.com/questions/12090503/listing-available-com-ports-with-python

# added a line to remove the Bluetooth port on osx

def serial_ports():
    """Lists serial ports

    :raises EnvironmentError:
        On unsupported or unknown platforms
    :returns:
        A list of available serial ports
    """
    if sys.platform.startswith('win'):
        ports = ['COM' + str(i + 1) for i in range(256)]

    elif sys.platform.startswith('linux'):
        # this is to exclude your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')

    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')

    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
				# this to remove the ever present Bluetooth port on osx
        if port == "/dev/tty.Bluetooth-Incoming-Port":
          continue
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result


if __name__ == '__main__':
    print(serial_ports())

