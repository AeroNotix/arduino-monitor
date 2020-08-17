import sys
import os
import time
import serial

PORT='/dev/ttyUSB0'
BAUD=115200
if os.getenv("DEBUG", False):
    SERIAL_CONN = sys.stdout.buffer
else:
    SERIAL_CONN = serial.Serial(port=PORT, baudrate=BAUD)

def write(ser, output):
    ser.write(output)
    ser.flush()

def pad_line(line):
    return line + b' ' * (20 - len(line))

def get_cpu_temp(n):
    f = open('/sys/class/thermal/thermal_zone%d/temp' % n)
    return int(f.read()) / 1000

def parse_memory_line(line):
    return line.split(':')[-1].strip(' kB\n')

def get_mem_info():
    f = open('/proc/meminfo')
    info = f.readlines()
    for line in info:
        if 'MemTotal' in line:
            mem_total = parse_memory_line(line)
        if 'Active' in line:
            mem_active = parse_memory_line(line)
    return 'Mem: {:.2f}%'.format(int(mem_active) / int(mem_total) * 100).encode()

while True:
    cpu0 = get_cpu_temp(0)
    cpu1 = get_cpu_temp(1)
    line0 = pad_line(b"CPU: %d\xdfc / %d\xdfc" % (cpu0, cpu1))
    line1 = (' ' * 20).encode()
    line2 = pad_line(get_mem_info())
    line3 = line1
    write(SERIAL_CONN, b''.join([line0, line1, line2, line1]))
    time.sleep(3)
