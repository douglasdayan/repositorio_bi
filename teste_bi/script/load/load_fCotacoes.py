import pandas as pd
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SOURCE_PATH = os.path.join(BASE_DIR, 'files', 'clean')
TARGET_PATH = os.path.join(BASE_DIR, 'files', 'enrich')

def load_fcotacoes():
    input_path = os.path.join(SOURCE_PATH, 'transform_cotacoes.csv')
    output_path = os.path.join(TARGET_PATH, 'fCotacoes.csv')

    if not os.path.exists(input_path):
        print("transform_cotacoes.csv não encontrado.")
        sys.exit(1)

    df = pd.read_csv(input_path, sep=';', decimal=',', encoding='utf-8')
    df['dt_pregao'] = pd.to_datetime(df['dt_pregao'])
    df.sort_values(by=['dt_pregao', 'cd_acao'], inplace=True)

    df.to_csv(output_path, index=False, sep=';', decimal=',', encoding='utf-8-sig')
    print(f"fCotacoes gerada com {len(df)} linhas.\n")

if __name__ == "__main__":
    load_fcotacoes()