import pandas as pd

# Dados de exemplo para o ranking
dados = {
    'CLIENTE': [
        'DIEGO SILVA',
        'ANA SOUZA', 
        'CARLOS LIMA',
        'BEATRIZ REIS',
        'FERNANDA COSTA',
        'LUCAS SANTOS',
        'JULIANA ALVES',
        'RODRIGO PEREIRA',
        'MARIANA OLIVEIRA',
        'GUSTAVO ROCHA',
        'PATRICIA GOMES',
        'RAFAEL MENDES'
    ],
    'INDICAÇÕES': [25, 20, 18, 15, 12, 10, 8, 7, 5, 4, 3, 2]
}

df = pd.DataFrame(dados)
df.to_excel('ranking.xlsx', index=False)
print('✅ Arquivo ranking.xlsx criado com sucesso!')
print(f'📊 Total de clientes: {len(df)}')
print(f'📈 Total de indicações: {df["INDICAÇÕES"].sum()}')
