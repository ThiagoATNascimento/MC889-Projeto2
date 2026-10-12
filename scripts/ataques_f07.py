from cipher_helper import encrypt_block, get_encrypter, BlockEncryption, block_to_str, get_blocks, block_from_str
from cipher_helper import BLOCK_SIZE
from encrypt.chosen_ciphers import s06, s07, f07
import math

DEFAULT_KEY = 0x3b46df018ec647a

IV = [0x22bfef7136, 0xa96ab909cf, 0xe232b72bba, 0x3ac5dc673b, 0x07d077fa76]

CI = [
    0x033ea7e714ce5afcd9fee0debaf601c25774d8b193f40ae40fcd56b4ccf4ac5e8db9,
    0x08ea480b65f21a50b0752eaf54146db359cbb43b286a6a087ab35e40f9682c3f2a4778f654d6b8762ca41d087a,
    0xb7b6e27167c960d8ab9285f3b23467df6f57bb92c423ce23688c7dd4acdf813d9c3e67d87c50ba9ec4a3a02328cd7fc5b5d1,
    0x98513bff04f24bc1c080f67324d80ea74415c69bb0cc5a9c0fe205d6c99db5d14bca02f54414c69bb04c3a9c0ee205d3cb87ae5125,
    0x57d4d75ddd3fe8ef52e154e58871911df56a43866854a557905ce9fc55c92811e25e980fa06a55d265c37491935ce4eb47c374d28e5d921de4615786675efa128a13e34c8e
]

N_BITS = [68*4, 90*4, 100*4, 106*4, 138*4]

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
    enc = get_encrypter(f07, 8, DEFAULT_KEY)
    e0 = enc.encrypt_block(0)

    def L(d: int) -> int:
        """Parte linear da cifra: L(d) = E(d) ^ E(0). Independe da chave."""
        return enc.encrypt_block(d) ^ e0

    idx = 2
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
    hh = "Sem"
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