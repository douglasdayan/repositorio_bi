import pandas as pd
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SOURCE_PATH = os.path.join(BASE_DIR, 'files', 'clean')
TARGET_PATH = os.path.join(BASE_DIR, 'files', 'enrich')

def get_data(filename):
    input_path = os.path.join(SOURCE_PATH, filename)
    if not os.path.exists(input_path):
        print(f"{filename} não encontrado.")
        return None
    return pd.read_csv(input_path, sep=';', decimal=',', encoding='utf-8')

def normalize_cnpj(series):
    return series.astype(str).str.replace(r'\.0$', '', regex=True).replace(['nan', 'NaN'], '')

def load_dempresas():
    df_cot = get_data('transform_cotacoes.csv')
    if df_cot is None:
        sys.exit("transform_cotacoes.csv necessário.")
    
    dEmpresas = df_cot[['cd_acao', 'cd_acao_rdz']].drop_duplicates()
    
    df_cad = get_data('transform_empresas_bolsa.csv')
    if df_cad is not None:
        cols = ['cd_acao_rdz', 'nm_empresa', 'vl_cnpj', 'setor_economico', 'subsetor', 'segmento']
    
        df_atributos = df_cad[df_cad.columns.intersection(cols)].drop_duplicates(subset=['cd_acao_rdz'])
        df_atributos.rename(columns={'vl_cnpj': 'cnpj'}, inplace=True)
        
        dEmpresas = dEmpresas.merge(df_atributos, on='cd_acao_rdz', how='left')

    files = [
        'transform_df_empresas.csv',
        'transform_empresas_nivel_atividade.csv',
        'transform_empresas_porte.csv',
        'transform_empresas_saude_tributaria.csv',
        'transform_empresas_simples.csv'
    ]

    for f in files:
        df_aux = get_data(f)
        if df_aux is not None and 'cnpj' in df_aux.columns:
            df_aux['cnpj'] = normalize_cnpj(df_aux['cnpj'])
            if 'cnpj' in dEmpresas.columns:
                dEmpresas['cnpj'] = normalize_cnpj(dEmpresas['cnpj'])
                dEmpresas = dEmpresas.merge(df_aux, on='cnpj', how='left')
            
    cols_limpar = ['cnpj', 'optante_simples', 'optante_simei', 'saude_tributaria', 'nivel_atividade']
    
    cols_existentes = [c for c in cols_limpar if c in dEmpresas.columns]
    
    dEmpresas[cols_existentes] = dEmpresas[cols_existentes].replace(['nan', 'NaN', 'NAN'], '')

    dEmpresas.to_csv(os.path.join(TARGET_PATH, 'dEmpresas.csv'), index=False, sep=';', decimal=',', encoding='utf-8-sig')

    print(f"dEmpresas gerada com {len(dEmpresas)} linhas.")

if __name__ == "__main__":
    load_dempresas()