from PIL import Image, ImageDraw, ImageFont

def linear_gradient(draw, start_color, end_color):
    """Функция для создания градиента"""
    width, height = draw.im.size
    for y in range(height):
        r = start_color[0] + (end_color[0] - start_color[0]) * y // height
        g = start_color[1] + (end_color[1] - start_color[1]) * y // height
        b = start_color[2] + (end_color[2] - start_color[2]) * y // height
        draw.line((0, y, width, y), fill=(r, g, b))

def gen_banner(hi,username):
    # Открываем изображение аватарки
    avatar = Image.open("avatar.png")

    # Уменьшаем размер аватарки в два раза
    new_avatar_size = (avatar.width // 2, avatar.height // 2)
    avatar = avatar.resize(new_avatar_size)

    # Создаем новое изображение с заданными размерами
    width, height = 1500, 650
    image = Image.new("RGB", (width, height), (255, 255, 255))
    mask = Image.new("L", avatar.size, 0)
    mask_ellipse = ImageDraw.Draw(mask)
    mask_ellipse.ellipse((0, 0, avatar.width, avatar.height), fill=255)

    # Создаем объект для рисования
    draw = ImageDraw.Draw(image)

    # Определяем начальный и конечный цвета градиента (в формате RGB)
    start_color = (0, 0, 255)  # Синий
    end_color = (128, 0, 128)  # Фиолетовый

    # Рисуем прямоугольник с градиентом
    linear_gradient(draw, start_color, end_color)

    # Задаем радиус для округления аватарки
    radius = avatar.width // 2

    # Задаем координаты для аватарки по центру внизу
    avatar_x = int((width - avatar.width) / 2)
    avatar_y = height - avatar.height - radius

    # Рисуем округленный прямоугольник
    draw.rounded_rectangle([(avatar_x, avatar_y), (avatar_x + avatar.width, avatar_y + avatar.height)], radius, fill=(255, 255, 255))

    # Рисуем округленный контур аватарки
    image.paste(avatar, (avatar_x, avatar_y), mask=mask)
    image.paste(avatar, (avatar_x, avatar_y), mask=mask)

    # Открываем шрифт для никнейма и переменной "ad"
    font = ImageFont.truetype("Comfortaa-Bold.ttf", 36)

    # Задаем координаты для переменной "ad"
    ad_x = int(width / 2)
    ad_y = avatar_y - 70

    # Задаем координаты для имени пользователя
    username_x = int(width / 2)
    username_y = avatar_y + avatar.height + 40

    # Задаем текст и цвет для переменной "ad"
    ad_text = f"{hi}, {username}"
    ad_color = "white"

    # Задаем текст и цвет для имени пользователя
    username_text = username
    username_color = "white"

    # Рисуем текст переменной "ad"
    draw.text((ad_x, ad_y), ad_text, font=font, fill=ad_color, anchor="mm")

    # Рисуем текст имени пользователя
    draw.text((username_x, username_y), username_text, font=font, fill=username_color, anchor="mm")

    # Сохраняем изображение
    image.save("result_image.png")

gen_banner("С добрым утром ","MuRuLOSE")