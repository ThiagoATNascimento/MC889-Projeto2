import math

from encrypt.spn import SPN80
from encrypt.feistel import Feistel80
from encrypt.cipher_base import BLOCK_SIZE, SPN_ROUNDS, FEISTEL_ROUNDS

BLOCK_BYTES = BLOCK_SIZE // 8

class BlockEncryption:
    def __init__(self, c: int, m: int):
        self.c = c
        self.m = m
        self.c_b = f"0b{c:0{BLOCK_SIZE}b}"
        self.m_b = f"0b{m:0{BLOCK_SIZE}b}"
        self.c_hex = f"0x{c:0{BLOCK_BYTES*2}x}"
        self.m_hex = f"0x{m:0{BLOCK_BYTES*2}x}"

    def c_bit_count(self) -> tuple[int, int]:
        """
            Retorn count_0, count_1
        """
        count_1 = self.c.bit_count()
        return BLOCK_SIZE - count_1, count_1


def block_from_str(block_text: str) -> int:
    data = block_text.encode()
    m = int.from_bytes(data.ljust(BLOCK_BYTES, b"\x00"), "big")
    return m

def block_to_str(m: int) -> str:
    data = m.to_bytes(BLOCK_BYTES, "big")
    return data.rstrip(b"\x00").decode()

import math

def get_blocks(msg_int: int, total_bits: int) -> list:
    """
    Divide a mensagem inteira em uma lista de blocos de 80 bits.
    Alinha o último bloco (truncado) à esquerda, preenchendo com zeros à direita.
    """
    block_bits = BLOCK_BYTES * 8
    num_blocks = math.ceil(total_bits / block_bits)
    blocks = []
    
    mask = (1 << block_bits) - 1
    
    for i in range(num_blocks):
        shift_amount = total_bits - ((i + 1) * block_bits)
        
        if shift_amount >= 0:
            # CASO 1: Bloco completo (80 bits)
            bloco = (msg_int >> shift_amount) & mask
            blocks.append(bloco)
            
        else:
            # CASO 2: Último bloco incompleto (truncado)
            bits_restantes = total_bits - (i * block_bits)
            
            # 1. Isola os bits que sobraram na extremidade direita do inteiro original
            bloco_truncado = msg_int & ((1 << bits_restantes) - 1)
            
            # 2. Desloca para a esquerda para alinhar com o topo do bloco de 80 bits
            # Isso adiciona os zeros à direita necessários para a matemática do XOR bater
            alinhamento = block_bits - bits_restantes
            bloco_alinhado = bloco_truncado << alinhamento
            
            blocks.append(bloco_alinhado)
            
    return blocks


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
