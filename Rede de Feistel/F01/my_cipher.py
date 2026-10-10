SBOX: list[int] = [(x*x + 3) % 16 for x in range(16)]
SPN_PBOX: list[int] = [i ^ 1 for i in range(80)]
FEISTEL_PBOX: list[int] = [i ^ 1 for i in range(40)]