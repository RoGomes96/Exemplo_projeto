from datetime import datetime
import webbrowser
import os
import shutil
import time
from zipfile import ZipFile
import pandas as pd
from src.common.logger.logger import logger


def download_cvm_zip(currentMonth):
    url = f'https://dados.cvm.gov.br/dados/FI/DOC/INF_DIARIO/DADOS/inf_diario_fi_{currentMonth}.zip'

    webbrowser.open(url, new=2)


def get_cvm_csv_file():
    current_month = datetime.now().strftime("%Y%m")
    download_cvm_zip(current_month)
    cwd = os.getcwd()
    user_windows = os.getlogin()
    download_dir = f'C:/Users/{user_windows}/Downloads/'
    os.chdir(download_dir)
    m_path = os.path.join(download_dir)
    time.sleep(20)

    file_path_zip = 'inf_diario_fi_' + current_month + '.zip'
    error, attemps = 0, 1
    while error == 0:
        try:
            with ZipFile(file_path_zip, 'r') as zip:
                zip.extractall()
            dirCvmFile = f'{download_dir}inf_diario_fi{current_month}'
            error = 1
        except:
            attemps += 1
            time.sleep(20)
            if attemps > 4:  # seta o mes para o anterior para buscar os dados
                attemps = 1
                temp_date = datetime.now()
                temp_month, temp_year = temp_date.month, temp_date.year
                temp_year = str(
                    temp_year-1) if temp_month == 0 else str(temp_year)
                temp_month = '0' + \
                    str(temp_month) if temp_month <= 9 else str(temp_month)
                file_month = temp_year + temp_month
                file_path_zip = 'inf_diario_fi_' + current_month + '.zip'
                download_cvm_zip(file_month)
                logger(
                    f'The file {file_path_zip} was extracted')
            else:
                error = 3
                logger(f'CVM file not founded - Attemp #{attemps}')
    if error == 1:
        try:
            m_path = os.path.join(dirCvmFile)
            os.chdir(m_path)
        except:
            None
        file_path_csv = file_path_zip.replace('.zip', '.csv')
        df_cvm_csv = pd.read_csv(file_path_csv, sep=';')
        os.chdir(download_dir)
        os.remove(file_path_zip)
        if os.path.exists(dirCvmFile):
            try:
                shutil.rmtree(dirCvmFile)
            except:
                try:
                    os.remove(file_path_csv)
                except:
                    logger(
                        f'The file {dirCvmFile} could not be deleted from Downloads folder')
        os.chdir(cwd)
        cvm_csv_formated = (df_cvm_csv['CNPJ_FUNDO_CLASSE']
                            ).drop_duplicates().reset_index()
        dict_cvm = []
        for index, row in cvm_csv_formated.iterrows():
            Cnpj = row['CNPJ_FUNDO_CLASSE']
            temp_df = df_cvm_csv[df_cvm_csv['CNPJ_FUNDO_CLASSE']
                                 == Cnpj].sort_values(['DT_COMPTC'])
            temp_df.reset_index(drop=True, inplace=True)
            fund_cnpj = str(temp_df['CNPJ_FUNDO_CLASSE'].iloc[-1])
            fund_cnpj = fund_cnpj.replace('.', '').replace(
                '/', '').replace('-', '')
            dict_cvm.append({
                'TP_CLASS_FUNDS': temp_df['TP_FUNDO_CLASSE'].iloc[-1],
                'FUND_CNPJ': fund_cnpj,
                'DT_COMPTC': temp_df['DT_COMPTC'].iloc[-1],
                'TOTAL_VALUE': temp_df['VL_TOTAL'].iloc[-1],
                'QUOTA_VALUE': temp_df['VL_QUOTA'].iloc[-1],
                'LIQ_PATRIM_VALUE': temp_df['VL_PATRIM_LIQ'].iloc[-1],
                'DAY_CAPT': temp_df['CAPTC_DIA'].iloc[-1],
                'DAY_RESC': temp_df['RESG_DIA'].iloc[-1],
                'COTST_NUMBER': temp_df['NR_COTST'].iloc[-1]
            })
        df_cvm = pd.DataFrame(dict_cvm)
        return df_cvm
    else:
        logger(f'The {file_path_zip} ncould not be downloaded')

        return pd.DataFrame()
