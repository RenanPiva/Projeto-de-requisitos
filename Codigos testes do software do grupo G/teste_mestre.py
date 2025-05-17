import os
import unittest
import requests
from datetime import datetime

BASE_URL = 'http://localhost:15243'

ARQ_USUARIOS   = 'usuarios.txt'
ARQ_LIVROS     = 'livros.txt'
ARQ_EMPRESTIMOS = 'emprestimos.txt'
ARQ_HISTORICO   = 'historico.txt'

def limpa_arquivos():
    """Zera ou cria arquivos de dados."""
    for path in (ARQ_USUARIOS, ARQ_LIVROS, ARQ_EMPRESTIMOS, ARQ_HISTORICO):
        with open(path, 'w', encoding='utf-8') as f:
            pass  

def le_arquivo(path):
    """Retorna lista de linhas sem quebra-de-linha."""
    with open(path, 'r', encoding='utf-8') as f:
        return [l.strip() for l in f if l.strip()]

class TestSistemaBiblioteca(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        limpa_arquivos()
        with open(ARQ_USUARIOS, 'a', encoding='utf-8') as f:
            f.write('Alice Souza;alice@example.com;s3nhAlic3\n')
        livros = [
            '1984;George Orwell;Companhia das Letras;1949;Distopia;978-8525430390',
            'O Pequeno Príncipe;Antoine de Saint-Exupéry;Agir;1943;Infantil;978-8522014744',
            'Clean Code;Robert C. Martin;Alta Books;2008;Programação;978-8576082673'
        ]
        with open(ARQ_LIVROS, 'a', encoding='utf-8') as f:
            f.write('\n'.join(livros) + '\n')

    def setUp(self):
        self.session = requests.Session()

    def test_1_cadastro_login(self):
        resp = self.session.post(
            f"{BASE_URL}/salvar_cadastro",
            data={'nome': 'Bruno Pereira', 'email': 'bruno@mail.com', 'senha': 'P4ssBrun0'},
            allow_redirects=False
        )
        self.assertEqual(resp.status_code, 302)
        usuarios = le_arquivo(ARQ_USUARIOS)
        self.assertIn('Bruno Pereira;bruno@mail.com;P4ssBrun0', usuarios)
        resp = self.session.post(
            f"{BASE_URL}/login",
            data={'email': 'bruno@mail.com', 'senha': 'P4ssBrun0'},
            allow_redirects=False
        )
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(resp.headers['Location'].endswith('/biblioteca'))
        self.session.cookies.clear()
        resp = self.session.post(
            f"{BASE_URL}/login",
            data={'email': 'bruno@mail.com', 'senha': 'senha_errada'},
            allow_redirects=False
        )
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(resp.headers['Location'].endswith('/'))

    def test_2_cadastrar_e_listar_livro(self):
        self.session.post(
            f"{BASE_URL}/login",
            data={'email': 'alice@example.com', 'senha': 's3nhAlic3'}
        )
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
        resp = self.session.post(
            f"{BASE_URL}/emprestar_livro",
            data={'livro_idx': '0', 'prazo': '7 dias'}, 
            allow_redirects=False
        )
        self.assertEqual(resp.status_code, 302)
        emprestimos = le_arquivo(ARQ_EMPRESTIMOS)
        hoje = datetime.now().strftime('%Y-%m-%d')
        esperado = f"alice@example.com;1984;{hoje};7 dias"
        self.assertIn(esperado, emprestimos)

    def test_4_devolver_e_historico(self):
        resp = self.session.post(
            f"{BASE_URL}/devolver_livro",
            data={'livro_idx': '0'},
            allow_redirects=False
        )
        self.assertEqual(resp.status_code, 302)

        emprestimos = le_arquivo(ARQ_EMPRESTIMOS)
        self.assertEqual(len(emprestimos), 0)

        historico = le_arquivo(ARQ_HISTORICO)
        self.assertTrue(len(historico) >= 1)
        ultima = historico[-1].split(';')
        self.assertEqual(ultima[0], 'alice@example.com')
        self.assertEqual(ultima[1], '1984')

    def test_5_historico_usuario(self):
        resp = self.session.get(f"{BASE_URL}/historico")
        self.assertEqual(resp.status_code, 200)
        self.assertIn('alice@example.com', resp.text)

    def test_6_erro_emprestar_livro_duplicado(self):
        self.session.post(f"{BASE_URL}/login", data={'email': 'alice@example.com', 'senha': 's3nhAlic3'})
        self.session.post(f"{BASE_URL}/emprestar_livro", data={'livro_idx': '1', 'prazo': '7 dias'})
        resp = self.session.post(f"{BASE_URL}/emprestar_livro", data={'livro_idx': '1', 'prazo': '7 dias'})
        self.assertEqual(resp.status_code, 400)
        emprestimos = le_arquivo(ARQ_EMPRESTIMOS)
        self.assertEqual(len([e for e in emprestimos if '1' in e]), 1)


if __name__ == '__main__':
    unittest.main(verbosity=2)
