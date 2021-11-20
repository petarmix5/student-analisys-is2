from pathlib import Path

ROOT_DIR = Path("C:\\Users\\AndreaHrelja\\Documents\\Faks\\IS2\\Završni\\Projekt\\data")

RAZRED_5 = [
    ROOT_DIR / Path("raw/5c_2018-2019_izostanci.xls"),
    ROOT_DIR / Path("raw/5c_2018-2019_vladanje-pedagoske-mjere.xls"),
    ROOT_DIR / Path("raw/5c_2018-2019_zakljucne-ocjene.xls"),
]

RAZRED_6 = [
    ROOT_DIR / Path("raw/6c_2019-2020_izostanci.xls"),
    ROOT_DIR / Path("raw/6c_2019-2020_vladanje-pedagoske-mjere.xls"),
    ROOT_DIR / Path("raw/6c_2019-2020_zakljucne-ocjene.xls"),
]

RAZRED_7 = [
    ROOT_DIR / Path("raw/7c_2020-2021_izostanci.xls"),
    ROOT_DIR / Path("raw/7c_2020-2021_vladanje-pedagoske-mjere.xls"),
    ROOT_DIR / Path("raw/7c_2020-2021_zakljucne-ocjene.xls"),
]

RAZREDI = [
    {
        'name': '5c',
        'year': '2018-2019',
        'files': RAZRED_5
    },
    {
        'name': '6c',
        'year': '2019-2020',
        'files': RAZRED_6
    },
    {
        'name': '7c',
        'year': '2020-2021',
        'files': RAZRED_7   
    }
]