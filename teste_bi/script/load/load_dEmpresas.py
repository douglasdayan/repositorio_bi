import pandas as pd
import os
import sys

# Configuração
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CLEAN_PATH = os.path.join(BASE_DIR, 'files', 'clean')
ENRICH_PATH = os.path.join(BASE_DIR, 'files', 'enrich')

os.makedirs(ENRICH_PATH, exist_ok=True)

def load_dempresas():
    print("--- [LOAD] Gerando Dimensão: dEmpresas ---")
    
    # 1. Carrega a Tabela Ponte
    try:
        dEmpresas = pd.read_csv(os.path.join(CLEAN_PATH, 'clean_empresas_bolsa.csv'), sep=';', decimal=',', encoding='utf-8')
        
        # Seleciona colunas chave
        dEmpresas = dEmpresas[['cd_acao', 'nm_empresa', 'vl_cnpj', 'setor_economico', 'subsetor', 'segmento']]
        dEmpresas.rename(columns={'vl_cnpj': 'cnpj', 'cd_acao': 'ticker'}, inplace=True)
        
    except FileNotFoundError:
        print("ERRO CRÍTICO: clean_empresas_bolsa.csv não encontrado.")
        sys.exit(1)

    # 2. Lista de Enriquecimentos
    enrich_files = [
        'clean_df_empresas.csv',
        'clean_empresas_nivel_atividade.csv',
        'clean_empresas_porte.csv',
        'clean_empresas_saude_tributaria.csv',
        'clean_empresas_simples.csv'
    ]

    for file_name in enrich_files:
        file_path = os.path.join(CLEAN_PATH, file_name)
        if os.path.exists(file_path):
            try:
                df_aux = pd.read_csv(file_path, sep=';', decimal=',', encoding='utf-8')
                
                # Garante que CNPJ é string
                if 'cnpj' in df_aux.columns:
                    df_aux['cnpj'] = df_aux['cnpj'].astype(str).str.replace(r'\.0$', '', regex=True)
                    dEmpresas['cnpj'] = dEmpresas['cnpj'].astype(str).str.replace(r'\.0$', '', regex=True)
                    
                    dEmpresas = dEmpresas.merge(df_aux, on='cnpj', how='left')
                    print(f"   -> Enriquecido com {file_name}")
            except Exception as e:
                print(f"   AVISO: Falha ao ler {file_name}: {e}")

    # 3. Limpeza Final
    dEmpresas['cnpj'] = dEmpresas['cnpj'].replace('nan', '')

    # 4. Salva como dEmpresas.csv
    output_path = os.path.join(ENRICH_PATH, 'dEmpresas.csv')
    dEmpresas.to_csv(output_path, index=False, sep=';', decimal=',', encoding='utf-8-sig')
    print(f"SUCESSO: dEmpresas gerada com {len(dEmpresas)} linhas.\n")

if __name__ == "__main__":
    load_dempresas()