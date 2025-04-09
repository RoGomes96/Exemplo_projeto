from datetime import datetime, timedelta
from src.common.constants import tableExample, databricksToken, hostnameDatabricks, pathWarehouse
from databricks import sql
import pandas as pd


def extracao_dados_datalake(referenceDate):
    referenceDate = datetime.strptime(referenceDate, '%Y-%m-%d')
    inicialDate = referenceDate - timedelta(days=30)
    querySQL = f"""
    SELECT Coluna1 AS Col1, Coluna2 As Col2 FROM {tableExample} where CAST(refereceDate as Date = {inicialDate})"""
    connectionTimeOut = 2000
    conn = sql.connect(
        serverHostname=hostnameDatabricks,
        htppPath=pathWarehouse,
        acessToken=databricksToken,
        connectionTimeOut=connectionTimeOut
    )
    resultDf = pd.read_sql(querySQL, conn)
    return resultDf
