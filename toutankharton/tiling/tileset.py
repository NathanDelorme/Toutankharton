class Tileset:
    def __init__(self, image, tile_size, tile_margin, tile_spacing):
        self.image = image
        self.tile_size = tile_size
        self.tile_margin = tile_margin
        self.tile_spacing = tile_spacing
        self.tiles = Tileset.get_tiles(image, tile_size, tile_margin, tile_spacing)

    @staticmethod
    def get_tiles(image, tile_size, tile_margin, tile_spacing):
        tiles = []
        for y in range(tile_margin, image.get_height(), tile_size + tile_spacing):
            for x in range(tile_margin, image.get_width(), tile_size + tile_spacing):
                tile = image.subsurface(x, y, tile_size, tile_size)
                tiles.append(tile)
        return tiles
