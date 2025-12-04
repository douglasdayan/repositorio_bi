import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SOURCE_PATH = os.path.join(BASE_DIR, 'files', 'raw')
TARGET_PATH = os.path.join(BASE_DIR, 'files', 'clean')

def transform_empresas():
    files = [
        'extract_df_empresas.csv',
        'extract_empresas_bolsa.csv',
        'extract_empresas_nivel_atividade.csv',
        'extract_empresas_porte.csv',
        'extract_empresas_saude_tributaria.csv',
        'extract_empresas_simples.csv'
    ]

    for file_name in files:
        input_path = os.path.join(SOURCE_PATH, file_name)
        output_name = file_name.replace('extract_', 'transform_')
        output_path = os.path.join(TARGET_PATH, output_name)

        if not os.path.exists(input_path):
            print(f"{file_name} não encontrado.")
            continue

        try:
            df = pd.read_csv(input_path, sep=';', decimal=',', encoding='utf-8')

            cols_cnpj = [c for c in df.columns if 'cnpj' in c.lower()]
            for col in cols_cnpj:
                df[col] = df[col].replace('nan', '')

            cols_text = df.select_dtypes(include=['object']).columns
            for col in cols_text:
                if col not in cols_cnpj:
                    df[col] = df[col].astype(str).str.strip().str.upper()
                    df[col] = df[col].replace(['NAN', 'Nan', 'nan'], '')

            if file_name == 'extract_empresas_bolsa.csv':
                if 'cd_acao' in df.columns:
                    df['cd_acao'] = df['cd_acao'].str.split(',')
                    df = df.explode('cd_acao')
                    df['cd_acao'] = df['cd_acao'].str.strip()

            df.to_csv(output_path, index=False, sep=';', decimal=',', encoding='utf-8')
            
            print(f"{file_name} -> {output_name} ({len(df)} linhas)")

        except Exception as e:
            print(f"ERRO em {file_name}: {e}")

if __name__ == "__main__":
    transform_empresas()