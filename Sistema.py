from tabulate import tabulate
from datetime import datetime
from abc import ABC, abstractclassmethod, abstractproperty

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []
        
    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)
    
    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, cpf, nome, data_nascimento, endereco):
        super().__init__(endereco)
        self.cpf = cpf, 
        self.nome = nome,
        self.data_nascimento = data_nascimento

class Conta:
    def __init__(self, numero, cliente):
        self.saldo = 0
        self.numero = numero
        self.agencia = "0001"
        self.cliente = cliente
        self.historico = Historico()
        
    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)
        
    @property    
    def saldo(self):
        return self._saldo
    
    @property    
    def numero(self):
        return self._numero
    
    @property    
    def agencia(self):
        return self._agencia
    
    @property    
    def cliente(self):
        return self._cliente
    
    @property    
    def historico(self):
        return self._historico
    
    
    def sacar(self, valor):    
        saldo = self.saldo
        execedeu_saldo = valor > saldo
        
        if execedeu_saldo:
            print("Saldo insuficiente para comcluir operação!")
        
        elif valor > 0:
            self._saldo -= valor
            print("Saque realizado com sucesso!")
            return True
        
        else:
            print("Operação falhou! Valor inválido.")
            
        return False
    
    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("Depósito realizado com sucesso!")
                    
        else:
            print("Operação falhou! Valor inválido.")
            return False
        
        return True

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes 
            if transacao["tipo"]== Saque.__name__]
            )
        
        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saques > self.limite_saques
        
        if excedeu_limite:
            print("Operação falhou! O valor excede o limite.")
            
        elif excedeu_saques: 
            print("Operação falhou! Número máximo de saques excedido.")
            
        else: 
            return super().sacar(valor)
        
        return False
    
    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """

class Historico:
    def __init__(self):
        self._transacoes = []
    
    @property
    def transacoes(self):
        return self._transacoes
    
    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%s"),
            }
        )

class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass
    
    @abstractclassmethod
    def registrar(self, conta):
        pass
    
class Saque(Transacao):
    def __init__(self, valor):
        self.valor = valor
        
    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)
        
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
   def __init__(self, valor):
        self.valor = valor
        
   @property
   def valor(self):
        return self._valor
    
   def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)
        
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

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



