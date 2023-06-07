import pytmx

tmxdata = pytmx.TiledMap("C:\\Users\\natha\Desktop\\test.tmx")
image = tmxdata.get_tile_image(x, y, layer)
screen.blit(image, position)
