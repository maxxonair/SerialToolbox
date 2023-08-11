

import serial
import time 
import sys 
import glob
import numpy as np

class SerialConnector():
    
    # Serial baud rate
    baud_rate = 115200 
    # Serial Port name 
    usb_port = ''

    def __init__(self):
        print(f'----------------------------------------------')
        print(f'              [SerialPortStream]')
        print(f'----------------------------------------------')
        print(f'Baud rate: {self.baud_rate}')
        print('')
        print('Find serial ports:')
        # Find usb ports
        usb_ports = self._listSerialPorts()
        if len(usb_ports) == 0:
            print(f'No serial ports found.')
            print('Exiting')
            exit(1)
        elif len(usb_ports) == 1:
            self.usb_port = usb_ports[0]
            print(f'Select only port found: {usb_ports[0]}')
        else:
            print(f"--> {len(usb_ports)} serial ports found. ")
            print(f'Ports: ')
            for portCounter, usb_port in enumerate(usb_ports):
                print(f'{portCounter} -> {usb_port}')

            portID = input("Select port:")
            portID = int(portID)

            if portID < 0 or portID > len(usb_ports):
                print(f'Port index not valid.')
                print('Exiting')
                exit(1)
            else:
                print(f'Select port: {usb_ports[portID]}')

        # Try to open and read from port 
        self.usb_port = usb_ports[portID]
        self.serCon = serial.Serial(self.usb_port, 
                                    self.baud_rate)

        if self.serCon.isOpen():
            self.serCon.close()

    def stream(self):
        self._openConnection()
        
        while True:
            print(f'{self.serCon.readline()}')
    
    #-------------------------------------------------------------------------
    #       [Private Functions]
    #-------------------------------------------------------------------------

    def _openConnection(self):
        if self.serCon.isOpen():
            self.serCon.close()
        
        # Open serial port 
        self.serCon.open()

    def _closeConnection(self):
        print("close serial")
        self.serCon.close()
        
    def _listSerialPorts(self):
        """ 
        Lists serial port names

            :raises EnvironmentError:
                On unsupported or unknown platforms
            :returns:
                A list of the serial ports available on the system
        """
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')

        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
        return result

    #-------------------------------------------------------------------------

def main():
  serialConnector = SerialConnector()
  serialConnector.stream()

if __name__=="__main__":
  main()