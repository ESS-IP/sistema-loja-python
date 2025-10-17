from database import Database

class Produto:
    def __init__(self):
        self.db = Database()
        
    def listar_todos(self):
        """Lista todos os produtos"""
        query = "SELECT * FROM produtos ORDER BY id;"
        return self.db.execute_query(query, fetch=True)
    
    def buscar_por_id(self, produto_id):
        """Busca produto por ID"""
        query = "SELECT * FROM produtos WHERE id = ?;"
        return self.db.execute_query(query, (produto_id,), fetch=True)
    
    def filtrar_por_categoria(self, categoria):
        """Filtra produtos por categoria"""
        query = "SELECT * FROM produtos WHERE categoria = ? ORDER BY nome;"
        return self.db.execute_query(query, (categoria,), fetch=True)
    
    def atualizar_estoque(self, produto_id, novo_estoque):
        """Atualiza estoque do produto"""
        query = "UPDATE produtos SET estoque = ? WHERE id = ?;"
        return self.db.execute_query(query, (novo_estoque, produto_id))
    
    def criar_produto(self, nome, preco, categoria, estoque=0):
        """Cria novo produto"""
        query = """
        INSERT INTO produtos (nome, preco, categoria, estoque) 
        VALUES (?, ?, ?, ?);
        """
        if self.db.execute_query(query, (nome, preco, categoria, estoque)):
            # Pegar o último ID inserido
            result = self.db.execute_query("SELECT last_insert_rowid()", fetch=True)
            if result:
                print(f"✅ Produto '{nome}' criado com ID: {result[0][0]}")
                return result[0][0]
        return None
    
    def produtos_estoque_baixo(self, limite=3):
        """Lista produtos com estoque crítico"""
        query = "SELECT * FROM produtos WHERE estoque < ? ORDER BY estoque;"
        return self.db.execute_query(query, (limite,), fetch=True)