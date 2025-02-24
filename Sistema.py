from tabulate import tabulate
from datetime import datetime

menu = '''

[d] Depositar 💰
[s] Sacar 💵
[e] Extrato 🧾
[u] Cadastro de Usuário 👥
[l] Listar Usuários 👥
[c] Criar Conta Corrente 🏧
[lc] Listar Conta Corrente 🏧
[q] Sair ❌

=> '''

##VARIAVEIS
data=datetime.now()
saldo=0
limite = 500
extrato = []
limite_saques=3
n_conta = 0
agencia = "0001"
usuarios = []
contas = []

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

def buscar_usuario(cpf, usuarios):
    for usuario in usuarios:
        if usuario["cpf"] == cpf:
            return True
    return False

    
def criar_usuario(usuarios):
    print("---Criação de usuário---")
    cpf=input("Informe o seu CPF: ")
   
    if buscar_usuario(cpf, usuarios):
        print("Usuário já cadastrado!")
        return
    
    nome = input("Informe o seu nome: ")
    data_nascimento =input("Informe a sua data de nascimento: ")
    endereco = input("Informe o seu endereço: ")
    
    usuario = {
        "cpf": cpf,
        "nome": nome,
        "data_nascimento": data_nascimento, 
        "endereco": endereco        
    }
    usuarios.append(usuario)
    print("Cadastro realizado com sucesso!")
 
def exibir_usuarios(usuarios):
    if usuarios== []:
        print("Não há usuários registrados!")
    else :    
        tabela = tabulate(usuarios, headers="keys", tablefmt="grid")
        print(tabela)
    
    return        


def criar_conta(contas, n_conta, agencia, usuarios):
    print("---Criação de Conta Corrente---")
    cpf=input("Informe o seu CPF: ")
   
    if buscar_usuario(cpf, usuarios):
        n_conta +=1
        conta = {
        "cpf": cpf,
        "agencia": agencia,
        "numero_conta": n_conta, 
          
            }
        contas.append(conta)
        print("Conta criada com sucesso!")
        print(f"Agência: {agencia}")
        print(f"Número: {n_conta}")
        return n_conta
    
    print("Usuário não cadastrado!")
    return None

def exibir_contas(contas):
    if contas== []:
        print("Não há contas registradas!")
    else :    
        tabela = tabulate(contas, headers="keys", tablefmt="grid")
        print(tabela)
    
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
        
    elif opcao == "u":
        criar_usuario(usuarios)
    
    elif opcao == "l":
        exibir_usuarios(usuarios)
        
    elif opcao == "c":
        n_conta = criar_conta(contas, n_conta, agencia, usuarios)
        
    elif opcao == "lc":
        exibir_contas(contas)
        
        
    elif opcao == "q":
        print("Sair")
        break
    else: 
        print("Operação inválida, por favor selecione novamente a operação desejada.")



