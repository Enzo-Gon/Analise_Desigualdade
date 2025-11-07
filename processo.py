import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
import os
warnings.filterwarnings('ignore')

# Configuração para melhor visualização
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

# Diretório específico onde estão os arquivos
DIRETORIO_BASE = r"C:\Users\Pedro\Documents\coisas que o FDP do ENZO quer\IPEA\data\raw\ipea"

def verificar_arquivos():
    """Verifica se os arquivos existem no diretório específico"""
    print(f"Verificando arquivos no diretório: {DIRETORIO_BASE}")
    
    # Verificar se o diretório existe
    if not os.path.exists(DIRETORIO_BASE):
        print(f"❌ Diretório não encontrado: {DIRETORIO_BASE}")
        return {}
    
    # Listar todos os arquivos CSV no diretório
    arquivos_csv = [f for f in os.listdir(DIRETORIO_BASE) if f.endswith('.csv')]
    print("Arquivos CSV encontrados no diretório:")
    for arquivo in arquivos_csv:
        print(f"  - {arquivo}")
    
    # Arquivos necessários
    arquivos_necessarios = {
        'inflacao': 'inflacao_ipca_raw.csv',
        'desocupacao': 'taxa_desocupacao_raw.csv'
    }
    
    arquivos_encontrados = {}
    
    for tipo, nome_arquivo in arquivos_necessarios.items():
        caminho_arquivo = os.path.join(DIRETORIO_BASE, nome_arquivo)
        if os.path.exists(caminho_arquivo):
            arquivos_encontrados[tipo] = caminho_arquivo
            print(f"✓ {tipo.upper()}: {nome_arquivo} - ENCONTRADO")
        else:
            print(f"✗ {tipo.upper()}: {nome_arquivo} - NÃO ENCONTRADO")
    
    return arquivos_encontrados

def carregar_dados_raw():
    """Carrega os dados dos arquivos CSV raw do diretório específico"""
    print("\nCarregando dados raw...")
    
    # Verificar arquivos
    arquivos_encontrados = verificar_arquivos()
    
    if len(arquivos_encontrados) < 2:
        print("\n❌ ERRO: Arquivos necessários não encontrados!")
        print(f"Diretório verificado: {DIRETORIO_BASE}")
        print("Nomes corretos dos arquivos:")
        print("  - inflacao_ipca_raw.csv")
        print("  - taxa_desocupacao_raw.csv")
        
        # Tentar encontrar arquivos com nomes similares
        print("\n🔍 Procurando arquivos com nomes similares...")
        if os.path.exists(DIRETORIO_BASE):
            todos_arquivos = os.listdir(DIRETORIO_BASE)
            for arquivo in todos_arquivos:
                if 'inflacao' in arquivo.lower() or 'ipca' in arquivo.lower():
                    print(f"  📈 Possível arquivo de inflação: {arquivo}")
                if 'desocupacao' in arquivo.lower() or 'taxa' in arquivo.lower() or 'desemprego' in arquivo.lower():
                    print(f"  👥 Possível arquivo de desocupação: {arquivo}")
        else:
            print("  Diretório não existe!")
        
        return None, None
    
    try:
        # Carregar dados de inflação
        print(f"📥 Carregando: {arquivos_encontrados['inflacao']}")
        inflacao_df = pd.read_csv(arquivos_encontrados['inflacao'])
        
        # Carregar dados de desocupação
        print(f"📥 Carregando: {arquivos_encontrados['desocupacao']}")
        desocupacao_df = pd.read_csv(arquivos_encontrados['desocupacao'])
        
        print(f"✅ Dados de inflação carregados: {inflacao_df.shape}")
        print(f"✅ Dados de desocupação carregados: {desocupacao_df.shape}")
        
        return inflacao_df, desocupacao_df
        
    except Exception as e:
        print(f"❌ Erro ao carregar arquivos: {e}")
        return None, None

def processar_inflacao(inflacao_df):
    """Processa e limpa os dados de inflação"""
    print("\n🔄 Processando dados de inflação...")
    
    # Converter coluna VALDATA para datetime
    inflacao_df['VALDATA'] = pd.to_datetime(inflacao_df['VALDATA'])
    
    # Ordenar por data
    inflacao_df = inflacao_df.sort_values('VALDATA').reset_index(drop=True)
    
    # Verificar dados
    print("✅ Datas convertidas e ordenadas")
    print(f"  📅 Período: {inflacao_df['VALDATA'].min()} até {inflacao_df['VALDATA'].max()}")
    print(f"  📊 Total de meses: {len(inflacao_df)}")
    
    # Mostrar primeiras linhas
    print(f"  👀 Primeiros valores:")
    print(f"     {inflacao_df['VALVALOR'].head(3).tolist()}")
    print(f"  👀 Últimos valores:")
    print(f"     {inflacao_df['VALVALOR'].tail(3).tolist()}")
    
    return inflacao_df

def processar_desocupacao(desocupacao_df):
    """Processa e limpa os dados de desocupação"""
    print("\n🔄 Processando dados de desocupação...")
    
    # Corrigir nome da coluna se necessário
    if 'CODIGO' in desocupacao_df.columns:
        desocupacao_df = desocupacao_df.rename(columns={'CODIGO': 'CODIGO'})
    
    # Converter coluna VALDATA para datetime
    desocupacao_df['VALDATA'] = pd.to_datetime(desocupacao_df['VALDATA'])
    
    # Ordenar por data
    desocupacao_df = desocupacao_df.sort_values('VALDATA').reset_index(drop=True)
    
    # Verificar dados
    print("✅ Datas convertidas e ordenadas")
    print(f"  📅 Período: {desocupacao_df['VALDATA'].min()} até {desocupacao_df['VALDATA'].max()}")
    print(f"  📊 Total de meses: {len(desocupacao_df)}")
    
    # Mostrar primeiras linhas
    print(f"  👀 Primeiros valores:")
    print(f"     {desocupacao_df['VALVALOR'].head(3).tolist()}")
    print(f"  👀 Últimos valores:")
    print(f"     {desocupacao_df['VALVALOR'].tail(3).tolist()}")
    
    return desocupacao_df

def filtrar_periodo_comum(inflacao_df, desocupacao_df, ano_inicio=2012):
    """Filtra os dados para o período comum entre as duas séries"""
    print(f"\n🎯 Filtrando para período comum (a partir de {ano_inicio})...")
    
    # Filtrar inflação a partir de 2012 (quando começa a desocupação)
    inflacao_filtrada = inflacao_df[inflacao_df['VALDATA'] >= f'{ano_inicio}-01-01'].copy()
    
    # Desocupação já começa em 2012
    desocupacao_filtrada = desocupacao_df.copy()
    
    print(f"✅ Inflação após filtro: {inflacao_filtrada.shape[0]} meses")
    print(f"✅ Desocupação após filtro: {desocupacao_filtrada.shape[0]} meses")
    
    return inflacao_filtrada, desocupacao_filtrada

def criar_dataset_combinado(inflacao_df, desocupacao_df):
    """Combina os dois datasets em um único DataFrame"""
    print("\n🔗 Criando dataset combinado...")
    
    # Renomear colunas para evitar conflitos
    inflacao_clean = inflacao_df[['VALDATA', 'VALVALOR']].copy()
    inflacao_clean = inflacao_clean.rename(columns={'VALVALOR': 'IPCA'})
    
    desocupacao_clean = desocupacao_df[['VALDATA', 'VALVALOR']].copy()
    desocupacao_clean = desocupacao_clean.rename(columns={'VALVALOR': 'TAXA_DESOCUPACAO'})
    
    # Combinar os datasets
    dataset_combinado = pd.merge(inflacao_clean, desocupacao_clean, on='VALDATA', how='inner')
    
    print(f"✅ Dataset combinado criado: {dataset_combinado.shape}")
    print(f"  📅 Período coberto: {dataset_combinado['VALDATA'].min()} até {dataset_combinado['VALDATA'].max()}")
    print(f"  📊 Total de observações: {len(dataset_combinado)}")
    
    return dataset_combinado

def criar_features_adicionais(dataset_combinado):
    """Cria features adicionais para análise"""
    print("\n⚙️ Criando features adicionais...")
    
    df = dataset_combinado.copy()
    
    # Garantir que VALDATA está como datetime
    df['VALDATA'] = pd.to_datetime(df['VALDATA'])
    
    # Extrair componentes de data
    df['ANO'] = df['VALDATA'].dt.year
    df['MES'] = df['VALDATA'].dt.month
    df['TRIMESTRE'] = df['VALDATA'].dt.quarter
    df['ANO_MES'] = df['VALDATA'].dt.strftime('%Y-%m')
    
    # Calcular variações mensais e anuais
    df['IPCA_VARIACAO_MENSAL'] = df['IPCA'].pct_change() * 100
    df['IPCA_VARIACAO_ANUAL'] = df['IPCA'].pct_change(12) * 100
    
    df['DESOCUPACAO_VARIACAO_MENSAL'] = df['TAXA_DESOCUPACAO'].diff()
    df['DESOCUPACAO_VARIACAO_ANUAL'] = df['TAXA_DESOCUPACAO'].diff(12)
    
    # Classificar períodos por nível de inflação
    conditions = [
        df['IPCA_VARIACAO_ANUAL'] < 3,
        (df['IPCA_VARIACAO_ANUAL'] >= 3) & (df['IPCA_VARIACAO_ANUAL'] < 6),
        (df['IPCA_VARIACAO_ANUAL'] >= 6) & (df['IPCA_VARIACAO_ANUAL'] < 10),
        df['IPCA_VARIACAO_ANUAL'] >= 10
    ]
    choices = ['Baixa', 'Moderada', 'Alta', 'Muito Alta']
    df['CLASSIFICACAO_INFLACAO'] = np.select(conditions, choices, default='Moderada')
    
    # Classificar desocupação
    conditions_desocup = [
        df['TAXA_DESOCUPACAO'] < 8,
        (df['TAXA_DESOCUPACAO'] >= 8) & (df['TAXA_DESOCUPACAO'] < 12),
        df['TAXA_DESOCUPACAO'] >= 12
    ]
    choices_desocup = ['Baixa', 'Moderada', 'Alta']
    df['CLASSIFICACAO_DESOCUPACAO'] = np.select(conditions_desocup, choices_desocup, default='Moderada')
    
    print("✅ Features adicionais criadas")
    
    return df

def analisar_dados(dataset_completo):
    """Realiza análise exploratória dos dados"""
    print("\n📊 Realizando análise exploratória...")
    
    # Correlação entre as variáveis
    correlacao = dataset_completo[['IPCA', 'TAXA_DESOCUPACAO', 'IPCA_VARIACAO_ANUAL']].corr()
    print("\n📈 Matriz de correlação:")
    print(correlacao)
    
    # Estatísticas por ano
    stats_anual = dataset_completo.groupby('ANO').agg({
        'IPCA': ['mean', 'std', 'min', 'max'],
        'TAXA_DESOCUPACAO': ['mean', 'std', 'min', 'max'],
        'IPCA_VARIACAO_ANUAL': 'mean'
    }).round(2)
    
    print("\n📅 Estatísticas anuais:")
    print(stats_anual)
    
    return correlacao, stats_anual

def visualizar_dados(dataset_completo):
    """Cria visualizações dos dados"""
    print("\n📈 Criando visualizações...")
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Análise de Inflação e Taxa de Desocupação (2012-2025)', fontsize=16, fontweight='bold')
    
    # Gráfico 1: Evolução temporal do IPCA
    axes[0, 0].plot(dataset_completo['VALDATA'], dataset_completo['IPCA'], linewidth=2, color='red')
    axes[0, 0].set_title('Evolução do IPCA (2012-2025)')
    axes[0, 0].set_ylabel('IPCA')
    axes[0, 0].grid(True, alpha=0.3)
    axes[0, 0].tick_params(axis='x', rotation=45)
    
    # Gráfico 2: Evolução temporal da taxa de desocupação
    axes[0, 1].plot(dataset_completo['VALDATA'], dataset_completo['TAXA_DESOCUPACAO'], linewidth=2, color='blue')
    axes[0, 1].set_title('Evolução da Taxa de Desocupação (2012-2025)')
    axes[0, 1].set_ylabel('Taxa de Desocupação (%)')
    axes[0, 1].grid(True, alpha=0.3)
    axes[0, 1].tick_params(axis='x', rotation=45)
    
    # Gráfico 3: Variação anual do IPCA
    axes[1, 0].plot(dataset_completo['VALDATA'], dataset_completo['IPCA_VARIACAO_ANUAL'], linewidth=2, color='orange')
    axes[1, 0].axhline(y=0, color='black', linestyle='-', alpha=0.3)
    axes[1, 0].axhline(y=4.5, color='red', linestyle='--', alpha=0.5, label='Meta BC (4.5%)')
    axes[1, 0].set_title('Variação Anual do IPCA (%)')
    axes[1, 0].set_ylabel('Variação Anual (%)')
    axes[1, 0].grid(True, alpha=0.3)
    axes[1, 0].tick_params(axis='x', rotation=45)
    axes[1, 0].legend()
    
    # Gráfico 4: Dispersão entre inflação e desocupação
    scatter = axes[1, 1].scatter(dataset_completo['TAXA_DESOCUPACAO'], 
                               dataset_completo['IPCA_VARIACAO_ANUAL'], 
                               c=dataset_completo['ANO'],
                               alpha=0.6, 
                               cmap='viridis')
    axes[1, 1].set_xlabel('Taxa de Desocupação (%)')
    axes[1, 1].set_ylabel('Variação Anual do IPCA (%)')
    axes[1, 1].set_title('Relação entre Desocupação e Inflação (Cor por Ano)')
    axes[1, 1].grid(True, alpha=0.3)
    plt.colorbar(scatter, ax=axes[1, 1], label='Ano')
    
    plt.tight_layout()
    plt.show()

def salvar_dados_processados(dataset_completo):
    """Salva os dados processados em novos arquivos CSV"""
    print("\n💾 Salvando dados processados...")
    
    # Criar diretório para dados processados se não existir
    dir_processados = r"C:\Users\Pedro\Documents\coisas que o FDP do ENZO quer\IPEA\data\processed"
    os.makedirs(dir_processados, exist_ok=True)
    
    # Formatar datas para exibição
    dataset_salvar = dataset_completo.copy()
    dataset_salvar['VALDATA'] = dataset_salvar['VALDATA'].dt.strftime('%Y-%m-%d')
    
    # Salvar dataset completo
    caminho_completo = os.path.join(dir_processados, 'dados_combinados_processados.csv')
    dataset_salvar.to_csv(caminho_completo, index=False, encoding='utf-8')
    
    # Salvar resumo estatístico
    resumo = dataset_completo.groupby('ANO').agg({
        'IPCA': ['mean', 'std', 'min', 'max'],
        'TAXA_DESOCUPACAO': ['mean', 'std', 'min', 'max'],
        'IPCA_VARIACAO_ANUAL': 'mean'
    }).round(2)
    
    caminho_resumo = os.path.join(dir_processados, 'resumo_estatistico_anual.csv')
    resumo.to_csv(caminho_resumo, encoding='utf-8')
    
    print("✅ Arquivos salvos em:")
    print(f"   📄 {caminho_completo}")
    print(f"   📊 {caminho_resumo}")
    
    # Mostrar preview dos dados salvos
    print("\n👀 Preview dos dados processados:")
    print(dataset_salvar.head())

def main():
    """Função principal"""
    print("=== PROCESSAMENTO DE DADOS ECONÔMICOS DO IPEA ===\n")
    print(f"📁 Diretório dos dados: {DIRETORIO_BASE}")
    
    try:
        # 1. Carregar dados raw
        inflacao_raw, desocupacao_raw = carregar_dados_raw()
        
        if inflacao_raw is None or desocupacao_raw is None:
            return
        
        # 2. Processar dados individuais
        inflacao_processada = processar_inflacao(inflacao_raw)
        desocupacao_processada = processar_desocupacao(desocupacao_raw)
        
        # 3. Filtrar período comum
        inflacao_filtrada, desocupacao_filtrada = filtrar_periodo_comum(inflacao_processada, desocupacao_processada)
        
        # 4. Combinar datasets
        dataset_combinado = criar_dataset_combinado(inflacao_filtrada, desocupacao_filtrada)
        
        # 5. Criar features adicionais
        dataset_completo = criar_features_adicionais(dataset_combinado)
        
        # 6. Análise dos dados
        correlacao, stats_anual = analisar_dados(dataset_completo)
        
        # 7. Visualizações
        visualizar_dados(dataset_completo)
        
        # 8. Salvar dados processados
        salvar_dados_processados(dataset_completo)
        
        print("\n🎉 PROCESSAMENTO CONCLUÍDO COM SUCESSO ===")
        print(f"📊 Total de observações processadas: {len(dataset_completo)}")
        print(f"📅 Período: {dataset_completo['VALDATA'].min().strftime('%Y-%m')} a {dataset_completo['VALDATA'].max().strftime('%Y-%m')}")
        print(f"🔗 Correlação Inflação-Desocupação: {correlacao.loc['IPCA_VARIACAO_ANUAL', 'TAXA_DESOCUPACAO']:.3f}")
        
    except Exception as e:
        print(f"❌ Erro durante o processamento: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()