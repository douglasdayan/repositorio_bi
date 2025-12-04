import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SOURCE_PATH = os.path.join(BASE_DIR, 'files', 'spreadsheets')
TARGET_PATH = os.path.join(BASE_DIR, 'files', 'raw')

def extract_empresas():
    files_to_process = [
        'df_empresas.csv',
        'empresas_bolsa.csv',
        'empresas_nivel_atividade.csv',
        'empresas_porte.csv',
        'empresas_saude_tributaria.csv',
        'empresas_simples.csv'
    ]

    for file_name in files_to_process:
        input_file = os.path.join(SOURCE_PATH, file_name)
        output_name = f"extract_{file_name}"
        output_file = os.path.join(TARGET_PATH, output_name)

        if not os.path.exists(input_file):
            print(f"{file_name} não encontrado.")
            continue

        df = pd.read_csv(input_file, sep=';', decimal=',', encoding='utf-8')
        df.to_csv(output_file, index=False, sep=';', decimal=',', encoding='utf-8')
            
        print(f"{file_name} -> {output_name} ({len(df)} linhas)")

if __name__ == "__main__":
    extract_empresas()