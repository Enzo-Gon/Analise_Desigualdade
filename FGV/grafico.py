import pandas as pd
import matplotlib.pyplot as plt
import io

# Dados do CSV como string
dados_csv = """data,valor
2018-01-01,25.98
2018-02-01,26.56
2018-03-01,25.88
2018-04-01,25.61
2018-05-01,24.64
2018-06-01,24.31
2018-07-01,24.14
2018-08-01,24.1
2018-09-01,24.09
2018-10-01,24.38
2018-11-01,24.37
2018-12-01,23.05
2019-01-01,24.46
2019-02-01,24.79
2019-03-01,25.07
2019-04-01,25.13
2019-05-01,24.96
2019-06-01,24.85
2019-07-01,24.74
2019-08-01,24.85
2019-09-01,24.07
2019-10-01,23.58
2019-11-01,23.66
2019-12-01,22.66
2020-01-01,23.17
2020-02-01,23.14
2020-03-01,22.76
2020-04-01,21.37
2020-05-01,20.54
2020-06-01,19.14
2020-07-01,18.91
2020-08-01,18.49
2020-09-01,17.95
2020-10-01,18.52
2020-11-01,18.39
2020-12-01,18.24
2021-01-01,19.9
2021-02-01,19.62
2021-03-01,19.79
2021-04-01,20.26
2021-05-01,19.79
2021-06-01,19.92
2021-07-01,20.3
2021-08-01,20.97
2021-09-01,21.46
2021-10-01,22.93
2021-11-01,23.95
2021-12-01,24.26
2022-01-01,25.24
2022-02-01,25.63
2022-03-01,26.55
2022-04-01,27.47
2022-05-01,27.43
2022-06-01,27.89
2022-07-01,29.25
2022-08-01,28.63
2022-09-01,28.6
2022-10-01,29.71
2022-11-01,30.55
2022-12-01,29.68
2023-01-01,30.54
2023-02-01,30.48
2023-03-01,30.99
2023-04-01,31.62
2023-05-01,31.63
2023-06-01,30.84
2023-07-01,30.43
2023-08-01,29.91
2023-09-01,29.66
2023-10-01,29.24
2023-11-01,29.01
2023-12-01,28.13
2024-01-01,27.99
2024-02-01,27.84
2024-03-01,28.13
2024-04-01,27.86
2024-05-01,27.74
2024-06-01,27.81
2024-07-01,27.74
2024-08-01,27.59
2024-09-01,27.48
2024-10-01,27.93
2024-11-01,28.44
2024-12-01,28.5"""

# Ler os dados diretamente da string
df = pd.read_csv(io.StringIO(dados_csv), parse_dates=['data'])
df = df.sort_values('data')

print("Dados carregados diretamente do código!")
print(f"Período: {df['data'].min().strftime('%Y-%m-%d')} a {df['data'].max().strftime('%Y-%m-%d')}")

# Criar gráfico
plt.figure(figsize=(14, 8))
plt.plot(df['data'], df['valor'], linewidth=2.5, marker='o', markersize=4, color='blue')
plt.title('Evolução do Crédito Total (2018-2024)', fontsize=16, fontweight='bold')
plt.xlabel('Data', fontsize=12)
plt.ylabel('Valor (R$ Trilhões)', fontsize=12)
plt.grid(True, alpha=0.3)

# Destacar mínimo e máximo
min_idx = df['valor'].idxmin()
max_idx = df['valor'].idxmax()

plt.scatter(df.loc[min_idx, 'data'], df.loc[min_idx, 'valor'], color='red', s=100, zorder=5)
plt.scatter(df.loc[max_idx, 'data'], df.loc[max_idx, 'valor'], color='green', s=100, zorder=5)

plt.text(df.loc[min_idx, 'data'], df.loc[min_idx, 'valor'] - 0.5, 
         f'Mín: R$ {df.loc[min_idx, "valor"]:.1f}T', ha='center', color='red')
plt.text(df.loc[max_idx, 'data'], df.loc[max_idx, 'valor'] + 0.5, 
         f'Máx: R$ {df.loc[max_idx, "valor"]:.1f}T', ha='center', color='green')

plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Estatísticas
print(f"\nValor mínimo: R$ {df['valor'].min():.2f} trilhões")
print(f"Valor máximo: R$ {df['valor'].max():.2f} trilhões")
print(f"Variação total: {((df['valor'].iloc[-1] / df['valor'].iloc[0]) - 1) * 100:.2f}%")
