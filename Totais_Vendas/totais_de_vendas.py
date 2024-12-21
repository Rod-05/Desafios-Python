print("RHIAN OLIVEIRA DANTAS\n")
print("GABRIELA BERTUZZI VILIMAS\n")
print("ARTUT PEREIRA DOS SANTOS\n")

from operator import itemgetter

def totais_dias(arquivo_saida):
    with open('vendas.txt', 'r') as arquivo_vendas:
        arquivo_saida.write('TOTAIS DE VENDAS POR DIA\n')
        arquivo_saida.write('Dia             Total  Média/Dia\n')

        linha = arquivo_vendas.readline().rstrip()
        ano_atual, dias_validos = '', 0
        soma_dia, contagem = 0.0, 0

        while linha:
            linha = linha.split(';')
            if not ano_atual:
                ano_atual, mes_atual, dia_atual = linha[0], linha[1], linha[2]
                soma_dia, contagem = float(linha[5]), 1
            else:
                if linha[0] == ano_atual and linha[1] == mes_atual and linha[2] == dia_atual:
                    soma_dia += float(linha[5])
                    contagem += 1
                else:
                    dia_atual = dia_atual.zfill(2)
                    mes_atual = mes_atual.zfill(2)
                    media_dia = soma_dia / contagem
                    arquivo_saida.write(f'{dia_atual}/{mes_atual}/{ano_atual} {soma_dia:>10.2f} {media_dia:>10.2f}\n')
                    dias_validos += 1
                    ano_atual, mes_atual, dia_atual = linha[0], linha[1], linha[2]
                    soma_dia, contagem = float(linha[5]), 1
            linha = arquivo_vendas.readline().rstrip()
        if contagem > 0:
            dia_atual = dia_atual.zfill(2)
            mes_atual = mes_atual.zfill(2)
            media_dia = soma_dia / contagem
            arquivo_saida.write(f'{dia_atual}/{mes_atual}/{ano_atual} {soma_dia:>10.2f} {media_dia:>10.2f}\n')
            dias_validos += 1
        arquivo_saida.write('\n')
    return dias_validos

def totais_produtos(arquivo_saida, total_dias_validos):
    arquivo_saida.write('TOTAIS DE VENDAS POR PRODUTO\n')
    arquivo_saida.write('Produto   VlrTot     Qtde  Pç Médio  Lucrat.\n')

    cos_prod, categorias, custo_unit = [], [], []
    with open('produtos.txt', 'r') as arquivo_produtos:
        for linha_produto in arquivo_produtos:
            linha_produto = linha_produto.rstrip().split(';')
            cos_prod.append(int(linha_produto[0]))
            categorias.append(linha_produto[1])
            custo_unit.append(float(linha_produto[3]))

    soma_vendas, quantidades_totais, taxas_lucro = {}, {}, {}

    with open('vendas.txt', 'r') as arquivo_vendas:
        for linha_venda in arquivo_vendas:
            linha_venda = linha_venda.rstrip().split(';')
            codigo = int(linha_venda[3])
            qtde_vendas = float(linha_venda[4])
            preco_unitario = float(linha_venda[5])

            quantidades_totais[codigo] = quantidades_totais.get(codigo, 0) + qtde_vendas
            soma_vendas[codigo] = soma_vendas.get(codigo, 0) + preco_unitario * qtde_vendas

    soma_total_vendas, soma_total_quantidades, soma_lucros = 0, 0, 0
    participacao_produto = {}

    for i in range(len(cos_prod)):
        if cos_prod[i] in soma_vendas:
            preco_medio = soma_vendas[cos_prod[i]] / quantidades_totais[cos_prod[i]]
            valor_total = soma_vendas[cos_prod[i]]
            quantidade_str = f'{quantidades_totais[cos_prod[i]]:.2f}' if categorias[i] == 'P' else int(quantidades_totais[cos_prod[i]])
            lucro_produto = ((preco_medio / custo_unit[i]) - 1) * 100  # Alterado para evitar conflito com `taxas_lucro`

            soma_total_vendas += valor_total
            soma_total_quantidades += quantidades_totais[cos_prod[i]]
            taxas_lucro[cos_prod[i]] = lucro_produto
            soma_lucros += (lucro_produto / 100) * valor_total
            participacao_produto[cos_prod[i]] = valor_total

            arquivo_saida.write(f'{cos_prod[i]} {valor_total:>10.2f} {quantidade_str:>8} {preco_medio:>9.2f} {lucro_produto:>7.1f}%\n')

    arquivo_saida.write('\n')

    media_dia = soma_total_vendas / max(1, total_dias_validos)
    media_produto = soma_total_vendas / max(1, soma_total_quantidades)
    soma_total_vendas_str = f'{soma_total_vendas:.2f}'
    soma_total_quantidades_str = f'{soma_total_quantidades:.2f}'
    lucro_medio_percentual = f'{(soma_lucros / soma_total_quantidades) * 100:.1f}' if soma_total_quantidades else '0.0'

    arquivo_saida.write('TOTAL E ESTATÍSTICAS DO PERÍODO\n')
    arquivo_saida.write(f'Total Geral de Vendas (R$) {soma_total_vendas_str:>16}\n')
    arquivo_saida.write(f'Quantidade de produtos vendidos {soma_total_quantidades_str:>11}\n')
    arquivo_saida.write(f'Média de Vendas por dia útil (R$) {media_dia:>9.2f}\n')
    arquivo_saida.write(f'Média de Vendas por produto (R$) {media_produto:>10.2f}\n')
    arquivo_saida.write(f'Lucratividade Média {lucro_medio_percentual:>22}%\n\n')

    arquivo_saida.write('PRODUTOS MAIS LUCRATIVOS\n')
    arquivo_saida.write(f'Lucratividade Média = {lucro_medio_percentual}%\n\n')
    arquivo_saida.write('Produto   Lucrat.\n')
    for codigo, taxa in sorted(taxas_lucro.items(), key=itemgetter(1), reverse=True):
        arquivo_saida.write(f'{codigo} {taxa:>8.1f}%\n')
    arquivo_saida.write('\n')

    arquivo_saida.write('CONTRIBUIÇÃO DE CADA PRODUTO\n')
    arquivo_saida.write('Produto   VlrTot  Contrib.\n')
    for codigo, valor in sorted(participacao_produto.items(), key=lambda x: x[1], reverse=True):
        participacao = (valor / soma_total_vendas) * 100 if soma_total_vendas else 0
        arquivo_saida.write(f'{codigo} {valor:>10.2f} {participacao:>7.1f}%\n')

with open('totvendas.txt', 'w') as arquivo_saida:
    total_dias_validos = totais_dias(arquivo_saida)
    totais_produtos(arquivo_saida, total_dias_validos)
