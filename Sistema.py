from tabulate import tabulate
from datetime import datetime

menu = '''

[d] Depositar 💰
[s] Sacar 💵
[e] Extrato 🧾
[q] Sair ❌

=> '''

##VARIAVEIS
data=datetime.now()
saldo=0
limite = 500
extrato =[]

limite_saques=3

def depositar(saldo, valor, data, extrato):
    if valor > 0:
        extrato.append({"tipo": "Depósito", "valor": valor, "data": data})
        saldo += valor
        print(f"Depósito no valor de R$ {valor} realizado com sucesso!")
    else:
        print("O valor informado é inválido para a operação.")

    return saldo, extrato

def saque(saldo, valor, data, extrato, limite, limite_saques):
    if limite_saques > 0 and valor <= limite and valor <= saldo  :
        extrato.append({"tipo": "Saque", "valor": valor, "data": data})
        saldo -= valor
        limite_saques -= 1
        print(f"Saque no valor de R$ {valor} realizado com sucesso!")
    elif valor > saldo:
        print("Saldo insuficiente para a operação.")
    elif valor > limite:
        print("Valor do saque excede o limite permitido por transação.")
    elif limite_saques == 0:
        print("Você atingiu o limite de saques diário.")

    
    return saldo, extrato, limite_saques

def exibir_extrato(saldo, extrato):
    if extrato== []:
        print("Não há movimentações registradas!")
    else :    
        tabela = tabulate(extrato, headers="keys", tablefmt="grid")
        print(tabela)

    print(f"Saldo disponível: R$ {saldo}")    
    return 


print("Bem-vindo ao sistema de gerenciamento de contas bancárias!")

while True:

    opcao = input(menu)

    if opcao =="d":
        valor=float(input("Informe o valor que deseja depositar:"))
        saldo, extrato = depositar(saldo, valor, data, extrato)

    elif opcao == "s":
        valor=float(input("Informe o valor que deseja sacar:"))
        saldo, extrato, limite_saques = saque(saldo, valor, data, extrato, limite, limite_saques)

    elif opcao == "e":
        
        exibir_extrato(saldo, extrato)
    elif opcao == "q":
        print("Sair")
        break
    else: 
        print("Operação inválida, por favor selecione novamente a operação desejada.")



