import pandas as pd
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CLEAN_PATH = os.path.join(BASE_DIR, 'files', 'clean')
ENRICH_PATH = os.path.join(BASE_DIR, 'files', 'enrich')

def load_fdados_externos():
    print("--- [LOAD] Gerando Fato: fDadosExternos (Série Diária) ---")
    
    # 1. Cria o esqueleto diário completo
    start_date = '2010-01-01'
    end_date = '2022-10-21'
    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    fDadosExternos = pd.DataFrame({'Data': dates})

    # 2. Carrega indicadores limpos
    try:
        df_selic = pd.read_csv(os.path.join(CLEAN_PATH, 'clean_selic.csv'), sep=';', decimal=',')
        df_dolar = pd.read_csv(os.path.join(CLEAN_PATH, 'clean_dolar.csv'), sep=';', decimal=',')
        df_ipca = pd.read_csv(os.path.join(CLEAN_PATH, 'clean_ipca.csv'), sep=';', decimal=',')

        df_selic['Data'] = pd.to_datetime(df_selic['Data'])
        df_dolar['Data'] = pd.to_datetime(df_dolar['Data'])
        df_ipca['Data'] = pd.to_datetime(df_ipca['Data'])

        # 3. Merges
        fDadosExternos = fDadosExternos.merge(df_selic, on='Data', how='left')
        fDadosExternos = fDadosExternos.merge(df_dolar, on='Data', how='left')
        fDadosExternos = fDadosExternos.merge(df_ipca, on='Data', how='left')

    except Exception as e:
        print(f"ERRO ao processar indicadores: {e}")
        sys.exit(1)

    # 4. Salva como fDadosExternos.csv
    output_path = os.path.join(ENRICH_PATH, 'fDadosExternos.csv')
    fDadosExternos.to_csv(output_path, index=False, sep=';', decimal=',', encoding='utf-8-sig')
    print(f"SUCESSO: fDadosExternos gerada de {start_date} a {end_date}.\n")

if __name__ == "__main__":
    load_fdados_externos()