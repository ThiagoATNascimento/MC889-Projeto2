from math import floor, log2

SBOX: list[int] = [floor(log2(x+1)*x) % 16 for x in range(16)]

# Exemplo de forma (não use como resposta): [20 * (b % 4) + b // 4 for b in range(80)]
SPN_PBOX: list[int] = [(i*43 + 17) % 80 for i in range(80)]

FEISTEL_PBOX: list[int] = [(i*23 + 11) % 40 for i in range(40)]

