import math

# TODO: inserir sua S-box. Exatamente 16 entradas.
SBOX: list[int] = [0] + [ round(3 * math.log(3*x**3)) % 16 for x in range(1,16) ]

# TODO: inserir sua P-box da SPN (80 bits). Exatamente 80 entradas.
# Exemplo de forma (não use como resposta): [20 * (b % 4) + b // 4 for b in range(80)]
SPN_PBOX: list[int] = [ (3*i - 2) % 80 for i in range(80) ]

# TODO: inserir sua P-box da Feistel (40 bits). Exatamente 40 entradas.
FEISTEL_PBOX: list[int] = [ (3*i - 2) % 40 for i in range(40) ]
