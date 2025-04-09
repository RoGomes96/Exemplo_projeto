from src.common.constants import apiUrl, apiHeader
import requests


def getApiData():
    response = requests.get(apiUrl, headers=apiHeader)
    print(response.text)
    return response.text
