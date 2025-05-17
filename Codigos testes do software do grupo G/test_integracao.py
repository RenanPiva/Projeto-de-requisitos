from app import *
import unittest


class caseTests(unittest.TestCase):
   
    def test_ti_01A(self):
        self.assertEqual(salvar_usuario('user1', 'user@user', '123'), None, 'Teste de cadastro conforme falhou')
        
    def test_ti_01B(self):
        self.assertNotEqual(salvar_usuario('', '', ''), None, 'Teste Cadastro Vazio falhou')
        
    def test_ti_01C(self):
        self.assertNotEqual(salvar_usuario('user4', 'user4', '123'), None, 'Teste Cadastro de email inválido falhou')
        
    def test_ti_01D(self):
        salvar_usuario('gemeos1', 'gemeos@gemini', '123')
        # salvar_usuario('gemeos1', 'gemeos@gemini', '123')
        self.assertNotEqual(salvar_usuario('gemeos1', 'gemeos@gemini', '123'), None, "Teste de itens duplicados falhou")

    # def test_ti_01E(self):
    #     """Teste Cadastro null"""
    #     self.assertNotEqual(salvar_usuario(), None, 'Teste Cadastro null')       
    
    def test_ti_02A(self):
        self.assertEqual(validar_login('user@user','123'), True, 'Teste de Login conforme falhou')
    
    def test_ti_02B(self):
        self.assertNotEqual(validar_login('naocadastrado@user','123'), True, 'Teste de Login sem cadastro falhou')
    
    def test_ti_02C(self):
        self.assertNotEqual(validar_login('user@user','321'), True, 'Teste de Login com senha errada falhou')

    def test_ti_02D(self):
        self.assertNotEqual(validar_login('',''), True, 'Teste de Login vazio falhou')


    def test_ti_03A(self):
        self.assertEqual(adicionar_linha('livros.txt', ['Nice title', 'Nice author', 'editora paia', '2025', 'horror', '001']), None, 'Teste de cadastro de livro conforme falhou')

    def test_ti_03B(self):
        self.assertNotEqual(adicionar_linha('livros.txt', ['', '', '', '', '', '']), None, 'Teste de cadastro de livro sem informações falhou')

    def test_ti_03C(self):
        self.assertNotEqual(adicionar_linha('livros.txt', ['Nice title', 'Nice author', 'editora paia', '2025', 'horror', '001']), None, 'Teste de cadastro de livro duplicado falhou')

    def test_ti_03D(self):
        self.assertNotEqual(adicionar_linha('livros.txt', ['.', '@@!', '+-*/', 'dois mil e dois', 'horror', 'oitenta']), None, 'Teste de tratamento de dados do cadastro de livro falhou')


    def test_ti_04A(self):
        self.assertEqual(adicionar_linha('emprestimos.txt', ['user@user', 'emprest test', '16/05/2025', '21/05/2025']), None, 'Teste de emprestimo de livro conforme falhou')
    
    def test_ti_04B(self):
        self.assertNotEqual(adicionar_linha('emprestimos.txt', ['user@user', 'emprest test', '16/05/2025', '21/05/2002']), None, 'Teste de emprestimo de livro não conforme foi sucedido')
        self.assertNotEqual(adicionar_linha('emprestimos.txt', ['user@user', 'emprest test', '16/05/2025', '']), None, 'Teste de emprestimo de livro não conforme foi sucedido')
    
    def test_ti_04C(self):
        self.assertNotEqual(adicionar_linha('emprestimos.txt', ['', '', '', '']), None, 'Teste de emprestimo de livro vazio falhou')
    
    def test_ti_04D(self):
        self.assertNotEqual(adicionar_linha('emprestimos.txt', ['user@user', 'Livro inexistente', '16/05/2025', '21/05/2025']), None, 'Teste de emprestimo de livro não-conforme falhou')
        self.assertNotEqual(adicionar_linha('emprestimos.txt', ['unregistered@email', 'LivroXYZ', '16/05/2025', '21/05/2025']), None, 'Teste de emprestimo de livro não-conforme falhou')

    # def test_ti_04E(self):
    #     self.assertEqual(adicionar_linha('emprestimos.txt', ['user@user', 'emprest test', '16/05/2025', '21/05/2025']), None, 'Teste de emprestimo de livro conforme falhou')


    def test_ti_05A(self):
        historico = ler_arquivo('historico.txt')
        usuario_historico = [h for h in historico if h[0] == 'user@user']
        # print(usuario_historico)
        self.assertEqual(usuario_historico, [['user@user', '', '2025-05-16', 'a', '2025-05-16']], 'Teste de historico falhou')

    def test_ti_05B(self):
        historico = ler_arquivo('historico.txt')
        usuario_historico = [h for h in historico if h[0] == 'naoregistrado@user']
        # print(usuario_historico)
        self.assertEqual(usuario_historico, [], 'Teste de historico falhou')

    def test_ti_06A(self):
        email_usuario = 'user@user'
        emprestimos = ler_arquivo('emprestimos.txt')
        livro_idx = 0
        # print(len(emprestimos))
        emprestimo = emprestimos[livro_idx]
        emprestimos.remove(emprestimo)
        
        adicionar_linha('historico.txt', emprestimo + [datetime.now().strftime('%Y-%m-%d')])
        aux = ''
        with open('emprestimos.txt', 'w', encoding='utf-8') as f:
            for e in emprestimos:
                f.write(';'.join(e) + '\n')
                # print(';'.join(e)+'\n')
                aux += ';'.join(e)+'\n'
        # print(aux)
        self.assertEqual(aux, "user@user;emprest test;16/05/2025;21/05/2002\n;;;\nuser@user;Livro inexistente;16/05/2025;21/05/2025\nuser@user;empresttest;16/05/2025;21/05/2025\n", 'Teste de Devolução')
        # self.assertEqual(devolver_livro(), None, 'Teste de Devolução')
