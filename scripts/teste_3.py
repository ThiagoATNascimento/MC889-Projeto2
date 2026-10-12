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
    Requer uma sequência grande de bits (N >= 1.000.000) para validade estatística.
    """
    n = len(bits)
    num_blocks = n // m
    if num_blocks < 1:
        raise ValueError("Quantidade de bits insuficiente para realizar o teste com o M especificado.")
    
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
    
    return chi_squared, p_value, num_blocks

def evaluate_cipher(cipher_design, name, master_key):
    print(f"=== Avaliando Cifra: {name} ===")
    
    # Define o tamanho correto do bloco em bits (80 para SPN, 40 para Feistel)
    block_len = 40 if "Feistel" in name or "f" in name.lower() else 80
    
    # Meta de 1.000.000 de bits exigida pelo NIST SP 800-22
    target_bits = 1_000_000
    num_messages = math.ceil(target_bits / block_len)
    
    print(f"Gerando {num_messages} blocos para acumular >= {target_bits} bits...")
    
    bit_stream = []
    for i in range(num_messages):
        # Mensagem gerada de forma incremental
        m = 0b11000110101010010110101 + i
        enc = encrypt_block(m, cipher_design, master_key)
        
        # Mostra os primeiros exemplos apenas nos 3 primeiros blocos para inspeção visual
        if i < 3:
            print(f"[{name}] Bloco {i+1}:")
            print(f"  m = {enc.m_hex}")
            print(f"  c = {enc.c_hex}")
            print(f"  m (bin) = {enc.m_b}")
            print(f"  c (bin) = {enc.c_b}\n")
            
        c_str = str(enc.c_b)
        if c_str.startswith("0b"):
            c_str = c_str[2:]
        c_str = c_str.zfill(block_len)
        
        c_bits = [int(b) for b in c_str]
        bit_stream.extend(c_bits)

    print(f"Total de bits coletados: {len(bit_stream)}")

    try:
        # Executando o teste com blocos de M = 500
        chi_stat, p_val, blocks_used = linear_complexity_test(bit_stream, m=500)
        
        print(f"--- Resultado do Teste de Complexidade Linear ({name}) ---")
        print(f"Sub-blocos analisados (M=500): {blocks_used}")
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