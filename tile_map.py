from pytmx import TiledMap

TILE_WIDTH = 256
TILE_HEIGHT = 149


class MyMap:
    def __init__(self):
        self.tmxdata = TiledMap("data/maps/first.tmx")
        self.map_width = self.tmxdata.width
        self.map_height = self.tmxdata.height
        self.tile_width = self.tmxdata.tilewidth
        self.tile_height = self.tmxdata.tileheight
        self.floor_list = self.get_tile_info('floor')
        self.items_list = self.get_tile_info('items')
        self.city_list = self.get_tile_info('city')
        self.layers = [self.floor_list, self.items_list, self.city_list]

    def get_tile_info(self, name, scaling=.5):
        tiles_list = []
        layer = self.tmxdata.get_layer_by_name(name)
        for column_index, row_index, image in layer.tiles():
            tile = Tile()
            tile.column_index = column_index
            tile.row_index = row_index
            if row_index % 2 == 0:
                tile.center_x = column_index * (TILE_WIDTH * scaling)
                tile.center_y = (self.map_height - row_index - 1) * ((TILE_HEIGHT * scaling) / 2)
            else:
                tile.center_x = column_index * (TILE_WIDTH * scaling) + ((TILE_WIDTH * scaling) / 2)
                tile.center_y = (self.map_height - row_index-1) * ((TILE_HEIGHT * scaling) / 2)
            tile.width = self.tile_width * scaling
            tile.height = self.tile_height * scaling+10
            tile.image = str(image[0])
            tiles_list.append(tile)
        return tiles_list


class Tile:
    def __init__(self):
        self.column_index = None
        self.row_index = None
        self.center_x = None
        self.center_y = None
        self.height = None
        self.width = None
        self.image = None
