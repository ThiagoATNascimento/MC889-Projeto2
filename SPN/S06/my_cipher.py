
# TODO: inserir sua S-box. Exatamente 16 entradas.
SBOX: list[int] = [12, 8, 11, 10, 13, 0, 14, 7, 2, 5, 4, 3, 15, 1, 9, 6]

# from random import choice
# values = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
# SBOX = []
# while(len(values) > 0):
#     value = choice(values)
#     values.remove(value)
#     SBOX.append(value)
# print(SBOX)


# TODO: inserir sua P-box da SPN (80 bits). Exatamente 80 entradas.
# Exemplo de forma (não use como resposta): [20 * (b % 4) + b // 4 for b in range(80)]
SPN_PBOX: list[int] = [(40 - b + 13 if b < 40 else 120-b + 13) % 80 for b in range(80)]

# TODO: inserir sua P-box da Feistel (40 bits). Exatamente 40 entradas.
FEISTEL_PBOX: list[int] = [(3 * b + 1) % 40 for b in range(40)]

# print(FEISTEL_PBOX)
