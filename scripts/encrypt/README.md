# Projeto 1: Implementação da cifra de bloco

As duas cifras já estão implementadas. Somente a S-box, duas P-box e
a chave devem ser fornecidas; as funções de rodada, a expansão de chave e o modo de operação
rodam em cima da sua configuração.

Python 3.10 ou mais novo, sem dependências.

## Configurando a Cifra

Editar somente o arquivo [`my_cipher.py`](my_cipher.py):

| constante | o que é |
|---|---|
| `SBOX` | 16 entradas, cada uma um valor de `0..15`. Não precisa ser bijetora. Usada pelas duas cifras. |
| `SPN_PBOX` | 80 entradas, uma permutação de `0..79`. A camada de difusão da SPN. |
| `FEISTEL_PBOX` | 40 entradas, uma permutação de `0..39`. Dentro da função de rodada da Feistel. |
| `MASTER_KEY` | um inteiro em `[0, 2**80)`, diferente de 0. |

O número de rodadas está fixado em
[`cipher_base.py`](cipher_base.py) em 4 para a SPN e 8 para a rede de Feistel.

## Como executar

```bash
python3 spn.py "Hello" "MC889"              # um bloco por mensagem, pela SPN
python3 feistel.py "Hello" "MC889"          # o mesmo pela rede de Feistel
python3 ctr.py "uma mensagem de qualquer tamanho"   # as duas cifras em modo CTR
python3 ctr.py --nonce 0x0011223344 "uma mensagem"  # repete uma cifragem, uma mensagem só
```

`spn.py` e `feistel.py` cifram um bloco por argumento: a mensagem precisa
caber nos 10 bytes do bloco e é completada com zeros. Mensagem maior é
recusada, e é para isso que serve o `ctr.py`, que aceita qualquer tamanho.
Sem argumentos, cada script usa uma mensagem de exemplo.

Os três verificam o seu projeto antes de qualquer coisa e listam o que ainda
está fora das regras, então um `my_cipher.py` incompleto produz uma lista de
problemas, não um traceback.

## As cifras

O bloco tem 80 bits nas duas, com uma S-box de 4 bits. Os bits são numerados
de 0 a 79, sendo o bit 0 o menos significativo, e uma tabela de permutação é
lida como `PBOX[origem] = destino`.

**SPN**, 4 rodadas: três de `XOR chave de rodada -> camada de S-box -> P-box`,
e uma última de `XOR -> S-box -> XOR`. A permutação final é dispensada porque
não acrescenta nada antes do último XOR. São 20 S-boxes por rodada e 5 chaves
de rodada de 80 bits.

A SPN **não é garantidamente inversível**: como a sua função não linear não
precisa ser bijetora, dois blocos diferentes podem ir para o mesmo criptograma,
e por isso não existe `decrypt_block`. Mensagens são cifradas em modo CTR. A
Feistel continua inversível, porque `F` nunca precisa ser invertida.

**Feistel**: o bloco é partido em uma metade esquerda e uma direita, de 40 bits
cada. A rodada `i` leva `(left, right)` em `(right, left ^ F(left, subkey[i]))`, e a
troca da última rodada é desfeita na saída, então decifrar é o mesmo laço com
as subchaves na ordem inversa. A função de rodada é

```
F(x, k) = FEISTEL_PBOX( sbox_layer( x ^ k ) )
```

a sua S-box sobre 10 nibbles, depois a sua permutação de 40 bits. `F` nunca
precisa ser invertida, e por isso uma rede de Feistel aceita funções de rodada
que uma SPN não aceitaria. Cada rodada mexe em metade do bloco, e é por isso
que a Feistel roda o dobro de rodadas da SPN.

**Expansão de chave**: localizado em `cipher_base.py`.

```
chave de rodada i da SPN = rotl80(MASTER_KEY, i) ^ i                 para i em 0..4
subchave i da Feistel    = MSB40(w) ^ LSB40(w) ^ i                   para i em 0..7,
                           com w = rotl80(MASTER_KEY, i)
```

**Modo CTR**: o bloco de contador é um nonce de 40 bits acima de um contador
de 40 bits. A cifragem dele é o keystream, que entra na mensagem por XOR e é
truncado no último bloco. Sem preenchimento, qualquer tamanho, e cifrar e
decifrar são a mesma chamada. Cada mensagem recebe um nonce novo, sorteado com
`secrets` e impresso junto do criptograma. Ele não é segredo, mas não pode se
repetir com a mesma chave: duas mensagens sob o mesmo nonce compartilham o
keystream, e o XOR dos dois criptogramas revela o XOR das duas mensagens. Salve
o nonce de cada mensagem, é ele que permite repetir a cifragem depois, com
`--nonce`, que vale para uma mensagem por vez.
