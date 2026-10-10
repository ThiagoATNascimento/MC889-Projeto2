"""Configuração da cifra: S-box, P-box e chave.

Escolhas de projeto (justificadas no relatório):

  S-box  -> inverso multiplicativo em GF(2^4) módulo x^4 + x + 1, com 0 -> 0.
            É a não linearidade forte de um nibble (uniformidade diferencial 4,
            não linearidade 4), a versão de 4 bits da S-box do AES. Bijetora.

  P-box  -> π(i) = (7·i + 3) mod n, com n = 80 na SPN e n = 40 na Feistel.
            7 é coprimo com 80 e com 40, logo é permutação nos dois casos; o
            passo 7 leva bits vizinhos para posições distantes (difusão real),
            ao contrário de uma rotação (i+1) que só desliza o bloco.
"""

# Inverso multiplicativo em GF(2^4), gerado com o polinômio irredutível x^4+x+1.
SBOX: list[int] = [0, 1, 9, 14, 13, 11, 7, 6, 15, 2, 12, 5, 10, 4, 3, 8]

# π(i) = (7·i + 3) mod 80
SPN_PBOX: list[int] = [(7 * i + 3) % 80 for i in range(80)]

# π(i) = (7·i + 3) mod 40
FEISTEL_PBOX: list[int] = [(7 * i + 3) % 40 for i in range(40)]

