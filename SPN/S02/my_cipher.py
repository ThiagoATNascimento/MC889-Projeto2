
# TODO: inserir sua S-box. Exatamente 16 entradas.
SBOX: list[int] = [(x**3) % 16 for x in range(16)]

# TODO: inserir sua P-box da SPN (80 bits). Exatamente 80 entradas.
# Exemplo de forma (não use como resposta): [20 * (b % 4) + b // 4 for b in range(80)]
SPN_PBOX: list[int] = [i - 54 if i >= 54 else i + 26 for i in range(80)]

# TODO: inserir sua P-box da Feistel (40 bits). Exatamente 40 entradas.
FEISTEL_PBOX: list[int] = [i - 26 if i >= 26 else i + 14 for i in range(40)]
