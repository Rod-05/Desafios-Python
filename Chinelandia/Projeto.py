# Programa realizado por:
# RHIAN OLIVEIRA DANTAS
# GABRIELA BERTUZZI VILIMAS
# ARTUR PEREIRA DOS SANTOS

Dados = []
arqE = open('7_in.txt', 'r')
NPC = int(arqE.readline().strip())
for i in range(NPC):
    E, D = map(int, arqE.readline().strip().split())
    Dados.append((E, 'E'))
    Dados.append((D, 'D'))
arqE.close()
qtde_pares = {}
for modelo, pe in Dados:
    if (modelo, pe) not in qtde_pares:
        qtde_pares[(modelo, pe)] = 0
    qtde_pares[(modelo, pe)] += 1 
trocas_disponiveis = []
for chave in sorted(qtde_pares):
    if qtde_pares[chave] > 1:
        modelo, pe = chave
        trocas_disponiveis.append(f"{modelo} {pe} {qtde_pares[chave] - 1}")
arqS = open('7_out.txt', 'w')
if len(trocas_disponiveis) == 0:
    arqS.write("SEM TROCAS DESTA VEZ\n")
else:
    for linha in trocas_disponiveis:
        arqS.write(linha + "\n")
arqS.close()
print("Fim do Programa")
