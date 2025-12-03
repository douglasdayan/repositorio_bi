import pandas as pd
import os
import sys

# --- CONFIGURAÇÃO ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RAW_PATH = os.path.join(BASE_DIR, 'files', 'raw')
CLEAN_PATH = os.path.join(BASE_DIR, 'files', 'clean')

os.makedirs(CLEAN_PATH, exist_ok=True)

def clean_numeric(series):
    """Converte para float, transformando erros (hífens) em NaN"""
    if series.dtype == 'object':
        series = series.astype(str).str.replace(',', '.')
    return pd.to_numeric(series, errors='coerce')

def transform_dados_externos():
    print("--- [TRANSFORM] Iniciando Dados Externos (Macro) ---")
    
    # 1. SELIC
    try:
        df_selic = pd.read_csv(os.path.join(RAW_PATH, 'raw_selic.csv'), sep=';', decimal=',')
        col_data = [c for c in df_selic.columns if 'Data' in c][0]
        col_valor = [c for c in df_selic.columns if '%' in c][0]
        
        df_selic['Data'] = pd.to_datetime(df_selic[col_data], format='%d/%m/%Y', errors='coerce')
        df_selic['Selic'] = clean_numeric(df_selic[col_valor])
        
        df_selic = df_selic[['Data', 'Selic']]
        df_selic.to_csv(os.path.join(CLEAN_PATH, 'clean_selic.csv'), index=False, sep=';', decimal=',', encoding='utf-8')
        print("OK: Selic limpa.")
    except Exception as e:
        print(f"ERRO Selic: {e}")

    # 2. DÓLAR
    try:
        df_dolar = pd.read_csv(os.path.join(RAW_PATH, 'raw_dolar.csv'), sep=';', decimal=',')
        col_data = [c for c in df_dolar.columns if 'Data' in c][0]
        col_valor = [c for c in df_dolar.columns if 'venda' in c][0]
        
        df_dolar['Data'] = df_dolar[col_data].astype(str).str.split(' ').str[0]
        df_dolar['Data'] = pd.to_datetime(df_dolar['Data'], format='%d/%m/%Y', errors='coerce')
        df_dolar['Dolar_Venda'] = clean_numeric(df_dolar[col_valor])
        
        df_dolar = df_dolar[['Data', 'Dolar_Venda']]
        df_dolar.to_csv(os.path.join(CLEAN_PATH, 'clean_dolar.csv'), index=False, sep=';', decimal=',', encoding='utf-8')
        print("OK: Dólar limpo.")
    except Exception as e:
        print(f"ERRO Dólar: {e}")

    # 3. IPCA
    try:
        df_ipca = pd.read_csv(os.path.join(RAW_PATH, 'raw_ipca.csv'), sep=';', decimal=',')
        col_data = [c for c in df_ipca.columns if 'Data' in c][0]
        col_valor = [c for c in df_ipca.columns if '%' in c][0]
        
        df_ipca['Data'] = pd.to_datetime(df_ipca[col_data], format='%d/%m/%Y', errors='coerce')
        df_ipca['IPCA_Mensal'] = clean_numeric(df_ipca[col_valor])
        
        df_ipca = df_ipca[['Data', 'IPCA_Mensal']]
        df_ipca.to_csv(os.path.join(CLEAN_PATH, 'clean_ipca.csv'), index=False, sep=';', decimal=',', encoding='utf-8')
        print("OK: IPCA limpo.")
    except Exception as e:
        print(f"ERRO IPCA: {e}")

if __name__ == "__main__":
    transform_dados_externos()