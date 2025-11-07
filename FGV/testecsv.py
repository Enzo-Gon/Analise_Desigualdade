import pandas as pd
import matplotlib.pyplot as plt
import os

# CONFIGURAÇÃO DO CAMINHO
CAMINHO_BASE = r"C:\Users\Pedro\Documents\coisas que o FDP do ENZO quer\csv"

def encontrar_arquivo_csv():
    """Encontra automaticamente arquivos CSV no diretório específico"""
    print("🔍 Procurando arquivos CSV...")
    print(f"📁 Diretório: {CAMINHO_BASE}")
    
    try:
        if not os.path.exists(CAMINHO_BASE):
            print(f"❌ Diretório não encontrado: {CAMINHO_BASE}")
            return None
        
        arquivos_csv = [f for f in os.listdir(CAMINHO_BASE) if f.endswith('.csv')]
        
        if not arquivos_csv:
            print("❌ Nenhum arquivo CSV encontrado no diretório!")
            return None
        
        print("📁 Arquivos CSV encontrados:")
        for i, arquivo in enumerate(arquivos_csv, 1):
            print(f"   {i}. {arquivo}")
        
        if len(arquivos_csv) == 1:
            print(f"✅ Usando automaticamente: {arquivos_csv[0]}")
            return arquivos_csv[0]
        else:
            try:
                escolha = int(input(f"\n🎯 Escolha o arquivo (1-{len(arquivos_csv)}): "))
                return arquivos_csv[escolha-1]
            except:
                print("⚠️  Escolha inválida. Usando o primeiro arquivo.")
                return arquivos_csv[0]
                
    except Exception as e:
        print(f"❌ Erro ao acessar diretório: {e}")
        return None

def carregar_dados(arquivo_csv):
    """Carrega o arquivo CSV com tratamento de erros"""
    try:
        caminho_completo = os.path.join(CAMINHO_BASE, arquivo_csv)
        print(f"📂 Tentando carregar: {caminho_completo}")
        
        codificacoes = ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252', 'windows-1252']
        
        for encoding in codificacoes:
            try:
                df = pd.read_csv(caminho_completo, encoding=encoding)
                print(f"✅ Arquivo '{arquivo_csv}' carregado com encoding: {encoding}")
                return df
            except UnicodeDecodeError:
                continue
        
        print("❌ Não foi possível ler o arquivo com nenhum encoding comum")
        return None
        
    except Exception as e:
        print(f"❌ Erro ao carregar arquivo: {e}")
        return None

def validar_coluna(df, coluna, tipo='qualquer'):
    """Valida se a coluna existe no DataFrame"""
    if coluna in df.columns:
        if tipo == 'numero' and not pd.api.types.is_numeric_dtype(df[coluna]):
            print(f"⚠️  A coluna '{coluna}' não é numérica!")
            return False
        elif tipo == 'texto' and pd.api.types.is_numeric_dtype(df[coluna]):
            print(f"⚠️  A coluna '{coluna}' não é de texto!")
            return False
        return True
    else:
        print(f"❌ Coluna '{coluna}' não encontrada!")
        print(f"   Colunas disponíveis: {list(df.columns)}")
        return False

def menu_graficos_interativo(df, nome_arquivo):
    """Menu interativo para diferentes tipos de gráfico"""
    
    while True:
        print(f"\n{'='*50}")
        print("🎨 MENU DE GRÁFICOS INTERATIVO")
        print(f"{'='*50}")
        print("1. Gráfico de Linha")
        print("2. Gráfico de Barras")
        print("3. Gráfico de Dispersão")
        print("4. Histograma")
        print("5. Gráfico de Pizza")
        print("6. Voltar")
        
        opcao = input("\nEscolha uma opção (1-6): ")
        
        if opcao == '6':
            break
        
        print(f"\n📋 Colunas disponíveis: {list(df.columns)}")
        
        colunas_numericas = df.select_dtypes(include=['number']).columns.tolist()
        colunas_texto = df.select_dtypes(include=['object']).columns.tolist()
        
        if opcao in ['1', '2', '3']:
            # Gráficos que precisam de X e Y
            if colunas_texto:
                print(f"📊 Colunas para eixo X (texto): {colunas_texto}")
            if colunas_numericas:
                print(f"📈 Colunas para eixo Y (numéricas): {colunas_numericas}")
            
            while True:
                coluna_x = input("Digite o nome da coluna para o eixo X: ")
                if validar_coluna(df, coluna_x, 'texto'):
                    break
            
            while True:
                coluna_y = input("Digite o nome da coluna para o eixo Y: ")
                if validar_coluna(df, coluna_y, 'numero'):
                    break
            
            plt.figure(figsize=(12, 7))
            
            if opcao == '1':
                plt.plot(df[coluna_x], df[coluna_y], marker='o', linewidth=2, markersize=6)
                plt.title(f'Gráfico de Linha: {coluna_y} vs {coluna_x}', fontsize=14, fontweight='bold')
            elif opcao == '2':
                plt.bar(df[coluna_x], df[coluna_y], color='skyblue', edgecolor='black')
                plt.title(f'Gráfico de Barras: {coluna_y} vs {coluna_x}', fontsize=14, fontweight='bold')
            elif opcao == '3':
                plt.scatter(df[coluna_x], df[coluna_y], alpha=0.7, s=60)
                plt.title(f'Gráfico de Dispersão: {coluna_y} vs {coluna_x}', fontsize=14, fontweight='bold')
            
            plt.xlabel(coluna_x, fontsize=12)
            plt.ylabel(coluna_y, fontsize=12)
            plt.xticks(rotation=45)
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            plt.show()
        
        elif opcao == '4':
            # Histograma
            if colunas_numericas:
                print(f"📊 Colunas numéricas para histograma: {colunas_numericas}")
                while True:
                    coluna = input("Digite o nome da coluna: ")
                    if validar_coluna(df, coluna, 'numero'):
                        break
                
                plt.figure(figsize=(10, 6))
                plt.hist(df[coluna], bins=15, alpha=0.7, edgecolor='black', color='lightgreen')
                plt.title(f'Histograma de {coluna}', fontsize=14, fontweight='bold')
                plt.xlabel(coluna, fontsize=12)
                plt.ylabel('Frequência', fontsize=12)
                plt.grid(True, alpha=0.3)
                plt.tight_layout()
                plt.show()
            else:
                print("❌ Nenhuma coluna numérica encontrada para histograma!")
        
        elif opcao == '5':
            # Gráfico de Pizza
            if colunas_texto:
                print(f"🎯 Colunas para gráfico de pizza: {colunas_texto}")
                while True:
                    coluna = input("Digite o nome da coluna: ")
                    if validar_coluna(df, coluna, 'texto'):
                        break
                
                contagem = df[coluna].value_counts()
                plt.figure(figsize=(10, 8))
                plt.pie(contagem.values, labels=contagem.index, autopct='%1.1f%%', startangle=90)
                plt.title(f'Distribuição de {coluna}', fontsize=14, fontweight='bold')
                plt.tight_layout()
                plt.show()
            else:
                print("❌ Nenhuma coluna de texto encontrada para gráfico de pizza!")

def criar_grafico_automatico(df, nome_arquivo):
    """Cria gráfico automático baseado nos dados"""
    
    print(f"\n🎯 CRIANDO GRÁFICO AUTOMÁTICO")
    
    colunas_numericas = df.select_dtypes(include=['number']).columns.tolist()
    colunas_texto = df.select_dtypes(include=['object']).columns.tolist()
    
    if len(colunas_numericas) >= 1 and len(colunas_texto) >= 1:
        coluna_x = colunas_texto[0]
        coluna_y = colunas_numericas[0]
        
        print(f"🔄 Gráfico automático: X='{coluna_x}', Y='{coluna_y}'")
        
        plt.figure(figsize=(12, 7))
        plt.bar(df[coluna_x], df[coluna_y], color='lightcoral', edgecolor='black')
        plt.title(f'{coluna_y} por {coluna_x}\nArquivo: {nome_arquivo}', fontsize=14, fontweight='bold')
        plt.xlabel(coluna_x, fontsize=12)
        plt.ylabel(coluna_y, fontsize=12)
        plt.xticks(rotation=45)
        plt.grid(True, alpha=0.3, axis='y')
        plt.tight_layout()
        plt.show()
    else:
        print("❌ Não foi possível criar gráfico automático.")

# PROGRAMA PRINCIPAL
print("=" * 60)
print("📈 VISUALIZADOR DE CSV - COM VALIDAÇÃO")
print("=" * 60)
print(f"📍 Diretório: {CAMINHO_BASE}")

# 1. Encontrar arquivo CSV
arquivo_csv = encontrar_arquivo_csv()

if arquivo_csv is None:
    print("❌ Nenhum arquivo CSV encontrado. Encerrando.")
    exit()

# 2. Carregar dados
df = carregar_dados(arquivo_csv)

if df is None:
    print("❌ Não foi possível carregar os dados. Encerrando.")
    exit()

# 3. Explorar dados
print(f"\n📊 INFORMACÕES DO DATASET:")
print(f"   Dimensões: {df.shape[0]} linhas × {df.shape[1]} colunas")
print(f"   Colunas: {list(df.columns)}")
print(f"\n👀 Primeiras linhas:")
print(df.head())

# 4. Criar gráfico automático
criar_grafico_automatico(df, arquivo_csv)

# 5. Menu interativo
while True:
    usar_menu = input("\n🎯 Deseja criar mais gráficos? (s/n): ").lower()
    if usar_menu == 's':
        menu_graficos_interativo(df, arquivo_csv)
    else:
        break

print("\n✅ Processo concluído!")