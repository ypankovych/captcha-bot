import io
import random
from string import ascii_letters, digits
from PIL import ImageDraw, ImageFont, Image


def get_image():
    font = ImageFont.truetype("arial.ttf", 55)
    image = Image.new(mode="1", size=(500, 250), color=255)

    text_position = (80, 90)
    text_color = (0, 0, 0)

    draw = ImageDraw.Draw(image)
    text = ''.join(random.sample(ascii_letters + digits, 10))
    draw.text(xy=text_position, text=text, color=text_color, font=font)
    fp = io.BytesIO()
    image.save(fp, 'PNG')
    try:
        return {'image': fp.getvalue(), 'answer': text}
    finally:
        fp.close()
