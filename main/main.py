# Implementar o starter do projeto para inicializar com fastAPI

from src.infraestructure.extractions.data_lake import extracao_dados_datalake
from src.infraestructure.extractions.cvmFile import get_cvm_csv_file
from src.API.handler.handler import getApiData
df_data_lake = extracao_dados_datalake(referenceDate='20250408')
df_cvm = get_cvm_csv_file()
df_api = getApiData()
