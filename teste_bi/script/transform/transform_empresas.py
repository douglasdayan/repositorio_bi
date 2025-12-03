import pandas as pd
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RAW_PATH = os.path.join(BASE_DIR, 'files', 'raw')
CLEAN_PATH = os.path.join(BASE_DIR, 'files', 'clean')

os.makedirs(CLEAN_PATH, exist_ok=True)

def transform_empresas():
    print("--- [TRANSFORM] Iniciando Dados Cadastrais (Empresas) ---")
    
    files = [
        'raw_df_empresas.csv',
        'raw_empresas_bolsa.csv',
        'raw_empresas_nivel_atividade.csv',
        'raw_empresas_porte.csv',
        'raw_empresas_saude_tributaria.csv',
        'raw_empresas_simples.csv'
    ]

    for file_name in files:
        input_path = os.path.join(RAW_PATH, file_name)
        output_name = file_name.replace('raw_', 'clean_')
        output_path = os.path.join(CLEAN_PATH, output_name)

        if not os.path.exists(input_path):
            continue

        try:
            df = pd.read_csv(input_path, sep=';', decimal=',', encoding='utf-8')

            # --- Lógica de Limpeza Geral ---
            
            # 1. Tratamento de CNPJ (se a coluna existir)
            # Busca colunas que pareçam CNPJ (vl_cnpj, cnpj, tx_cnpj)
            cols_cnpj = [c for c in df.columns if 'cnpj' in c.lower()]
            for col in cols_cnpj:
                # Converte para string, remove o .0 decimal e remove 'nan'
                df[col] = df[col].astype(str).str.replace(r'\.0$', '', regex=True)
                df[col] = df[col].replace('nan', '')
                # Opcional: Remover pontuação (./-) se quiser deixar apenas números
                # df[col] = df[col].str.replace(r'[^\d]', '', regex=True)

            # 2. Tratamento de Texto (Upper case e strip)
            cols_text = df.select_dtypes(include=['object']).columns
            for col in cols_text:
                if col not in cols_cnpj: # Pula CNPJ
                    df[col] = df[col].astype(str).str.strip().str.upper()
                    df[col] = df[col].replace('NAN', '')

            df.to_csv(output_path, index=False, sep=';', decimal=',', encoding='utf-8')
            print(f"OK: {output_name}")

        except Exception as e:
            print(f"ERRO em {file_name}: {e}")

if __name__ == "__main__":
    transform_empresas()