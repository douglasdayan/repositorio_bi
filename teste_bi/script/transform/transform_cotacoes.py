import pandas as pd
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RAW_PATH = os.path.join(BASE_DIR, 'files', 'raw')
CLEAN_PATH = os.path.join(BASE_DIR, 'files', 'clean')

os.makedirs(CLEAN_PATH, exist_ok=True)

def transform_cotacoes():
    print("--- [TRANSFORM] Iniciando Transacional (Cotações) ---")
    
    input_path = os.path.join(RAW_PATH, 'raw_cotacoes.csv')
    output_path = os.path.join(CLEAN_PATH, 'clean_cotacoes.csv')

    if not os.path.exists(input_path):
        print("ERRO: raw_cotacoes.csv não encontrado.")
        return

    try:
        # Lê da RAW (Lembrando que na raw já padronizamos para ; e ,)
        df = pd.read_csv(input_path, sep=';', decimal=',', encoding='utf-8')

        # 1. Filtro de Mercado (Apenas Mercado a Vista = 10)
        df = df[df['tp_merc'] == 10].copy()

        # 2. Conversão de Data (Original YYYYMMDD numérico ou texto)
        df['dt_pregao'] = pd.to_datetime(df['dt_pregao'], format='%Y%m%d', errors='coerce')

        # 3. Seleção de Colunas Relevantes (Reduz tamanho do arquivo)
        cols_uteis = [
            'dt_pregao', 'cd_acao', 'vl_abertura', 'vl_maximo', 
            'vl_minimo', 'vl_fechamento', 'vl_volume', 'qt_tit_neg'
        ]
        # Garante que as colunas existem antes de filtrar
        cols_existentes = [c for c in cols_uteis if c in df.columns]
        df = df[cols_existentes]

        # 4. Renomear para facilitar o Load
        df.rename(columns={'cd_acao': 'ticker'}, inplace=True)

        df.to_csv(output_path, index=False, sep=';', decimal=',', encoding='utf-8')
        print(f"OK: clean_cotacoes.csv gerado com {len(df)} linhas.")

    except Exception as e:
        print(f"ERRO Crítico em Cotações: {e}")

if __name__ == "__main__":
    transform_cotacoes()