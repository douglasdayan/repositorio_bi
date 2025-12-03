import pandas as pd
import os
import sys

# --- CONFIGURAÇÃO DE DIRETÓRIOS ---
# O script assume que está em: teste_bi/scripts/extract/
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SOURCE_PATH = os.path.join(BASE_DIR, 'files', 'spreadsheets')
TARGET_PATH = os.path.join(BASE_DIR, 'files', 'raw')

# Garante que a pasta RAW existe
os.makedirs(TARGET_PATH, exist_ok=True)

def extract_dados_externos():
    """
    Extrai, padroniza e salva os indicadores econômicos (Dólar, Selic, IPCA).
    """
    # Dicionário mapeando: Nome do Arquivo Origem -> Nome do Arquivo Destino (RAW)
    files_map = {
        'cotacao_dolar.csv': 'raw_dolar.csv',
        'selic.csv':         'raw_selic.csv',
        'ipca.csv':          'raw_ipca.csv'
    }

    print("--- [EXTRACT] Iniciando Extração de Dados Externos (Macro) ---")

    for source_file, target_file in files_map.items():
        input_path = os.path.join(SOURCE_PATH, source_file)
        output_path = os.path.join(TARGET_PATH, target_file)

        # 1. Verificação de Existência
        if not os.path.exists(input_path):
            print(f"AVISO: Arquivo de origem não encontrado: {source_file}. Pulando...")
            continue

        try:
            # 2. Leitura Robusta (Tenta UTF-8, se falhar tenta Latin-1)
            # Esses arquivos costumam vir com separador ';' e decimal ','
            try:
                df = pd.read_csv(input_path, sep=';', decimal=',', encoding='utf-8')
            except UnicodeDecodeError:
                df = pd.read_csv(input_path, sep=';', decimal=',', encoding='latin1')

            # 3. Salvamento Padronizado (RAW)
            # Salvamos sempre em UTF-8, com separador ';' e decimal ',' para consistência no Transform
            df.to_csv(output_path, index=False, sep=';', decimal=',', encoding='utf-8')
            
            print(f"SUCESSO: {source_file} -> {target_file} ({len(df)} linhas)")

        except Exception as e:
            print(f"ERRO CRÍTICO ao processar {source_file}: {e}")
            # Em produção, poderíamos usar sys.exit(1) aqui se os arquivos forem obrigatórios
            
    print("--- Extração de Dados Externos Concluída ---\n")

if __name__ == "__main__":
    extract_dados_externos()