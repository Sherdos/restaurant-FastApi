import pandas as pd

data_frame = pd.read_excel('admin/Menu.xlsx')
menu_title = data_frame[data_frame['Меню'].notna() & data_frame.loc[data_frame["Age"] > 35, "Name"] ]
print(menu_title)