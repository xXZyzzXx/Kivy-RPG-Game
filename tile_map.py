from pytmx import TiledMap
import config

TILE_WIDTH = config.TILE_WIDTH
TILE_HEIGHT = config.TILE_HEIGHT

'''
def get_screen_coordinates(tile_x, tile_y, width=mw, height=mh, tilewidth=TILE_WIDTH, tileheight=TILE_HEIGHT):
    screen_x = tilewidth * tile_x // 2 + height * tilewidth // 2 - tile_y * tilewidth // 2
    screen_y = (height - tile_y - 1) * tileheight // 2 + width * tileheight // 2 - tile_x * tileheight // 2
    return screen_x, screen_y


def screen_to_isometric_grid(cartX, cartY):
    screenx = mh - cartY / (TILE_HEIGHT * SPRITE_SCALING) + cartX / (TILE_WIDTH * SPRITE_SCALING) - mw / 2 - 1 / 2
    screeny = mh - cartY / (TILE_HEIGHT * SPRITE_SCALING) - cartX / (TILE_WIDTH * SPRITE_SCALING) + mw / 2 - 1 / 2
    screenx2 = round(screenx)
    screeny2 = round(screeny)
    return screenx2, screeny2'''


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
            tile.column_index = column_index
            tile.row_index = row_index
            tile.width = self.tile_width * scaling
            tile.height = self.tile_height * scaling + 10 * config.SCALING
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
        self.x = None
        self.y = None