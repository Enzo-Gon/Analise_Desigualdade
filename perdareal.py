import pandas as pd
import numpy as np
import os

# Carregar dados
ipea = pd.read_csv("FGV\\resumo_estatistico_anual.csv")  # colunas: ANO, IPCA_VARIACAO_ANUAL
classes = pd.read_csv("FGV\\distribuicao_classes_sociais.csv")  # colunas: classe_social, renda_media_mensal
print(ipea.columns)
print(ipea.head())

# Filtrar período de interesse
ipea = ipea[(ipea['ANO'] >= 2018) & (ipea['ANO'] <= 2024)]

# Transformar inflação para decimal
ipea['inflacao_dec'] = ipea['IPCA_VARIACAO_ANUAL'] / 100

# CORREÇÃO: Calcular fator acumulado CORRETO (base 2018 = 1)
ipea = ipea.sort_values('ANO')
ipea['fator_acumulado'] = (1 + ipea['inflacao_dec']).cumprod()

# Expandindo as classes para ter um valor por ano
df = classes.assign(key=1).merge(ipea.assign(key=1), on='key').drop('key', axis=1)

# Renda real corrigida para cada ano (usando 2018 como base)
df['renda_real'] = df['renda_media_mensal'] / df['fator_acumulado']

# Formatar tabela final
final = df[['ANO','classe_social','renda_media_mensal','renda_real','IPCA_VARIACAO_ANUAL']]
print(final.head(20))

# Salvar o CSV no caminho especificado
caminho_csv = r"C:\Users\Pedro\Documents\coisas que o FDP DO ENZO QUER\csv\analise_classes_sociais.csv"
final.to_csv(caminho_csv, index=False)

print(f"Arquivo salvo em: {caminho_csv}")

# Análise adicional: mostrar a perda real de renda por classe
print("\n--- ANÁLISE DA PERDA REAL DE RENDA ---")
base_2018 = final[final['ANO'] == 2018][['classe_social', 'renda_real']].rename(columns={'renda_real': 'renda_real_2018'})
analise = final.merge(base_2018, on='classe_social')
analise['perda_percentual'] = ((analise['renda_real'] - analise['renda_real_2018']) / analise['renda_real_2018']) * 100

# Mostrar resultados para 2024
print("\nPerda real de renda em 2024 (base 2018):")
print(analise[analise['ANO'] == 2024][['classe_social', 'renda_real', 'perda_percentual']].round(2))