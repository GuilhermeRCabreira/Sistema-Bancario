import textwrap
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
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento

class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()
        
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
            print("Saldo insuficiente para concluir operação!")
        
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
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
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
        self._valor = valor
        
    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)
        
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
   def __init__(self, valor):
        self._valor = valor
        
   @property
   def valor(self):
        return self._valor
    
   def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)
        
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

def menu():
    menu = '''

    [d] Depositar 💰
    [s] Sacar 💵
    [e] Extrato 🧾
    [u] Cadastro de Usuário 👥
    [c] Criar Conta Corrente 🏧
    [lc] Listar Conta Corrente 🏧
    [q] Sair ❌

    => '''
    return input(textwrap.dedent(menu))

def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    
    return clientes_filtrados[0] if clientes_filtrados else None

def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("Cliente não possui conta!")
        return
    
    return cliente.contas[0]

def depositar(clientes):
    cpf = input("Informe o seu CPF: ")
    cliente= filtrar_cliente(cpf, clientes)
    
    if not cliente:
        print("Cliente não encontrado!")
        return
    valor = float(input("Informe o valor que deseja depositar: "))
    transacao = Deposito(valor)
    
    conta = recuperar_conta_cliente(cliente)
    if not conta: 
        return
    
    cliente. realizar_transacao(conta, transacao)
    
def sacar(clientes):
    cpf = input("Informe o seu CPF: ")
    cliente= filtrar_cliente(cpf, clientes)
    
    if not cliente:
        print("Cliente não encontrado!")
        return
    
    valor = float(input("Informe o valor que deseja sacar: "))
    transacao = Saque(valor)
    
    conta = recuperar_conta_cliente(cliente)
    if not conta: 
        return
    
    cliente.realizar_transacao(conta, transacao)
    
def exibir_extrato(clientes):
    cpf = input("Informe o seu CPF: ")
    cliente= filtrar_cliente(cpf, clientes)
    
    if not cliente:
        print("Cliente não encontrado!")
        return
       
    conta = recuperar_conta_cliente(cliente)
    if not conta: 
        return
    
    print("________Extrato________")
    transacoes = conta.historico.transacoes
    extrato = ""
    if not transacoes:
        extrato = "Não há movimentações registradas!"
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}:\n\tR${transacao['valor']:.2f}"
            
    print(extrato)
    print(f"_____Saldo:\n\tR$ {conta.saldo:.2f}")
     
def criar_cliente(clientes):
    cpf = input("Informe o seu CPF: ")
    cliente= filtrar_cliente(cpf, clientes)
    
    if cliente:
        print("Cliente já cadastrado!")
        return
    
    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento: ")
    endereco = input("Informe o endereço: ")
    
    cliente = PessoaFisica(nome= nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)
    clientes.append(cliente)
    
    print("Cliente criado com sucesso!")
    
def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe o seu CPF: ")
    cliente= filtrar_cliente(cpf, clientes)
    
    if not cliente:
        print("Cliente não encontrado!")
        return
    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)
    
    print("Conta criada com sucesso!")   
   
def exibir_contas(contas):
    for conta in contas:
        print("=" * 100)
        print(textwrap.dedent(str(conta)))
    
def main():
    clientes = []
    contas = []
    
    print("Bem-vindo ao sistema de gerenciamento de contas bancárias!")

    while True:

        opcao = menu()

        if opcao =="d":
            depositar(clientes)

        elif opcao == "s":
            sacar(clientes)
            
        elif opcao == "e":
            exibir_extrato(clientes)
        
        elif opcao == "u":
            criar_cliente(clientes)
                    
        elif opcao == "c":
            n_conta = len(contas) + 1
            criar_conta(n_conta, clientes, contas)
            
        
        elif opcao == "lc":
            exibir_contas(contas)
        
        
        elif opcao == "q":
            print("Sair")
            break
        
        else: 
            print("Operação inválida, por favor selecione novamente a operação desejada.")

main()

