from cipher_helper import encrypt_block, block_from_str
from encrypt.chosen_ciphers import s06, s07, f07
import math

def berlekamp_massey(block):
    """
    Implementação do algoritmo de Berlekamp-Massey para calcular 
    a complexidade linear de um bloco de bits.
    """
    n = len(block)
    c = [0] * n
    b = [0] * n
    c[0] = 1
    b[0] = 1
    l = 0
    m = -1
    
    for i in range(n):
        v = block[i]
        for j in range(1, l + 1):
            v ^= c[j] & block[i - j]
        if v == 1:
            temp = list(c)
            shift = i - m
            for j in range(n - shift):
                c[j + shift] ^= b[j]
            if 2 * l <= i:
                l = i + 1 - l
                m = i
                b = temp
    return l

def linear_complexity_test(bits, m=500):
    """
    Teste de Complexidade Linear - NIST SP 800-22 (Seção 2.10).
    """
    n = len(bits)
    if n < m:
        m = n
        
    num_blocks = n // m
    if num_blocks < 1:
        raise ValueError("Quantidade de bits insuficiente para realizar o teste.")
    
    # Probabilidades teóricas para M = 500 (NIST SP 800-22)
    pi = [0.01047, 0.03125, 0.12500, 0.31250, 0.31250, 0.15625, 0.05208]
    v = [0] * 7
    
    for i in range(num_blocks):
        block = bits[i * m : (i + 1) * m]
        L = berlekamp_massey(block)
        
        if L <= m / 2 - 2:
            v[0] += 1
        elif L == m / 2 - 1:
            v[1] += 1
        elif L == m / 2:
            v[2] += 1
        elif L == m / 2 + 1:
            v[3] += 1
        elif L == m / 2 + 2:
            v[4] += 1
        elif L == m / 2 + 3:
            v[5] += 1
        else:
            v[6] += 1

    chi_squared = 0.0
    for i in range(7):
        expected = num_blocks * pi[i]
        if expected > 0:
            chi_squared += ((v[i] - expected) ** 2) / expected
            
    p_value = math.exp(-chi_squared / 2.0) if chi_squared > 0 else 1.0
    
    return chi_squared, p_value

def evaluate_cipher(cipher_design, name, master_key):
    print(f"\n----> Teste de BALANCEAMENTO para {cipher_design.NAME}:")
    
    # Define o tamanho correto do bloco em bits (80 para SPN, 40 para Feistel)
    block_len = 40 if "Feistel" in name or "f" in name.lower() else 80
    
    bit_stream = []
    for i in range(30):
        m = 0b11000110101010010110101 + i
        enc = encrypt_block(m, cipher_design, master_key)
        
        if i < 3:
            print(f"[{name}] Bloco {i+1}:")
            print(f"  m = {enc.m_hex}")
            print(f"  c = {enc.c_hex}")
            print(f"  m (bin) = {enc.m_b}")
            print(f"  c (bin) = {enc.c_b}\n")
            
        # Tratamento seguro da string binária removendo '0b' e aplicando zfill
        c_str = str(enc.c_b)
        if c_str.startswith("0b"):
            c_str = c_str[2:]
        c_str = c_str.zfill(block_len)
        
        c_bits = [int(b) for b in c_str]
        bit_stream.extend(c_bits)

    try:
        block_size = min(500, len(bit_stream))
        chi_stat, p_val = linear_complexity_test(bit_stream, m=block_size)
        
        print(f"--- Resultado do Teste de Complexidade Linear ({name}) ---")
        print(f"Estatística Chi-quadrado: {chi_stat:.4f}")
        print(f"P-Value: {p_val:.4f}")
        
        status = "APROVADO (Aleatório)" if p_val >= 0.01 else "REPROVADO (Não-aleatório)"
        print(f"Status: {status}\n")
    except Exception as e:
        print(f"Erro ao executar o teste para {name}: {e}\n")

def main():
    master_key = 0x000ABBA
    
    ciphers = [
        (s06, "SPN s06"),
        (s07, "SPN s07"),
        (f07, "Feistel f07")
    ]
    
    for cipher_design, name in ciphers:
        evaluate_cipher(cipher_design, name, master_key)

if __name__ == "__main__":
    main()