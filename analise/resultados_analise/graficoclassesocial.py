import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Dados do distribuicao_classes_sociais.csv
distribuicao_classes_data = {
    'classe_social': ['Extrema Pobreza', 'Pobreza', 'Vulnerabilidade', 'Classe Média Baixa', 'Classe Média', 'Classe Média Alta', 'Classe Alta'],
    'percentual_populacao': [7.5, 11.4, 21.2, 25.8, 23.1, 7.3, 3.7],
    'renda_media_mensal': [330, 990, 1980, 3960, 9240, 18480, 45000],
    'faixa_renda_sm': ['Até 0,25 SM', '0,25-1 SM', '1-2 SM', '2-4 SM', '4-10 SM', '10-20 SM', 'Acima de 20 SM']
}

# Criar DataFrame
distribuicao_classes = pd.DataFrame(distribuicao_classes_data)

print("📊 Dados carregados com sucesso!")
print("\nTabela de Classes Sociais:")
print(distribuicao_classes.to_string(index=False))

# Configuração do estilo dos gráficos
plt.style.use('default')
cores = ['#FF6B6B', '#FFA726', '#FFD54F', '#AED581', '#4FC3F7', '#7986CB', '#BA68C8']

# Criar figura com dois subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))

# GRÁFICO 1: PIZZA - Percentual da População por Classe Social
explode = (0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05)  # Destacar cada fatia

wedges, texts, autotexts = ax1.pie(
    distribuicao_classes['percentual_populacao'],
    labels=distribuicao_classes['classe_social'],
    autopct='%1.1f%%',
    startangle=90,
    colors=cores,
    explode=explode,
    shadow=True
)

# Melhorar a aparência do gráfico de pizza
for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontweight('bold')
    autotext.set_fontsize(9)

ax1.set_title('DISTRIBUIÇÃO DA POPULAÇÃO POR CLASSE SOCIAL\n(% da população)', 
              fontsize=14, fontweight='bold', pad=20)

# GRÁFICO 2: BARRAS - Renda Média por Classe Social
bars = ax2.bar(distribuicao_classes['classe_social'], 
               distribuicao_classes['renda_media_mensal'], 
               color=cores, alpha=0.8, edgecolor='black', linewidth=0.5)

ax2.set_title('RENDA MÉDIA MENSAL POR CLASSE SOCIAL\n(Valores em R$)', 
              fontsize=14, fontweight='bold', pad=20)
ax2.set_ylabel('Renda Média Mensal (R$)', fontsize=12)
ax2.set_xlabel('Classe Social', fontsize=12)

# Rotacionar labels do eixo x para melhor visualização
ax2.set_xticklabels(distribuicao_classes['classe_social'], rotation=45, ha='right')

# Adicionar valores nas barras
for bar in bars:
    height = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2., height + 100,
             f'R$ {height:,.0f}'.replace(',', '.'),
             ha='center', va='bottom', fontweight='bold', fontsize=9)

# Formatar eixo Y para melhor visualização
ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'R$ {x:,.0f}'.replace(',', '.')))
ax2.grid(True, alpha=0.3, axis='y')

# Ajustar layout
plt.tight_layout()

# Salvar gráfico
plt.savefig('distribuicao_classes_sociais.png', dpi=300, bbox_inches='tight')
plt.show()

# GRÁFICO 3: GRÁFICO DE BARRAS HORIZONTAIS (alternativo)
plt.figure(figsize=(14, 8))

# Ordenar por renda para melhor visualização
df_ordenado = distribuicao_classes.sort_values('renda_media_mensal', ascending=True)

bars_h = plt.barh(df_ordenado['classe_social'], df_ordenado['renda_media_mensal'], 
                  color=cores, alpha=0.8, edgecolor='black', linewidth=0.5)

plt.title('RENDA MÉDIA MENSAL POR CLASSE SOCIAL\n(Ordenado por valor)', 
          fontsize=16, fontweight='bold', pad=20)
plt.xlabel('Renda Média Mensal (R$)', fontsize=12)
plt.ylabel('Classe Social', fontsize=12)

# Adicionar valores nas barras horizontais
for bar in bars_h:
    width = bar.get_width()
    plt.text(width + 500, bar.get_y() + bar.get_height()/2,
             f'R$ {width:,.0f}'.replace(',', '.'),
             ha='left', va='center', fontweight='bold', fontsize=10)

plt.grid(True, alpha=0.3, axis='x')
plt.tight_layout()
plt.savefig('renda_media_horizontal.png', dpi=300, bbox_inches='tight')
plt.show()

# ESTATÍSTICAS DESCRITIVAS
print("\n" + "="*60)
print("📈 ESTATÍSTICAS DESCRITIVAS")
print("="*60)

total_populacao = distribuicao_classes['percentual_populacao'].sum()
populacao_media_baixa = distribuicao_classes.loc[distribuicao_classes['classe_social'].isin(['Extrema Pobreza', 'Pobreza', 'Vulnerabilidade']), 'percentual_populacao'].sum()
populacao_classe_media = distribuicao_classes.loc[distribuicao_classes['classe_social'].isin(['Classe Média Baixa', 'Classe Média', 'Classe Média Alta']), 'percentual_populacao'].sum()

print(f"📊 Distribuição da População:")
print(f"   • Extrema Pobreza + Pobreza + Vulnerabilidade: {populacao_media_baixa:.1f}%")
print(f"   • Classe Média (Baixa + Média + Alta): {populacao_classe_media:.1f}%")
print(f"   • Classe Alta: {distribuicao_classes.loc[distribuicao_classes['classe_social'] == 'Classe Alta', 'percentual_populacao'].values[0]:.1f}%")
print(f"   • Total: {total_populacao:.1f}%")

print(f"\n💰 Faixas de Renda:")
renda_min = distribuicao_classes['renda_media_mensal'].min()
renda_max = distribuicao_classes['renda_media_mensal'].max()
diferenca_absoluta = renda_max - renda_min
diferenca_relativa = (renda_max / renda_min)

print(f"   • Menor renda média: R$ {renda_min:,.0f}".replace(',', '.'))
print(f"   • Maior renda média: R$ {renda_max:,.0f}".replace(',', '.'))
print(f"   • Diferença absoluta: R$ {diferenca_absoluta:,.0f}".replace(',', '.'))
print(f"   • Classe Alta ganha {diferenca_relativa:.1f}x mais que Extrema Pobreza")

print(f"\n🎯 Concentração de Renda:")
# Calcular participação na renda total
renda_total_ponderada = (distribuicao_classes['percentual_populacao'] * distribuicao_classes['renda_media_mensal']).sum()

print("   Participação na renda total:")
for _, row in distribuicao_classes.iterrows():
    participacao = (row['percentual_populacao'] * row['renda_media_mensal']) / renda_total_ponderada * 100
    print(f"   • {row['classe_social']:20}: {participacao:.1f}%")

print(f"\n✅ Gráficos salvos como 'distribuicao_classes_sociais.png' e 'renda_media_horizontal.png'")