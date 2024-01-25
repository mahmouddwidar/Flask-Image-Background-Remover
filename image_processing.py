import rembg
from PIL import Image

def remove_background(input_path, output_path):
    input = Image.open(input_path)
    output = rembg.remove(input)
    output.save(output_path)