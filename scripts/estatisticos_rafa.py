import random

from cipher_helper import encrypt_block, get_encrypter, BlockEncryption
from cipher_helper import BLOCK_SIZE
from encrypt.chosen_ciphers import s06, s07, f07
from teste_3 import evaluate_cipher as t3_evaluate

def main():

    efeito_avalanche([1, 2, 3, 4, 5, 6], s06)
    efeito_avalanche([1, 2, 3, 4, 5], s07)
    efeito_avalanche([1, 2, 3, 4, 5, 6, 7, 8, 9], f07)

    print("\n==================================================")
    """
    teste_1_balanceamento(s06)
    teste_1_balanceamento(s07)
    teste_1_balanceamento(f07)

    print("\n==================================================")

    teste_3_(s06)
    teste_3_(s07)
    teste_3_(f07)
    """

def efeito_avalanche(rounds_list: list[int], cipher_design, master_key=0x100, qtd=1000):
    print(f"\n----> EFEITO AVALANCHE para {cipher_design.NAME}:")
    for r in rounds_list:
        print(f">> Até round {r}:")
        encrypter = get_encrypter(cipher_design, r, master_key)
        efeito_avalanche_for_round(encrypter, qtd)

def efeito_avalanche_for_round(encrypter, qtd=1000):

    total_dif: float = 0
    total_proportion: float = 0
    min_proportion = 0
    max_proportion = 0

    changed_pairs = [[False for _ in range(BLOCK_SIZE)] for _ in range(BLOCK_SIZE)]

    for i in range(qtd):
        m_base = random.randint(0, 2**BLOCK_SIZE - 1)
        enc_base = BlockEncryption(encrypter.encrypt_block(m_base), m_base)

        for j in range(BLOCK_SIZE):
            mi: int = m_base ^ (2**j)
            enc_i = BlockEncryption(encrypter.encrypt_block(mi), mi)

            difs = enc_base.c ^ enc_i.c
            dif_count = difs.bit_count()
            total_dif += float(dif_count)

            prop = float(dif_count) / BLOCK_SIZE
            total_proportion += prop

            if prop < min_proportion:
                min_proportion = prop
            if prop > max_proportion:
                max_proportion = prop

            for k in range(BLOCK_SIZE):
                if (difs >> k) & 1:
                    changed_pairs[j][k] = True

    never_change_pairs_count = 0
    for j in range(BLOCK_SIZE):
        for k in range(BLOCK_SIZE):
            if not changed_pairs[j][k]:
                never_change_pairs_count += 1

    mean_dif: float = total_dif/(qtd*BLOCK_SIZE)
    mean_proportion: float = total_proportion/(qtd*BLOCK_SIZE)

    print(f"  diferença média (n bits) = {mean_dif:.4f}")
    print(f"  fração diferença média = {mean_proportion}")
    print(f"  fração diferença mínima = {min_proportion}")
    print(f"  fração diferença máxima = {max_proportion}")
    print(f"  número de pares que nunca mudam = {never_change_pairs_count}")
    #print(f"  posições que nunca mudam para j=0: {[k for k in range(BLOCK_SIZE-1, -1, -1) if not changed_pairs[j][k]]}")
    print(f"  posições que mudaram (ao menos 1x) para j=0: {[k for k in range(BLOCK_SIZE-1, -1, -1) if changed_pairs[j][k]]}")


def teste_1_balanceamento(cipher_design, master_key=0x100, qtd=10000):
    """Verifica se a saída da cifra tem aproximadamente L/2 bits 1 e 0."""
    total_ones = 0
    total_zeros = 0

    encrypter = get_encrypter(cipher_design, master_key=master_key)

    for i in range(qtd):
        m = random.randint(0, 2**BLOCK_SIZE - 1)
        enc = BlockEncryption(encrypter.encrypt_block(m), m)
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
