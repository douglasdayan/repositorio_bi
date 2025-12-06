import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SOURCE_PATH = os.path.join(BASE_DIR, 'files', 'raw')
TARGET_PATH = os.path.join(BASE_DIR, 'files', 'clean')

def clean_numeric(series):
    if series.dtype == 'object':
        series = series.astype(str).str.replace(',', '.')
    return pd.to_numeric(series, errors='coerce')

def transform_dados_externos():

    files_map = {
        'extract_dolar.csv': ['venda','Dolar_Venda'],
        'extract_ipca.csv' : ['%','IPCA_Mensal'],
        'extract_selic.csv': ['%', 'Selic']
    }

    for source_file, config in files_map.items():
        
        target_file   = source_file.replace('extract_', 'transform_')
        source_column = config[0]
        target_column = config[1]

        input_path  = os.path.join(SOURCE_PATH, source_file)
        output_path = os.path.join(TARGET_PATH, target_file)

        if not os.path.exists(input_path):
            print(f"{source_file} não encontrado.")
            continue

        try:
            df = pd.read_csv(input_path, sep=';', decimal=',', encoding='utf-8')
            
            col_data = [c for c in df.columns if 'Data' in c][0]
            col_valor = [c for c in df.columns if source_column in c][0]
            
            df['Data_Temp'] = df[col_data].astype(str).str.split(' ').str[0]
            
            df['Data'] = pd.to_datetime(df['Data_Temp'], format='%d/%m/%Y', errors='coerce')

            data_corte = '2022-01-01'
            df = df[df['Data'] >= data_corte].copy()
            
            df[target_column] = clean_numeric(df[col_valor])
            
            df = df[['Data', target_column]]

            df.to_csv(output_path, index=False, sep=';', decimal=',', encoding='utf-8')

            print(f"{source_file} -> {target_file} ({len(df)} linhas)")

        except Exception as e:
            print(f"ERRO {source_file}: {e}")

if __name__ == "__main__":
    transform_dados_externos()