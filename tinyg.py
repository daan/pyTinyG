import sys

import serial
from findSerialPorts import serial_ports
import time
import json

class tinyg(object):
  def __init__(self):
    self._response = ""
    self._rest = {}   # in this dictionary we store the RESTfull state of the tinyg.

  def open(self, p):
    try:
      self.ser = serial.Serial(port=p, baudrate=115200, timeout=0, xonxoff=False)
    except:
	    print "Error opening serial port ", p
	    sys.exit()
    self.handle_response()
    self.ser.write('{"fv":""\n')
    time.sleep(0.1)
    self.handle_response()

  def close(self):
      sys.exit()

  def move_x(self, x, speed = 200):
    gcode = "G01 X "+str(x)+ "F"+str(speed)
    self.send_gcode(gcode)

  def move_y(self, y, speed = 200):
    gcode = "G01 Y "+str(y)+ "F"+str(speed)
    self.send_gcode(gcode)

  def move_z(self, z, speed = 200):
    gcode = "G01 Z "+str(z)+ "F"+str(speed)
    self.send_gcode(gcode)

  def check_status(self) :
    status = None
    if "sr" in self._rest:
      sr = self._rest["sr"]
      if "stat" in sr:
        status = sr["stat"]
    return status

  def send_gcode(self,gcode):
    print "sending gcode", gcode
    self.ser.write( '{"gc":"' + gcode + '"}\n' )
    print "waiting for status ok..."
    while 1:
     time.sleep(0.1)
     self.handle_response()  # ignore the return value
     if self.check_status() == 3:
        break
    print "status ok"
  
  def handle_response(self):
    j = {}
    while self.ser.inWaiting() :
      c = self.ser.read()
      if( c == '\n' ) :
        print "received a line", self._response
        try:
          j = json.loads(self._response)
          # now merge the current response with the REST dictionary
          self._rest = dict(self._rest, **j)
        except:
          print "error in json. ignoring line:", self._response
        self._response = ""
      else:
         self._response += c; # append the character  
    return j

if __name__ == "__main__":
  print "connecting to the first available serial port"
  tg = tinyg()
  tg.open( serial_ports()[0] )
  #tg.close


