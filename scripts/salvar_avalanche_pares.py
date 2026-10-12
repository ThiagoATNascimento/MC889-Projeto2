import json

from cipher_helper import encrypt_block, get_encrypter, BlockEncryption, block_to_str, get_blocks, block_from_str
from cipher_helper import BLOCK_SIZE
from encrypt.chosen_ciphers import s06, s07, f07
from estatisticos import efeito_avalanche_counter_for_round

DEFAULT_KEY = 0x3b46df018ec647a

COUNTER_MAX = 20

def main():

    print(f"\n----> AVALANCHE na keystream para {s06.NAME}:")
    encrypter = get_encrypter(s06, 4, DEFAULT_KEY)
    s06_changed_pairs = efeito_avalanche_counter_for_round(encrypter, qtd=10000, counter_max=COUNTER_MAX)
    s06_changes = [
        [k for k in range(BLOCK_SIZE) if s06_changed_pairs[j][k]]
        for j in range(COUNTER_MAX-1)
    ]

    print(f"\n----> AVALANCHE na keystream para {s07.NAME}:")
    encrypter = get_encrypter(s07, 4, DEFAULT_KEY)
    s07_changed_pairs = efeito_avalanche_counter_for_round(encrypter, qtd=10000, counter_max=COUNTER_MAX)
    s07_changes = [
        [k for k in range(BLOCK_SIZE) if s07_changed_pairs[j][k]]
        for j in range(COUNTER_MAX-1)
    ]

    print(f"\n----> AVALANCHE na keystream para {f07.NAME}:")
    encrypter = get_encrypter(f07, 8, DEFAULT_KEY)
    f07_changed_pairs = efeito_avalanche_counter_for_round(encrypter, qtd=10000, counter_max=COUNTER_MAX)
    f07_changes = [
        [k for k in range(BLOCK_SIZE) if f07_changed_pairs[j][k]]
        for j in range(COUNTER_MAX-1)
    ]

    to_save = {
        "s06_changes": s06_changes,
        "s07_changes": s07_changes,
        "f07_changes": f07_changes,
    }

    with open("avalanche_pares.json", "w", encoding="utf-8") as f:
        json.dump(to_save, f, indent=2)

if __name__ == "__main__":
    main()