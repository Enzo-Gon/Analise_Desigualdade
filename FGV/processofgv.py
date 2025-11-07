import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os

# Configurar o diretório de trabalho
diretorio_base = r"C:\Users\Pedro\Documents\coisas que o FDP do ENZO quer\data\raw\fgv"
os.makedirs(diretorio_base, exist_ok=True)

# Configuração para visualização
plt.style.use('default')
sns.set_palette("husl")

# 1. CARREGAR OS DADOS
print("=== CARREGANDO DADOS ===")

# Caminhos completos dos arquivos
caminho_serie = os.path.join(diretorio_base, "serie_temporal_desigualdade.csv")
caminho_classes = os.path.join(diretorio_base, "distribuicao_classes_sociais.csv")
caminho_links = os.path.join(diretorio_base, "metadados_links.csv")

# Carregar dados
try:
    df_classes = pd.read_csv(caminho_classes)
    df_links = pd.read_csv(caminho_links)
    df_serie = pd.read_csv(caminho_serie)
    print("Todos os arquivos carregados com sucesso!")
except FileNotFoundError as e:
    print(f" Erro ao carregar arquivos: {e}")
    print("Verifique se os arquivos estão no diretório correto:")
    print(f"Diretório: {diretorio_base}")
    exit()

print(f"Classes sociais: {df_classes.shape}")
print(f"Metadados links: {df_links.shape}")
print(f"Série temporal: {df_serie.shape}")

# 2. LIMPEZA E PROCESSAMENTO DOS DADOS

# 2.1 Limpar dados de classes sociais
print("\n=== LIMPEZA - CLASSES SOCIAIS ===")
df_classes_clean = df_classes.copy()
df_classes_clean['percentual_populacao'] = df_classes_clean['percentual_populacao'].astype(float)
df_classes_clean['renda_media_mensal'] = df_classes_clean['renda_media_mensal'].astype(float)

# Verificar consistência dos percentuais
total_percentual = df_classes_clean['percentual_populacao'].sum()
print(f"Total percentual população: {total_percentual}%")
if abs(total_percentual - 100) > 1:
    print("Atenção: Soma dos percentuais difere significativamente de 100%")

# 2.2 Limpar dados de links (remover duplicatas)
print("\n=== LIMPEZA - METADADOS LINKS ===")
df_links_clean = df_links.drop_duplicates().reset_index(drop=True)
print(f"Links após remover duplicatas: {df_links_clean.shape}")

# 2.3 Limpar série temporal
print("\n=== LIMPEZA - SÉRIE TEMPORAL ===")
df_serie_clean = df_serie.copy()

# Verificar valores nulos
print("Valores nulos na série temporal:")
print(df_serie_clean.isnull().sum())

# Converter para tipos numéricos (caso necessário)
colunas_numericas = ['pobreza_percentual', 'extrema_pobreza_percentual', 'indice_gini', 
                     'renda_media_50pobres', 'renda_media_10ricos', 'classe_media_percentual']
for coluna in colunas_numericas:
    df_serie_clean[coluna] = pd.to_numeric(df_serie_clean[coluna], errors='coerce')

# 3. ANÁLISE EXPLORATÓRIA

# 3.1 Análise da distribuição de classes sociais
print("\n=== ANÁLISE - DISTRIBUIÇÃO CLASSES SOCIAIS ===")
print("\nDistribuição por classe social:")
for _, row in df_classes_clean.iterrows():
    print(f"{row['classe_social']}: {row['percentual_populacao']}% - R$ {row['renda_media_mensal']:,.0f}")

# Calcular estatísticas
populacao_vulneravel = df_classes_clean.loc[
    df_classes_clean['classe_social'].isin(['Extrema Pobreza', 'Pobreza', 'Vulnerabilidade']), 
    'percentual_populacao'
].sum()

populacao_media_alta = df_classes_clean.loc[
    df_classes_clean['classe_social'].isin(['Classe Média', 'Classe Média Alta', 'Classe Alta']), 
    'percentual_populacao'
].sum()

print(f"\n População vulnerável: {populacao_vulneravel:.1f}%")
print(f"População classe média e alta: {populacao_media_alta:.1f}%")

# 3.2 Análise da série temporal
print("\n=== ANÁLISE - SÉRIE TEMPORAL ===")

# Calcular variações
df_serie_clean['var_pobreza'] = df_serie_clean['pobreza_percentual'].pct_change() * 100
df_serie_clean['var_extrema_pobreza'] = df_serie_clean['extrema_pobreza_percentual'].pct_change() * 100
df_serie_clean['var_classe_media'] = df_serie_clean['classe_media_percentual'].pct_change() * 100

# Estatísticas da série
print(f"Período analisado: {df_serie_clean['ano'].min()} - {df_serie_clean['ano'].max()}")
print(f"Pobreza: {df_serie_clean['pobreza_percentual'].min():.1f}% a {df_serie_clean['pobreza_percentual'].max():.1f}%")
print(f"Extrema pobreza: {df_serie_clean['extrema_pobreza_percentual'].min():.1f}% a {df_serie_clean['extrema_pobreza_percentual'].max():.1f}%")
print(f"Classe média: {df_serie_clean['classe_media_percentual'].min():.1f}% a {df_serie_clean['classe_media_percentual'].max():.1f}%")

# 3.3 Análise de desigualdade
print("\n=== ANÁLISE - DESIGUALDADE ===")

# Calcular razão entre renda dos 10% mais ricos e 50% mais pobres
df_serie_clean['razao_ricos_pobres'] = df_serie_clean['renda_media_10ricos'] / df_serie_clean['renda_media_50pobres']

print("\nRazão entre renda dos 10% mais ricos e 50% mais pobres:")
for ano in [2012, 2019, 2020, 2023]:
    if ano in df_serie_clean['ano'].values:
        razao = df_serie_clean.loc[df_serie_clean['ano'] == ano, 'razao_ricos_pobres'].values[0]
        print(f"{ano}: {razao:.1f} vezes")

# 4. VISUALIZAÇÕES

print("\n=== GERANDO VISUALIZAÇÕES ===")

# Criar diretório para imagens
diretorio_imagens = os.path.join(diretorio_base, "imagens")
os.makedirs(diretorio_imagens, exist_ok=True)

plt.figure(figsize=(15, 12))

# 4.1 Gráfico de distribuição de classes sociais
plt.subplot(2, 2, 1)
colors = ['#ff6b6b', '#ffa726', '#ffee58', '#90caf9', '#42a5f5', '#1e88e5', '#0d47a1']
plt.pie(df_classes_clean['percentual_populacao'], labels=df_classes_clean['classe_social'], 
        autopct='%1.1f%%', colors=colors, startangle=90)
plt.title('Distribuição da População por Classe Social')

# 4.2 Evolução temporal da pobreza
plt.subplot(2, 2, 2)
plt.plot(df_serie_clean['ano'], df_serie_clean['pobreza_percentual'], marker='o', label='Pobreza', linewidth=2)
plt.plot(df_serie_clean['ano'], df_serie_clean['extrema_pobreza_percentual'], marker='s', label='Extrema Pobreza', linewidth=2)
plt.xlabel('Ano')
plt.ylabel('Percentual (%)')
plt.title('Evolução da Pobreza e Extrema Pobreza')
plt.legend()
plt.grid(True, alpha=0.3)

# 4.3 Evolução da classe média e desigualdade
plt.subplot(2, 2, 3)
plt.plot(df_serie_clean['ano'], df_serie_clean['classe_media_percentual'], marker='o', color='green', label='Classe Média', linewidth=2)
plt.xlabel('Ano')
plt.ylabel('Percentual (%)')
plt.title('Evolução da Classe Média')
plt.grid(True, alpha=0.3)

# 4.4 Índice de Gini
plt.subplot(2, 2, 4)
plt.plot(df_serie_clean['ano'], df_serie_clean['indice_gini'], marker='o', color='red', linewidth=2)
plt.xlabel('Ano')
plt.ylabel('Índice de Gini')
plt.title('Evolução da Desigualdade (Índice de Gini)')
plt.grid(True, alpha=0.3)

plt.tight_layout()

# Salvar gráfico
caminho_grafico = os.path.join(diretorio_imagens, "analise_desigualdade.png")
plt.savefig(caminho_grafico, dpi=300, bbox_inches='tight')
plt.show()

# 5. ANÁLISE DETALHADA DO IMPACTO DA PANDEMIA
print("\n=== ANÁLISE DO IMPACTO DA PANDEMIA (2020) ===")
df_antes_pandemia = df_serie_clean[df_serie_clean['ano'] == 2019].iloc[0]
df_pandemia = df_serie_clean[df_serie_clean['ano'] == 2020].iloc[0]
df_pos_pandemia = df_serie_clean[df_serie_clean['ano'] == 2023].iloc[0]

print(f"Variação da pobreza 2019-2020: +{df_pandemia['pobreza_percentual'] - df_antes_pandemia['pobreza_percentual']:.1f}pp")
print(f"Variação da extrema pobreza 2019-2020: +{df_pandemia['extrema_pobreza_percentual'] - df_antes_pandemia['extrema_pobreza_percentual']:.1f}pp")
print(f"Recuperação da pobreza 2020-2023: -{df_pandemia['pobreza_percentual'] - df_pos_pandemia['pobreza_percentual']:.1f}pp")

# 6. EXPORTAR DADOS PROCESSADOS
print("\n=== EXPORTANDO DADOS PROCESSADOS ===")

# Criar diretório para dados processados
diretorio_processado = os.path.join(diretorio_base, "processado")
os.makedirs(diretorio_processado, exist_ok=True)

# Salvar dados limpos
df_classes_clean.to_csv(os.path.join(diretorio_processado, 'classes_sociais_processado.csv'), index=False, encoding='utf-8')
df_serie_clean.to_csv(os.path.join(diretorio_processado, 'serie_temporal_processado.csv'), index=False, encoding='utf-8')
df_links_clean.to_csv(os.path.join(diretorio_processado, 'links_processado.csv'), index=False, encoding='utf-8')

# Criar relatório resumido
caminho_relatorio = os.path.join(diretorio_processado, 'relatorio_analise.txt')
with open(caminho_relatorio, 'w', encoding='utf-8') as f:
    f.write("RELATÓRIO DE ANÁLISE - DESIGUALDADE SOCIAL (FGV)\n")
    f.write("=" * 60 + "\n\n")
    f.write(f"Data da análise: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n")
    f.write(f"Diretório: {diretorio_base}\n\n")
    
    f.write("DISTRIBUIÇÃO DE CLASSES SOCIAIS:\n")
    f.write("-" * 40 + "\n")
    for _, row in df_classes_clean.iterrows():
        f.write(f"- {row['classe_social']}: {row['percentual_populacao']}% (R$ {row['renda_media_mensal']:,.0f})\n")
    
    f.write(f"\nRESUMO:\n")
    f.write(f"- População em situação vulnerável: {populacao_vulneravel:.1f}%\n")
    f.write(f"- População classe média/alta: {populacao_media_alta:.1f}%\n\n")
    
    f.write("EVOLUÇÃO TEMPORAL (2012-2023):\n")
    f.write("-" * 40 + "\n")
    f.write(f"- Pobreza: {df_serie_clean['pobreza_percentual'].iloc[0]:.1f}% → {df_serie_clean['pobreza_percentual'].iloc[-1]:.1f}%\n")
    f.write(f"- Extrema pobreza: {df_serie_clean['extrema_pobreza_percentual'].iloc[0]:.1f}% → {df_serie_clean['extrema_pobreza_percentual'].iloc[-1]:.1f}%\n")
    f.write(f"- Classe média: {df_serie_clean['classe_media_percentual'].iloc[0]:.1f}% → {df_serie_clean['classe_media_percentual'].iloc[-1]:.1f}%\n")
    f.write(f"- Desigualdade (Gini): {df_serie_clean['indice_gini'].iloc[0]:.3f} → {df_serie_clean['indice_gini'].iloc[-1]:.3f}\n\n")
    
    f.write("IMPACTO DA PANDEMIA:\n")
    f.write("-" * 40 + "\n")
    f.write(f"- Aumento da pobreza (2019-2020): +{df_pandemia['pobreza_percentual'] - df_antes_pandemia['pobreza_percentual']:.1f}pp\n")
    f.write(f"- Aumento da extrema pobreza (2019-2020): +{df_pandemia['extrema_pobreza_percentual'] - df_antes_pandemia['extrema_pobreza_percentual']:.1f}pp\n")
    f.write(f"- Recuperação (2020-2023): -{df_pandemia['pobreza_percentual'] - df_pos_pandemia['pobreza_percentual']:.1f}pp\n")

print(" Análise concluída!")
print(f" Dados salvos em: {diretorio_processado}")
print(" Gráficos gerados e salvos")
print(" Relatório criado")
print("\nArquivos gerados:")
print(f"   - {os.path.join(diretorio_processado, 'classes_sociais_processado.csv')}")
print(f"   - {os.path.join(diretorio_processado, 'serie_temporal_processado.csv')}") 
print(f"   - {os.path.join(diretorio_processado, 'links_processado.csv')}")
print(f"   - {os.path.join(diretorio_processado, 'relatorio_analise.txt')}")
print(f"   - {caminho_grafico}")