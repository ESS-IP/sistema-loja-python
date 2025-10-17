import unittest
from produto import Produto
from venda import Venda

class TestSistemaLoja(unittest.TestCase):
    
    def setUp(self):
        self.produto = Produto()
        self.venda = Venda()
    
    def test_listar_produtos(self):
        produtos = self.produto.listar_todos()
        self.assertIsNotNone(produtos)
    
    def test_buscar_produto_existente(self):
        produto = self.produto.buscar_por_id(1)
        self.assertIsNotNone(produto)
    
    def test_criar_produto(self):
        novo_id = self.produto.criar_produto("Produto Teste", 99.99, "Teste", 10)
        self.assertIsNotNone(novo_id)

if __name__ == '__main__':
    unittest.main()