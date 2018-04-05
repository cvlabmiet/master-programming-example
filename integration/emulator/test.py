#!/usr/bin/env python3

import sys, random, array
sys.dont_write_bytecode = True

from device import Pram, Lram

test_vector = list(range(0, 200))
random.shuffle(test_vector)

pram = Pram()
lram = Lram()

lram[:] = bytes(test_vector)
pram[:] = b'[u16:0]add(u8:0, u8:100)'

pram.run(lram)

view = array.array('H', lram)
error_count = 0
for x in range(len(view)):
    if view[x] != test_vector[x] + test_vector[x + 100]:
        print("Error:", x, view[x], test_vector[x], test_vector[x + 100])
        error_count += 1

sys.exit(error_count)
