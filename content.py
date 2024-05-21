import pandas as pd
import numpy as np

from app.models import Field, FieldType, FieldValue


def get_database_data(filename: str):
    df = pd.read_excel(filename, engine='openpyxl')
    list_of_dicts = [dict(zip(df.columns, [item.item() if isinstance(item, np.generic) else item for item in row]))
                     for row in df.values]
    return list_of_dicts


db_data = get_database_data('databases/domophon.xlsx')

monitors = ['4', '5', '7']
fingerprint = ['Да', 'Нет']
monitor_size = ['4.3', '7']
price_range = ['До 500', 'До 1000', 'До 2000', 'Более 2000']

monitors_content = [FieldValue(id=idx, name=name) for idx, name in enumerate(monitors)]
fingerprint_content = [FieldValue(id=idx, name=name) for idx, name in enumerate(fingerprint)]
monitor_size_content = [FieldValue(id=idx, name=name) for idx, name in enumerate(monitor_size)]
price_range_content = [FieldValue(id=idx, name=name) for idx, name in enumerate(price_range)]

fields = [
    Field(id=1, description="Какое количество мониторов?", name='Количество мониторов', content=monitors_content, type=FieldType.ENUM),
    Field(id=2, description="Нужна ли функция отпечатка пальца?", name='Функция отпечатка пальца', content=fingerprint_content, type=FieldType.ENUM),
    Field(id=3, description="Какой размер монитора в дюймах?", name='Размер монитора в дюймах', content=monitor_size_content, type=FieldType.ENUM),
    Field(id=4, description="Какой диапозон цен?", name='Цена', content=price_range_content, type=FieldType.ENUM),
    Field(id=5, description="Какое количество семей?", name='Количество семей', content=[], type=FieldType.TEXT)
]
