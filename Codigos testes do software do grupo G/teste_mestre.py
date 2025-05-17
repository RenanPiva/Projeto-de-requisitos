import os
import unittest
import requests
from datetime import datetime

BASE_URL = 'http://localhost:15243'

# Caminhos dos arquivos de dados (ajuste conforme seu setup)
ARQ_USUARIOS   = 'usuarios.txt'
ARQ_LIVROS     = 'livros.txt'
ARQ_EMPRESTIMOS = 'emprestimos.txt'
ARQ_HISTORICO   = 'historico.txt'

def limpa_arquivos():
    """Zera ou cria arquivos de dados."""
    for path in (ARQ_USUARIOS, ARQ_LIVROS, ARQ_EMPRESTIMOS, ARQ_HISTORICO):
        with open(path, 'w', encoding='utf-8') as f:
            pass  # apenas limpa o conteúdo

def le_arquivo(path):
    """Retorna lista de linhas sem quebra-de-linha."""
    with open(path, 'r', encoding='utf-8') as f:
        return [l.strip() for l in f if l.strip()]

class TestSistemaBiblioteca(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Limpa e popula dados iniciais
        limpa_arquivos()
        # Usuários iniciais
        with open(ARQ_USUARIOS, 'a', encoding='utf-8') as f:
            f.write('Alice Souza;alice@example.com;s3nhAlic3\n')
        # Livros iniciais
        livros = [
            '1984;George Orwell;Companhia das Letras;1949;Distopia;978-8525430390',
            'O Pequeno Príncipe;Antoine de Saint-Exupéry;Agir;1943;Infantil;978-8522014744',
            'Clean Code;Robert C. Martin;Alta Books;2008;Programação;978-8576082673'
        ]
        with open(ARQ_LIVROS, 'a', encoding='utf-8') as f:
            f.write('\n'.join(livros) + '\n')

    def setUp(self):
        # Mantém sessão entre requisições
        self.session = requests.Session()

    def test_1_cadastro_login(self):
        # 1. Cadastro de novo usuário
        resp = self.session.post(
            f"{BASE_URL}/salvar_cadastro",
            data={'nome': 'Bruno Pereira', 'email': 'bruno@mail.com', 'senha': 'P4ssBrun0'},
            allow_redirects=False
        )
        self.assertEqual(resp.status_code, 302)
        usuarios = le_arquivo(ARQ_USUARIOS)
        self.assertIn('Bruno Pereira;bruno@mail.com;P4ssBrun0', usuarios)

        # 2. Login com credenciais válidas
        resp = self.session.post(
            f"{BASE_URL}/login",
            data={'email': 'bruno@mail.com', 'senha': 'P4ssBrun0'},
            allow_redirects=False
        )
        self.assertEqual(resp.status_code, 302)
        # redireciona para /biblioteca
        self.assertTrue(resp.headers['Location'].endswith('/biblioteca'))

        # 3. Logout (limpar sessão)
        self.session.cookies.clear()

        # 4. Login inválido
        resp = self.session.post(
            f"{BASE_URL}/login",
            data={'email': 'bruno@mail.com', 'senha': 'senha_errada'},
            allow_redirects=False
        )
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(resp.headers['Location'].endswith('/'))

    def test_2_cadastrar_e_listar_livro(self):
        # Login com Alice
        self.session.post(
            f"{BASE_URL}/login",
            data={'email': 'alice@example.com', 'senha': 's3nhAlic3'}
        )
        # Cadastrar novo livro
        resp = self.session.post(
            f"{BASE_URL}/cadastrar_livro",
            data={
                'titulo':'Dom Casmurro', 'autor':'Machado de Assis',
                'editora':'Global', 'ano':'1899', 'genero':'Romance', 'isbn':'978-8525409169'
            },
            allow_redirects=False
        )
        self.assertEqual(resp.status_code, 302)
        livros = le_arquivo(ARQ_LIVROS)
        self.assertIn('Dom Casmurro;Machado de Assis;Global;1899;Romance;978-8525409169', livros)

    def test_3_emprestar_livro(self):
        # Já logada como Alice
        # Empréstimo do primeiro livro ("1984")
        resp = self.session.post(
            f"{BASE_URL}/emprestar_livro",
            data={'livro_idx': '0', 'prazo': '7 dias'},  # livro_idx é necessário!
            allow_redirects=False
        )
        self.assertEqual(resp.status_code, 302)
        emprestimos = le_arquivo(ARQ_EMPRESTIMOS)
        hoje = datetime.now().strftime('%Y-%m-%d')
        esperado = f"alice@example.com;1984;{hoje};7 dias"
        self.assertIn(esperado, emprestimos)

    def test_4_devolver_e_historico(self):
        # Devolver o empréstimo 0
        resp = self.session.post(
            f"{BASE_URL}/devolver_livro",
            data={'livro_idx': '0'},
            allow_redirects=False
        )
        self.assertEqual(resp.status_code, 302)

        # Checar que emprestimos.txt está vazio
        emprestimos = le_arquivo(ARQ_EMPRESTIMOS)
        self.assertEqual(len(emprestimos), 0)

        # Checar histórico
        historico = le_arquivo(ARQ_HISTORICO)
        self.assertTrue(len(historico) >= 1)
        # O último registro deve corresponder ao empréstimo devolvido
        ultima = historico[-1].split(';')
        self.assertEqual(ultima[0], 'alice@example.com')
        self.assertEqual(ultima[1], '1984')

    def test_5_historico_usuario(self):
        # Acessar /historico e verificar texto
        resp = self.session.get(f"{BASE_URL}/historico")
        self.assertEqual(resp.status_code, 200)
        # Deve conter ao menos o e-mail no HTML
        self.assertIn('alice@example.com', resp.text)

    def test_6_erro_emprestar_livro_duplicado(self):
        # Tentar emprestar livro que já está emprestado
        self.session.post(f"{BASE_URL}/login", data={'email': 'alice@example.com', 'senha': 's3nhAlic3'})
        # Primeiro empréstimo
        self.session.post(f"{BASE_URL}/emprestar_livro", data={'livro_idx': '1', 'prazo': '7 dias'})
        # Tentar emprestar novamente
        resp = self.session.post(f"{BASE_URL}/emprestar_livro", data={'livro_idx': '1', 'prazo': '7 dias'})
        # Verificar erro
        self.assertEqual(resp.status_code, 400)
        # Verificar que não há duplicação no arquivo
        emprestimos = le_arquivo(ARQ_EMPRESTIMOS)
        self.assertEqual(len([e for e in emprestimos if '1' in e]), 1)


if __name__ == '__main__':
    unittest.main(verbosity=2)
