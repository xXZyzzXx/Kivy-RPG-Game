# CONFIG

buildings = {'Хижина': [[None], 100, [60, 40, 0, 5], r"data/images/buildings/house.png", 'Социальные', ['Рабочий']],
             'Ратуша': [['Колесо', 'Дома'], 40, [30, 0, 5, 0], r"data/images/buildings/building_found.png",
                        'Социальные', ['Рабочий']],
             'Казармы': [['Военное дело'], 60, [20, 30, 400, 50], r"data/images/buildings/barracks.png", 'Военные',
                         ['Рабочий', 'Воин', 'Стрелок']],
             'Мастерская': [['Обработка дерева'], 20, [7400, 2200, 500, 388],
                            r"data/images/buildings/building_found.png", 'Производственные', ['Рабочий']],
             'Казармы1': [['Военное дело'], 60, [2000, 3000, 40000, 500000], r"data/images/buildings/barracks.png",
                          'Военные', ['Рабочий']],
             'Казармы2': [['Военное дело'], 60, [20, 30, 400, 50], r"data/images/buildings/barracks.png", 'Военные',
                          ['Рабочий']],
             'Казармы3': [['Военное дело'], 60, [20, 30, 400, 50], r"data/images/buildings/barracks.png", 'Военные',
                          ['Рабочий']],
             'Казармы4': [['Военное дело'], 60, [20, 30, 400, 50], r"data/images/buildings/barracks.png", 'Военные',
                          ['Рабочий']],
             }

type_colors = {'Социальные': (1, 1, .2, .7),
               'Военные': (1, .2, .8, .7),
               'Производственные': (.3, 1, .3, .7)}

units = {'Рабочий': [[None], 100, [60, 40, 0, 0], r"data/images/units/worker.png", 'Социальные'],
         'Воин': [[None], 150, [300, 10, 10, 0], r"data/images/units/warrior.png", 'Социальные'],
         'Стрелок': [[None], 20, [60, 20, 10, 15], r"data/images/units/shooter.png", 'Социальные']}

player_units = {'Рабочий': 0,
                'Воин': 0,
                'Стрелок': 0}

money = [20000, 20, r'data/images/res_icons/money.png']

resourses = {'Древесина': [50000, 510, r'data/images/res_icons/wood.png'],
             'Еда': [560, 10000, r'data/images/res_icons/food.png'],
             'Железо': [200, 0, r'data/images/res_icons/iron.png'],
             'Глина': [15500, 5550, r'data/images/res_icons/clay.png']}

prod_upgrades = {'Ирригация': [[250, 0, 0, 0], r'data/images/gui_elements/irrigation.jpg'],
                 'Новый инструмент': [[20, 0, 0, 0], r'data/images/gui_elements/building_tools.png'],
                 'Внедрение роботов': [[200, 0, 0, 0], r'data/images/gui_elements/robots.png'],
                 'Модернизация наносхем': [[15500, 0, 0, 0], r'data/images/gui_elements/microprocessor.png']}

player = {'Население': [100, 2, r"data/images/units/worker.png"]}

res = {'Деньги': [1550, 5550],
       'Древесина': [20000, 20],
       'Еда': [600, 0.2],
       'Железо': [70000, 0],
       'Глина': [20, 9970]}

sklad = 60000

empty_icon = r'data/images/gui_elements/empty_icon.png'

data_center = {'Защита': [r'data/images/gui_elements/data_center.png', [250, 250]],
               'Взлом': [r'data/images/gui_elements/hack.png'],
               'Разработка': [r'data/images/gui_elements/malware_main.png'],
               'Улучшения': [r'data/images/gui_elements/robots.png']}

empty_antivirus_tech = 'Пусто', r'data/images/gui_elements/empty_icon.png', '--|--|--'
current_antivirus_tech = empty_antivirus_tech

programs = {'Червь': [r'data/images/gui_elements/data_center.png', [250, 250], 'Видимый'],
            'Руткит': [r'data/images/gui_elements/microprocessor.png', [230, 22420], 'Скрытный'],
            'Логическая бомба': [r'data/images/gui_elements/building_tools.png', [5250, 23250], 'Видимый'],
            'Троян': [r'data/images/gui_elements/robots.png', [6333, 6322], 'Видимый']}

antimalware_upgrades = {'Стелс узел': [r'data/images/gui_elements/eye_crossed.png', [5350, 2230], [47, 1.8]],
               'Активный узел': [r'data/images/gui_elements/eye.png', [230, 22420], [56, 1.8]]}
'''
<BoxLayout>
    canvas.before:
        Color:
            rgba: 1, 1, 1, 1
        Line:
            width: 1
            rectangle: self.x, self.y, self.width, self.height
'''
