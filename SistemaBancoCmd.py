import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import os
import sys
import re

# Variaveis das Opções.
novoCliente = 1
delCliente = 2
debita = 3
deposita = 4
saldo = 5
extrato = 6
transferir = 7
simular = 8
trocarTipo = 9
sair = 0

# Variaveis Globais Necessarias.
deletaCliente = ""
debitaCliente = ""
depositaCliente = ""
data_atual = datetime.today()
data_em_texto = "{}/{}/{} {}:{}".format(data_atual.day,
                                        data_atual.month,
                                        data_atual.year,
                                        data_atual.hour,
                                        data_atual.minute)

# Lista para usar de base para verificar se o usuario digitou uma opção valida em tipo de conta.
tipoContas = ['Comum', 'Salario', 'Plus', 'comum', 'salario', 'plus']

def validar_cpf(cpf):
    padrao = r'^\d{3}\.\d{3}\.\d{3}-\d{2}$'
    return re.match(padrao, cpf) is not None

def validar_email(email):
    padrao = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(padrao, email) is not None

def validar_senha(senha):
    return senha.isdigit() and len(senha) == 6

# Função que cadastra um novo cliente.
def nCliente():
    arq = open("cliente.txt", "a")

    nome = input("Digite o primeiro nome do novo cliente: ")
    cpf = input("Digite o CPF do novo cliente: ")
    while not validar_cpf(cpf):
        print("CPF inválido. Digite no formato xxx.xxx.xxx-xx.")
        cpf = input("Digite o CPF do novo cliente: ")

    email = input("Digite o e-mail do novo cliente: ")
    while not validar_email(email):
        print("E-mail inválido. Digite no formato nome@dominio.xxx.xx.")
        email = input("Digite o e-mail do novo cliente: ")

    senha = input("Digite a senha do usuario: ")
    while not validar_senha(senha):
        print("Senha inválida. Digite 6 dígitos numéricos.")
        senha = input("Digite a senha do usuario: ")

    tconta = input("Tipo de conta do cliente: \n (Salario) \n (Comum) \n (Plus) \n Digite: ")
    if tconta not in tipoContas:
        print(f'Não existe a opção {tconta}')
        return 'menu'
    valInicial = input("Digite o valor inicial da conta: ")

    carregamento()
    print("Cliente Cadastrado com sucesso!")

    arq.write("\n%s %s %s %s %s %s" % (nome, cpf, email, tconta, valInicial, senha))
    arq.close()

# Função que apaga um cliente junto com o seu arquivo do extrato.
def dCliente():
    dCpf = str(input("Digite o cpf da conta que deseja deletar: "))

    t = 0

    arq = open("cliente.txt", "r")
    checar = arq.readlines()
    arq.close()

    for linha in checar:
        linhaS = linha.split(" ")
        for line in linhaS:

            if line == dCpf:
                deletaCliente = linhaS
                if os.path.isfile("extrato" + deletaCliente[0] + ".txt"):
                    os.remove("extrato" + deletaCliente[0] + ".txt")
                arq = open("cliente.txt", "w")
                t += 1
                for linha in checar:
                    linhaS = linha.split(" ")
                    if linhaS != deletaCliente:
                        arq.write(linha)

                carregamento()
                print("\nCliente deletado com sucesso.")
                arq.close()
                break

    if t == 0:
        print("CPF não encontrado.")

# Função que Debita.
def debitarC():
    tentativas = 0
    while tentativas < 3:
        debCpf = input("Digite o seu CPF: ")
        debSenha = input("Digite sua senha: ")
        debValor = float(input("Digite o valor a ser debitado: "))

        arq = open("cliente.txt", "r")
        checar = arq.readlines()
        arq.close()

        for linha in checar:
            linhaS = linha.split(" ")
            debitaCliente = linha.split(" ")
            if linhaS[0] == '\n':
                continue
            if linhaS[1] == debCpf and linhaS[5] == debSenha:
                if linhaS[3] == "Salario" or linhaS[3] == "salario":
                    debitaCliente[4] = float(debitaCliente[4])
                    debitaCliente[4] = debitaCliente[4] - debValor * 1.05
                    tarifa = debValor * 0.05

                    if debitaCliente[4] < 0:
                        print("Debito não permitido.\n Seu saldo ficará abaixo de 0")
                        break

                elif linhaS[3] == "Comum" or linhaS[3] == "comum":
                    debitaCliente[4] = float(debitaCliente[4])
                    debitaCliente[4] = debitaCliente[4] - debValor * 1.03
                    tarifa = debValor * 0.03

                    if debitaCliente[4] < -500:
                        print("Debito não permitido.\n Seu saldo ficará abaixo de -500")
                        break

                elif linhaS[3] == "Plus" or linhaS[3] == 'plus':
                    debitaCliente[4] = float(debitaCliente[4])
                    debitaCliente[4] = debitaCliente[4] - debValor * 1.01
                    tarifa = debValor * 0.01

                    if debitaCliente[4] < -5000:
                        print("Debito não permitido.\n Seu saldo ficará abaixo de -5000")
                        break

                arq = open("cliente.txt", "w")

                i = 0

                for linha in checar:
                    linhaS = linha.split(" ")
                    if linhaS[0] == '\n':
                        continue
                    if linhaS[1] == debitaCliente[1]:
                        for dbt in debitaCliente:
                            dbt = str(dbt)

                            if i < 6:
                                i += 1
                                arq.write(dbt + " ")

                            else:
                                arq.write(dbt)

                            if i == 5:
                                extratoDeb = dbt
                                extratoDeb = float(extratoDeb)
                    else:
                        arq.write(linha)
                arq.close()
                extrato1 = open("extrato" + debitaCliente[0] + ".txt", "a")
                extrato1.write("Data: %s - %.2f Tarifa: %.2f Saldo: %.2f\n" % (data_em_texto, debValor, tarifa, extratoDeb))
                extrato1.close()

                carregamento()
                print("Debito Concluido com exito!")
                return
        tentativas += 1
        print("CPF ou senha inválidos. Tente novamente.")

    print("Número máximo de tentativas atingido. Saindo do sistema.")
    sys.exit()

# Função que Deposita.
def depositoC():
    tentativas = 0
    while tentativas < 3:
        depCpf = input("Digite o seu CPF: ")
        depValor = float(input("Digite o valor a ser depositado: "))

        arq = open("cliente.txt", "r")
        checar = arq.readlines()
        arq.close()

        for linha in checar:
            linhaS = linha.split(" ")
            depositaCliente = linha.split(" ")
            if linhaS[0] == '\n':
                continue
            if depCpf == linhaS[1]:
                depositaCliente[4] = float(depositaCliente[4])
                depositaCliente[4] = depositaCliente[4] + depValor

                arq = open("cliente.txt", "w")

                i = 0

                for linha in checar:
                    linhaS = linha.split(" ")
                    if linhaS[0] == '\n':
                        continue
                    if linhaS[1] == depositaCliente[1]:
                        for dbt in depositaCliente:
                            dbt = str(dbt)

                            if i < 6:
                                i += 1
                                arq.write(dbt + " ")

                            else:
                                arq.write(dbt)

                            if i == 5:
                                extratoDep = dbt
                                extratoDep = float(extratoDep)
                    else:
                        arq.write(linha)
                arq.close()

                extrato1 = open("extrato" + depositaCliente[0] + ".txt", "a")
                extrato1.write("Data: %s + %.2f Tarifa: 0.00 Saldo: %.2f\n" % (data_em_texto, depValor, extratoDep))
                extrato1.close()

                carregamento()
                print("Deposito Concluido com exito!")
                return
        tentativas += 1
        print("CPF inválido. Tente novamente.")

    print("Número máximo de tentativas atingido. Saindo do sistema.")
    sys.exit()

# Função para verificar o saldo.
def saldoC():
    tentativas = 0
    while tentativas < 3:
        salCpf = input("Digite o seu CPF: ")
        salSenha = input("Digite sua senha: ")

        arq = open("cliente.txt", "r")
        checar = arq.readlines()
        arq.close()

        for linha in checar:
            linhaS = linha.split(" ")
            if linhaS[0] == '\n':
                continue
            if linhaS[1] == salCpf and linhaS[5] == salSenha:
                print("\nSeu Saldo é de: " + linhaS[4])
                return

        tentativas += 1
        print("CPF ou senha incorretos. Tente novamente.")

    print("Número máximo de tentativas atingido. Saindo do sistema.")
    sys.exit()

# Função para verificar o extrato.
def extratoC():
    tentativas = 0
    while tentativas < 3:
        exCpf = input("Digite o seu CPF: ")
        exSenha = input("Digite sua senha: ")

        arq = open("cliente.txt", "r")
        checar = arq.readlines()
        arq.close()

        for linha in checar:
            extratoCliente = linha.split(" ")
            if linha[0] == '\n':
                continue
            if extratoCliente[1] == exCpf and extratoCliente[5] == exSenha:
                try:
                    extrato1 = open("extrato" + extratoCliente[0] + ".txt",
                                    "r")
                    extratoArq = extrato1.readlines()
                    extrato1.close()

                    print("\nNome: %s" % extratoCliente[0])
                    print("CPF: %s" % extratoCliente[1])
                    print("Conta: %s\n" % extratoCliente[3])
                    for linha in extratoArq:
                        print(linha, end=" ")

                    return
                except:
                    print("\nVocê ainda não realizou nenhum debito ou "
                          "deposito.")
                    return

        tentativas += 1
        print("CPF ou senha incorretos. Tente novamente.")

    print("Número máximo de tentativas atingido. Saindo do sistema.")
    sys.exit()

# Função que faz o efeito de carregamento do programa.
def carregamento():
    print(".")
    sleep(0.5)
    print("..")
    sleep(0.4)
    print("...")
    sleep(0.3)

# Função para realizar transferências.
def transferirC():
    tentativas = 0
    while tentativas < 3:
        transCpfOrigem = input("Digite o seu CPF: ")
        transSenha = input("Digite sua senha: ")

        arq = open("cliente.txt", "r")
        checar = arq.readlines()
        arq.close()

        clienteOrigem = None
        clienteDestino = None

        for linha in checar:
            linhaS = linha.split(" ")
            if linhaS[0] == '\n':
                continue
            if linhaS[1] == transCpfOrigem and linhaS[5] == transSenha:
                clienteOrigem = linhaS
                break

        if not clienteOrigem:
            tentativas += 1
            print("CPF ou senha inválidos. Tente novamente.")
            continue

        transCpfDestino = input("Digite o CPF do destinatário: ")
        transValor = float(input("Digite o valor a ser transferido: "))
        observacao = input("Digite uma observação para a transferência: ")

        for linha in checar:
            linhaS = linha.split(" ")
            if linhaS[0] == '\n':
                continue
            if linhaS[1] == transCpfDestino:
                clienteDestino = linhaS
                break

        if not clienteDestino:
            print("CPF do destinatário inválido.")
            return

        clienteOrigem[4] = float(clienteOrigem[4])
        clienteDestino[4] = float(clienteDestino[4])

        if clienteOrigem[4] < transValor:
            print("Saldo insuficiente para realizar a transferência.")
            return

        clienteOrigem[4] -= transValor
        clienteDestino[4] += transValor

        arq = open("cliente.txt", "w")

        for linha in checar:
            linhaS = linha.split(" ")
            if linhaS[0] == '\n':
                continue
            if linhaS[1] == clienteOrigem[1]:
                arq.write(" ".join(map(str, clienteOrigem)) + "\n")
            elif linhaS[1] == clienteDestino[1]:
                arq.write(" ".join(map(str, clienteDestino)) + "\n")
            else:
                arq.write(linha)

        arq.close()

        extratoOrigem = open("extrato" + clienteOrigem[0] + ".txt", "a")
        extratoOrigem.write("Data: %s Transferência para %s: -%.2f Observação: %s Saldo: %.2f\n" % (data_em_texto, clienteDestino[0], transValor, observacao, clienteOrigem[4]))
        extratoOrigem.close()

        extratoDestino = open("extrato" + clienteDestino[0] + ".txt", "a")
        extratoDestino.write("Data: %s Transferência de %s: +%.2f Observação: %s Saldo: %.2f\n" % (data_em_texto, clienteOrigem[0], transValor, observacao, clienteDestino[4]))
        extratoDestino.close()

        carregamento()
        print("Transferência Concluída com sucesso!")
        return

    print("Número máximo de tentativas atingido. Saindo do sistema.")
    sys.exit()

# Função para simulação de investimento.
def simularInvestimento():
    valor = float(input("Digite o valor a ser investido: "))
    data_final = input("Digite a data final do investimento (mm/aaaa): ")

    try:
        data_final = datetime.strptime(data_final, "%m/%Y")
    except ValueError:
        print("Formato de data inválido. Use mm/aaaa.")
        return

    data_atual = datetime.today()
    meses = (data_final.year - data_atual.year) * 12 + data_final.month - data_atual.month

    if meses <= 0:
        print("A data final deve ser posterior à data atual.")
        return

    taxa_mensal = 0.005  # Exemplo de taxa mensal de 0.5%
    valor_final = valor * (1 + taxa_mensal) ** meses

    print(f"Valor final do investimento após {meses} meses: R${valor_final:.2f}")

# Função para troca do tipo de conta.
def trocarTipoConta():
    tentativas = 0
    while tentativas < 3:
        cpf = input("Digite o seu CPF: ")
        senha = input("Digite sua senha: ")

        arq = open("cliente.txt", "r")
        checar = arq.readlines()
        arq.close()

        for linha in checar:
            linhaS = linha.split(" ")
            if linhaS[0] == '\n':
                continue
            if linhaS[1] == cpf and linhaS[5] == senha:
                novoTipo = input("Digite o novo tipo de conta (Salario, Comum, Plus): ")

                if novoTipo not in tipoContas:
                    print(f'Não existe a opção {novoTipo}')
                    return

                linhaS[3] = novoTipo
                arq = open("cliente.txt", "w")
                for linha in checar:
                    linhaS = linha.split(" ")
                    if linhaS[0] == '\n':
                        continue
                    if linhaS[1] == cpf:
                        arq.write(" ".join(linhaS) + "\n")
                    else:
                        arq.write(linha)
                arq.close()
                carregamento()
                print("Tipo de conta alterado com sucesso!")
                return

        tentativas += 1
        print("CPF ou senha incorretos. Tente novamente.")

    print("Número máximo de tentativas atingido. Saindo do sistema.")
    sys.exit()

# Função para exibir o menu principal
def exibir_menu_principal(cpf, tipo_conta):
    root = tk.Tk()
    root.title("Banco QuemPoupaTem")

    # Labels para exibir CPF e tipo de conta
    cpf_label = tk.Label(root, text=f"CPF: {cpf}", font=("Helvetica", 14))
    cpf_label.pack(pady=10)

    tipo_conta_label = tk.Label(root, text=f"Tipo de Conta: {tipo_conta}", font=("Helvetica", 14))
    tipo_conta_label.pack(pady=10)

    # Botões para as opções do menu
    botao_saldo = tk.Button(root, text="Ver Saldo", command=saldoC, font=("Helvetica", 12))
    botao_saldo.pack(pady=5)

    botao_extrato = tk.Button(root, text="Ver Extrato", command=extratoC, font=("Helvetica", 12))
    botao_extrato.pack(pady=5)

    botao_debitar = tk.Button(root, text="Debitar", command=debitarC, font=("Helvetica", 12))
    botao_debitar.pack(pady=5)

    botao_depositar = tk.Button(root, text="Depositar", command=depositoC, font=("Helvetica", 12))
    botao_depositar.pack(pady=5)

    botao_transferir = tk.Button(root, text="Transferir", command=transferirC, font=("Helvetica", 12))
    botao_transferir.pack(pady=5)

    botao_simular = tk.Button(root, text="Simular Investimento", command=simularInvestimento, font=("Helvetica", 12))
    botao_simular.pack(pady=5)

    botao_trocar_tipo = tk.Button(root, text="Trocar Tipo de Conta", command=trocarTipoConta, font=("Helvetica", 12))
    botao_trocar_tipo.pack(pady=5)

    botao_sair = tk.Button(root, text="Sair", command=root.quit, font=("Helvetica", 12))
    botao_sair.pack(pady=5)

    root.mainloop()

# Função para autenticar o usuário
def autenticar_usuario():
    tentativas = 0
    while tentativas < 3:
        cpf = input("Digite o seu CPF: ")
        senha = input("Digite sua senha: ")

        arq = open("cliente.txt", "r")
        checar = arq.readlines()
        arq.close()

        for linha in checar:
            linhaS = linha.split(" ")
            if linhaS[0] == '\n':
                continue
            if linhaS[1] == cpf and linhaS[5] == senha:
                exibir_menu_principal(cpf, linhaS[3])
                return

        tentativas += 1
        print("CPF ou senha incorretos. Tente novamente.")

    print("Número máximo de tentativas atingido. Saindo do sistema.")
    sys.exit()

# Função Menu que é responsavel por chamar todas as outras funções.
def MeinMenu():
    print("Bem Vindo ao Banco QuemPoupaTem!")
    autenticar_usuario()

MeinMenu()
