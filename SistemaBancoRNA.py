import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import os
import sys
import re

# Variáveis das Opções.
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

# Variáveis Globais Necessárias.
deletaCliente = ""
debitaCliente = ""
depositaCliente = ""
data_atual = datetime.today()
data_em_texto = "{}/{}/{} {}:{}".format(data_atual.day,
                                        data_atual.month,
                                        data_atual.year,
                                        data_atual.hour,
                                        data_atual.minute)

# Lista para usar de base para verificar se o usuário digitou uma opção válida em tipo de conta.
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
    nome = entry_nome.get()
    cpf = entry_cpf.get()
    email = entry_email.get()
    senha = entry_senha.get()
    tconta = entry_tconta.get()
    valInicial = entry_valInicial.get()

    if not validar_cpf(cpf):
        messagebox.showerror("Erro", "CPF inválido. Digite no formato xxx.xxx.xxx-xx.")
        return

    if not validar_email(email):
        messagebox.showerror("Erro", "E-mail inválido. Digite no formato nome@dominio.xxx.xx.")
        return

    if not validar_senha(senha):
        messagebox.showerror("Erro", "Senha inválida. Digite 6 dígitos numéricos.")
        return

    if tconta not in tipoContas:
        messagebox.showerror("Erro", f'Não existe a opção {tconta}')
        return
    
    if not valInicial.isdigit():
        messagebox.showerror("Erro", "Valor inicial inválido. Digite um número.")
        return
    
    with open("cliente.txt", "r") as arq:
        checar = arq.readlines()
    
    if any(linha.split()[1] == cpf for linha in checar):
        messagebox.showerror("Erro", "CPF já cadastrado.")
        return
    
    if any(linha.split()[2] == email for linha in checar):
        messagebox.showerror("Erro", "E-mail já cadastrado.")
        return

    with open("cliente.txt", "a") as arq:
        arq.write(f"\n{nome} {cpf} {email} {tconta} {valInicial} {senha}")

    messagebox.showinfo("Sucesso", "Cliente Cadastrado com sucesso!")
    tela_cadastro.destroy()
    abrir_tela_inicial()  # Volta para a tela inicial após o cadastro

# Função para verificar o saldo.
def saldoC():
    cpf = usuario_cpf
    senha = usuario_senha

    with open("cliente.txt", "r") as arq:
        checar = arq.readlines()

    for linha in checar:
        linhaS = linha.split()
        if linhaS[1] == cpf and linhaS[5] == senha:
            messagebox.showinfo("Saldo", f"Seu Saldo é de: {linhaS[4]}")
            return

    messagebox.showerror("Erro", "CPF ou senha incorretos.")

# Função para verificar o extrato.
def extratoC():
    cpf = usuario_cpf
    senha = usuario_senha

    with open("cliente.txt", "r") as arq:
        checar = arq.readlines()

    for linha in checar:
        extratoCliente = linha.split()
        if extratoCliente[1] == cpf and extratoCliente[5] == senha:
            try:
                with open(f"extrato{extratoCliente[0]}.txt", "r") as extrato1:
                    extratoArq = extrato1.readlines()

                extrato_text = "\n".join(extratoArq)
                messagebox.showinfo("Extrato", f"Nome: {extratoCliente[0]}\nCPF: {extratoCliente[1]}\nConta: {extratoCliente[3]}\n\n{extrato_text}")
                return
            except:
                messagebox.showinfo("Extrato", "Você ainda não realizou nenhum débito ou depósito.")
                return

    messagebox.showerror("Erro", "CPF ou senha incorretos.")

# Função que faz o efeito de carregamento do programa.
def carregamento():
    messagebox.showinfo("Carregamento", "Carregando...")

# Função para realizar transferências.
def transferirC():
    cpf_origem = usuario_cpf
    senha = usuario_senha
    cpf_destino = entry_cpf_destino.get()
    valor = float(entry_valor_transferencia.get())
    observacao = entry_observacao.get()

    with open("cliente.txt", "r") as arq:
        checar = arq.readlines()

    clienteOrigem = None
    clienteDestino = None

    for linha in checar:
        linhaS = linha.split()
        if linhaS[1] == cpf_origem and linhaS[5] == senha:
            clienteOrigem = linhaS
        if linhaS[1] == cpf_destino:
            clienteDestino = linhaS

    if not clienteOrigem:
        messagebox.showerror("Erro", "CPF ou senha inválidos.")
        return

    if not clienteDestino:
        messagebox.showerror("Erro", "CPF do destinatário inválido.")
        return

    clienteOrigem[4] = float(clienteOrigem[4])
    clienteDestino[4] = float(clienteDestino[4])

    if clienteOrigem[4] < valor:
        messagebox.showerror("Erro", "Saldo insuficiente para realizar a transferência.")
        return

    clienteOrigem[4] -= valor
    clienteDestino[4] += valor

    with open("cliente.txt", "w") as arq:
        for linha in checar:
            linhaS = linha.split()
            if linhaS[1] == clienteOrigem[1]:
                arq.write(" ".join(map(str, clienteOrigem)) + "\n")
            elif linhaS[1] == clienteDestino[1]:
                arq.write(" ".join(map(str, clienteDestino)) + "\n")
            else:
                arq.write(linha)

    with open(f"extrato{clienteOrigem[0]}.txt", "a") as extratoOrigem:
        extratoOrigem.write(f"Data: {data_em_texto} Transferência para {clienteDestino[0]}: -{valor} Observação: {observacao} Saldo: {clienteOrigem[4]}\n")

    with open(f"extrato{clienteDestino[0]}.txt", "a") as extratoDestino:
        extratoDestino.write(f"Data: {data_em_texto} Transferência de {clienteOrigem[0]}: +{valor} Observação: {observacao} Saldo: {clienteDestino[4]}\n")

    messagebox.showinfo("Sucesso", "Transferência Concluída com sucesso!")
    tela_transferencia.destroy()

# Função para simulação de investimento.
def simularInvestimento():
    valor = float(entry_valor_investimento.get())
    data_final = entry_data_final.get()

    try:
        data_final = datetime.strptime(data_final, "%m/%Y")
    except ValueError:
        messagebox.showerror("Erro", "Formato de data inválido. Use mm/aaaa.")
        return

    data_atual = datetime.today()
    meses = (data_final.year - data_atual.year) * 12 + data_final.month - data_atual.month

    if meses <= 0:
        messagebox.showerror("Erro", "A data final deve ser posterior à data atual.")
        return

    taxa_mensal = 0.005  # Exemplo de taxa mensal de 0.5%
    valor_final = valor * (1 + taxa_mensal) ** meses

    messagebox.showinfo("Investimento", f"Valor final do investimento após {meses} meses: R${valor_final:.2f}")
    tela_investimento.destroy()

# Função para trocar o tipo de conta.
def trocarTipoConta():
    cpf = usuario_cpf
    senha = usuario_senha
    novoTipo = entry_novo_tipo.get()

    if novoTipo not in tipoContas:
        messagebox.showerror("Erro", f'Não existe a opção {novoTipo}')
        return

    with open("cliente.txt", "r") as arq:
        checar = arq.readlines()

    with open("cliente.txt", "w") as arq:
        for linha in checar:
            linhaS = linha.split()
            if linhaS[1] == cpf and linhaS[5] == senha:
                linhaS[3] = novoTipo
                arq.write(" ".join(linhaS) + "\n")
            else:
                arq.write(linha)

    messagebox.showinfo("Sucesso", "Tipo de conta alterado com sucesso!")
    tela_troca_tipo.destroy()

# Função para abrir a tela de cadastro.
def abrir_tela_cadastro():
    global tela_cadastro, entry_nome, entry_cpf, entry_email, entry_senha, entry_tconta, entry_valInicial
    tela_cadastro = tk.Toplevel(tela_inicial)
    tela_cadastro.title("Cadastrar Novo Cliente")
    tela_cadastro.geometry("400x300")

    largura = 400
    altura = 300
    largura_tela = tela_cadastro.winfo_screenwidth()
    altura_tela = tela_cadastro.winfo_screenheight()
    pos_x = (largura_tela // 2) - (largura // 2)
    pos_y = (altura_tela // 2) - (altura // 2)
    tela_cadastro.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")

    frame_central = tk.Frame(tela_cadastro, bg="lightgray")
    frame_central.pack(expand=True)

    tk.Label(frame_central, text="Nome:", font=("Arial", 12)).grid(row=0, column=0, pady=5)
    entry_nome = tk.Entry(frame_central, font=("Arial", 12))
    entry_nome.grid(row=0, column=1, pady=5)

    tk.Label(frame_central, text="CPF:", font=("Arial", 12)).grid(row=1, column=0, pady=5)
    entry_cpf = tk.Entry(frame_central, font=("Arial", 12))
    entry_cpf.grid(row=1, column=1, pady=5)

    tk.Label(frame_central, text="E-mail:", font=("Arial", 12)).grid(row=2, column=0, pady=5)
    entry_email = tk.Entry(frame_central, font=("Arial", 12))
    entry_email.grid(row=2, column=1, pady=5)

    tk.Label(frame_central, text="Senha:", font=("Arial", 12)).grid(row=3, column=0, pady=5)
    entry_senha = tk.Entry(frame_central, show="*", font=("Arial", 12))
    entry_senha.grid(row=3, column=1, pady=5)

    tk.Label(frame_central, text="Tipo de Conta:", font=("Arial", 12)).grid(row=4, column=0, pady=5)
    entry_tconta = tk.Entry(frame_central, font=("Arial", 12))
    entry_tconta.grid(row=4, column=1, pady=5)

    tk.Label(frame_central, text="Valor Inicial:", font=("Arial", 12)).grid(row=5, column=0, pady=5)
    entry_valInicial = tk.Entry(frame_central, font=("Arial", 12))
    entry_valInicial.grid(row=5, column=1, pady=5)

    tk.Button(frame_central, text="Cadastrar", command=nCliente, font=("Arial", 12), bg="lightblue", fg="black").grid(row=6, column=0, columnspan=2, pady=10)

# Função para abrir a tela de login.
def abrir_tela_login():
    global tela_login, entry_cpf_login, entry_senha_login
    tela_login = tk.Toplevel(tela_inicial)
    tela_login.title("Login")
    tela_login.geometry("300x200")

    largura = 300
    altura = 200
    largura_tela = tela_login.winfo_screenwidth()
    altura_tela = tela_login.winfo_screenheight()
    pos_x = (largura_tela // 2) - (largura // 2)
    pos_y = (altura_tela // 2) - (altura // 2)
    tela_login.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")

    frame_central = tk.Frame(tela_login, bg="lightgray")
    frame_central.pack(expand=True)

    tk.Label(frame_central, text="CPF:", font=("Arial", 12)).grid(row=0, column=0, pady=5)
    entry_cpf_login = tk.Entry(frame_central, font=("Arial", 12))
    entry_cpf_login.grid(row=0, column=1, pady=5)

    tk.Label(frame_central, text="Senha:", font=("Arial", 12)).grid(row=1, column=0, pady=5)
    entry_senha_login = tk.Entry(frame_central, show="*", font=("Arial", 12))
    entry_senha_login.grid(row=1, column=1, pady=5)

    tk.Button(frame_central, text="Login", command=validar_login, font=("Arial", 12), bg="lightblue", fg="black").grid(row=2, column=0, columnspan=2, pady=10)

# Função para validar o login e abrir a tela principal.
def validar_login():
    global usuario_cpf, usuario_senha, usuario_nome, usuario_tipo_conta
    cpf = entry_cpf_login.get()
    senha = entry_senha_login.get()

    with open("cliente.txt", "r") as arq:
        checar = arq.readlines()

    for linha in checar:
        linhaS = linha.split()
        if linhaS[1] == cpf and linhaS[5] == senha:
            usuario_cpf = cpf
            usuario_senha = senha
            usuario_nome = linhaS[0]
            usuario_tipo_conta = linhaS[3]
            abrir_tela_principal()
            return

    messagebox.showerror("Erro", "CPF ou senha incorretos.")

# Função para abrir a tela principal após o login.
def abrir_tela_principal():
    global tela_principal
    tela_principal = tk.Toplevel(tela_inicial)
    tela_principal.title("Banco RNA")
    tela_principal.geometry("600x400")

    largura = 600
    altura = 400
    largura_tela = tela_principal.winfo_screenwidth()
    altura_tela = tela_principal.winfo_screenheight()
    pos_x = (largura_tela // 2) - (largura // 2)
    pos_y = (altura_tela // 2) - (altura // 2)
    tela_principal.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")

    frame_central = tk.Frame(tela_principal, bg="lightgray")
    frame_central.pack(expand=True)

    tk.Label(frame_central, text=f"Bem-vindo, {usuario_nome} (CPF: {usuario_cpf}) Conta: {usuario_tipo_conta}", font=("Arial", 14), fg="blue", bg="lightgray").pack(pady=10)

    tk.Button(frame_central, text="Ver Saldo", command=saldoC, font=("Arial", 12), bg="lightblue", fg="black").pack(pady=5)
    tk.Button(frame_central, text="Ver Extrato", command=extratoC, font=("Arial", 12), bg="lightblue", fg="black").pack(pady=5)
    tk.Button(frame_central, text="Transferir", command=abrir_tela_transferencia, font=("Arial", 12), bg="lightblue", fg="black").pack(pady=5)
    tk.Button(frame_central, text="Simular Investimento", command=abrir_tela_investimento, font=("Arial", 12), bg="lightblue", fg="black").pack(pady=5)
    tk.Button(frame_central, text="Trocar Tipo de Conta", command=abrir_tela_troca_tipo, font=("Arial", 12), bg="lightblue", fg="black").pack(pady=5)

    tela_login.destroy()

# Função para abrir a tela de transferência.
def abrir_tela_transferencia():
    global tela_transferencia, entry_cpf_destino, entry_valor_transferencia, entry_observacao
    tela_transferencia = tk.Toplevel(tela_principal)
    tela_transferencia.title("Transferir")
    tela_transferencia.geometry("400x300")

    largura = 400
    altura = 300
    largura_tela = tela_transferencia.winfo_screenwidth()
    altura_tela = tela_transferencia.winfo_screenheight()
    pos_x = (largura_tela // 2) - (largura // 2)
    pos_y = (altura_tela // 2) - (altura // 2)
    tela_transferencia.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")

    frame_central = tk.Frame(tela_transferencia, bg="lightgray")
    frame_central.pack(expand=True)

    tk.Label(frame_central, text="CPF do Destinatário:", font=("Arial", 12)).grid(row=0, column=0, pady=5)
    entry_cpf_destino = tk.Entry(frame_central, font=("Arial", 12))
    entry_cpf_destino.grid(row=0, column=1, pady=5)

    tk.Label(frame_central, text="Valor:", font=("Arial", 12)).grid(row=1, column=0, pady=5)
    entry_valor_transferencia = tk.Entry(frame_central, font=("Arial", 12))
    entry_valor_transferencia.grid(row=1, column=1, pady=5)

    tk.Label(frame_central, text="Observação:", font=("Arial", 12)).grid(row=2, column=0, pady=5)
    entry_observacao = tk.Entry(frame_central, font=("Arial", 12))
    entry_observacao.grid(row=2, column=1, pady=5)

    tk.Button(frame_central, text="Transferir", command=transferirC, font=("Arial", 12), bg="lightblue", fg="black").grid(row=3, column=0, columnspan=2, pady=10)

# Função para abrir a tela de investimento.
def abrir_tela_investimento():
    global tela_investimento, entry_valor_investimento, entry_data_final
    tela_investimento = tk.Toplevel(tela_principal)
    tela_investimento.title("Simular Investimento")
    tela_investimento.geometry("400x250")

    largura = 400
    altura = 250
    largura_tela = tela_investimento.winfo_screenwidth()
    altura_tela = tela_investimento.winfo_screenheight()
    pos_x = (largura_tela // 2) - (largura // 2)
    pos_y = (altura_tela // 2) - (altura // 2)
    tela_investimento.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")

    frame_central = tk.Frame(tela_investimento, bg="lightgray")
    frame_central.pack(expand=True)

    tk.Label(frame_central, text="Valor a Investir:", font=("Arial", 12)).grid(row=0, column=0, pady=5)
    entry_valor_investimento = tk.Entry(frame_central, font=("Arial", 12))
    entry_valor_investimento.grid(row=0, column=1, pady=5)

    tk.Label(frame_central, text="Data Final (mm/aaaa):", font=("Arial", 12)).grid(row=1, column=0, pady=5)
    entry_data_final = tk.Entry(frame_central, font=("Arial", 12))
    entry_data_final.grid(row=1, column=1, pady=5)

    tk.Button(frame_central, text="Simular", command=simularInvestimento, font=("Arial", 12), bg="lightblue", fg="black").grid(row=2, column=0, columnspan=2, pady=10)

# Função para abrir a tela de troca de tipo de conta.
def abrir_tela_troca_tipo():
    global tela_troca_tipo, entry_novo_tipo
    tela_troca_tipo = tk.Toplevel(tela_principal)
    tela_troca_tipo.title("Trocar Tipo de Conta")
    tela_troca_tipo.geometry("400x200")

    largura = 400
    altura = 200
    largura_tela = tela_troca_tipo.winfo_screenwidth()
    altura_tela = tela_troca_tipo.winfo_screenheight()
    pos_x = (largura_tela // 2) - (largura // 2)
    pos_y = (altura_tela // 2) - (altura // 2)
    tela_troca_tipo.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")

    frame_central = tk.Frame(tela_troca_tipo, bg="lightgray")
    frame_central.pack(expand=True)

    tk.Label(frame_central, text="Novo Tipo de Conta:", font=("Arial", 12)).grid(row=0, column=0, pady=5)
    entry_novo_tipo = tk.Entry(frame_central, font=("Arial", 12))
    entry_novo_tipo.grid(row=0, column=1, pady=5)

    tk.Button(frame_central, text="Trocar", command=trocarTipoConta, font=("Arial", 12), bg="lightblue", fg="black").grid(row=1, column=0, columnspan=2, pady=10)

# Função para abrir a tela inicial.
def abrir_tela_inicial():
    global tela_inicial
    tela_inicial = tk.Tk()
    tela_inicial.title("Banco RNA")
    tela_inicial.geometry("500x400")

    largura = 500
    altura = 400
    largura_tela = tela_inicial.winfo_screenwidth()
    altura_tela = tela_inicial.winfo_screenheight()
    pos_x = (largura_tela // 2) - (largura // 2)
    pos_y = (altura_tela // 2) - (altura // 2)
    tela_inicial.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")

    # Configurar o fundo da janela principal
    tela_inicial.configure(bg="lightgray")

    # Remover frame_central e adicionar os widgets diretamente na tela_inicial
    tk.Label(tela_inicial, text="Bem-vindo ao Banco RNA", font=("Arial", 16, "bold"), fg="blue", bg="lightgray").pack(pady=20)

    tk.Button(tela_inicial, text="Cadastrar", command=abrir_tela_cadastro, font=("Arial", 12, "bold"), bg="lightblue", fg="black", width=17, height=2).pack(pady=10)
    tk.Button(tela_inicial, text="Deletar Minha Conta", command=abrir_tela_deletar_conta, font=("Arial", 12, "bold"), bg="red", fg="black", width=17, height=2).pack(pady=10)
    tk.Button(tela_inicial, text="Logar", command=abrir_tela_login, font=("Arial", 12, "bold"), bg="lightgreen", fg="black", width=17, height=2).pack(pady=10)

    tela_inicial.mainloop()

# Função para abrir a tela de deletar conta.
def abrir_tela_deletar_conta():
    global tela_deletar_conta, entry_cpf_deletar, entry_senha_deletar
    tela_deletar_conta = tk.Toplevel(tela_inicial)
    tela_deletar_conta.title("Deletar Conta")
    tela_deletar_conta.geometry("300x200")

    largura = 300
    altura = 200
    largura_tela = tela_deletar_conta.winfo_screenwidth()
    altura_tela = tela_deletar_conta.winfo_screenheight()
    pos_x = (largura_tela // 2) - (largura // 2)
    pos_y = (altura_tela // 2) - (altura // 2)
    tela_deletar_conta.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")

    frame_central = tk.Frame(tela_deletar_conta, bg="lightgray")
    frame_central.pack(expand=True)

    tk.Label(frame_central, text="CPF:", font=("Arial", 12)).grid(row=0, column=0, pady=5)
    entry_cpf_deletar = tk.Entry(frame_central, font=("Arial", 12))
    entry_cpf_deletar.grid(row=0, column=1, pady=5)

    tk.Label(frame_central, text="Senha:", font=("Arial", 12)).grid(row=1, column=0, pady=5)
    entry_senha_deletar = tk.Entry(frame_central, show="*", font=("Arial", 12))
    entry_senha_deletar.grid(row=1, column=1, pady=5)

    tk.Button(frame_central, text="Deletar Conta", command=deletar_conta, font=("Arial", 12), bg="lightblue", fg="black").grid(row=2, column=0, columnspan=2, pady=10)

# Função para deletar a conta do usuário.
def deletar_conta():
    cpf = entry_cpf_deletar.get()
    senha = entry_senha_deletar.get()

    with open("cliente.txt", "r") as arq:
        checar = arq.readlines()

    with open("cliente.txt", "w") as arq:
        for linha in checar:
            linhaS = linha.split()
            if linhaS[1] != cpf or linhaS[5] != senha:
                arq.write(linha)

    messagebox.showinfo("Sucesso", "Conta deletada com sucesso!")
    tela_deletar_conta.destroy()

# Iniciar a aplicação.
abrir_tela_inicial()