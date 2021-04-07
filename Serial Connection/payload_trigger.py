#!/usr/bin/env python
import time
import serial
import struct
import codecs


class Listener():

	# Current default setting: "launch" will be detected at 120ft, in the event "launch" doesn't trigger a timeout is used 
    def __init__(self, launch_alt_ft=120, timeout_s=240):

        self.launch_alt = launch_alt_ft / 3.281
        self.launch_timeout = timeout_s

        self.pnut_init_alt = None
        self.mpl_init_alt = None

        self.pnut_data = {'agl': 0.0}
        self.mpl_data = {'asl': 0.0}
        self.bno_data = {'accel': 0.0}

        self.time_begin = time.time()

    def parse_pnut(self, raw):

        delimit_index = raw.index('<')
        if delimit_index == -1:
            return
        altitude = float(raw[:delimit_index])

        if self.pnut_init_alt is None:
            self.pnut_init_alt = altitude
            return

        self.pnut_data['agl'] = altitude

    def parse_telemetry(self, raw):

        parced = raw[:2]
        if len(parced) is not 2:
            return

        if parced == '##':
            self.parse_mpl(raw)
        elif parced == '%%':
            self.parse_bno(raw)

    def parse_mpl(self, raw):

        parsed = raw.split(',')

        if len(parsed) is not 5:
            return

        if self.mpl_init_alt is None:
            self.mpl_init_alt = float(parsed[4])
            return

        self.mpl_data['asl'] = float(parsed[4])

    def parse_bno(self, raw):

        parsed = raw.split(',')

        if len(parsed) is not 16:
            return

        self.bno_data['accel'] = float(parsed[14])

    def launched(self):

        points = 0

        if self.bno_data['accel'] <= 0:
            points += 1
        if self.mpl_init_alt is not None and self.mpl_data['asl'] - self.mpl_init_alt >= self.launch_alt:
            points += 1
        if self.pnut_init_alt is not None and self.pnut_data['agl'] >= self.launch_alt:
            points += 1

        return (points >= 2) or (time.time() - self.time_begin >= self.launch_timeout)


def serial_listen():

	# Telemetry Teensy serial connection, operating on PL011 (UART0, ttyAMA0)
	serT = serial.Serial(
		port='/dev/ttyAMA0',
		baudrate=9600,
		parity=serial.PARITY_NONE,
		stopbits=serial.STOPBITS_ONE,
		bytesize=serial.EIGHTBITS,
		timeout=1,
	)

	# Payload Pnut serial connection, operating on miniUART (UART1, ttyS0)
	serP = serial.Serial(
		port='/dev/ttyS0',
		baudrate=9600,
		parity=serial.PARITY_NONE,
		stopbits=serial.STOPBITS_ONE,
		bytesize=serial.EIGHTBITS,
		timeout=1
	)

	listener = Listener()

	while True:
		x = serT.readline(5)
		print(x)
		listener.parse_telemetry(x)

		y = serP.readline(5)
		print(y)
		listener.parse_pnut(y)

		if listener.launched():
			return