from noisemaker import effects
import random


class EffectWrapper:
    def __init__(self, tensor):
        self.tensor = tensor

    def abberiation(self):
        self.tensor = effects.aberration(self.tensor, self.tensor.shape, displacement=random.uniform(
            0, 0.01), time=random.uniform(0, 0.1), speed=random.uniform(0, 1))

    def bloom(self):
        self.tensor = effects.bloom(
            self.tensor, self.tensor.shape, alpha=random.uniform(0, 1))

    def conv_feedback(self):
        self.tensor = effects.conv_feedback(
            self.tensor, self.tensor.shape, iterations=random.randint(5, 100), alpha=random.uniform(0, 1))

    def crease(self):
        self.tensor = effects.crease(self.tensor)

    def density_map(self):
        self.tensor = effects.density_map(self.tensor, self.tensor.shape)

    def derivative(self):
        self.tensor = effects.derivative(self.tensor, self.tensor.shape, with_normalize=random.choice(
            (False, True)), alpha=random.uniform(0, 1))

    def glowing_edges(self):
        self.tensor = effects.glowing_edges(
            self.tensor, self.tensor.shape, sobel_func=2, alpha=random.uniform(0, 1))

    def normal_map(self):
        self.tensor = effects.normal_map(self.tensor, self.tensor.shape)

    def outline(self):
        self.tensor = effects.outline(
            self.tensor, self.tensor.shape, sobel_func=1, invert=random.choice((False, True)))

    def pixel_sort(self):
        self.tensor = effects.pixel_sort(self.tensor, self.tensor.shape, angled=random.choice(
            (False, True)), darkest=random.choice((False, True)), time=random.uniform(0, 1), speed=random.uniform(1, 3))

    def posterize(self):
        self.tensor = effects.posterize(self.tensor, random.randint(1, 20))

    def refract(self):
        self.tensor = effects.refract(self.tensor, self.tensor.shape, displacement=random.uniform(0.1, 1), reference_x=None, reference_y=None, warp_freq=None, spline_order=random.randint(
            0, 3), from_derivative=random.choice([False, True]), signed_range=random.choice([False, True]), time=random.uniform(0, 1), speed=random.uniform(0, 1), y_from_offset=random.choice([False, True]))

    def reindex(self):
        self.tensor = effects.reindex(
            self.tensor, self.tensor.shape, displacement=random.uniform(0, 1))

    def reverb(self):
        self.tensor = effects.reverb(self.tensor, self.tensor.shape, random.randint(
            1, 10), iterations=random.randint(1, 5), ridges=random.choice((False, True)))

    def ripple(self):
        self.tensor = effects.ripple(self.tensor, self.tensor.shape, [random.randint(1, 100) for i in range(random.randint(1, 20))], displacement=random.uniform(
            0, 1), kink=random.uniform(0, 1), reference=None, spline_order=random.randint(0, 3), time=random.uniform(0, 1), speed=random.uniform(0, 1))

    def shadow(self):
        self.tensor = effects.shadow(
            self.tensor, self.tensor.shape, alpha=random.uniform(0, 1), reference=None)

    def sketch(self):
        self.tensor = effects.sketch(self.tensor, self.tensor.shape, time=random.uniform(
            0, 1), speed=random.uniform(0, 3))

    def sobel(self):
        self.tensor = effects.sobel(
            self.tensor, self.tensor.shape, dist_func=1, rgb=random.choice((False, True)))

    def sobel_operator(self):
        self.tensor = effects.sobel_operator(self.tensor, self.tensor.shape)

    def vaseline(self):
        self.tensor = effects.vaseline(
            self.tensor, self.tensor.shape, alpha=random.uniform(0, 1))

    def vignette(self):
        self.tensor = effects.vignette(self.tensor, self.tensor.shape, brightness=random.uniform(
            0, 1), alpha=random.uniform(0, 1))

    def voronoi(self):
        self.tensor = effects.voronoi(self.tensor, self.tensor.shape, density=random.uniform(0, 0.5), nth=random.randint(0, 10), alpha=random.uniform(0, 1), with_refract=random.uniform(
            0, 1), inverse=random.choice((False, True)), xy=None, ridges_hint=random.choice((False, True)), image_count=None, refract_y_from_offset=random.choice((False, True)))

    def vortex(self):
        self.tensor = effects.vortex(self.tensor, self.tensor.shape, displacement=random.uniform(
            32, 100), time=random.uniform(0, 1), speed=random.uniform(0, 3))

    def warp(self):
        self.tensor = effects.warp(self.tensor, self.tensor.shape, [random.randint(1, 1000) for _ in range(1, 100)], octaves=random.randint(1, 10), displacement=random.uniform(
            1, 5), spline_order=random.randint(1, 10), warp_map=None, signed_range=random.choice((False, True)), time=random.uniform(0, 1), speed=random.uniform(0, 3))

    def wormhole(self):
        self.tensor = effects.wormhole(self.tensor, self.tensor.shape, random.uniform(
            1, 100), random.uniform(1, 100), alpha=random.uniform(0, 1))

    def worms(self):
        self.tensor = effects.worms(self.tensor, self.tensor.shape, behavior=random.randint(0, 5), density=random.uniform(0, 10), duration=random.uniform(
            0, 10), stride=random.uniform(0, 2), stride_deviation=random.uniform(0, 1), alpha=random.uniform(0, 1), kink=random.uniform(0, 1), colors=None)



    all_effects = [abberiation, bloom, conv_feedback, crease, density_map, derivative, glowing_edges, normal_map, outline, pixel_sort, posterize, refract, reindex, reverb, ripple, shadow, sketch, sobel, sobel_operator, vaseline, vignette, voronoi, vortex, warp, wormhole, worms]
    
    def random_effects(self, n = -1, max_n = len(all_effects)):
        if n == -1:
            chosens = random.choices(self.all_effects, k = random.randint(2, max_n))
        else:
            chosens = random.choices(self.all_effects, k = n)
        
        for e in chosens:
            while True:
                tries = 0
                try:
                    e.__call__(self)
                    break
                except Exception:
                    if tries == 10:
                        break
                    tries += 1

    def random_effect(self):
        chosen = random.choice(self.all_effects)
        while True:
            tries = 0
            try:
                chosen.__call__(self)
                break
            except Exception:
                if tries == 10:
                    break
                tries += 1


    def apply_all_effects(self):
        for e in self.all_effects:
            while True:
                tries = 0
                try:
                    e.__call__(self)
                    break
                except Exception:
                    if tries == 10:
                        break
                    tries += 1

    
    def ordered_effects(self, order):
        for ind in order:
            while True:
                tries = 0
                try:
                    self.all_effects[ind].__call__(self)
                    break
                except Exception:
                    if tries == 10:
                        break
                    tries += 1
