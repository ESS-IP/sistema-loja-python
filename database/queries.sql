-- 1. Produtos com estoque maior que 5, ordenados por categoria e preço
SELECT nome, categoria, preco, estoque 
FROM produtos 
WHERE estoque > 5 
ORDER BY categoria, preco;

-- 2. Relatório de vendas com nome do produto, categoria e data
SELECT 
    v.id as venda_id,
    p.nome as produto,
    p.categoria,
    v.quantidade,
    v.valor_total,
    v.data_venda
FROM vendas v
JOIN produtos p ON v.produto_id = p.id
ORDER BY v.data_venda DESC;

-- 3. Total de vendas e receita por categoria nos últimos 30 dias
SELECT 
    p.categoria,
    COUNT(v.id) as total_vendas,
    SUM(v.valor_total) as receita_total
FROM vendas v
JOIN produtos p ON v.produto_id = p.id
WHERE v.data_venda >= datetime('now', '-30 days')
GROUP BY p.categoria
ORDER BY receita_total DESC;

-- 4. Top 5 produtos mais vendidos por quantidade
SELECT 
    p.nome,
    p.categoria,
    SUM(v.quantidade) as total_vendido
FROM vendas v
JOIN produtos p ON v.produto_id = p.id
GROUP BY p.id, p.nome, p.categoria
ORDER BY total_vendido DESC
LIMIT 5;

-- 5. Produtos nunca vendidos ou com estoque crítico (< 3 unidades)
SELECT 
    p.id,
    p.nome,
    p.categoria,
    p.estoque,
    COALESCE(SUM(v.quantidade), 0) as total_vendido
FROM produtos p
LEFT JOIN vendas v ON p.id = v.produto_id
WHERE p.estoque < 3 OR v.id IS NULL
GROUP BY p.id, p.nome, p.categoria, p.estoque;