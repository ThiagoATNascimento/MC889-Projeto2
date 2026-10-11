from cipher_helper import encrypt_block, block_from_str, BlockEncryption
from encrypt.chosen_ciphers import s06, s07, f07

def main():

    teste_balanceamento(s07)
    teste_balanceamento(s06)
    teste_balanceamento(f07)


def teste_balanceamento(cipher_design, master_key=0x100, qtd=256):
    """Verifica se a saída da cifra tem aproximadamente L/2 bits 1 e 0."""
    total_ones = 0
    total_zeros = 0

    for i in range(qtd):
        enc = encrypt_block(i, cipher_design, master_key)
        bits_0, bits_1 = enc.c_bit_count()
        total_zeros += bits_0
        total_ones += bits_1

    total_bits = total_ones + total_zeros
    esperado = total_bits / 2
    diferenca = abs(total_ones - esperado)
    #tolerancia = max(2, 0.1 * esperado)

    print(f"\n----> Teste de balanceamento para {cipher_design.NAME}:")
    print(f"  total 1s = {total_ones}")
    print(f"  total 0s = {total_zeros}")
    print(f"  esperado ~= {esperado:.2f} 1s / 0s")
    print(f"  diferenca absoluta = {diferenca:.2f}")
    #print(f"  resultado = {'OK' if diferenca <= tolerancia else 'FALHOU'}\n")

    return


if __name__ == "__main__":
    main()
