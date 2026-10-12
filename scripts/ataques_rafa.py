from cipher_helper import encrypt_block, get_encrypter, BlockEncryption, block_to_str, get_blocks, block_from_str
from cipher_helper import BLOCK_SIZE
from encrypt.chosen_ciphers import s06, s07, f07
import math

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

DIF_POS: list[list[int]] = []
DIF_MASK: list[int] = []

BLOCK_BYTES = BLOCK_SIZE // 8
CELL = BLOCK_BYTES  # largura de uma célula = 10 caracteres


def block_anal_bytes(block: int, nbytes: int = BLOCK_BYTES) -> str:
    """ASCII dos nbytes primeiros bytes (big-endian); '.' = não imprimível; completa com espaço."""
    data = block.to_bytes(BLOCK_BYTES, byteorder="big")[:nbytes]
    text = "".join(chr(b) if 32 <= b <= 126 else "." for b in data)
    return text.ljust(BLOCK_BYTES)


def main():
    enc = get_encrypter(s07, 4, DEFAULT_KEY)
    e0 = enc.encrypt_block(0)

    def L(d: int) -> int:
        """Parte linear da cifra: L(d) = E(d) ^ E(0). Independe da chave."""
        return enc.encrypt_block(d) ^ e0

    idx = 0
    c_all, total_bits = CI[idx], N_BITS[idx]
    total_bytes = total_bits // 8

    blocks = get_blocks(c_all, total_bits)
    n = len(blocks)
    # bytes realmente existentes em cada bloco (o último é truncado)
    valid = [min(BLOCK_BYTES, total_bytes - BLOCK_BYTES * i) for i in range(n)]

    # xors[i][j] = m_i ^ m_j, válido nos min(valid[i], valid[j]) primeiros bytes
    xors = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j:
                xors[i][j] = blocks[i] ^ blocks[j] ^ L(i ^ j)

    # ---------- tabela simétrica ----------
    header = " " * 6 + "".join(f"| {('m' + str(j)).ljust(CELL)} " for j in range(n))
    sep = "-" * len(header)
    lines = [header, sep]
    for i in range(n):
        row = f"{('m' + str(i)).ljust(5)} "
        for j in range(n):
            if i == j:
                cell = "-".ljust(CELL)   # m_i ^ m_i = 0, sem informação
            else:
                cell = block_anal_bytes(xors[i][j], min(valid[i], valid[j]))
            row += f"| {cell} "
        lines.append(row)
    table = "\n".join(lines)

    print(f"{n} blocos, bytes válidos no último: {valid[-1]}")
    print("Célula (i, j) = m_i ^ m_j  ('.' = byte não imprimível)\n")
    print(table)

    """
    with open("results/xors_mi_mj.txt", "w", encoding="utf-8") as f:
        f.write(table + "\n\n")
        f.write("HEX (m_i ^ m_j):\n")
        for i in range(n):
            for j in range(i + 1, n):
                k = min(valid[i], valid[j])
                h = xors[i][j].to_bytes(BLOCK_BYTES, "big")[:k].hex()
                f.write(f"m{i} ^ m{j} = {h}\n")
    """

    plain, conf, ranking, d = solve_columns(xors, valid, n)
    show_solution(plain, conf, ranking, d, n)

    # depois de ler o resultado, force o que você tem certeza:
    hh = "Comer......... "
    hints = {}#{(1,4): ord('c'), (1,5): ord('o'), (1,6): ord('n'), (1,7): ord('d'), (1,8): ord('e'), (1, 9): ord('n'), (2, 0): ord('a'), (2, 1): ord('d')}
    for i in range(len(hh)):
        cc = hh[i]
        if cc == '.':
            continue
        if cc == "*":
            cc = '.'

        hints[(i//10, i%10)] = ord(cc)
    plain, conf, ranking, d = solve_columns(xors, valid, n, hints=hints)
    show_solution(plain, conf, ranking, d, n)



# frequências aproximadas (%) em português; só a ordem de grandeza importa
_FREQ = {' ': 17, 'a': 12.5, 'e': 11.5, 'o': 10, 's': 6, 'r': 6, 'i': 6, 'n': 5,
         'd': 4, 'm': 4, 'u': 4, 't': 4, 'c': 3, 'l': 3, 'p': 2.5, 'v': 1.5,
         'g': 1, 'h': 1, 'q': 1, 'b': 1, 'f': 1, 'z': .4, 'j': .4, 'x': .3,
         'k': .1, 'w': .1, 'y': .1, ',': 1.5, '.': 1.5}

def _build_score():
    t = [1e-4] * 256                       # controle / inválido
    for b in range(0x80, 0x100):
        t[b] = 0.3                         # possível byte de acento (UTF-8)
    for b in range(33, 127):
        t[b] = 0.2                         # pontuação, dígitos...
    for b in range(ord('A'), ord('Z') + 1):
        t[b] = 0.4                         # maiúsculas
    for b in range(ord('0'), ord('9') + 1):
        t[b] = 0.3
    t[ord('\n')] = 0.2
    for ch, f in _FREQ.items():
        t[ord(ch)] = f
        if ch.isalpha():
            t[ord(ch.upper())] = max(t[ord(ch.upper())], f * 0.15)
    return [math.log(v) for v in t]

LOGP = _build_score()

def solve_columns(xors, valid, n, hints=None, top=3):
    """
    Para cada posição p (0..9) acha x = m_0[p] maximizando a verossimilhança
    de toda a coluna. hints = {(i, p): byte} fixa m_i[p] (ex.: ord(' ')).
    Retorna: plain[i] (bytes recuperados, palpite) e conf[p] (margem de log-prob).
    """
    hints = hints or {}
    d = [xors[0][i].to_bytes(BLOCK_BYTES, "big") for i in range(n)]  # d[0] = 0
    col_x, conf, ranking = [], [], []

    for p in range(BLOCK_BYTES):
        rows = [i for i in range(n) if valid[i] > p]
        fixed = [h ^ d[i][p] for (i, pp), h in hints.items() if pp == p and i in rows]
        cands = set(fixed) if fixed else range(256)
        if len(set(fixed)) > 1:
            print(f"aviso: hints conflitantes na coluna {p}")
        scores = sorted(((sum(LOGP[x ^ d[i][p]] for i in rows), x) for x in cands),
                        reverse=True)
        col_x.append(scores[0][1])
        conf.append(scores[0][0] - scores[1][0] if len(scores) > 1 else float("inf"))
        ranking.append(scores[:top])

    plain = [bytes(col_x[p] ^ d[i][p] for p in range(valid[i])) for i in range(n)]
    return plain, conf, ranking, d


def show_solution(plain, conf, ranking, d, n, thr=3.0):
    printable = lambda b: chr(b) if 32 <= b <= 126 else "·"
    print("confiança por coluna (margem do 1º p/ 2º candidato; baixa = duvidoso):")
    print("  " + " ".join(f"{p}:{c:5.1f}" for p, c in enumerate(conf)))
    print("\nplaintext estimado (· = não imprimível, ? = coluna de baixa confiança):")
    for i, blk in enumerate(plain):
        s = "".join(printable(b) if conf[p] >= thr else "?" for p, b in enumerate(blk))
        print(f"  m{i:<3d}|{s}|")
    print("\ntexto contínuo:")
    print("".join(printable(b) for blk in plain for b in blk))
    print("\ntop candidatos por coluna (m_0[p]) e como ficam nos 4 primeiros blocos:")
    for p, cands in enumerate(ranking):
        for sc, x in cands:
            col = "".join(printable(x ^ d[i][p]) for i in range(min(n, 4)))
            print(f"  col {p} x=0x{x:02x} score={sc:7.1f}  {col}")
        print()

if __name__ == "__main__":
    main()