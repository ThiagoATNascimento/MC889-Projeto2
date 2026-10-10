# S-box: f(x) = round(7.5 + 7.5 * sin(x)) % 16.
SBOX: list[int] = [8, 14, 14, 9, 2, 0, 5, 12, 15, 11, 3, 0, 3, 11, 15, 12]

SPN_PBOX: list[int] = [
    ((i - 1) // 2) if i % 2 == 1 else (40 + i // 2) for i in range(80)
]

FEISTEL_PBOX: list[int] = [
    ((i - 1) // 2) if i % 2 == 1 else (20 + i // 2) for i in range(40)
]
