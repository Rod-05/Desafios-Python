print("RHIAN OLIVEIRA DANTAS")
print("ARTUR PEREIRA DOS SANTOS")
print("GABRIELA BERTUZZI VILIMAS")

import csv

def carregar_produtos(arquivo):
    prod = {}
    with open(arquivo, 'r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=';')
        for linha in reader:
            codigo = int(linha[0])
            prod[codigo] = {'QtCO': int(linha[1]), 'QtMin': int(linha[2])}
    return prod

def carregar_vendas(arquivo):
    vendas = []
    with open(arquivo, 'r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=';')
        for linha in reader:
            vendas.append({
                'Codigo': int(linha[0]),
                'Quantidade': int(linha[1]),
                'Situacao': int(linha[2]),
                'Canal': int(linha[3])
            })
    return vendas

def salvar_transferencias(transferencias, arquivo):
    with open(arquivo, 'w', encoding='utf-8') as file:
        file.write(f"{'Produto':<10} {'QtCO':<10} {'QtMin':<10} {'QtVendas':<12} {'Estq. após Vendas':<20} {'Necess.':<10} {'Transf. de Arm p/ CO':<20}\n")
        for t in transferencias:
            file.write(f"{t['Produto']:<10} {t['QtCO']:<10} {t['QtMin']:<10} {t['QtVendas']:<12} {t['Estq. após Vendas']:<20} {t['Necess.']:<10} {t['Transf. de Arm p/ CO']:<20}\n")


def salvar_divergencias(divergencias, arquivo):
    with open(arquivo, 'w', encoding='utf-8') as file:
        for d in divergencias:
            file.write(d + "\n")

def salvar_totais_canais(canais_total, arquivo):
    with open(arquivo, 'w', encoding='utf-8') as file:
        file.write(f"{'Canal':<25} {'QtVendas':<10}\n") 
        canais = {
            1: "Representantes",
            2: "Website",
            3: "App móvel android",
            4: "App móvel iphone"
        }
        for canal, total in canais_total.items():
            if canal in canais:
                file.write(f"{canais[canal]:<25} {total:<10}\n")

def calcular_transferencias(produtos, vendas):
    transferencias = []
    divergencias = []
    totais_por_canal = {1: 0, 2: 0, 3: 0, 4: 0}

    for i, venda in enumerate(vendas):
        codigo = venda['Codigo']
        if codigo not in produtos:
            divergencias.append(f"Linha {i + 1} – Código de Produto não encontrado {codigo}")
            continue

        produto = produtos[codigo]
        situacao = venda['Situacao']
        
        if situacao == 135:
            divergencias.append(f"Linha {i + 1} – Venda cancelada")
        elif situacao == 190:
            divergencias.append(f"Linha {i + 1} – Venda não finalizada")
        elif situacao == 999:
            divergencias.append(f"Linha {i + 1} – Erro desconhecido. Acionar equipe de TI.")
        else:
            if situacao in [100, 102]:
                totais_por_canal[venda['Canal']] += venda['Quantidade']

            estoque_pos_venda = produto['QtCO'] - venda['Quantidade']
            necessario = produto['QtMin'] - estoque_pos_venda
            transf_arm_para_CO = max(0, necessario) if necessario >= 10 else 0

            transferencias.append({
                'Produto': codigo,
                'QtCO': produto['QtCO'],
                'QtMin': produto['QtMin'],
                'QtVendas': venda['Quantidade'],
                'Estq. após Vendas': estoque_pos_venda,
                'Necess.': necessario,
                'Transf. de Arm p/ CO': transf_arm_para_CO
            })

    return transferencias, divergencias, totais_por_canal

produtos = carregar_produtos('c1_produtos.txt')
vendas = carregar_vendas('c1_vendas.txt')
transferencias, divergencias, totais_canais = calcular_transferencias(produtos, vendas)
salvar_transferencias(transferencias, 'TRANSFERE.TXT')
salvar_divergencias(divergencias, 'DIVERGENCIAS.TXT')
salvar_totais_canais(totais_canais, 'TOTCANAL.TXT')
