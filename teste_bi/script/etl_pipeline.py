import pandas as pd
import os
import sys
from datetime import datetime

# --- CONFIGURAÇÃO DE DIRETÓRIOS ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FILES_DIR = os.path.join(BASE_DIR, 'files')
INPUT_PATH = os.path.join(FILES_DIR, 'spreadsheets')
ENRICH_PATH = os.path.join(FILES_DIR, 'enrich')

os.makedirs(ENRICH_PATH, exist_ok=True)

class ETLProcess:
    def __init__(self):
        self.log("Iniciando ETL (fEconomia Diária Completa)...")

    def log(self, msg):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

    def load_csv(self, filename, sep=';', decimal=','):
        path = os.path.join(INPUT_PATH, filename)
        
        if not os.path.exists(path) or os.path.getsize(path) == 0:
            self.log(f"ERRO: Arquivo inexistente ou vazio: {path}")
            return None

        try:
            return pd.read_csv(path, sep=sep, encoding='utf-8', decimal=decimal)
        except UnicodeDecodeError:
            try:
                return pd.read_csv(path, sep=sep, encoding='latin1', decimal=decimal)
            except Exception as e:
                self.log(f"ERRO CRÍTICO ao ler {filename}: {e}")
                return None

    def clean_numeric_col(self, series):
        """Converte coluna para numérico, tratando erros como vazios."""
        if series.dtype == 'object':
            series = series.astype(str).str.replace(',', '.')
        return pd.to_numeric(series, errors='coerce')

    def run(self):
        # ---------------------------------------------------------
        # 1. CARREGAMENTO - MERCADO
        # ---------------------------------------------------------
        self.log("--- Carregando Arquivos ---")
        
        df_cotacoes = self.load_csv('cotacoes_bolsa.csv', sep=';', decimal='.') 
        df_emp_bolsa = self.load_csv('empresas_bolsa.csv')
        df_empresas = self.load_csv('df_empresas.csv')
        
        if df_cotacoes is None or df_emp_bolsa is None or df_empresas is None:
            self.log("ABORTANDO: Arquivos principais faltando.")
            sys.exit(1)

        df_ativ = self.load_csv('empresas_nivel_atividade.csv')
        df_porte = self.load_csv('empresas_porte.csv')
        df_saude = self.load_csv('empresas_saude_tributaria.csv')
        df_simples = self.load_csv('empresas_simples.csv')

        # ---------------------------------------------------------
        # 2. DIMENSÃO: dAtivo
        # ---------------------------------------------------------
        self.log("Gerando dAtivo...")
        dAtivo = df_emp_bolsa[['cd_acao', 'nm_empresa', 'vl_cnpj', 'setor_economico', 'subsetor', 'segmento']].copy()
        dAtivo.rename(columns={'vl_cnpj': 'cnpj', 'cd_acao': 'ticker'}, inplace=True)
        dAtivo = dAtivo.merge(df_empresas, on='cnpj', how='left')
        
        if df_ativ is not None: dAtivo = dAtivo.merge(df_ativ, on='cnpj', how='left')
        if df_porte is not None: dAtivo = dAtivo.merge(df_porte, on='cnpj', how='left')
        if df_saude is not None: dAtivo = dAtivo.merge(df_saude, on='cnpj', how='left')
        if df_simples is not None: dAtivo = dAtivo.merge(df_simples, on='cnpj', how='left')
        
        # Limpeza CNPJ
        dAtivo['cnpj'] = dAtivo['cnpj'].astype(str).str.replace(r'\.0$', '', regex=True).replace('nan', '')

        # ---------------------------------------------------------
        # 3. FATO: fCotacoes
        # ---------------------------------------------------------
        self.log("Gerando fCotacoes...")
        fCotacoes = df_cotacoes[df_cotacoes['tp_merc'] == 10].copy()
        fCotacoes['dt_pregao'] = pd.to_datetime(fCotacoes['dt_pregao'], format='%Y%m%d', errors='coerce')
        
        cols_fato = ['dt_pregao', 'cd_acao', 'vl_abertura', 'vl_maximo', 'vl_minimo', 'vl_fechamento', 'vl_volume', 'qt_tit_neg']
        fCotacoes = fCotacoes[cols_fato]
        fCotacoes.rename(columns={'cd_acao': 'ticker'}, inplace=True)

        # ---------------------------------------------------------
        # 4. MACROECONOMIA (Range Completo)
        # ---------------------------------------------------------
        self.log("Processando Economia (Estrutura Diária Completa)...")
        
        # 1. Define o intervalo exato solicitado
        start_date = '2010-01-01'
        end_date = '2022-10-21'
        full_dates = pd.date_range(start=start_date, end=end_date, freq='D')
        
        # Cria o esqueleto da tabela fEconomia
        fEconomia = pd.DataFrame({'Data': full_dates})

        # 2. Carrega os indicadores
        df_selic = self.load_csv('selic.csv')
        df_dolar = self.load_csv('cotacao_dolar.csv')
        df_ipca = self.load_csv('ipca.csv')

        # 3. Tratamento e Merge SELIC
        if df_selic is not None and not df_selic.empty:
            df_selic['Data'] = pd.to_datetime(df_selic['Data'], format='%d/%m/%Y', errors='coerce')
            df_selic.rename(columns={'% a.a.': 'Selic'}, inplace=True)
            df_selic['Selic'] = self.clean_numeric_col(df_selic['Selic'])
            # Left join mantém todos os dias do esqueleto, preenchendo com NaN onde não tem Selic (fds)
            fEconomia = fEconomia.merge(df_selic[['Data', 'Selic']], on='Data', how='left')

        # 4. Tratamento e Merge DÓLAR
        if df_dolar is not None and not df_dolar.empty:
            col_data = [c for c in df_dolar.columns if 'Data' in c][0]
            col_valor = [c for c in df_dolar.columns if 'venda' in c][0]
            
            df_dolar['Data'] = df_dolar[col_data].astype(str).str.split(' ').str[0]
            df_dolar['Data'] = pd.to_datetime(df_dolar['Data'], format='%d/%m/%Y', errors='coerce')
            df_dolar.rename(columns={col_valor: 'Dolar_Venda'}, inplace=True)
            df_dolar['Dolar_Venda'] = self.clean_numeric_col(df_dolar['Dolar_Venda'])
            
            fEconomia = fEconomia.merge(df_dolar[['Data', 'Dolar_Venda']], on='Data', how='left')

        # 5. Tratamento e Merge IPCA
        if df_ipca is not None and not df_ipca.empty:
            col_data = [c for c in df_ipca.columns if 'Data' in c][0]
            col_valor = [c for c in df_ipca.columns if '%' in c][0]
            
            df_ipca['Data'] = pd.to_datetime(df_ipca[col_data], format='%d/%m/%Y', errors='coerce')
            df_ipca.rename(columns={col_valor: 'IPCA_Mensal'}, inplace=True)
            df_ipca['IPCA_Mensal'] = self.clean_numeric_col(df_ipca['IPCA_Mensal'])
            
            fEconomia = fEconomia.merge(df_ipca[['Data', 'IPCA_Mensal']], on='Data', how='left')

        # Nota: Não fazemos fillna(0) ou ffill() aqui para não distorcer médias (AVERAGE ignora blanks)
        fEconomia.sort_values('Data', inplace=True)

        # ---------------------------------------------------------
        # 5. CALENDÁRIO MESTRE
        # ---------------------------------------------------------
        self.log("Gerando dCalendario...")
        dates_cot = fCotacoes['dt_pregao'] if not fCotacoes.empty else pd.Series(dtype='datetime64[ns]')
        dates_eco = fEconomia['Data'] if not fEconomia.empty else pd.Series(dtype='datetime64[ns]')
        
        all_unique_dates = pd.concat([dates_cot, dates_eco]).dropna().unique()
        
        if len(all_unique_dates) > 0:
            min_date = all_unique_dates.min()
            max_date = all_unique_dates.max()
            if min_date.day > 1: min_date = min_date.replace(day=1)

            full_range = pd.date_range(start=min_date, end=max_date, freq='D')
            
            dCalendario = pd.DataFrame({'Date': full_range})
            dCalendario['Ano'] = dCalendario['Date'].dt.year
            dCalendario['Mes'] = dCalendario['Date'].dt.month
            dCalendario['Trimestre'] = dCalendario['Date'].dt.quarter
            
            meses_pt = {
                1: 'Jan', 2: 'Fev', 3: 'Mar', 4: 'Abr', 5: 'Mai', 6: 'Jun', 
                7: 'Jul', 8: 'Ago', 9: 'Set', 10: 'Out', 11: 'Nov', 12: 'Dez'
            }
            dCalendario['MesNome'] = dCalendario['Mes'].map(meses_pt)
        else:
            dCalendario = pd.DataFrame(columns=['Date'])

        # ---------------------------------------------------------
        # 6. EXPORTAÇÃO
        # ---------------------------------------------------------
        self.log(f"Salvando CSVs em: {ENRICH_PATH}")
        csv_kwargs = {'index': False, 'sep': ';', 'decimal': ',', 'encoding': 'utf-8-sig'}

        dAtivo.to_csv(os.path.join(ENRICH_PATH, 'dAtivo.csv'), **csv_kwargs)
        fCotacoes.to_csv(os.path.join(ENRICH_PATH, 'fCotacoes.csv'), **csv_kwargs)
        fEconomia.to_csv(os.path.join(ENRICH_PATH, 'fEconomia.csv'), **csv_kwargs)
        dCalendario.to_csv(os.path.join(ENRICH_PATH, 'dCalendario.csv'), **csv_kwargs)

        self.log("Sucesso! ETL Finalizado.")

if __name__ == "__main__":
    ETLProcess().run()