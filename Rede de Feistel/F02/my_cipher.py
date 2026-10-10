import math

SBOX: list[int] = [round(8 * math.cos(x**2)) % 16 for x in range(16)]

SPN_PBOX: list[int] = [(11*i+4) % 80 for i in range(80)]

FEISTEL_PBOX: list[int] = [(11*i+4) % 40 for i in range(40)]
