from app.api import bp
from flask import send_file
import noisemaker
from noisemaker import generators, effects
import random
from PIL import Image
from app.api.effects import EffectWrapper
from datetime import datetime
import os
import os.path

def generate_noises(n, width, height):
    tensors = list()
    for i in range(n):
        tensors.append(random.choice((noisemaker.generators.basic([random.randint(1, 20), random.randint(1, 20)], [width, height, 3]),
                                      noisemaker.generators.multires([random.randint(1, 20), random.randint(1, 20)], [width, height, 3]))))
    return tensors


def mix_all(tensors):
    cur = tensors[0]
    for i in range(1, len(tensors)):
        cur = random.choice((noisemaker.effects.morph(cur, tensors[i], random.uniform(0, 1), random.randint(1, 3), spline_order=random.randint(
            1, 2)), noisemaker.effects.blend(cur, tensors[i], random.uniform(0, 1)), noisemaker.effects.blend_cosine(cur, tensors[i], random.uniform(0, 1))))
    return cur


def choose(tensors, mode, index=0):
    # mode:
    # 0 - mix randomly
    # 1 - choose random index
    # 2 - mix all
    # 3 - choose by index (default is 0)

    if mode == 0:
        return tensors[index]
    elif mode == 1:
        return random.choice(tensors)
    elif mode == 2:
        return mix_all(tensors)
    elif mode == 3:
        chosens = random.choices(tensors, k=random.randint(2, len(tensors)))
        return mix_all(chosens)


def put_effects(tensor, mode=0, order=[]):
    # mode:
    # 0 - randomly choose effects
    # 1 - one random effect
    # 2 - all effects
    # 3 - effects are specified by indices in order

    wrapper = EffectWrapper(tensor)

    if mode == 0:
        wrapper.random_effects()
    elif mode == 1:
        wrapper.random_effect()
    elif mode == 2:
        wrapper.apply_all_effects()
    elif mode == 3:
        wrapper.ordered_effects(order)

    return wrapper.tensor


def render(tensor, width, height):
    img = Image.new('RGB', (width, height))
    pixels = img.load()

    for x in range(width):
        for y in range(height):
            r, g, b = tensor[x][y]
            r = round(float(r) * 255)
            g = round(float(g) * 255)
            b = round(float(b) * 255)
            pixels[x, y] = r, g, b

    return img


@bp.route("/all_random/<int:width>/<int:height>", methods=["GET"])
def all_random(width, height):
    tensors = generate_noises(random.randint(2, 15), width, height)
    chosen_tensor = choose(tensors, random.randint(0, 2))
    tensor_with_effects = put_effects(chosen_tensor, random.randint(0, 2))
    img = render(tensor_with_effects, width, height)

    pic_name = os.path.abspath(os.path.join("results", datetime.now().strftime("%Y-%m-%d-%H:%M:%S") + ".png"))
    img.save(pic_name, "PNG")
    return send_file(pic_name)
    # os.remove(pic_name)


def all_effects(width, height):
    tensors = generate_noises(random.randint(2, 15), width, height)
    chosen_tensor = choose(tensors, random.randint(0, 2))
    tensor_with_effects = put_effects(chosen_tensor, random.randint(0, 2))
    img = render(tensor_with_effects, width, height)

    pic_name = os.path.join("results", datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ".png")
    img.save(pic_name, "PNG")
    yield send_file(pic_name, mimetype="image/png")
    os.remove(pic_name)


def by_modes(width, height, n, mode1, index, mode2, order):
    if n == -1:
        n = random.randint(1, 15)

    tensors = generate_noises(n, width, height)

    if mode1 == -1:
        mode1 = random.randint(0, 3)

    if index == -1:
        index = random.randint(0, len(tensors))

    chosen_tensor = choose(tensors, mode=mode1, index=index)

    if mode2 == -1:
        mode2 = random.randint(0, 3)

    if order == -1:
        mode2 = 0

    tensor_with_effects = put_effects(chosen_tensor, mode=mode2, order=order)

    img = render(tensor_with_effects, width, height)

    pic_name = os.path.join("results", datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ".png")
    img.save(pic_name, "PNG")
    yield send_file(pic_name, mimetype="image/png")
    os.remove(pic_name)
