# Game properties
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
        self.science = 0
        self.mutagen = 0
        self.malware_points = 8
        self.rare_materials = 5
        self.energy_slots = 10
        self.mutantcoin = config.money
        self.programs_max = config.programs_max
        self.player = player

    def add_city(self, pos, name='Default'):
        city = City(pos, name)
        self.pre_cities.append(city)


class City:
    def __init__(self, pos, name):
        self.pos = pos
        self.name = name
