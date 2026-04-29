from PIL import Image, ImageDraw, ImageFont
import os
from datetime import datetime


def wrap_text(text, font, max_width, draw):
    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        test_line = current_line + " " + word if current_line else word
        bbox = draw.textbbox((0, 0), test_line, font=font)

        if bbox[2] <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word

    if current_line:
        lines.append(current_line)

    return lines


def create_meme(image_path, top_text, bottom_text):
    os.makedirs("outputs", exist_ok=True)

    img = Image.open(image_path).convert("RGB")
    img = img.resize((500, 500))

    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("arial.ttf", 28)
    except:
        font = ImageFont.load_default()

    def draw_centered(lines, y_start):
        y = y_start
        for line in lines:
            bbox = draw.textbbox((0, 0), line, font=font)
            x = (img.width - bbox[2]) / 2

            for dx in [-1, 1]:
                for dy in [-1, 1]:
                    draw.text((x+dx, y+dy), line, font=font, fill="black")

            draw.text((x, y), line, font=font, fill="white")
            y += 30

    top_lines = wrap_text(top_text, font, img.width - 40, draw)
    bottom_lines = wrap_text(bottom_text, font, img.width - 40, draw)

    draw_centered(top_lines, 10)
    draw_centered(bottom_lines, img.height - 80)

    filename = f"outputs/meme_{datetime.now().strftime('%H%M%S')}.png"
    img.save(filename)

    return filename