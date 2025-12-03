import pandas as pd
import os
import sys

# Configuração de Caminhos
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SOURCE_PATH = os.path.join(BASE_DIR, 'files', 'spreadsheets')
TARGET_PATH = os.path.join(BASE_DIR, 'files', 'raw')

os.makedirs(TARGET_PATH, exist_ok=True)

def extract_empresas_domain():
    # Lista de arquivos cadastrais a serem processados
    files_to_process = [
        'df_empresas.csv',
        'empresas_bolsa.csv',
        'empresas_nivel_atividade.csv',
        'empresas_porte.csv',
        'empresas_saude_tributaria.csv',
        'empresas_simples.csv'
    ]

    print(f"--- [EXTRACT] Processando Domínio Empresas ({len(files_to_process)} arquivos) ---")

    for file_name in files_to_process:
        input_file = os.path.join(SOURCE_PATH, file_name)
        # Define nome de saída padronizado: ex raw_df_empresas.csv
        output_name = f"raw_{file_name}"
        output_file = os.path.join(TARGET_PATH, output_name)

        if not os.path.exists(input_file):
            print(f"AVISO: Arquivo {file_name} não encontrado. Pulando...")
            continue

        try:
            # Leitura Padrão (Separador ; e Decimal ,)
            try:
                df = pd.read_csv(input_file, sep=';', decimal=',', encoding='utf-8')
            except UnicodeDecodeError:
                df = pd.read_csv(input_file, sep=';', decimal=',', encoding='latin1')

            # Salva na camada RAW padronizado em UTF-8
            df.to_csv(output_file, index=False, sep=';', decimal=',', encoding='utf-8')
            
            print(f"OK: {file_name} -> {output_name} ({len(df)} linhas)")

        except Exception as e:
            print(f"ERRO ao processar {file_name}: {e}")
            # Não damos sys.exit(1) aqui para permitir que os outros arquivos sejam processados

if __name__ == "__main__":
    extract_empresas_domain()