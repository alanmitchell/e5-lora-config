#!/usr/bin/env python3
"""Configures a LoRa-E5 device to work on the US915 Things Network.
"""

from secrets import token_hex
from pathlib import Path
import sys
from serial import Serial

from questionary import select, confirm

from find_serial_ports import list_serial_ports

APP_EUI = '0000000000000001'      # will be programmed into E5 device

# Let the user choose the serial port, if there is more than one.
ser_ports = list_serial_ports()
if len(ser_ports) == 0:
    print("No USB-serial Converter attached. Exiting now.")
    sys.exit()

elif len(ser_ports) == 1:
    port_name = ser_ports[0].device
    print(f"Using '{ser_ports[0]}' to communicate to E5 module.")

else:
    # ask the user to select
        choices = { str(p): p.device for p in ser_ports}
        port_desc = select(
            'Select Serial Port communicating with E5 Module:',
            choices=[*choices],
            default=[*choices][0],
        ).ask()
        port_name = choices[port_desc]

# Select the Data Rate to use
choices = { 
    '0: Longest Distance, but only 11 bytes of data': 0,
    '1: Long Distance': 1,
    '2: Medium Distance': 2,
    '3: Gateway in Building': 3
}
dr_desc = select(
    'Select LoRa Data Rate to use:',
    choices=[*choices],
    default=[*choices][1],
).ask()
data_rate = choices[dr_desc]


# A CSV file is used to track Device IDs and Keys
FN_KEYS = 'keys.csv'
if not Path(FN_KEYS).exists():
    # start the file with a header row
    with open(FN_KEYS, 'w') as fkeys:
        fkeys.write('dev_eui,app_eui,app_key\n')

# Generate a random App Key
app_key = token_hex(16).upper()

# Commands that need to be executed to configure the device; will be later
# prefaced with an AT+.
cmds = (
    'FDEFAULT',
    'UART=TIMEOUT, 2000',
    f'ID=APPEUI, "{APP_EUI}"',
    f'KEY=APPKEY,"{app_key}"',
    'MODE=LWOTAA',
    'DR=US915HYBRID',
    'CH=NUM,8-15',
    'CLASS=A',
    'ADR=OFF',
    f'DR={data_rate}',
    'DELAY=RX1,5000',
    'DELAY=RX2,6000',
    'JOIN=AUTO,10,1200,0',
)

while True:

    try:
        p = Serial(port_name, timeout=1.0)

        # determine the Dev EUI of the device
        p.write(b'AT+ID=DEVEUI\n')
        resp = p.readline()
        dev_eui = resp.decode('utf-8').strip().split(' ')[-1].replace(':','')

        for cmd in cmds:
            print('\n' + cmd)
            cmd_full = f'AT+{cmd}\n'.encode('utf-8')
            p.write(cmd_full)
            resp = p.readlines()
            for lin in resp:
                print(lin.decode('utf-8').strip())

    except Exception as e:
        raise e

    finally:
        p.close()
        # Save the IDs and App Key for this device.
        with open(FN_KEYS, 'a') as fkeys:
            fkeys.write(f'{dev_eui}, {APP_EUI}, {app_key}\n')

        print(f'\nDevice EUI: {dev_eui[:11]} {dev_eui[-5:]}')

    print()
    do_again = confirm("Do you want to configure another E5 module the same way?").ask()
    if do_again:
        print()
        do_again = confirm("Plug in the new E5 module and press Enter to configure.").ask()
        if not do_again:
            sys.exit()
    else:
        sys.exit()
