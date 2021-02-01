import config
from pytmx import TiledMap

TILE_WIDTH = config.TILE_WIDTH
TILE_HEIGHT = config.TILE_HEIGHT


class MyMap:
    def __init__(self, source="data/maps/first.tmx"):
        self.source = source
        self.players = 2
        self.tmxdata = TiledMap(source)
        self.map_width = self.tmxdata.width
        self.map_height = self.tmxdata.height
        self.tile_width = self.tmxdata.tilewidth
        self.tile_height = self.tmxdata.tileheight
        self.floor_list = self.get_tile_info('floor')
        self.objects_list = self.get_tile_info('items')
        self.city_list = self.get_tile_info('city')
        self.screen = r'data/maps/map_screen.png'
        self.layers = [self.floor_list, self.objects_list, self.city_list]

    def get_tile_info(self, name, scaling=config.SCALING):
        tiles_list = []
        layer = self.tmxdata.get_layer_by_name(name)
        for column_index, row_index, image in layer.tiles():
            tile = Tile()
            if row_index % 2 == 0:
                tile.x = column_index * (TILE_WIDTH * scaling)
                tile.y = (self.map_height - row_index - 1) * ((TILE_HEIGHT * scaling) / 2)
            else:
                tile.x = column_index * (TILE_WIDTH * scaling) + ((TILE_WIDTH * scaling) / 2)
                tile.y = (self.map_height - row_index - 1) * ((TILE_HEIGHT * scaling) / 2)
            tile.coordinates = (column_index, row_index)
            tile.column_index = column_index
            tile.row_index = row_index
            tile.width = self.tile_width * scaling
            tile.height = self.tile_height * scaling + 10 * config.SCALING
            tile.image = str(image[0])
            tiles_list.append(tile)
        return tiles_list


class Tile:
    def __init__(self):
        self.type = 'tile'
        self.coordinates = None
        self.column_index = None  # Можно убрать
        self.row_index = None
        self.center_x = None
        self.center_y = None
        self.height = None
        self.width = None
        self.image = None
        self.x = None
        self.y = None
