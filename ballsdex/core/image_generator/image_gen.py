import os
import textwrap
from pathlib import Path
from typing import TYPE_CHECKING

from PIL import Image, ImageDraw, ImageFont, ImageOps

if TYPE_CHECKING:
    from ballsdex.core.models import BallInstance


SOURCES_PATH = Path(os.path.dirname(os.path.abspath(__file__)), "./src")
WIDTH = 1500
HEIGHT = 2000

RECTANGLE_WIDTH = WIDTH - 40
RECTANGLE_HEIGHT = (HEIGHT // 5) * 2

CORNERS = ((34, 261), (1393, 992))
artwork_size = [b - a for a, b in zip(*CORNERS)]

title_font = ImageFont.truetype(str(SOURCES_PATH / "ArsenicaTrial-Extrabold.ttf"), 165)
capacity_name_font = ImageFont.truetype(str(SOURCES_PATH / "Bobby Jones Soft.otf"), 90)
capacity_description_font = ImageFont.truetype(str(SOURCES_PATH / "OpenSans-Semibold.ttf"), 55)
stats_font = ImageFont.truetype(str(SOURCES_PATH / "Bobby Jones Soft.otf"), 90)
stats_percent = ImageFont.truetype(str(SOURCES_PATH / "Pusab.ttf"), 50)
credits_font = ImageFont.truetype(str(SOURCES_PATH / "arial.ttf"), 40)

credits_color_cache = {}


def get_credit_color(image: Image.Image, region: tuple) -> tuple:
    image = image.crop(region)
    brightness = sum(image.convert("L").getdata()) / image.width / image.height
    return (0, 0, 0, 255) if brightness > 100 else (255, 255, 255, 255)


def draw_card(ball_instance: "BallInstance", media_path: str = "./admin_panel/media/"):
    ball = ball_instance.countryball
    ball_health = (255, 255, 255, 255)
    ball_credits = ball.credits
    card_name = ball.cached_regime.name
    if special_image := ball_instance.special_card:
        card_name = getattr(ball_instance.specialcard, "name", card_name)
        image = Image.open(media_path + special_image)
        if ball_instance.specialcard and ball_instance.specialcard.credits:
            ball_credits += f" • {ball_instance.specialcard.credits}"
    else:
        image = Image.open(media_path + ball.cached_regime.background)
    image = image.convert("RGBA")
    icon = (
        Image.open(media_path + ball.cached_economy.icon).convert("RGBA")
        if ball.cached_economy
        else None
    )

    draw = ImageDraw.Draw(image)
    draw.text(
        (50, 20),
        ball.short_name or ball.country,
        font=title_font,
        stroke_width=2,
        stroke_fill=(0, 0, 0, 255),
    )
    for i, line in enumerate(textwrap.wrap(f"Ability: {ball.capacity_name}", width=26)):
        draw.text(
            (100, 1050 + 100 * i),
            line,
            font=capacity_name_font,
            fill=(2555, 255, 255, 255),
            stroke_width=3,
            stroke_fill=(0, 0, 0, 255),
        )
    for i, line in enumerate(textwrap.wrap(ball.capacity_description, width=42)):
        draw.text(
            (60, 1300 + 80 * i),
            line,
            font=capacity_description_font,
            stroke_width=3,
            stroke_fill=(0, 0, 0, 255),
        )
    draw.text(
        (320, 1670),
        str(ball_instance.health),
        font=stats_font,
        fill=ball_health,
        stroke_width=3,
        stroke_fill=(0, 0, 0, 255),
    )
    draw.text(
        (1120, 1670),
        str(ball_instance.attack),
        font=stats_font,
        fill=(255, 255, 255, 255),
        stroke_width=3,
        stroke_fill=(0, 0, 0, 255),
        anchor="ra",
    )
    if card_name in credits_color_cache:
        credits_color = credits_color_cache[card_name]
    else:
        credits_color = get_credit_color(
            image, (0, int(image.height * 0.8), image.width, image.height)
        )
    if ball_instance.health_bonus >= 0:
        draw.text(
            (320, 1795),
            str("(+{}%)").format(ball_instance.health_bonus),
            font=stats_percent,
            stroke_width=3,
            stroke_fill=(0, 0, 0, 255),
        )
    else:
         draw.text(
            (320, 1795),
            str("({}%)").format(ball_instance.health_bonus),
            font=stats_percent,
            stroke_width=3,
            stroke_fill=(0, 0, 0, 255),
        )
    if ball_instance.attack_bonus >= 0:
        draw.text(
            (1120, 1795),
            str("(+{}%)").format(ball_instance.attack_bonus),
            font=stats_percent,
            stroke_width=3,
            stroke_fill=(0, 0, 0, 255),
            anchor="ra",
        )
    else:
         draw.text(
            (1120, 1795),
            str("({}%)").format(ball_instance.attack_bonus),
            font=stats_percent,
            stroke_width=3,
            stroke_fill=(0, 0, 0, 255),
            anchor="ra",
    )
    draw.text(
    (2470, 30),
    str(ball_instance.health),
    font=stats_font,
    stroke_width=3,
    stroke_fill=(0, 0, 0, 255),
    )
    draw.text(
        (1820, 30),
        str(ball_instance.attack),
        font=stats_font,
        stroke_width=3,
        stroke_fill=(0, 0, 0, 255),
    )
    if ball_instance.health_bonus >= 0:
        draw.text(
            (2470, 100),
            str("(+{}%)").format(ball_instance.health_bonus),
            font=stats_percent,
            stroke_width=3,
            stroke_fill=(0, 0, 0, 255),
        )
    else:
         draw.text(
            (2470, 100),
            str("({}%)").format(ball_instance.health_bonus),
            font=stats_percent,
            stroke_width=3,
            stroke_fill=(0, 0, 0, 255),
        )
    if ball_instance.attack_bonus >= 0:
        draw.text(
            (1820, 100),
            str("(+{}%)").format(ball_instance.attack_bonus),
            font=stats_percent,
            stroke_width=3,
            stroke_fill=(0, 0, 0, 255),
        )
    else:
         draw.text(
            (1820, 100),
            str("({}%)").format(ball_instance.attack_bonus),
            font=stats_percent,
            stroke_width=3,
            stroke_fill=(0, 0, 0, 255),
        )
    for i, line in enumerate(textwrap.wrap(f"Ability: {ball.capacity_name}", width=26)):
        draw.text(
            (1750, 200 + 75 * i),
            line,
            font=capacity_name_font,
            fill=(255, 255, 255, 255),
            stroke_width=3,
            stroke_fill=(0, 0, 0, 255),
        )
    for i, line in enumerate(textwrap.wrap(ball.capacity_description, width=40)):
        draw.text(
            (1750, 400 + 50 * i),
            line,
            font=capacity_description_font,
            stroke_width=3,
            stroke_fill=(0, 0, 0, 255),
        )
        credits_color_cache[card_name] = credits_color
    draw.text(
        (30, 1870),
        # Modifying the line below is breaking the licence as you are removing credits
        # If you don't want to receive a DMCA, just don't
        "Created by El Laggron\n" f"Artwork author: {ball_credits}",
        font=credits_font,
        fill=credits_color,
        stroke_width=3,
        stroke_fill=(0, 0, 0, 255),
    )
        draw.text(
        (30, 1927),
        str("ID {}").format(hex(ball_instance.pk).upper()[2:]),
        font=credits_font,
        fill=(0, 0, 0, 255),
        stroke_width=0,
        stroke_fill=(255, 255, 255, 255),
    )
    tmfcg = (f"{ball_instance.catch_date}"[11:19])
    draw.text(
        (30, 1956),
        str("Catch Date: {}".format(ball_instance.catch_date)[:22]),
        font=credits_font,
        fill=(0, 0, 0, 255),
        stroke_width=0,
        stroke_fill=(255, 255, 255, 255),
    )
    draw.text(
        (550, 1956),
        str("(Time: {} UTC)".format(tmfcg)),
        font=credits_font,
        fill=(0, 0, 0, 255),
        stroke_width=0,
        stroke_fill=(255, 255, 255, 255),
    )
    draw.text(
        (1700, 900),
        "Created by El Laggron\n" f"Artwork author: {ball.credits}",
        font=credits_font,
        fill=(0, 0, 0, 255),
        stroke_width=0,
        stroke_fill=(255, 255, 255, 255),
    )
    draw.text(
        (1700, 957),
        str("ID {}").format(hex(ball_instance.pk).upper()[2:]),
        font=credits_font,
        fill=(0, 0, 0, 255),
        stroke_width=0,
        stroke_fill=(255, 255, 255, 255),
    )
    draw.text(
        (1700, 986),
        str("Catch Date: {}".format(ball_instance.catch_date)[:22]),
        font=credits_font,
        fill=(0, 0, 0, 255),
        stroke_width=0,
        stroke_fill=(255, 255, 255, 255),
    )
    draw.text(
        (2220, 986),
        str("(Time: {} UTC)".format(tmfcg)),
        font=credits_font,
        fill=(0, 0, 0, 255),
        stroke_width=0,
        stroke_fill=(255, 255, 255, 255),
    )

    artwork = Image.open(media_path + ball.collection_card).convert("RGBA")
    image.paste(ImageOps.fit(artwork, artwork_size), CORNERS[0])  # type: ignore

    if icon:
        icon = ImageOps.fit(icon, (192, 192))
        image.paste(icon, (1200, 30), mask=icon)
        icon.close()
    artwork.close()

    return image
