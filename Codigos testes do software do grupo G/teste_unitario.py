import unittest
import os
import tempfile
import time
from app import app, salvar_usuario, validar_login, ler_arquivo, adicionar_linha
import app as library_app

class TestUTCases(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()
        self.tmp = tempfile.TemporaryDirectory()
        for attr in ['ARQ_LIVROS','ARQ_USUARIOS','ARQ_EMPRESTIMOS','ARQ_HISTORICO']:
            new = os.path.join(self.tmp.name, getattr(library_app, attr))
            setattr(library_app, attr, new)
            os.makedirs(os.path.dirname(new), exist_ok=True)
            open(new,'w',encoding='utf-8').close()

    def tearDown(self):
        self.tmp.cleanup()

    
    # UT-01A Cadastro de Livros
    def test_ut01_cadastro_perfeito_livro(self):
        salvar_usuario('Admin', 'admin@example.com', '123')
        self.client.post('/login', data={
            'email': 'admin@example.com',
            'senha': '123'
        })
        rv = self.client.post('/cadastrar_livro', data={
            'titulo': 'T1',
            'autor': 'A1',
            'editora': 'E1',
            'ano': '2000',
            'genero': 'G1',
            'isbn': '123'
        }, follow_redirects=True)
        self.assertEqual(rv.status_code, 200)
        livros = ler_arquivo(library_app.ARQ_LIVROS)
        self.assertIn(['T1','A1','E1','2000','G1','123'], livros)

    # UT-01B Cadastro de Livro com Campos Faltando
    def test_ut01_cadastro_faltando_campo_livro(self):
        salvar_usuario('Admin', 'admin@example.com', '123')
        self.client.post('/login', data={
            'email': 'admin@example.com',
            'senha': '123'
        })
        
        rv = self.client.post('/cadastrar_livro', data={
            'titulo':'T2',
            'autor':'A2',
            'editora':'E2',
            'ano':'2001',
            'genero':'G2'
        }, follow_redirects=True)
        
        self.assertEqual(rv.status_code, 400)
        livros = ler_arquivo(library_app.ARQ_LIVROS)
        self.assertNotIn(['T2','A2','E2','2001','G2',''], livros)
        self.assertTrue(rv.data, "Deveria haver alguma resposta de erro")
        self.assertTrue(b'form' in rv.data.lower() or b'error' in rv.data.lower() or 
                    b'erro' in rv.data.lower(), "Deveria haver alguma indicio de erro")

    # UT-02A Edição de Dados de Livro
    def test_ut02_edicao_perfeita_livro(self):
        salvar_usuario('Admin', 'admin@example.com', 'admin123')
        self.client.post('/login', data={
            'email': 'admin@example.com',
            'senha': 'admin123'
        }) 

        adicionar_linha(library_app.ARQ_LIVROS,
                    ['Livro Original','Autor Original','Editora','2020','Genero','123'])
        
        rv = self.client.post('/editar_livro', data={
            'livro_idx': '0',
            'titulo': 'Livro Editado',
            'autor': 'Autor Editado',
            'editora': 'Nova Editora',
            'ano': '2021',
            'genero': 'Novo Genero',
            'isbn': '456'
        }, follow_redirects=True)
        
        self.assertEqual(rv.status_code, 200)
        livros = ler_arquivo(library_app.ARQ_LIVROS)
        self.assertIn(['Livro Editado','Autor Editado','Nova Editora','2021','Novo Genero','456'], livros)
        self.assertNotIn(['Livro Original','Autor Original','Editora','2020','Genero','123'], livros)

    # UT-02B Edição de Livro com Campos Inválidos
    def test_ut02_edicao_invalida_livro(self):
        salvar_usuario('Admin', 'admin@example.com', 'admin123')
        self.client.post('/login', data={
            'email': 'admin@example.com',
            'senha': 'admin123'
        })
        
        adicionar_linha(library_app.ARQ_LIVROS,['Livro Test','Autor Test','Editora Test','2020','Genero Test','789'])
        rv = self.client.post('/editar_livro', data={
            'livro_idx': '0',
            'titulo': '',  
            'autor': 'Novo Autor',
            'editora': 'Nova Editora',
            'ano': '2021',
            'genero': 'Novo Genero',
            'isbn': '012'
        }, follow_redirects=True)
        
        self.assertEqual(rv.status_code, 400)
        livros = ler_arquivo(library_app.ARQ_LIVROS)
        self.assertIn(['Livro Test','Autor Test','Editora Test','2020','Genero Test','789'], livros)


    # UT-03A Exclusão de Livro
    def test_ut03_exclusao_perfeita(self):
        salvar_usuario('Admin', 'admin@example.com', 'admin123')
        self.client.post('/login', data={
            'email': 'admin@example.com',
            'senha': 'admin123'
        })
        
        adicionar_linha(library_app.ARQ_LIVROS,['Livro Excluir','Autor','Editora','2020','Genero','111'])
        rv = self.client.post('/excluir_livro', data={
            'livro_idx': '0'
        }, follow_redirects=True)
        
        self.assertEqual(rv.status_code, 200)
        livros = ler_arquivo(library_app.ARQ_LIVROS)
        self.assertNotIn(['Livro Excluir','Autor','Editora','2020','Genero','111'], livros)

    # UT-03B Exclusão de Livro Inexistente
    def test_ut03_exclusao_inexistente(self):
        salvar_usuario('Admin', 'admin@example.com', 'admin123')
        self.client.post('/login', data={
            'email': 'admin@example.com',
            'senha': 'admin123'
        })
        
        rv = self.client.post('/excluir_livro', data={
            'livro_idx': '999'  
        }, follow_redirects=True)
        
        self.assertEqual(rv.status_code, 400)
        self.assertIn(b'Livro nao encontrado', rv.data)

    # UT-04A Registro de Empréstimo
    def test_ut04_emprestimo_valido(self):
        salvar_usuario('U4','u4@example.com','pw')
        self.client.post('/login',data={'email':'u4@example.com','senha':'pw'})
        adicionar_linha(library_app.ARQ_LIVROS,['L4','A4','E4','2004','G4','444'])
        rv = self.client.post('/emprestar_livro',data={'livro_idx':'0','prazo':'2025-12-31'})
        self.assertIn(rv.status_code, [200, 302])
        emprestimos = ler_arquivo(library_app.ARQ_EMPRESTIMOS)
        self.assertTrue(any(e[0]=='u4@example.com' for e in emprestimos))

    # UT-04B Registro de Empréstimo com Livro Já Emprestado
    def test_ut04_emprestimo_livro_ja_emprestado(self):
        salvar_usuario('U4a','u4a@example.com','pw4a')
        self.client.post('/login',data={'email':'u4a@example.com','senha':'pw4a'})
        adicionar_linha(library_app.ARQ_LIVROS,['L4','A4','E4','2004','G4','444'])
        self.client.post('/emprestar_livro',data={'livro_idx':'0','prazo':'2025-12-31'})
        salvar_usuario('U4b','u4b@example.com','pw4b')
        self.client.post('/login',data={'email':'u4b@example.com','senha':'pw4b'})
        rv = self.client.post('/emprestar_livro',data={'livro_idx':'0','prazo':'2025-12-31'})
        self.assertEqual(rv.status_code, 400)
        emprestimos = ler_arquivo(library_app.ARQ_EMPRESTIMOS)
        self.assertEqual(len(emprestimos), 1)
        self.assertEqual(emprestimos[0][0], 'u4a@example.com')

    # UT-05A Registro de Devolução
    def test_ut05_devolucao_valida(self):
        salvar_usuario('U5','u5@example.com','pw5')
        self.client.post('/login',data={'email':'u5@example.com','senha':'pw5'})
        adicionar_linha(library_app.ARQ_LIVROS,['L5','A5','E5','2005','G5','555'])
        self.client.post('/emprestar_livro',data={'livro_idx':'0','prazo':'2025-12-31'})
        rv = self.client.post('/devolver_livro',data={'livro_idx':'0'})
        self.assertIn(rv.status_code, [200, 302])
        emp = ler_arquivo(library_app.ARQ_EMPRESTIMOS)
        hist = ler_arquivo(library_app.ARQ_HISTORICO)
        self.assertEqual(emp,[])
        self.assertTrue(any(h[0]=='u5@example.com' for h in hist))

    # UT-05B Registro de Devolução com Livro Não Emprestado
    def test_ut05_devolucao_sem_emprestimo(self):
        salvar_usuario('U5b','u5b@example.com','pw5b')
        self.client.post('/login',data={'email':'u5b@example.com','senha':'pw5b'})
        adicionar_linha(library_app.ARQ_LIVROS,['L5b','A5b','E5b','2005','G5b','556'])
        emprestimos_antes = ler_arquivo(library_app.ARQ_EMPRESTIMOS)
        historico_antes = ler_arquivo(library_app.ARQ_HISTORICO)
        
        try:
            rv = self.client.post('/devolver_livro',data={'livro_idx':'0'}, follow_redirects=True)
            self.assertEqual(rv.status_code, 400)
            self.assertTrue(rv.data, "Deveria haver alguma resposta de erro")
        except:
            self.fail("O sistema lança exceção ao tentar devolver livro não emprestado - " + "deveria validar e retornar erro 400 em vez de falhar")
        
        emprestimos_depois = ler_arquivo(library_app.ARQ_EMPRESTIMOS)
        historico_depois = ler_arquivo(library_app.ARQ_HISTORICO)
        self.assertEqual(emprestimos_antes, emprestimos_depois)
        self.assertEqual(historico_antes, historico_depois)

    # UT-06A Histórico por usuário
    def test_ut06_historico_exibe(self):
        salvar_usuario('U6','u6@example.com','pw6')
        self.client.post('/login',data={'email':'u6@example.com','senha':'pw6'})
        adicionar_linha(library_app.ARQ_HISTORICO,['u6@example.com','L6','2025-06-01','2025-06-15','2025-06-15'])
        rv = self.client.get('/historico')
        self.assertEqual(rv.status_code, 200)
        self.assertIn(b'L6',rv.data)

    # UT-06B Histórico vazio
    def test_ut06_historico_vazio(self):
        salvar_usuario('U6b','u6b@example.com','pw6b')
        self.client.post('/login',data={'email':'u6b@example.com','senha':'pw6b'})
        rv = self.client.get('/historico')
        self.assertEqual(rv.status_code, 200)
        self.assertNotIn(b'<li>',rv.data)

    # UT-07A Cadastro de Usuários
    def test_ut07_cadastro_valido(self):
        rv = self.client.post('/salvar_cadastro',data={'nome':'N7','email':'u7@example.com','senha':'pw7'})
        self.assertIn(rv.status_code, [200, 302])
        users = ler_arquivo(library_app.ARQ_USUARIOS)
        self.assertTrue(any(u[1]=='u7@example.com' for u in users))

    # UT-07B Cadastro de Usuário com Campos Inválidos
    def test_ut07_cadastro_duplicado(self):
        salvar_usuario('N7b','u7b@example.com','pw7b')
        rv = self.client.post('/salvar_cadastro',data={'nome':'N7b','email':'u7b@example.com','senha':'pw7b'})
        self.assertEqual(rv.status_code, 400)
        users = ler_arquivo(library_app.ARQ_USUARIOS)
        self.assertEqual(sum(1 for u in users if u[1]=='u7b@example.com'), 1)

    # UT-07C Cadastro de Usuário com Campos Faltando
    def test_ut07_cadastro_faltando(self):
        rv = self.client.post('/salvar_cadastro',data={'nome':'','email':'','senha':''})
        self.assertEqual(rv.status_code, 400)
        users = ler_arquivo(library_app.ARQ_USUARIOS)
        self.assertEqual(len(users), 0)

    # UT-08A Login de Usuários
    def test_ut08_login_valido(self):
        salvar_usuario('N8','u8@example.com','pw8')
        rv = self.client.post('/login',data={'email':'u8@example.com','senha':'pw8'})
        self.assertEqual(rv.status_code,302)
        self.assertIn('/biblioteca',rv.location)

    # UT-08B Login com Campos Inválidos
    def test_ut08_login_invalido(self):
        rv = self.client.post('/login',data={'email':'x','senha':'y'})
        self.assertEqual(rv.status_code,302)
        self.assertIn('/',rv.location)
   
if __name__ == '__main__':
    unittest.main()