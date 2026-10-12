from encrypt.spn import SPN80
from encrypt.feistel import Feistel80
from encrypt.cipher_base import BLOCK_SIZE, SPN_ROUNDS, FEISTEL_ROUNDS

block_bytes = BLOCK_SIZE // 8

class BlockEncryption:
    def __init__(self, c: int, m: int):
        self.c = c
        self.m = m
        self.c_b = f"0b{c:0{BLOCK_SIZE}b}"
        self.m_b = f"0b{m:0{BLOCK_SIZE}b}"
        self.c_hex = f"0x{c:0{block_bytes*2}x}"
        self.m_hex = f"0x{m:0{block_bytes*2}x}"

    def c_bit_count(self) -> tuple[int, int]:
        """
            Retorn count_0, count_1
        """
        count_1 = self.c.bit_count()
        return BLOCK_SIZE - count_1, count_1


def block_from_str(block_text: str) -> int:
    data = block_text.encode()
    m = int.from_bytes(data.ljust(block_bytes, b"\x00"), "big")
    return m

def get_encrypter(cipher_design: object, rounds: int | None = None, master_key: int | None = None) -> SPN80 | Feistel80:
    if master_key is not None:
            cipher_design.MASTER_KEY = master_key
    
    if cipher_design.SPEC == "spn":
        #print("spn!")
        r = rounds if rounds is not None else SPN_ROUNDS
        encrypter = SPN80(cipher_design.SBOX, cipher_design.SPN_PBOX, r, cipher_design.MASTER_KEY)
    else:
        #print("feistel!")
        r = rounds if rounds is not None else FEISTEL_ROUNDS
        encrypter = Feistel80(cipher_design.SBOX, cipher_design.FEISTEL_PBOX, r, cipher_design.MASTER_KEY)

    return encrypter

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
