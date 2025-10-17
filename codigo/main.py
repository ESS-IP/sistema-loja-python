from produto import Produto
from venda import Venda
import os

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def menu_principal():
    print("\n" + "="*50)
    print("🏪 SISTEMA DE GERENCIAMENTO DE LOJA")
    print("="*50)
    print("1. Gestão de Produtos")
    print("2. Gestão de Vendas")
    print("3. Relatórios")
    print("0. Sair")
    print("="*50)

def menu_produtos():
    produto = Produto()
    
    while True:
        print("\n" + "="*40)
        print("📦 GESTÃO DE PRODUTOS")
        print("="*40)
        print("1. Listar todos os produtos")
        print("2. Buscar produto por ID")
        print("3. Filtrar por categoria")
        print("4. Atualizar estoque")
        print("5. Criar novo produto")
        print("6. Produtos com estoque crítico")
        print("0. Voltar")
        print("="*40)
        
        opcao = input("Escolha uma opção: ")
        
        if opcao == "1":
            produtos = produto.listar_todos()
            if produtos:
                print("\n📋 Lista de Produtos:")
                print("-" * 60)
                for prod in produtos:
                    print(f"ID: {prod[0]:2d} | {prod[1]:20} | R$ {prod[2]:8.2f} | {prod[3]:12} | Estoque: {prod[4]:2d}")
            else:
                print("Nenhum produto encontrado!")
                
        elif opcao == "2":
            try:
                id_prod = int(input("ID do produto: "))
                resultado = produto.buscar_por_id(id_prod)
                if resultado:
                    prod = resultado[0]
                    print(f"\n🔍 Produto encontrado:")
                    print(f"ID: {prod[0]}")
                    print(f"Nome: {prod[1]}")
                    print(f"Preço: R$ {prod[2]:.2f}")
                    print(f"Categoria: {prod[3]}")
                    print(f"Estoque: {prod[4]}")
                    print(f"Criado em: {prod[5]}")
                else:
                    print("Produto não encontrado!")
            except ValueError:
                print("ID deve ser um número!")
                
        elif opcao == "3":
            categoria = input("Categoria: ")
            produtos = produto.filtrar_por_categoria(categoria)
            if produtos:
                print(f"\n📂 Produtos na categoria '{categoria}':")
                for prod in produtos:
                    print(f"ID: {prod[0]} | {prod[1]} | R$ {prod[2]:.2f} | Estoque: {prod[4]}")
            else:
                print("Nenhum produto encontrado!")
                
        elif opcao == "4":
            try:
                id_prod = int(input("ID do produto: "))
                novo_estoque = int(input("Novo estoque: "))
                if produto.atualizar_estoque(id_prod, novo_estoque):
                    print("✅ Estoque atualizado com sucesso!")
            except ValueError:
                print("Valores devem ser números!")
                
        elif opcao == "5":
            nome = input("Nome do produto: ")
            try:
                preco = float(input("Preço: R$ "))
                categoria = input("Categoria: ")
                estoque = int(input("Estoque inicial: "))
                produto.criar_produto(nome, preco, categoria, estoque)
            except ValueError:
                print("Preço e estoque devem ser números!")
                
        elif opcao == "6":
            produtos = produto.produtos_estoque_baixo()
            if produtos:
                print("\n⚠️  Produtos com estoque crítico:")
                for prod in produtos:
                    print(f"ID: {prod[0]} | {prod[1]} | Estoque: {prod[4]}")
            else:
                print("Nenhum produto com estoque crítico!")
                
        elif opcao == "0":
            break
        else:
            print("Opção inválida!")

def menu_vendas():
    venda = Venda()
    
    while True:
        print("\n" + "="*40)
        print("💰 GESTÃO DE VENDAS")
        print("="*40)
        print("1. Listar todas as vendas")
        print("2. Registrar nova venda")
        print("3. Buscar vendas por período")
        print("4. Total de vendas")
        print("0. Voltar")
        print("="*40)
        
        opcao = input("Escolha uma opção: ")
        
        if opcao == "1":
            vendas = venda.listar_todas()
            if vendas:
                print("\n📊 Histórico de Vendas:")
                print("-" * 70)
                for v in vendas:
                    print(f"ID: {v[0]:2d} | {v[5]:20} | Qtd: {v[2]:2d} | Total: R$ {v[4]:8.2f} | Data: {v[3]}")
            else:
                print("Nenhuma venda encontrada!")
                
        elif opcao == "2":
            try:
                produto_id = int(input("ID do produto: "))
                quantidade = int(input("Quantidade: "))
                venda.registrar_venda(produto_id, quantidade)
            except ValueError:
                print("ID e quantidade devem ser números!")
                
        elif opcao == "3":
            data_inicio = input("Data início (YYYY-MM-DD): ")
            data_fim = input("Data fim (YYYY-MM-DD): ")
            vendas = venda.buscar_por_periodo(data_inicio, data_fim)
            if vendas:
                print(f"\n📅 Vendas de {data_inicio} a {data_fim}:")
                for v in vendas:
                    print(f"ID: {v[0]} | Produto: {v[5]} | Qtd: {v[2]} | Total: R$ {v[4]:.2f} | Data: {v[3]}")
            else:
                print("Nenhuma venda no período!")
                
        elif opcao == "4":
            total = venda.calcular_total_vendas()
            if total and total[0]:
                count, receita = total[0]
                print(f"\n💰 Total de Vendas: {count}")
                print(f"💰 Receita Total: R$ {receita or 0:.2f}")
                
        elif opcao == "0":
            break
        else:
            print("Opção inválida!")

def menu_relatorios():
    from database import Database
    db = Database()
    
    while True:
        print("\n" + "="*40)
        print("📈 RELATÓRIOS")
        print("="*40)
        print("1. Produtos com estoque > 5")
        print("2. Relatório completo de vendas")
        print("3. Vendas por categoria (30 dias)")
        print("4. Top 5 produtos mais vendidos")
        print("5. Produtos nunca vendidos ou estoque crítico")
        print("0. Voltar")
        print("="*40)
        
        opcao = input("Escolha uma opção: ")
        
        if opcao == "1":
            query = "SELECT nome, categoria, preco, estoque FROM produtos WHERE estoque > 5 ORDER BY categoria, preco;"
            resultado = db.execute_query(query, fetch=True)
            if resultado:
                print("\n📦 Produtos com estoque > 5:")
                for prod in resultado:
                    print(f"{prod[0]:20} | {prod[1]:12} | R$ {prod[2]:8.2f} | Estoque: {prod[3]:2d}")
        
        elif opcao == "2":
            query = """
            SELECT v.id, p.nome, p.categoria, v.quantidade, v.valor_total, v.data_venda 
            FROM vendas v JOIN produtos p ON v.produto_id = p.id 
            ORDER BY v.data_venda DESC;
            """
            resultado = db.execute_query(query, fetch=True)
            if resultado:
                print("\n📊 Relatório de Vendas:")
                for venda in resultado:
                    print(f"Venda {venda[0]:3d} | {venda[1]:20} | {venda[2]:12} | Qtd: {venda[3]:2d} | R$ {venda[4]:8.2f} | {venda[5]}")
        
        elif opcao == "3":
            query = """
            SELECT p.categoria, COUNT(v.id), SUM(v.valor_total)
            FROM vendas v JOIN produtos p ON v.produto_id = p.id 
            WHERE v.data_venda >= datetime('now', '-30 days')
            GROUP BY p.categoria ORDER BY SUM(v.valor_total) DESC;
            """
            resultado = db.execute_query(query, fetch=True)
            if resultado:
                print("\n📅 Vendas por Categoria (30 dias):")
                for cat in resultado:
                    print(f"{cat[0]:15} | Vendas: {cat[1]:2d} | Receita: R$ {cat[2] or 0:8.2f}")
        
        elif opcao == "4":
            query = """
            SELECT p.nome, p.categoria, SUM(v.quantidade) as total_vendido
            FROM vendas v JOIN produtos p ON v.produto_id = p.id
            GROUP BY p.id, p.nome, p.categoria ORDER BY total_vendido DESC LIMIT 5;
            """
            resultado = db.execute_query(query, fetch=True)
            if resultado:
                print("\n🏆 Top 5 Produtos Mais Vendidos:")
                for i, prod in enumerate(resultado, 1):
                    print(f"{i}º - {prod[0]:20} | {prod[1]:12} | Vendidos: {prod[2]:2d}")
        
        elif opcao == "5":
            query = """
            SELECT p.id, p.nome, p.categoria, p.estoque, COALESCE(SUM(v.quantidade), 0) as total_vendido
            FROM produtos p LEFT JOIN vendas v ON p.id = v.produto_id
            WHERE p.estoque < 3 OR v.id IS NULL
            GROUP BY p.id, p.nome, p.categoria, p.estoque;
            """
            resultado = db.execute_query(query, fetch=True)
            if resultado:
                print("\n⚠️  Produtos Nunca Vendidos ou Estoque Crítico:")
                for prod in resultado:
                    status = "ESTOQUE BAIXO" if prod[3] < 3 else "NUNCA VENDIDO"
                    print(f"ID: {prod[0]:2d} | {prod[1]:20} | {prod[2]:12} | Estoque: {prod[3]:2d} | Vendidos: {prod[4]:2d} | {status}")
        
        elif opcao == "0":
            break
        else:
            print("Opção inválida!")

def main():
    print("🚀 Iniciando Sistema de Gerenciamento de Loja...")
    
    while True:
        menu_principal()
        opcao = input("Escolha uma opção: ")
        
        if opcao == "1":
            menu_produtos()
        elif opcao == "2":
            menu_vendas()
        elif opcao == "3":
            menu_relatorios()
        elif opcao == "0":
            print("👋 Saindo do sistema...")
            break
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    main()