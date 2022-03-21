import math

size = 22
mps = 10
bp = [2, 9, 12, 22]

s = math.ceil(size/mps)
step = math.ceil(size / s)

count = 1

for i in range(1, size, step):
    if count + step >= size:
        print(str(i) + " to " + str(size) + " size=" + str(size - i + 1))
    else:
        print(str(i) + " to " + str(i + step) + " size=" + str(step))
    count = count + step