
# arquivo mantido para não dar warning / erro no ctr.py / feistel.py
# mas não devemos usar esta cifra para nada no projeto 2

SBOX: list[int] = [i for i in range(16)]
SPN_PBOX: list[int] = [b for b in range(80)]
FEISTEL_PBOX: list[int] = [b for b in range(40)]
MASTER_KEY: int = 0x0000000000000000

SPEC = "spn"
