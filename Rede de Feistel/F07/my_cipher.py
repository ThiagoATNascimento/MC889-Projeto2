# S-box: complemento do nibble, S(x) = 15 - x.
# Bijetora, os 16 valores aparecem uma vez cada.
SBOX: list[int] = [15 - x for x in range(16)]

# P-box da SPN: passo 29, primo com 80, entao e permutacao.
SPN_PBOX: list[int] = [(29 * i + 7) % 80 for i in range(80)]

# P-box da Feistel: mesma ideia com passo 17, primo com 40.
FEISTEL_PBOX: list[int] = [(17 * i + 9) % 40 for i in range(40)]