import datetime


def logger(texto):
    data_log = datetime.datetime.now().strftime('%Y-%m-%d %H:M')
    print(f'[{data_log}] {texto}')
