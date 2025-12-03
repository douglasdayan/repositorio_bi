import pandas as pd
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CLEAN_PATH = os.path.join(BASE_DIR, 'files', 'clean')
ENRICH_PATH = os.path.join(BASE_DIR, 'files', 'enrich')

def load_fcotacoes():
    print("--- [LOAD] Gerando Fato: fCotacoes ---")
    
    input_path = os.path.join(CLEAN_PATH, 'clean_cotacoes.csv')
    output_path = os.path.join(ENRICH_PATH, 'fCotacoes.csv')

    if not os.path.exists(input_path):
        print("ERRO: clean_cotacoes.csv não encontrado.")
        sys.exit(1)

    df = pd.read_csv(input_path, sep=';', decimal=',', encoding='utf-8')
    df['dt_pregao'] = pd.to_datetime(df['dt_pregao'])
    df.sort_values(by=['dt_pregao', 'ticker'], inplace=True)

    df.to_csv(output_path, index=False, sep=';', decimal=',', encoding='utf-8-sig')
    print(f"SUCESSO: fCotacoes gerada com {len(df)} linhas.\n")

if __name__ == "__main__":
    load_fcotacoes()