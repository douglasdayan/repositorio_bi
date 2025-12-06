import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SOURCE_PATH = os.path.join(BASE_DIR, 'files', 'raw')
TARGET_PATH = os.path.join(BASE_DIR, 'files', 'clean')

def transform_cotacoes():
    
    input_path = os.path.join(SOURCE_PATH, 'extract_cotacoes.csv')
    output_path = os.path.join(TARGET_PATH, 'transform_cotacoes.csv')

    if not os.path.exists(input_path):
        print("extract_cotacoes.csv não encontrado.")
        return

    try:
        df = pd.read_csv(input_path, sep=';', decimal=',', encoding='utf-8')
        df['dt_pregao'] = pd.to_datetime(df['dt_pregao'], format='%Y%m%d', errors='coerce')

        df = df[df['dt_pregao'] >= '2022-01-01'].copy()
        
        eventos = [
            {'cd_acao': 'GFSA3', 'data_ex': '2022-09-23', 'fator': 9.0},
        ]

        df_eventos = pd.DataFrame(eventos)
        df_eventos['data_ex'] = pd.to_datetime(df_eventos['data_ex'])
        
        df = df.merge(df_eventos, on='cd_acao', how='left')
        df['fator'] = df['fator'].fillna(1.0)
        
        mask_ajuste = df['dt_pregao'] < df['data_ex']
        cols_preco = ['vl_abertura', 'vl_maximo', 'vl_minimo', 'vl_fechamento']
        
        for col in cols_preco:
            df.loc[mask_ajuste, col] = df.loc[mask_ajuste, col] * df.loc[mask_ajuste, 'fator']
        
        df.drop(columns=['data_ex', 'fator'], inplace=True)

        mapa_mercado = {
            10: 'Mercado à Vista',
            70: 'Opção de Compra',
            80: 'Opção de Venda'
        }
        df['tipo_mercado_desc'] = df['tp_merc'].map(mapa_mercado).fillna('Outros')

        cols_uteis = [
            'dt_pregao', 'cd_acao', 'cd_acao_rdz', 'tp_merc', 'tipo_mercado_desc',
            'vl_abertura', 'vl_maximo', 'vl_minimo', 'vl_fechamento', 
            'vl_volume', 'qt_tit_neg'
        ]
        
        cols_finais = [c for c in cols_uteis if c in df.columns]
        df = df[cols_finais]

        df.to_csv(output_path, index=False, sep=';', decimal=',', encoding='utf-8')
        print(f"transform_cotacoes.csv gerado com {len(df)} linhas.")

    except Exception as e:
        print(f"Erro em Cotações: {e}")

if __name__ == "__main__":
    transform_cotacoes()