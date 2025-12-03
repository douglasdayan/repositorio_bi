import pandas as pd
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ENRICH_PATH = os.path.join(BASE_DIR, 'files', 'enrich')

def load_dcalendario():
    print("--- [LOAD] Gerando Dimensão: dCalendario ---")
    
    dates_list = []
    
    # 1. Lê Datas das Cotações
    if os.path.exists(os.path.join(ENRICH_PATH, 'fCotacoes.csv')):
        df_cot = pd.read_csv(os.path.join(ENRICH_PATH, 'fCotacoes.csv'), usecols=['dt_pregao'], sep=';')
        dates_list.append(pd.to_datetime(df_cot['dt_pregao']))

    # 2. Lê Datas de DADOS EXTERNOS (Novo nome)
    if os.path.exists(os.path.join(ENRICH_PATH, 'fDadosExternos.csv')):
        df_eco = pd.read_csv(os.path.join(ENRICH_PATH, 'fDadosExternos.csv'), usecols=['Data'], sep=';')
        dates_list.append(pd.to_datetime(df_eco['Data']))

    if not dates_list:
        print("ERRO: Nenhuma tabela fato encontrada em 'enrich'. Rode fCotacoes ou fDadosExternos primeiro.")
        sys.exit(1)

    # 3. Une todas as datas
    all_dates = pd.concat(dates_list).dropna().unique()
    min_date = all_dates.min()
    max_date = all_dates.max()

    if min_date.day > 1:
        min_date = min_date.replace(day=1)

    full_range = pd.date_range(start=min_date, end=max_date, freq='D')
    dCalendario = pd.DataFrame({'Date': full_range})

    # Atributos
    dCalendario['Ano'] = dCalendario['Date'].dt.year
    dCalendario['Mes'] = dCalendario['Date'].dt.month
    dCalendario['Trimestre'] = dCalendario['Date'].dt.quarter
    
    meses_pt = {
        1: 'Jan', 2: 'Fev', 3: 'Mar', 4: 'Abr', 5: 'Mai', 6: 'Jun', 
        7: 'Jul', 8: 'Ago', 9: 'Set', 10: 'Out', 11: 'Nov', 12: 'Dez'
    }
    dCalendario['MesNome'] = dCalendario['Mes'].map(meses_pt)
    
    # Colunas Auxiliares Power BI
    dCalendario['SortMesAno'] = dCalendario['Ano'] * 100 + dCalendario['Mes']
    dCalendario['MesAno'] = dCalendario['MesNome'] + "/" + dCalendario['Ano'].astype(str)

    output_path = os.path.join(ENRICH_PATH, 'dCalendario.csv')
    dCalendario.to_csv(output_path, index=False, sep=';', decimal=',', encoding='utf-8-sig')
    print(f"SUCESSO: dCalendario gerada de {min_date.date()} a {max_date.date()}.\n")

if __name__ == "__main__":
    load_dcalendario()