import pandas as pd


def extractTextFromTextFile(file):
    text = []
    if file[-3:] in ['TXT', 'txt', 'csv', 'CSV']:
        with open(file, encoding='utf-8') as f:
            text = f.readlines()
    elif file[-3:] in ['XLS', 'xls'] or file[-4:] in ['XLSX', 'xlsx']:
        df = pd.read_excel(file, dtype=str, header=None)
        print(df)
        text = [' - '.join(x) for x in df.values.tolist()]
        print(text)
    return text