import pandas as pd
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TARGET_PATH = os.path.join(BASE_DIR, 'files', 'enrich')

def load_dcalendario():
    dates_list = []
    
    files_map = {
        'fCotacoes.csv': 'dt_pregao',
        'fDadosExternos.csv': 'Data'
    }

    for file_name, file_col in files_map.items():
        input_path = os.path.join(TARGET_PATH, file_name)
        output_path = os.path.join(TARGET_PATH, 'dCalendario.csv')

        if not os.path.exists(input_path):
            print(f"{file_name} não encontrado.")
            continue

        if os.path.exists(input_path):
            df = pd.read_csv(input_path, usecols=[file_col], sep=';')
            dates_list.append(pd.to_datetime(df[file_col]))

        if not dates_list:
            print("ERRO: Nenhuma tabela fato encontrada. Rode o script das fatos primeiro.")
            sys.exit(1)

    all_dates = pd.concat(dates_list).dropna().unique()
    min_date = all_dates.min()
    max_date = all_dates.max()

    if min_date.day > 1:
        min_date = min_date.replace(day=1)

    full_range = pd.date_range(start=min_date, end=max_date, freq='D')
    dCalendario = pd.DataFrame({'Date': full_range})

    dCalendario['Ano'] = dCalendario['Date'].dt.year
    dCalendario['Mes'] = dCalendario['Date'].dt.month
    dCalendario['Trimestre'] = dCalendario['Date'].dt.quarter

    meses_pt = {
        1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril', 5: 'Maio', 6: 'Junho', 
        7: 'Julho', 8: 'Agosto', 9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'
    }
    dCalendario['MesNome'] = dCalendario['Mes'].map(meses_pt)

    dCalendario.to_csv(output_path, index=False, sep=';', decimal=',', encoding='utf-8-sig')
    print(f"dCalendario gerada de {min_date.date()} à {max_date.date()}.\n")

if __name__ == "__main__":
    load_dcalendario()