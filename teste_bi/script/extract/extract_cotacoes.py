import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SOURCE_PATH = os.path.join(BASE_DIR, 'files', 'spreadsheets')
TARGET_PATH = os.path.join(BASE_DIR, 'files', 'raw')

def extract_cotacoes():
    file_name = 'cotacoes_bolsa.csv'
    input_file = os.path.join(SOURCE_PATH, file_name)
    output_file = os.path.join(TARGET_PATH, 'extract_cotacoes.csv')

    print(f"{file_name}")

    if not os.path.exists(input_file):
        print(f"{file_name} não encontrado.")

    df = pd.read_csv(input_file, sep=';', decimal='.', encoding='utf-8')
    df.to_csv(output_file, index=False, sep=';', decimal=',', encoding='utf-8')
    
    print(f"{len(df)} linhas extraídas para: {output_file}")

if __name__ == "__main__":
    extract_cotacoes()