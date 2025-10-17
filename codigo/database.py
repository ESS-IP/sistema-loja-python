import sqlite3
import os

class Database:
    def __init__(self):
        self.connection = None
        self.db_path = "loja.db"
        self.connect()
        
    def connect(self):
        """Estabelece conexão com o banco SQLite"""
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row
            print("✅ Conectado ao banco SQLite!")
            
            # Criar tabelas se não existirem
            self.criar_tabelas()
            
        except Exception as e:
            print(f"❌ Erro ao conectar: {e}")
            
    def criar_tabelas(self):
        """Cria as tabelas necessárias"""
        try:
            # Criar tabela produtos
            cursor = self.connection.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS produtos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    preco REAL NOT NULL,
                    categoria TEXT,
                    estoque INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Criar tabela vendas
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS vendas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    produto_id INTEGER,
                    quantidade INTEGER NOT NULL,
                    data_venda TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    valor_total REAL NOT NULL,
                    FOREIGN KEY (produto_id) REFERENCES produtos(id)
                )
            ''')
            
            self.connection.commit()
            print("✅ Tabelas criadas/verificadas!")
            
            # Popular com dados iniciais se estiver vazio
            self.popular_dados_iniciais()
            
        except Exception as e:
            print(f"❌ Erro ao criar tabelas: {e}")
    
    def popular_dados_iniciais(self):
        """Popula o banco com dados iniciais"""
        try:
            cursor = self.connection.cursor()
            
            # Verifica se já existem produtos
            cursor.execute("SELECT COUNT(*) as count FROM produtos")
            count = cursor.fetchone()[0]
            
            if count == 0:
                print("📝 Inserindo dados iniciais...")
                
                produtos = [
                    ('Smartphone Samsung', 899.99, 'Eletrônicos', 15),
                    ('Notebook Dell', 2499.99, 'Informática', 8),
                    ('Fone de Ouvido Bluetooth', 199.99, 'Áudio', 20),
                    ('Teclado Mecânico', 299.99, 'Informática', 12),
                    ('Mouse Gamer', 149.99, 'Informática', 6),
                    ('Smart TV 55"', 1899.99, 'Eletrônicos', 4),
                    ('Tablet iPad', 1299.99, 'Eletrônicos', 10),
                    ('Câmera Digital', 799.99, 'Fotografia', 2),
                    ('Impressora Laser', 499.99, 'Escritório', 7),
                    ('Monitor 24"', 699.99, 'Informática', 9)
                ]
                
                cursor.executemany(
                    "INSERT INTO produtos (nome, preco, categoria, estoque) VALUES (?, ?, ?, ?)",
                    produtos
                )
                
                self.connection.commit()
                print("✅ Dados iniciais inseridos!")
                
        except Exception as e:
            print(f"❌ Erro ao popular dados: {e}")
            
    def execute_query(self, query, params=None, fetch=False):
        """Executa queries no banco de dados"""
        try:
            cursor = self.connection.cursor()
            
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
                
            if fetch:
                return cursor.fetchall()
                
            self.connection.commit()
            return True
            
        except Exception as e:
            print(f"❌ Erro na query: {e}")
            return False
            
    def close(self):
        """Fecha a conexão com o banco"""
        if self.connection:
            self.connection.close()
            print("🔌 Conexão fechada!")