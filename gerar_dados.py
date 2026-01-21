import pandas as pd
import random
from datetime import datetime, timedelta

# Produtos e categorias
produtos = [
    ("Notebook", "Eletrônicos"),
    ("Smartphone", "Eletrônicos"),
    ("Mouse", "Periféricos"),
    ("Teclado", "Periféricos"),
    ("Monitor", "Eletrônicos"),
    ("Cadeira Gamer", "Móveis"),
    ("Mesa Escritório", "Móveis"),
    ("Fone de Ouvido", "Periféricos"),
]

dados = []

data_inicial = datetime(2024, 1, 1)

for _ in range(500):  # 500 vendas
    produto, categoria = random.choice(produtos)
    data_venda = data_inicial + timedelta(days=random.randint(0, 365))
    preco = round(random.uniform(50, 5000), 2)
    quantidade = random.randint(1, 5)
    estoque = random.randint(0, 200)

    dados.append([
        data_venda,
        produto,
        categoria,
        preco,
        quantidade,
        estoque
    ])

df = pd.DataFrame(dados, columns=[
    "data_vendas",
    "produto",
    "categoria",
    "preco_unitario",
    "quantidade_vendida",
    "estoque"
])

df.to_csv("dados/vendas.csv", index=False)

print("CSV criado com sucesso!")
