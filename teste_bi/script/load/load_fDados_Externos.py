import pandas as pd
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SOURCE_PATH = os.path.join(BASE_DIR, 'files', 'clean')
TARGET_PATH = os.path.join(BASE_DIR, 'files', 'enrich')

def load_fdados_externos():
    start_date = '2022-01-01'
    end_date = '2022-10-21'
    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    fDadosExternos = pd.DataFrame({'Data': dates})

    try:
        df_selic = pd.read_csv(os.path.join(SOURCE_PATH, 'transform_selic.csv'), sep=';', decimal=',')
        df_dolar = pd.read_csv(os.path.join(SOURCE_PATH, 'transform_dolar.csv'), sep=';', decimal=',')
        df_ipca = pd.read_csv(os.path.join(SOURCE_PATH, 'transform_ipca.csv'), sep=';', decimal=',')

        df_selic['Data'] = pd.to_datetime(df_selic['Data'])
        df_dolar['Data'] = pd.to_datetime(df_dolar['Data'])
        df_ipca['Data'] = pd.to_datetime(df_ipca['Data'])

        fDadosExternos = fDadosExternos.merge(df_selic, on='Data', how='left')
        fDadosExternos = fDadosExternos.merge(df_dolar, on='Data', how='left')
        fDadosExternos = fDadosExternos.merge(df_ipca, on='Data', how='left')

    except Exception as e:
        print(f"Erro ao processar indicadores: {e}")
        sys.exit(1)

    output_path = os.path.join(TARGET_PATH, 'fDadosExternos.csv')
    fDadosExternos.to_csv(output_path, index=False, sep=';', decimal=',', encoding='utf-8-sig')
    print(f"fDadosExternos gerada de {start_date} a {end_date}.\n")

if __name__ == "__main__":
    load_fdados_externos()