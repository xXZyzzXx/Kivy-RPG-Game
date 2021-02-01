# Game properties, инициализация игры и игроков
import config


class Game:
    def __init__(self):
        self.turn = 0
        self.map = None
        self.teams = None
        self.players = []


class Player:
    def __init__(self, player=False):
        self.name = None
        self.current_city = None
        self.team = None
        self.era = 'Эпоха упадка'
        self.pre_cities = []
        self.cities = []
        self.technologies = []
        self.programs = config.player_programs
        self.units = config.player_units
        self.resources = config.resources  # resources
        self.buildings = []
        self.science = config.science
        self.mutagen = config.mutagen
        self.people = config.people
        self.malware_points = config.malware_points
        self.rare_materials = config.rare_materials
        self.energy_slots = config.energy_slots
        self.mutantcoin = config.money
        self.programs_max = config.programs_max
        self.player = player
        self.selected_unit = None
        self.map_units = []

    def add_city(self, pos, name='Default'):
        city = City(pos, name)
        self.pre_cities.append(city)


class City:
    def __init__(self, pos, name):
        self.pos = pos
        self.name = name
