import random

from cipher_helper import encrypt_block, block_from_str, BlockEncryption
from cipher_helper import BLOCK_SIZE
from encrypt.chosen_ciphers import s06, s07, f07
from teste_3 import evaluate_cipher as t3_evaluate

def main():

    teste_1_balanceamento(s06)
    teste_1_balanceamento(s07)
    teste_1_balanceamento(f07)

    print("\n==================================================")

    efeito_avalanche(s06)
    efeito_avalanche(s07)
    efeito_avalanche(f07)

    print("\n==================================================")

    teste_3_(s06)
    teste_3_(s07)
    teste_3_(f07)


def efeito_avalanche(cipher_design, master_key=0x100, qtd=1000):

    total_dif: float = 0
    total_proportion: float = 0

    for i in range(qtd):
        m_base = random.randint(0, 2**BLOCK_SIZE - 1)
        enc_base = encrypt_block(m_base, cipher_design, master_key)

        ld = 0
        lp = 0

        for j in range(BLOCK_SIZE):
            mi: int = m_base ^ (2**j)
            enc_i = encrypt_block(mi, cipher_design, master_key)

            dif = (enc_base.c ^ enc_i.c).bit_count()
            ld += float(dif)

            prop = float(dif) / BLOCK_SIZE
            lp += prop

        total_dif += ld / BLOCK_SIZE
        total_proportion += lp / BLOCK_SIZE

    mean_dif: float = total_dif/qtd
    mean_proportion: float = total_proportion/qtd

    print(f"\n----> Teste de AVALANCHE para {cipher_design.NAME}:")
    print(f"  diferença média = {mean_dif}")
    print(f"  proporção de diferença média = {mean_proportion}")


def teste_1_balanceamento(cipher_design, master_key=0x100, qtd=10000):
    """Verifica se a saída da cifra tem aproximadamente L/2 bits 1 e 0."""
    total_ones = 0
    total_zeros = 0

    for i in range(qtd):
        m = random.randint(0, 2**BLOCK_SIZE - 1)
        enc = encrypt_block(m, cipher_design, master_key)
        bits_0, bits_1 = enc.c_bit_count()
        total_zeros += bits_0
        total_ones += bits_1

    total_bits = total_ones + total_zeros
    esperado = total_bits / 2
    diferenca = abs(total_ones - esperado)
    #tolerancia = max(2, 0.1 * esperado)

    print(f"\n----> Teste de BALANCEAMENTO para {cipher_design.NAME}:")
    print(f"  total 1s = {total_ones}")
    print(f"  total 0s = {total_zeros}")
    print(f"  esperado ~= {esperado:.2f} 1s / 0s")
    print(f"  diferenca absoluta = {diferenca:.2f}")
    #print(f"  resultado = {'OK' if diferenca <= tolerancia else 'FALHOU'}\n")

    return

def teste_3_(cipher_design, master_key=0x100, qtd=1000):
    t3_evaluate(cipher_design, cipher_design.NAME, master_key=master_key)

if __name__ == "__main__":
    main()
