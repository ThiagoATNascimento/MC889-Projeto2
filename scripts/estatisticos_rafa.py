import random

from cipher_helper import encrypt_block, block_from_str, BlockEncryption
from cipher_helper import BLOCK_SIZE
from encrypt.chosen_ciphers import s06, s07, f07

def main():

    teste_balanceamento(s06)
    teste_balanceamento(s07)
    teste_balanceamento(f07)

    print("===============================")

    teste_avalanche(s06)
    teste_avalanche(s07)
    teste_avalanche(f07)


def teste_balanceamento(cipher_design, master_key=0x100, qtd=1000):
    """Verifica se a saída da cifra tem aproximadamente L/2 bits 1 e 0."""
    total_ones = 0
    total_zeros = 0

    for i in range(qtd):
        m = random.randint(0, 2**BLOCK_SIZE - 1)
        #m = i
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

def teste_avalanche(cipher_design, master_key=0x100, qtd=1000):

    mean_proportion: float = 0
    mean_dif: float = 0

    for i in range(qtd):
        m_base = random.randint(0, 2**BLOCK_SIZE - 1)
        #m_base = i
        enc_base = encrypt_block(m_base, cipher_design, master_key)

        for j in range(BLOCK_SIZE):
            mi: int = m_base ^ (2**j)
            enc_i = encrypt_block(mi, cipher_design, master_key)

            dif = (enc_base.c ^ enc_i.c).bit_count()
            mean_dif += float(dif)
            mean_dif /= 2

            prop = float(dif) / BLOCK_SIZE
            mean_proportion += prop
            mean_proportion /= 2

    print(f"\n----> Teste de AVALANCHE para {cipher_design.NAME}:")
    print(f"  diferença média = {mean_dif}")
    print(f"  proporção de diferença média = {mean_proportion}")


if __name__ == "__main__":
    main()
