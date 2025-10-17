from database import Database

class Venda:
    def __init__(self):
        self.db = Database()
        
    def listar_todas(self):
        """Lista todas as vendas"""
        query = """
        SELECT v.*, p.nome as produto_nome, p.categoria 
        FROM vendas v 
        JOIN produtos p ON v.produto_id = p.id 
        ORDER BY v.data_venda DESC;
        """
        return self.db.execute_query(query, fetch=True)
    
    def buscar_por_periodo(self, data_inicio, data_fim):
        """Busca vendas por período"""
        query = """
        SELECT v.*, p.nome as produto_nome, p.categoria 
        FROM vendas v 
        JOIN produtos p ON v.produto_id = p.id 
        WHERE date(v.data_venda) BETWEEN ? AND ? 
        ORDER BY v.data_venda;
        """
        return self.db.execute_query(query, (data_inicio, data_fim), fetch=True)
    
    def registrar_venda(self, produto_id, quantidade):
        """Registra nova venda e atualiza estoque"""
        try:
            # Busca preço e estoque do produto
            query_preco = "SELECT preco, estoque FROM produtos WHERE id = ?;"
            produto = self.db.execute_query(query_preco, (produto_id,), fetch=True)
            
            if not produto:
                print("❌ Produto não encontrado!")
                return False
                
            preco, estoque_atual = produto[0]
            
            # Verifica estoque
            if estoque_atual < quantidade:
                print(f"❌ Estoque insuficiente! Disponível: {estoque_atual}")
                return False
            
            # Calcula valor total
            valor_total = preco * quantidade
            
            # Registra venda
            query_venda = """
            INSERT INTO vendas (produto_id, quantidade, valor_total) 
            VALUES (?, ?, ?);
            """
            
            # Atualiza estoque
            query_estoque = "UPDATE produtos SET estoque = estoque - ? WHERE id = ?;"
            
            # Executa ambas as operações
            if self.db.execute_query(query_venda, (produto_id, quantidade, valor_total)):
                if self.db.execute_query(query_estoque, (quantidade, produto_id)):
                    print(f"✅ Venda registrada! Valor: R$ {valor_total:.2f}")
                    return True
            
            return False
            
        except Exception as e:
            print(f"❌ Erro ao registrar venda: {e}")
            return False
    
    def calcular_total_vendas(self):
        """Calcula o total de vendas e receita"""
        query = "SELECT COUNT(*), SUM(valor_total) FROM vendas;"
        return self.db.execute_query(query, fetch=True)