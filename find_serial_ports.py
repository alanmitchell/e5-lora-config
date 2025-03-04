"""Module for listing serial ports on the current machine (any OS).
"""
import serial.tools.list_ports

def list_serial_ports(usb_only=True):
    """Returns a list of USB-based serial ports. Objects in the list are pyserial 
    ListPortInfo objects. str(port) includes port name and description. port.device
    is just the port name, e.g. "/dev/ttyUSB0" or "COM1".
    """
    ports = serial.tools.list_ports.comports()
    usb_ports = [port for port in ports if usb_only==False or 'USB' in port.description or 'USB' in port.hwid]
    return usb_ports

if __name__ == "__main__":
    usb_ports = list_serial_ports()
    print("USB-based serial ports found:")
    for port in usb_ports:
        print(str(port))

    usb_ports = list_serial_ports(usb_only=False)
    print("\nAll serial ports found:")
    for port in usb_ports:
        print(str(port))
