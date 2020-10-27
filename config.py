# CONFIG

buildings = {'Сервера': [[None], 100, [60, 0, 1000], r"data/images/buildings/servers.png", 'Социальные', ['Рабочий']],
             'Хижина': [[None], 100, [60, 40, 0], r"data/images/buildings/house.png", 'Социальные', ['Рабочий']],
             'Ратуша': [['Колесо', 'Дома'], 40, [30, 0, 5], r"data/images/buildings/building_found.png",
                        'Социальные', ['Рабочий']],
             'Казармы': [['Военное дело'], 60, [20, 30, 400], r"data/images/buildings/barracks.png", 'Военные',
                         ['Рабочий', 'Воин', 'Стрелок']],
             'Мастерская': [['Обработка дерева'], 20, [7400, 2200, 50],
                            r"data/images/buildings/building_found.png", 'Производственные', ['Рабочий']],
             'Казармы1': [['Военное дело'], 60, [2000, 3000, 40000], r"data/images/buildings/barracks.png",
                          'Военные', ['Рабочий']],
             'Казармы2': [['Военное дело'], 60, [20, 30, 400], r"data/images/buildings/barracks.png", 'Военные',
                          ['Рабочий']],
             'Казармы3': [['Военное дело'], 60, [20, 30, 400], r"data/images/buildings/barracks.png", 'Военные',
                          ['Рабочий']],
             'Казармы4': [['Военное дело'], 60, [20, 30, 400], r"data/images/buildings/barracks.png", 'Военные',
                          ['Рабочий']],
             }

type_colors = {'Социальные': (1, 1, .2, .7),
               'Военные': (1, .2, .8, .7),
               'Производственные': (.3, 1, .3, .7)}

units = {'Рабочий': [[None], 100, [60, 40, 0], r"data/images/units/worker.png", 'Социальные'],
         'Воин': [[None], 150, [300, 10, 10], r"data/images/units/warrior.png", 'Социальные'],
         'Стрелок': [[None], 20, [60, 20, 10], r"data/images/units/shooter.png", 'Социальные']}

player_units = {'Рабочий': 1,
                'Воин': 20,
                'Стрелок': 5}

money = [20000, 20, r'data/images/res_icons/bitcoin.png']
people = [35, 2, r'data/images/res_icons/worker.png']
mutagen = [220, 15, r'data/images/res_icons/malware.png']
science = [220, 15, r'data/images/res_icons/kolba.png']
rare_materials = [8, r'data/images/res_icons/rare.png']
malware_points = [15, r'data/images/res_icons/malware-point.png']
energy_slots = [20, 5, r'data/images/res_icons/slots.png']

resources = {'Электричество': [200, 0, r'data/images/res_icons/lighting.png', 500],
             'Еда': [250, 0, r'data/images/res_icons/food.png', 500],
             'Сырьевые ресурсы': [1000, 15, r'data/images/res_icons/iron.png', 6000],
             }

prod_upgrades = {'Ирригация': [[250, 0, 0, 0], r'data/images/gui_elements/irrigation.jpg'],
                 'Новый инструмент': [[20, 0, 0, 0], r'data/images/gui_elements/building_tools.png'],
                 'Внедрение роботов': [[200, 0, 0, 0], r'data/images/gui_elements/robots.png'],
                 'Модернизация наносхем': [[15500, 0, 0, 0], r'data/images/gui_elements/microprocessor.png']}

player = {'Население': [100, 2, r"data/images/units/worker.png"]}

resourses_generation = {'main_base': {'Электричество': 500, 'Еда': 500, 'Сырьевые ресурсы': 0}}

res = {'Деньги': [1550, 5550],
       'Древесина': [20000, 20],
       'Еда': [600, 0.2],
       'Железо': [70000, 0],
       'Глина': [20, 9970]}

sklad = 1000

empty_icon = r'data/images/gui_elements/empty_icon.png'

stealh_default = 250
active_default = 350
percent_amount = 10

data_center = {'Защита': [r'data/images/gui_elements/data_center.png', [stealh_default, stealh_default, 5],
                          [active_default, active_default, 0]],
               'Взлом': [r'data/images/gui_elements/malvare_icon.zip'],
               'Разработка': [r'data/images/gui_elements/malware_main.png'],
               'Улучшения': [r'data/images/gui_elements/robots.png']}

empty_antivirus_tech = 'Пусто', r'data/images/gui_elements/empty_icon.png', '--|--|--'
current_antivirus_tech = empty_antivirus_tech

programs = {'Червь': [r'data/images/gui_elements/data_center.png', [250, 250], 'Видимый', 3],
            'Руткит': [r'data/images/gui_elements/microprocessor.png', [230, 22420], 'Скрытный', 5],
            'Логическая бомба': [r'data/images/gui_elements/disketa.png', [5250, 23250], 'Видимый', 2],
            'Троян': [r'data/images/gui_elements/robots.png', [6333, 6322], 'Видимый', 1]}

antimalware_upgrades = {'Стелс узел': [r'data/images/gui_elements/eye_crossed.png', [5350, 2230], [47, 1.8], 0],
                        'Активный узел': [r'data/images/gui_elements/eye.png', [230, 22420], [56, 1.8], 0]}

descriptions = {'Защита от взлома': 'При защите от хакерских атак  противников предусмотрено два режима работы '
                                    'фаервола: для обнаружения скрытных атак и для противодействия прямому вторжению '
                                    'в систему. Выбрав нужный режим для подавления компьютерной мощи противника он '
                                    'вступит в силу через три хода, постепенно набирая влияние на систему. Включённый '
                                    'режим постепенно увеличивает процент, который будет добавлен к текущей выбранной '
                                    'защите, пока не достигнет своего максимума. Увеличить процент защиты можно '
                                    'улучшением выбранной области. При смене режимов бонус фаервола сбрасывается до '
                                    'нуля и восстанавливается заново.'}


player_programs = {'Червь': 0,
                   'Руткит': 1,
                   'Логическая бомба': 0,
                   'Троян': 0}

city_list = []
current_city = None
map_units = []
map_gui_list = []

programs_max = 15

queue_list = []
city_info_labels = []

SCALING = .5

TILE_WIDTH = 256
TILE_HEIGHT = 149
TILE_Z = 10

MW = 25
MH = 50


selected_unit = None
game = None
current_player = None
# TODO: Добавить словари со стоимостью, харастеристикой и прочим в словаре всех юнитов и программ

'''
<BoxLayout>
    canvas.before:
        Color:
            rgba: 1, 1, 1, 1
        Line:
            width: 1
            rectangle: self.x, self.y, self.width, self.height
<RelativeLayout>
    canvas.before:
        Color:
            rgba: 1, 1, 1, 1
        Line:
            width: 1
            rectangle: 0, 0, self.width, self.height
'''

