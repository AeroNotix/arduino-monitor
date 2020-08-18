import sys
import os
import time
import datetime
import serial
import datetime
import socket

PORT=os.getenv("SERIAL_PORT", "/dev/ttyUSB0")
BAUD=int(os.getenv("SERIAL_BAUD_RATE", "115200"))

if os.getenv("DEBUG", False):
  SERIAL_CONN = sys.stdout.buffer
else:
  SERIAL_CONN = serial.Serial(port=PORT, baudrate=BAUD)

def get_ip():
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  try:
    s.connect(('10.255.255.255', 1))
    IP = s.getsockname()[0]
  except Exception:
    IP = '127.0.0.1'
  finally:
    s.close()
  return IP

def write(ser, output):
  ser.write(output)
  ser.flush()

def pad_line(line):
  return line + b' ' * (20 - len(line))

def get_cpu_temp(n):
  with open('/sys/class/thermal/thermal_zone%d/temp' % n) as f:
    return int(f.read()) / 1000

def parse_memory_line(line):
  return line.split(':')[-1].strip(' kB\n')

def get_mem_info():
  with open('/proc/meminfo') as f:
    info = f.readlines()
    for line in info:
      if 'MemTotal' in line:
        mem_total = parse_memory_line(line)
      if 'Active:' in line:
        mem_active = parse_memory_line(line)
    return 'Mem: {:.2f}%'.format(int(mem_active) / int(mem_total) * 100).encode()

while True:
  cpu0 = get_cpu_temp(0)
  cpu1 = get_cpu_temp(1)
  line0 = pad_line(b"CPU: %d\xdfc / %d\xdfc" % (cpu0, cpu1))
  line2 = pad_line(get_mem_info())
  line3 = pad_line("IP:  {}".format(get_ip()).encode())
  line4 = pad_line("{:>20}".format(datetime.datetime.fromtimestamp(time.time()).strftime('%H:%M:%S')).encode())
  write(SERIAL_CONN, b''.join([line0, line3, line2, line4]))
  time.sleep(1)
