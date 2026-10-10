
# DONE: inserir sua S-box. Exatamente 16 entradas.
# teste bijetora, não linear
# um mapeamento simples {0, ... 16} -> {0, ... 16}
# a expressão resulta em: [11, 8, 9, 6, 7, 4, 5, 2, 3, 0, 1, 14, 15, 12, 13, 10]
SBOX: list[int] = [(((15-i) -5) + (-1)**i) % 16 for i in range(16)]

# teste não bijetora, não linear
# a expressão resulta em: [5, 5, 11, 0, 4, 0, 13, 11, 3, 14, 12, 6, 5, 9, 11, 4]
#SBOX: list[int] = [(((i)**3) + 5 - i%3) % 16 for i in range(16)]

# teste randomizado 
#SBOX: list[int] = [8, 5, 11, 3, 13, 10, 2, 12, 1, 7, 15, 6, 14, 4, 0, 9]

# DONE: inserir sua P-box da SPN (80 bits). Exatamente 80 entradas.
# Exemplo de forma (não use como resposta): [20 * (b % 4) + b // 4 for b in range(80)]
# Um esquema parecido com o exemplo, mas a partir dos faores 16 * 5 e aplicando um deslocamento / inversão da ordem
SPN_PBOX: list[int] = [16 * ((2-b) % 5) + (79-b) // 5 for b in range(80)]

# DONE: inserir sua P-box da Feistel (40 bits). Exatamente 40 entradas.
# mesmo esquema utilizado na SPN_BOX, adapatado para 40 (fatores 8 * 5)
FEISTEL_PBOX: list[int] = [8 * ((2-b) % 5) + (39-b) // 5 for b in range(40)]
