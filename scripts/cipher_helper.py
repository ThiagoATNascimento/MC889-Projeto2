from encrypt.spn import SPN80
from encrypt.feistel import Feistel80
from encrypt.cipher_base import BLOCK_SIZE

block_bytes = BLOCK_SIZE // 8

class BlockEncryption:
    def __init__(self, c: int, m: int):
        self.c = c
        self.m = m
        self.c_b = f"0b{c:b}"
        self.m_b = f"0b{m:b}"
        self.c_hex = f"0x{c:x}"
        self.m_hex = f"0x{m:x}"


def block_from_str(block_text: str) -> int:
    data = block_text.encode()
    m = int.from_bytes(data.ljust(block_bytes, b"\x00"), "big")
    return m

def encrypt_block(m: int, cipher_design: object, master_key: int | None = None) -> BlockEncryption:
    """
        Retorna (c, c_hex_str), (m, m_hex_str)
        c -> hex do bloco encryptado
        
    """

    if master_key != None:
        cipher_design.MASTER_KEY = master_key
    
    if cipher_design.SPEC == "spn":
        #print("spn!")
        encrypter = SPN80.from_design(cipher_design)
    else:
        #print("feistel!")
        encrypter = Feistel80.from_design(cipher_design)

    

    c = encrypter.encrypt_block(m)

    return BlockEncryption(c, m)

if __name__ == "__main__":
    import encrypt.chosen_ciphers.f07 as mc
    print("Testando")
    b = encrypt_block("oi bobo", mc)
