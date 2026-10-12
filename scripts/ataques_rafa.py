from cipher_helper import encrypt_block, get_encrypter, BlockEncryption, block_to_str, get_blocks, block_from_str
from cipher_helper import BLOCK_SIZE
from encrypt.chosen_ciphers import s06, s07, f07

DEFAULT_KEY = 0x3b46df018ec647a

IV = [0xeb70721165, 0x6439edc357, 0x8a4375e1a2, 0xef273fd1e5, 0xfd8535bfae]

CI = [
    0xf297bb995377a57bbcd4d197b993012703a2f5decb8da,
    0xcade25839e7059fa98e7f13deccc907a5abc98fae49a22cc923547bf8ff4e9973b9e96,
    0xf42c3a8610ad45e85f33ce3d328943b804eef9ebc43f3f8d43b3e739f3f9d39df88743b4405b36b7dc37388910,
    0xe5fe3e04c22303baf3decdfe3019ca2109b8f7d4c9fe381fc03a0af2fc95c5f27d01c22646f9b597d9b09ecb60f609baf0c3cdfe2daf0a2615f1f8d08ce472,
    0xf12b9a02876a0fb4f4d7cc2b8303c3764af9a6d4d03b8f09cf2540fb8cbef27e9f09c36140b0a7d1dc2c9e0f8b6a5cfbb1dfdc2c9e0b822540f9a0d4d02a944c906042fba584cd7e95058d625a1a7d9c802f8909806c5cbef4d5c52c9803817746abf4d0803c930d956001
]

N_BITS = [45*4, 70*4, 90*4, 126*4, 214*4]

DIF_POS = [[], [17], [17, 6], [17], [17, 6, 75]]

DIF_MASK = []

for l in DIF_POS:
    mask: int = 0
    for d in l:
        mask += 2**d
    DIF_MASK.append(mask)

def main():
    iv = IV[2]
    c_all = CI[2]
    t = N_BITS[2]

    n_blocks = t // BLOCK_SIZE + 1
    print(n_blocks)

    c = get_blocks(c_all, t)

    print([f"{ci:x}" for ci in c])

    text = ""
    for i in range(len(c) - 1):
        m1_xor_m2 = c[i] ^ c[i+1] ^ DIF_MASK[0]
        text += "|" + block_anal_bytes(m1_xor_m2)

    print(f"Texto: {text}")

def block_anal_bytes(block: int) -> str:
    xor_bytes = block.to_bytes(10, byteorder='big')
    text = ""
    for i, b in enumerate(xor_bytes):
        # b já é um valor numérico entre 0 e 255 correspondente ao byte
        
        # Tenta imprimir o caractere se estiver no intervalo ASCII legível padrão
        readable_char = chr(b) if 32 <= b <= 126 else '.'
        text += readable_char
        
        #print(f"Byte {i:02d} | Hex: {b:02x} | Bin: {b:08b} | ASCII: {readable_char}")
    return text

if __name__ == "__main__":
    main()