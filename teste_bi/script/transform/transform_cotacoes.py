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

        mapa_mercado = {
            10: 'Vista (Padrão)',
            70: 'Opções de Compra',
            80: 'Opções de Venda'
        }
        df['tipo_mercado_desc'] = df['tp_merc'].map(mapa_mercado).fillna('Outros')

        cols_uteis = [
            'dt_pregao', 'cd_acao', 'cd_acao_rdz', 'tp_merc', 'tipo_mercado_desc',
            'vl_abertura', 'vl_maximo', 'vl_minimo', 'vl_fechamento', 
            'vl_volume', 'qt_tit_neg'
        ]
        
        df = df[cols_uteis]
        df.to_csv(output_path, index=False, sep=';', decimal=',', encoding='utf-8')
        print(f"transform_cotacoes.csv gerado com {len(df)} linhas.")

    except Exception as e:
        print(f"ERRO Crítico em Cotações: {e}")

if __name__ == "__main__":
    transform_cotacoes()