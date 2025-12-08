from PIL import Image
from scipy.spatial import KDTree
import numpy as np

def create_img_mosaic(target_image_path, tile_image_path, tile_size):
    target_img = Image.open(target_image_path).convert("RGB")
    target_width, target_height = target_img.size

    tile_images = []
    tile_avg_colors = []
    for path in tile_image_path:
        tile_img = Image.open(path).convert("RGB").resize(tile_size)
        tile_images.append(tile_img)
        tile_avg_colors.append(np.mean(np.array(tile_img), axis =(0, 1)))


    kdtree = KDTree(tile_avg_colors)
    mosaic_img = Image.new("RGB", (target_width, target_height))

    for y in range(0, target_height, tile_size[1]):
        for x in range(0, target_width, tile_size[0]):
            block = target_img.crop((x, y, x + tile_size[0], y + tile_size[1]))
            block_avg_color = np.mean(np.array(block), axis = (0, 1))

            _, index = kdtree.query(block_avg_color)
            select_tile = tile_images[index]

            mosaic_img.paste(select_tile, (x, y))


    return mosaic_img

mosaic_image = create_img_mosaic("face.png", ["smile.png", "face.png", "memoriam.png"], (20,20))
mosaic_image.save("output_mosaic.jpg")
    
