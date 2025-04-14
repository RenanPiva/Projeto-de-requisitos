
# 🏦 Projeto Banco RNA - Requisitos

## 👥 Integrantes

- **Álvaro Coelho Jesus** - RA: 22.221.002-3  
- **Nicolas Costa Copolla de Moraes** - RA: 22.122.099-9  
- **Renan Guastella Piva** - RA: 22.221.002-3  

---

## 📌 Requisitos Funcionais

| ID  | Descrição                                                                                         | Prioridade | Status      | Dependências                   | Critério de Aceitação                                                                 |
|-----|---------------------------------------------------------------------------------------------------|------------|-------------|--------------------------------|----------------------------------------------------------------------------------------|
| R1  | Permite cadastrar cliente                                                                         | Alta       | Em Aberto   | Nenhuma                        | Cliente é cadastrado com sucesso e os dados armazenados em arquivo TXT               |
| R2  | Só permite alterar valores monetários após CPF e senha                                            | Alta       | Em Aberto   | R1                             | Apenas usuários autenticados conseguem alterar valores monetários                    |
| R3  | Transferências devem ser registradas no histórico (TXT)                                          | Média      | Em Aberto   | R1                             | Cada transferência gera um registro no arquivo TXT com informações da operação       |
| R4  | Permite fazer simulações de investimento                                                          | Média      | Em Aberto   | Nenhuma                        | Sistema exibe resultado da simulação para o período informado                        |
| R5  | Permite realizar débitos de valores na conta                                                      | Alta       | Em Aberto   | R1                             | Débito é processado e o saldo da conta é atualizado                                   |
| R6  | Permite realizar transferências com um campo de observação                                        | Baixa      | Em Aberto   | R1, R3                         | Campo de observação é registrado e exibido no extrato                                 |
| R7  | Permite deletar a conta                                                                           | Média      | Em Aberto   | R1                             | Conta é removida do sistema após solicitação do usuário logado                        |
| R8  | Permite a troca do tipo de conta para: plus, normal ou salário                                    | Média      | Em Aberto   | R1                             | Usuário pode escolher o tipo de conta desejada                                        |

---

## 🛡️ Requisitos Não Funcionais

| ID   | Descrição                                                                 | Prioridade | Status    | Dependências | Critério de Aceitação                                                         |
|------|---------------------------------------------------------------------------|------------|-----------|--------------|--------------------------------------------------------------------------------|
| RN1  | Performance: respostas rápidas mesmo usando TXT                           | Alta       | Em Aberto | Nenhuma      | Tempo de resposta das operações deve ser de até 2 segundos                    |
| RN2  | Segurança: apenas usuários autenticados podem executar operações sensíveis | Alta       | Em Aberto | Nenhuma      | Operações sensíveis só são acessíveis após autenticação correta              |

---

## 🖥️ Requisitos de Interface

| ID   | Descrição                                                    | Prioridade | Status    | Dependências | Critério de Aceitação                                                          |
|------|--------------------------------------------------------------|------------|-----------|--------------|---------------------------------------------------------------------------------|
| RI1  | Exibição de CPF e Tipo de Conta na interface do sistema      | Alta       | Em Aberto | R1           | CPF e tipo de conta são exibidos de forma clara e contínua na tela             |
