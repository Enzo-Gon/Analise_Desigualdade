import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Configurar estilo dos gráficos
plt.style.use('seaborn-v0_8')

# Carregar o CSV gerado anteriormente
caminho_csv = r"C:\Users\Pedro\Documents\coisas que o FDP DO ENZO QUER\csv\analise_classes_sociais.csv"
df = pd.read_csv(caminho_csv)

# FILTRAR FORA A CLASSE ALTA
df_sem_alta = df[df['classe_social'] != 'Classe Alta']

# 1. GRÁFICO DA EVOLUÇÃO DA RENDA REAL POR CLASSE SOCIAL (SEM CLASSE ALTA)
plt.figure(figsize=(14, 8))

# Definir cores únicas e distintas para cada classe (sem a classe alta)
cores_classes = {
    'Extrema Pobreza': '#e74c3c',      # Vermelho forte
    'Pobreza': '#e67e22',              # Laranja
    'Vulnerabilidade': '#f1c40f',      # Amarelo
    'Classe Média Baixa': '#2ecc71',   # Verde
    'Classe Média': '#3498db',         # Azul
    'Classe Média Alta': '#9b59b6'     # Roxo
}

classes_ordenadas = ['Extrema Pobreza', 'Pobreza', 'Vulnerabilidade', 'Classe Média Baixa', 
                    'Classe Média', 'Classe Média Alta']

for classe in classes_ordenadas:
    dados_classe = df_sem_alta[df_sem_alta['classe_social'] == classe]
    plt.plot(dados_classe['ANO'], dados_classe['renda_real'], 
             marker='o', linewidth=2.5, label=classe, markersize=6,
             color=cores_classes[classe])

plt.title('EVOLUÇÃO DA RENDA REAL POR CLASSE SOCIAL (2018-2024)\nPoder de Compra em Valores de 2018 - Sem Classe Alta', 
          fontsize=16, fontweight='bold', pad=20)
plt.xlabel('Ano', fontsize=12)
plt.ylabel('Renda Real (R$)', fontsize=12)
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True, alpha=0.3)
plt.xticks(df_sem_alta['ANO'].unique())

# CONFIGURAR ESCALA DO EIXO Y DE 500 EM 500
max_renda = df_sem_alta['renda_real'].max()
plt.yticks(np.arange(0, max_renda + 1000, 500))
plt.ylim(bottom=0)  # Garantir que comece do zero

plt.tight_layout()
plt.savefig(r"C:\Users\Pedro\Documents\coisas que o FDP DO ENZO QUER\csv\evolucao_renda_real_sem_alta.png", 
            dpi=300, bbox_inches='tight')
plt.show()

# 2. GRÁFICO DE PERDA PERCENTUAL DA RENDA (2018 vs 2024) - SEM CLASSE ALTA
plt.figure(figsize=(12, 8))

# Calcular perda percentual
base_2018 = df_sem_alta[df_sem_alta['ANO'] == 2018][['classe_social', 'renda_real']].rename(columns={'renda_real': 'renda_2018'})
dados_2024 = df_sem_alta[df_sem_alta['ANO'] == 2024][['classe_social', 'renda_real']].rename(columns={'renda_real': 'renda_2024'})
analise_perda = base_2018.merge(dados_2024, on='classe_social')
analise_perda['perda_percentual'] = ((analise_perda['renda_2024'] - analise_perda['renda_2018']) / analise_perda['renda_2018']) * 100

# Ordenar por perda
analise_perda = analise_perda.sort_values('perda_percentual')

# Aplicar as mesmas cores do gráfico anterior
cores_barras = [cores_classes[classe] for classe in analise_perda['classe_social']]
bars = plt.barh(analise_perda['classe_social'], analise_perda['perda_percentual'], 
                color=cores_barras, alpha=0.8)

# Adicionar valores nas barras
for bar, valor in zip(bars, analise_perda['perda_percentual']):
    plt.text(bar.get_width() + (0.5 if valor >= 0 else -1), 
             bar.get_y() + bar.get_height()/2, 
             f'{valor:.1f}%', 
             ha='left' if valor >= 0 else 'right', 
             va='center', 
             fontweight='bold')

plt.axvline(x=0, color='black', linestyle='-', alpha=0.8)
plt.title('PERDA/GANHO REAL DE RENDA (2018-2024)\nVariação Percentual do Poder de Compra - Sem Classe Alta', 
          fontsize=16, fontweight='bold', pad=20)
plt.xlabel('Variação Percentual (%)', fontsize=12)
plt.grid(True, alpha=0.3, axis='x')
plt.tight_layout()
plt.savefig(r"C:\Users\Pedro\Documents\coisas que o FDP DO ENZO QUER\csv\perda_renda_sem_alta.png", 
            dpi=300, bbox_inches='tight')
plt.show()

# 3. GRÁFICO DE COMPARAÇÃO RENDA NOMINAL vs RENDA REAL (2024) - SEM CLASSE ALTA
plt.figure(figsize=(14, 8))

dados_2024 = df_sem_alta[df_sem_alta['ANO'] == 2024].sort_values('renda_media_mensal')

x = np.arange(len(dados_2024))
width = 0.35

# Aplicar cores consistentes
cores_nominal = [cores_classes[classe] for classe in dados_2024['classe_social']]
cores_real = [cores_classes[classe] for classe in dados_2024['classe_social']]

bars_nominal = plt.bar(x - width/2, dados_2024['renda_media_mensal'], width, 
                       label='Renda Nominal', alpha=0.8, color=cores_nominal)
bars_real = plt.bar(x + width/2, dados_2024['renda_real'], width, 
                    label='Renda Real (Valores 2018)', alpha=0.6, color=cores_real, hatch='//')

plt.xlabel('Classe Social', fontsize=12)
plt.ylabel('Renda Mensal (R$)', fontsize=12)
plt.title('COMPARAÇÃO: RENDA NOMINAL vs RENDA REAL EM 2024\nEfeito da Inflação no Poder de Compra - Sem Classe Alta', 
          fontsize=16, fontweight='bold', pad=20)
plt.xticks(x, dados_2024['classe_social'], rotation=45, ha='right')
plt.legend()
plt.grid(True, alpha=0.3, axis='y')

# CONFIGURAR ESCALA DO EIXO Y DE 1000 EM 1000
max_renda_nominal = dados_2024['renda_media_mensal'].max()
plt.yticks(np.arange(0, max_renda_nominal + 1000, 1000))

# Adicionar valores nas barras
for i, (nominal, real, classe) in enumerate(zip(dados_2024['renda_media_mensal'], 
                                               dados_2024['renda_real'], 
                                               dados_2024['classe_social'])):
    plt.text(i - width/2, nominal + 200, f'R$ {nominal:,.0f}', 
            ha='center', va='bottom', fontsize=9)
    plt.text(i + width/2, real + 200, f'R$ {real:,.0f}', 
            ha='center', va='bottom', fontsize=9)

plt.tight_layout()
plt.savefig(r"C:\Users\Pedro\Documents\coisas que o FDP DO ENZO QUER\csv\nominal_vs_real_2024_sem_alta.png", 
            dpi=300, bbox_inches='tight')
plt.show()

# 4. GRÁFICO DE HEATMAP - VARIAÇÃO POR CLASSE E ANO (SEM CLASSE ALTA)
plt.figure(figsize=(12, 6))

# Preparar dados para heatmap
heatmap_data = df_sem_alta.pivot_table(values='renda_real', index='classe_social', columns='ANO')
heatmap_variacao = (heatmap_data.div(heatmap_data[2018], axis=0) - 1) * 100

sns.heatmap(heatmap_variacao, annot=True, fmt='.1f', cmap='RdYlGn_r', center=0,
            cbar_kws={'label': 'Variação Percentual (%) vs 2018'})

plt.title('MAPA DE CALOR - VARIAÇÃO DO PODER DE COMPRA (2018-2024)\nSem Classe Alta - (2018 = 0%)', 
          fontsize=16, fontweight='bold', pad=20)
plt.xlabel('Ano')
plt.ylabel('Classe Social')
plt.tight_layout()
plt.savefig(r"C:\Users\Pedro\Documents\coisas que o FDP DO ENZO QUER\csv\heatmap_variacao_sem_alta.png", 
            dpi=300, bbox_inches='tight')
plt.show()

print("📊 Todos os gráficos SEM CLASSE ALTA foram salvos!")
print("📍 Gráficos gerados:")
print("   • evolucao_renda_real_sem_alta.png - Evolução sem Classe Alta")
print("   • perda_renda_sem_alta.png - Perda percentual sem Classe Alta")
print("   • nominal_vs_real_2024_sem_alta.png - Comparação sem Classe Alta")
print("   • heatmap_variacao_sem_alta.png - Mapa de calor sem Classe Alta")