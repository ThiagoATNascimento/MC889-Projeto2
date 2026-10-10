import math

SBOX: list[int] = [0] + [round(x*(math.log2(x))) % 16 for x in range (1, 16)]

SPN_PBOX: list[int] = []
for i in range(80):
    n = i // 4 # índice do bloco de 4 bits
    y = i % 4 # índice do bit dentro do bloco de 4 bits n
    bloco_dest = (n + y + 1) % 20 # 20 = número de blocos de 4 bits
    SPN_PBOX.append(4 * bloco_dest + y)

FEISTEL_PBOX: list[int] = []
for i in range(40):
    n = i // 4 # índice do bloco de 4 bits
    y = i % 4 # índice do bit dentro do bloco de 4 bits n
    bloco_dest = (n + y + 1) % 10 # 10 = número de blocos de 4 bits
    FEISTEL_PBOX.append(4 * bloco_dest + y)