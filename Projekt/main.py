import json
import pandas as pd

from config import RAZREDI, ROOT_DIR
import groups

TRANSFORM_ZAKLJUCNE_OCJENE = {
    'Učenik': lambda x: x.split(".")[1].strip()
}

UCENICI = set()
PREDMETI = set()
GRUPE = groups.__all__

razredi = (5, 6, 7)
replace_chars = {
    ' - ': '_',
    '(': '_',
    ')': '',
    ' ': '_',

    'č': 'c',
    'ć': 'c',
    'ž': 'z',
    'š': 's',
    'đ': 'dj',
    'dž': 'dz'
}

def get_renamed_columns(columns):
    for i, _ in enumerate(columns):
        columns[i] = columns[i].lower()
        for char, value in replace_chars.items():
            columns[i] = columns[i].replace(char, value)
    return columns


def read_json_to_dict(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        json_string = f.read()
        if json_string:
            return json.loads(json_string)
        return {}

def write_objs_to_json(df, type_name='students'):
    dictionary = read_json_to_dict(ROOT_DIR / 'json' / (type_name + '.json'))
    
    objs = None
    if type_name == 'students':
        UCENICI.update(dictionary.keys())
        UCENICI.update(df['Učenik'].unique())
        objs = {student: i for i, student in enumerate(sorted(UCENICI))}
    elif type_name == 'subjects':
        PREDMETI.update(dictionary.keys())
        PREDMETI.update(df.columns)
        objs = {subject: i for i, subject in enumerate(sorted(PREDMETI))}

    with open(ROOT_DIR / 'json' / (type_name + '.json'), 'w', encoding='utf-8') as f:
        json.dump(objs, f, indent=4, ensure_ascii=False)

def write_razred_df(df, razred):
    razred_filename = '_'.join((razred['name'], razred['year'] + '.csv'))
    df.to_csv(ROOT_DIR / 'csv' / razred_filename)


def get_joined_dataset(*dfs):
    dfs = list(dfs)
    for i, df in enumerate(dfs):
        dfs[i] = df.set_index('ucenik')
        dfs[i] = dfs[i].sort_index()
    
    main_df = dfs[0]
    joined_df = main_df.join(dfs[1:])
    return joined_df.fillna(0)


def rename_df(df):
    cols = df.columns.tolist()
    renamed_cols = get_renamed_columns(cols)
    df.columns = renamed_cols
    return df


def get_razred_df(razred):
    izostanci_df = pd.read_excel(razred['files'][0])
    vladanje_df = pd.read_excel(razred['files'][1])
    ocjene_df = pd.read_excel(razred['files'][2])

    for key, func in TRANSFORM_ZAKLJUCNE_OCJENE.items():
        ocjene_df[key] = ocjene_df[key].transform(func)
    
    izostanci_df['Učenik'] = izostanci_df['Ime'] + " " + izostanci_df['Prezime']
    izostanci_df['Broj Izostanaka'] = izostanci_df['Ukupno']
    vladanje_df['Vladanje'] = vladanje_df['Ocjena']  

    for group in GRUPE:
        subjects = group['subjects']
        for subject in group['subjects']:
            if subject not in ocjene_df.columns:
                subjects.remove(subject)
        
        ocjene_df[group['name']] = ocjene_df[subjects].sum()
    
    write_objs_to_json(ocjene_df, type_name='students') 
    write_objs_to_json(ocjene_df, type_name='subjects')
    
    izostanci_df = rename_df(izostanci_df)
    vladanje_df = rename_df(vladanje_df)
    ocjene_df = rename_df(ocjene_df)

    output_df = get_joined_dataset(ocjene_df, vladanje_df, izostanci_df)
    cols = [
        'vladanje', 'broj_izostanaka',
        'nastup', 'natjecanje', 'sportski_dopust',
        'srednja_ocjena', 'opci_uspjeh'
    ]
    return output_df[cols]



def main():
    numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']

    df_list = []
    for razred in RAZREDI:
        df = get_razred_df(razred)
        if df is not None:
            write_razred_df(df, razred)
            df_list.append(df)
    
    df = pd.concat(df_list, join='inner', sort=False)
    df = df.select_dtypes(include=numerics)

    grouped_df = df.groupby('ucenik')
    write_razred_df(grouped_df.aggregate(sum), razred={'name': 'AGG', 'year': '2021'})
    

if __name__ == '__main__':
    main()