from cipher_helper import encrypt_block, block_from_str
from encrypt.chosen_ciphers import s06, s07, f07

def main():
    master_key = 0x000ABBA
    cipher_design = s07

    # bloco
    m1 = block_from_str("opa")
    enc1 = encrypt_block(m1, cipher_design, master_key)
    print(f"m1 = {enc1.m_hex}")
    print(f"c1 = {enc1.c_hex}")
    print(f"m1 = {enc1.m_b}")
    print(f"c1 = {enc1.c_b}\n")

    # bloco
    m2 = 0b11000110101010010110101
    enc2 = encrypt_block(m1, cipher_design, master_key)
    print(f"m2 = {enc2.m_hex}")
    print(f"c2 = {enc2.c_hex}")
    print(f"m2 = {enc2.m_b}")
    print(f"c2 = {enc2.c_b}\n")

    # bloco
    m3 = m2 + 1
    enc3 = encrypt_block(m1, cipher_design, master_key)
    print(f"m3 = {enc3.m_hex}")
    print(f"c3 = {enc3.c_hex}")
    print(f"m3 = {enc3.m_b}")
    print(f"c3 = {enc3.c_b}\n")

if __name__ == "__main__":
    main()