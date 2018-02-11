import serial
from bitstring import BitArray
import random

def algorithm_1(s):
  interval_before_last = 0
  last_interval = 0
  current_interval = 0
  iterations = 0

  while True:
    data = s.read(2)
    if data[1] == 0:
      current_interval = current_interval + 1
    else:
      interval_before_last = last_interval
      last_interval = current_interval
      current_interval = 0
      iterations = iterations + 1
      #print(iterations)
      #print('interval_before_last', interval_before_last)
      #print('last_interval', last_interval)

      if iterations > 2:
        if interval_before_last > last_interval:
          yield 1
        elif last_interval > interval_before_last:
          yield 0


def algorithm_2(s):
  count_before_last = 0
  last_count = 0
  count = 0
  SECONDS_PER_PERIOD=10

  iterations = 0

  while True:

    for t in range(0,SECONDS_PER_PERIOD):
      data = s.read(2)
      count = count + data[1]
      print(t, count)
      
    count_before_last = last_count
    last_count = count
    count = 0

    iterations = iterations + 1

    if iterations > 2:

      print('count_before_last', count_before_last)
      print('last_count', last_count)

      if count_before_last > last_count:
        yield 1
      elif last_count > count_before_last:
        yield 0


#g = algorithm_2()


def get_random_bits(num):
  s = serial.Serial( "/dev/tty.wchusbserial1410", 57600 )
  s.write(b'<HEARTBEAT1>>')

  #gen = algorithm_1(s)
  gen = algorithm_2(s)
  bits = []

  for i in range(0, num):
    next_bit = next(gen)

    bits.append(next_bit)

    print(bits)

  bits_str = ''.join(str(num) for num in bits)
  number = BitArray(bin=bits_str)
  s.close()
  return number
  #random.seed(number.uint)
  #print(random.random())

def get_random_bytes(n):
  bits = get_random_bits(8)
  seed = bits.uint
  random.seed(seed)
  num = random.getrandbits(n * 8)
  return num.to_bytes(n, byteorder='big')
