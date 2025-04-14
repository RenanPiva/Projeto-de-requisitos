# Projeto-de-requisitos
Projeto para a disciplina SIMULAÇÃO E TESTE DE SOFTWARE


# ✅ Requisitos Funcionais
ID	Descrição	Prioridade	Status	Dependências	Critério de Aceitação
R1	Permite cadastrar cliente	Alta	Em Aberto	Nenhuma	Cadastro realizado com sucesso e salvo em arquivo TXT
R2	Só permite alterar valores monetários após CPF e senha	Alta	Em Aberto	R1	Apenas usuários autenticados conseguem alterar valores
R3	Transferências devem ser registradas no histórico (txt)	Média	Em Aberto	R1	Cada transferência gera um registro no arquivo TXT
R4	Permite fazer simulações de investimento	Média	Em Aberto	Nenhuma	Sistema exibe o resultado da simulação corretamente
R5	Permite realizar débitos de valores na conta	Alta	Em Aberto	R1	Débito é processado, registrado e saldo atualizado
R6	Permite realizar transferências com um campo de observação	Baixa	Em Aberto	R1, R3	Observação é registrada e exibida no extrato
R7	Permite deletar a conta	Média	Em Aberto	R1	Conta é removida do sistema somente se o cliente estiver logado
R8	Permite a troca do tipo de conta para: plus, normal ou salário	Média	Em Aberto	R1	Usuário consegue escolher e alterar o tipo de conta desejada
