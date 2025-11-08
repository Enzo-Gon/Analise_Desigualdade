import requests
import pandas as pd
import time
import os
from datetime import datetime

def create_directories():
    """Cria os diretórios necessários para salvar os dados"""
    os.makedirs('data/raw/bcb', exist_ok=True)
    os.makedirs('data/processed', exist_ok=True)

def get_bcb_series_with_retry():
    """
    Coleta séries do Banco Central Brasil (2018-2024) com retry para timeouts
    """
    print("Coletando dados do Banco Central...")
    
    # Códigos das séries do SGS
    series_bcb = {
        'ipca': 433,                    # IPCA
        'ipca_acumulado_12m': 13522,    # IPCA acumulado 12 meses
        'divida_total_familias': 4390,  # Dívida total das famílias (% renda)
        'credito_total': 20714,         # Crédito total
        'credito_pessoal': 20716,       # Crédito pessoal
        'taxa_juros_pessoal': 20796,    # Taxa de juros - pessoal
        'inadimplencia': 21082,         # Taxa de inadimplência
        'poupanca': 196,                # Poupança
    }
    
    bcb_data = {}
    failed_series = []
    
    for name, code in series_bcb.items():
        print(f"Coletando série BCB: {name} ({code})")
        
        max_retries = 3
        for attempt in range(max_retries):
            try:
                # API do BCB
                url = f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{code}/dados"
                params = {
                    'formato': 'json',
                    'dataInicial': '01/01/2018',
                    'dataFinal': '31/12/2024'
                }
                
                # Timeout menor para tentativas iniciais, maior para as seguintes
                timeout = 15 if attempt == 0 else 30
                response = requests.get(url, params=params, timeout=timeout)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    if data:
                        df = pd.DataFrame(data)
                        df['data'] = pd.to_datetime(df['data'], dayfirst=True)
                        df['valor'] = pd.to_numeric(df['valor'], errors='coerce')
                        
                        # Ordenar por data
                        df = df.sort_values('data')
                        
                        bcb_data[name] = df
                        df.to_csv(f'data/raw/bcb/{name}_2018_2024.csv', index=False)
                        print(f"✓ {name}: {len(df)} registros (de {df['data'].min().strftime('%Y-%m')} a {df['data'].max().strftime('%Y-%m')})")
                        break  # Sai do loop de retry se bem-sucedido
                    else:
                        print(f"✗ {name}: Dados vazios")
                        break
                else:
                    print(f"✗ {name}: HTTP {response.status_code} (tentativa {attempt + 1}/{max_retries})")
                    if attempt == max_retries - 1:
                        failed_series.append(name)
            
            except requests.exceptions.Timeout:
                print(f"✗ Timeout na série {name} (tentativa {attempt + 1}/{max_retries})")
                if attempt == max_retries - 1:
                    failed_series.append(name)
                    print(f"  ⚠️ Série {name} falhou após {max_retries} tentativas")
            
            except Exception as e:
                print(f"✗ Erro na série {name}: {e} (tentativa {attempt + 1}/{max_retries})")
                if attempt == max_retries - 1:
                    failed_series.append(name)
            
            # Aguarda antes da próxima tentativa (backoff exponencial)
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # 1, 2, 4 segundos
                print(f"  Aguardando {wait_time}s antes da próxima tentativa...")
                time.sleep(wait_time)
            else:
                time.sleep(1)  # Aguarda 1s entre séries diferentes
    
    if failed_series:
        print(f"\n⚠️ Séries que falharam: {', '.join(failed_series)}")
    
    return bcb_data

def calculate_inflation_impact():
    """
    Calcula impacto da inflação no poder de compra
    """
    try:
        # Carregar IPCA
        ipca_df = pd.read_csv('data/raw/bcb/ipca_2018_2024.csv')
        ipca_df['data'] = pd.to_datetime(ipca_df['data'])
        
        # Ordenar por data
        ipca_df = ipca_df.sort_values('data')
        
        # Calcular IPCA acumulado
        ipca_df['ipca_acumulado'] = (1 + ipca_df['valor']/100).cumprod() - 1
        ipca_df['perda_poder_compra'] = 1 - (1 / (1 + ipca_df['ipca_acumulado']))
        
        # Calcular perda percentual
        ipca_df['perda_poder_compra_pct'] = ipca_df['perda_poder_compra'] * 100
        
        # Salvar análise
        ipca_df.to_csv('data/processed/impacto_inflacao.csv', index=False)
        
        # Estatísticas resumidas
        ultimo_mes = ipca_df.iloc[-1]
        print(f"✓ Análise de impacto da inflação calculada")
        print(f"  Perda acumulada do poder de compra: {ultimo_mes['perda_poder_compra_pct']:.2f}%")
        print(f"  IPCA acumulado no período: {ultimo_mes['ipca_acumulado']*100:.2f}%")
        
        return ipca_df
        
    except Exception as e:
        print(f"Erro no cálculo do impacto da inflação: {e}")
        return None

def analyze_debt_credit_data():
    """
    Análise integrada de dívida e crédito (robusta a dados faltantes)
    """
    try:
        # Lista de arquivos disponíveis
        available_files = []
        required_files = [
            'divida_total_familias_2018_2024.csv',
            'credito_total_2018_2024.csv', 
            'inadimplencia_2018_2024.csv'
        ]
        
        for file in required_files:
            if os.path.exists(f'data/raw/bcb/{file}'):
                available_files.append(file)
            else:
                print(f"⚠️ Arquivo não encontrado: {file}")
        
        if len(available_files) < 2:
            print("❌ Dados insuficientes para análise de dívida e crédito")
            return None
        
        # Carregar dados disponíveis
        data_frames = {}
        for file in available_files:
            series_name = file.replace('_2018_2024.csv', '')
            df = pd.read_csv(f'data/raw/bcb/{file}')
            df['data'] = pd.to_datetime(df['data'])
            data_frames[series_name] = df
        
        # Começar com o primeiro dataframe
        analise_df = list(data_frames.values())[0].copy()
        current_name = list(data_frames.keys())[0]
        
        # Juntar todos os dados disponíveis
        for name, df in list(data_frames.items())[1:]:
            analise_df = analise_df.merge(df, on='data', how='outer', suffixes=('', f'_{name}'))
        
        # Renomear colunas para ficarem claras
        column_mapping = {
            'valor': current_name,
            'valor_divida_total_familias': 'divida_familias_pct',
            'valor_credito_total': 'credito_total', 
            'valor_inadimplencia': 'inadimplencia',
            'valor_taxa_juros_pessoal': 'taxa_juros'
        }
        
        analise_df = analise_df.rename(columns=column_mapping)
        
        # Manter apenas colunas relevantes
        keep_cols = ['data'] + [col for col in analise_df.columns if col.startswith(('divida', 'credito', 'inadimplencia', 'taxa_juros'))]
        analise_df = analise_df[keep_cols]
        
        # Ordenar por data
        analise_df = analise_df.sort_values('data')
        
        # Salvar análise consolidada
        analise_df.to_csv('data/processed/analise_divida_credito.csv', index=False)
        print(f"✓ Análise de dívida e crédito consolidada ({len(available_files)} séries)")
        
        # Estatísticas básicas
        print(f"  Período: {analise_df['data'].min().strftime('%Y-%m')} a {analise_df['data'].max().strftime('%Y-%m')}")
        print(f"  Séries incluídas: {', '.join(available_files)}")
        
        return analise_df
        
    except Exception as e:
        print(f"Erro na análise de dívida e crédito: {e}")
        return None

def generate_summary_report():
    """
    Gera um relatório resumido dos dados coletados
    """
    print("\n" + "="*50)
    print("RELATÓRIO RESUMO - DADOS BCB 2018-2024")
    print("="*50)
    
    # Verificar arquivos coletados
    raw_files = os.listdir('data/raw/bcb')
    processed_files = os.listdir('data/processed')
    
    print(f"\n📊 Arquivos coletados: {len(raw_files)}")
    for file in sorted(raw_files):
        file_path = f'data/raw/bcb/{file}'
        df = pd.read_csv(file_path)
        dates = pd.to_datetime(df['data'])
        print(f"   • {file.replace('_2018_2024.csv', '')}: {len(df)} registros ({dates.min().strftime('%Y-%m')} a {dates.max().strftime('%Y-%m')})")
    
    print(f"\n📈 Análises processadas: {len(processed_files)}")
    for file in sorted(processed_files):
        print(f"   • {file}")
    
    # Estatística principal da inflação
    if os.path.exists('data/processed/impacto_inflacao.csv'):
        inflacao_df = pd.read_csv('data/processed/impacto_inflacao.csv')
        ultimo_mes = inflacao_df.iloc[-1]
        print(f"\n💰 Impacto da Inflação (2018-2024):")
        print(f"   • IPCA Acumulado: {ultimo_mes['ipca_acumulado']*100:.2f}%")
        print(f"   • Perda do Poder de Compra: {ultimo_mes['perda_poder_compra_pct']:.2f}%")

# Executar coleta
if __name__ == "__main__":
    # Criar diretórios
    create_directories()
    
    # Coletar dados com retry
    bcb_data = get_bcb_series_with_retry()
    
    # Calcular análises
    inflation_impact = calculate_inflation_impact()
    debt_analysis = analyze_debt_credit_data()
    
    # Gerar relatório
    generate_summary_report()
    
    print("\n✅ Processamento concluído!")