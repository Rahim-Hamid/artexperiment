from PIL import Image

def pixelation(image_path, block_size):
    original_img = Image.open(image_path).convert("RGB")
    width, height = original_img.size

    new_width = width // block_size
    new_height = height // block_size

    new_img = original_img.resize((new_width, new_height), Image.NEAREST)

    pixel_img = new_img.resize((width, height), Image.NEAREST)

    return pixel_img

pixel_img = pixelation("labubu.png", 50)
pixel_img.save("output_pixel_art.png")
