import json

entrada = "testes_estatisticos/avalanche_ctr_counter.json"
saida = "testes_estatisticos/avalanche_ctr_counter_formatado.json"

with open(entrada, encoding="utf-8") as arquivo:
    dados = json.load(arquivo)

with open(saida, "w", encoding="utf-8") as arquivo:
    arquivo.write("{\n")

    for i, (chave, listas) in enumerate(dados.items()):
        arquivo.write(f"  {json.dumps(chave)}: [\n")

        for j, lista in enumerate(listas):
            virgula = "," if j < len(listas) - 1 else ""
            arquivo.write(f"    {json.dumps(lista)}{virgula}\n")

        virgula = "," if i < len(dados) - 1 else ""
        arquivo.write(f"  ]{virgula}\n")

    arquivo.write("}\n")