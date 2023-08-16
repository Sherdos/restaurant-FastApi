import uuid

import pandas as pd

from src.menu.repositories import DishRepository, MenuRepository, SubmenuRepository

PRE_MENU = 'admin/MenuPre.xlsx'
MENU = 'admin/Menu.xlsx'


def from_xlsx_to_dict() -> tuple[list, list, list]:
    data_frame = pd.read_excel(MENU)
    data = pr(data_frame)
    menu_structure = []
    submenu_structure = []
    dish_structure = []

    for index, row in data.iterrows():
        menu_id = row['Unnamed: 0']
        submenu_id = row['Unnamed: 1']
        dish_id = row['Unnamed: 2']

        if pd.notna(menu_id):
            menu = {
                'id': uuid.uuid4() if row['Unnamed: 7'] == 'C' else menu_id,
                'title': submenu_id,
                'description': dish_id,
                'move': row['Unnamed: 7']
            }
            menu_structure.append(menu)
        elif pd.notna(submenu_id):
            submenu = {
                'id': uuid.uuid4() if row['Unnamed: 7'] == 'C' else submenu_id,
                'title': dish_id,
                'description': row['Unnamed: 3'],
                'menu_id': menu_structure[-1]['id'],
                'move': 'D' if menu_structure[-1]['move'] == 'D' else row['Unnamed: 7']
            }
            submenu_structure.append(submenu)
        elif pd.notna(dish_id):
            dish = {
                'id': uuid.uuid4() if row['Unnamed: 7'] == 'C' else dish_id,
                'title': row['Unnamed: 3'],
                'description': row['Unnamed: 4'],
                'price': str(row['Unnamed: 5']),
                'submenu_id': submenu_structure[-1]['id'],
                'move': 'D' if submenu_structure[-1]['move'] == 'D' else row['Unnamed: 7']
            }
            dish_structure.append(dish)
    return menu_structure, submenu_structure, dish_structure


def get_reposytory(index: int):
    if index == 0:
        return MenuRepository
    elif index == 1:
        return SubmenuRepository
    elif index == 2:
        return DishRepository


def pr(current_data: pd.DataFrame):
    # Загрузка предыдущей и текущей версии данных
    try:
        previous_data = pd.read_excel(PRE_MENU)
    except FileNotFoundError:
        previous_data = pd.DataFrame()

    # Вызов функции для обозначения изменений
    return mark_changes(previous_data, current_data)


def is_not_na(data: pd.DataFrame):
    return data['Unnamed: 0'].notna() | data['Unnamed: 1'].notna() | data['Unnamed: 2'].notna()


def mark_changes(previous_data: pd.DataFrame, current_data: pd.DataFrame):
    added_rows = current_data[~current_data.isin(previous_data)]
    updated_rows = current_data[current_data.isin(previous_data)]
    deleted_rows = previous_data[~previous_data.isin(current_data)]

    added_rows['Unnamed: 7'] = 'C'
    updated_rows['Unnamed: 7'] = 'U'
    deleted_rows['Unnamed: 7'] = 'D'
    print(updated_rows)
    data_frame = pd.concat([previous_data, added_rows, updated_rows, deleted_rows], ignore_index=True)
    return data_frame
