# 📊 Análise Técnica do Projeto

## 🎯 Escolhas de Desenvolvimento

### Arquitetura e Organização
Optei por uma arquitetura modular separando responsabilidades:

- **`database.py`**: Classe única para gerenciamento de conexão e queries com SQLite
- **`produto.py`**: Lógica específica de negócio para produtos (CRUD completo)
- **`venda.py`**: Lógica específica de negócio para vendas com atualização automática de estoque
- **`main.py`**: Interface de usuário em console e controle de fluxo da aplicação
- **`tests.py`**: Testes unitários para validação das funcionalidades principais

### Padrões e Boas Práticas
- **Separation of Concerns**: Cada módulo tem responsabilidade bem definida
- **DRY (Don't Repeat Yourself)**: Classe Database centralizada evita código duplicado
- **Error Handling**: Tratamento robusto de exceções em operações de banco
- **SQL Injection Protection**: Uso de prepared statements em todas as queries
- **Atomic Operations**: Transações implícitas para garantir consistência

### Escolha do SQLite
Decisão estratégica para atender ao contexto do teste:

- **Zero Dependencies**: Não requer instalação de SGBD externo
- **Portabilidade Total**: Arquivo único .db, fácil execução em qualquer ambiente
- **Performance Adequada**: Suficiente para escala de teste/estágio
- **Compatibilidade Universal**: Funciona em qualquer sistema com Python

## 🏗️ Estrutura de Dados

### Modelo Relacional Implementado