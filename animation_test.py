from colors import *
import time
import pixelstrip
import math

def ease(x):
    return 16 * x * x * x * x * x if x < 0.5 else 1 - math.pow(-2 * x + 2, 5) / 2

def lerp(a, b, t):
    t = max(0, min(t, 1))
    return a + t * (b - a)

def interp(a, b, t):
    return lerp(a, b, ease(t))

def interp_col(a, b, t):
    out = []
    for i in range(3):
        out.append(interp(a[i], b[i], t))
    return out


def lerp_col(a, b, t):
    out = []
    for i in range(3):
        out.append(lerp(a[i], b[i], t))
    return out

class GradientAnimation(pixelstrip.Animation):

    def __init__(self):
        self.i = 0
        self.n = 24

    def reset(self, strip):
        self.timeout = 0.5
        strip.clear()

    def draw(self, strip, _delta_time):
        if self.is_timed_out():
            if self.i >= self.n/2:
                strip[self.i] = lerp_col(BLUE, RED, self.i/(self.n/2) - 1)
            else:
                strip[self.i] = lerp_col(RED, BLUE, self.i/(self.n/2))
            if self.i >= self.n:
                strip[self.i%self.n] = BLACK
            strip.show()
            self.i += 1
            self.i %= self.n*2
            self.timeout = 1/15
            

