import pandas as pd
import os
import sys

# Configuração de Caminhos
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SOURCE_PATH = os.path.join(BASE_DIR, 'files', 'spreadsheets')
TARGET_PATH = os.path.join(BASE_DIR, 'files', 'raw')

os.makedirs(TARGET_PATH, exist_ok=True)

def extract_cotacoes():
    file_name = 'cotacoes_bolsa.csv'
    input_file = os.path.join(SOURCE_PATH, file_name)
    output_file = os.path.join(TARGET_PATH, 'raw_cotacoes.csv')

    print(f"--- [EXTRACT] Processando Transacional: {file_name} ---")

    if not os.path.exists(input_file):
        print(f"ERRO FATAL: Arquivo {file_name} não encontrado.")
        sys.exit(1)

    try:
        # Leitura Específica: Esse arquivo usa ponto (.) como decimal
        try:
            df = pd.read_csv(input_file, sep=';', decimal='.', encoding='utf-8')
        except UnicodeDecodeError:
            df = pd.read_csv(input_file, sep=';', decimal='.', encoding='latin1')

        # Padronização para saída RAW:
        # Salvamos com decimal ',' para ficar igual aos outros arquivos do sistema (padrão BR)
        df.to_csv(output_file, index=False, sep=';', decimal=',', encoding='utf-8')
        
        print(f"Sucesso! {len(df)} linhas extraídas para: {output_file}")

    except Exception as e:
        print(f"Erro crítico em {file_name}: {e}")
        sys.exit(1)

if __name__ == "__main__":
    extract_cotacoes()