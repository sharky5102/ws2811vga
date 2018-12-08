import assembly
import geometry.simple
import math

class copperbar(assembly.assembly):
    def __init__(self):
        colors = [(1,0,0),(0,0,1),(0,1,0)]
        self.bars = []

        for color in colors:
            copper = geometry.simple.copper()
            copper.setColor(color)
            self.bars.append(copper)

    def setModelView(self, M):
        for bar in self.bars:
            bar.setModelView(M)

    def setProjection(self, M):
        for bar in self.bars:
            bar.setProjection(M)

    def render(self, t):

        r = math.cos(t/10) * math.pi * 2 * 5
        n = (math.sin(t * math.pi * 2 / 5.3) + 1.2) / 1

        self.bars[0].setDirection((math.sin(r) * n , math.cos(r) * n))

        r = math.cos(t/11) * math.pi * 2 * 3 
        n = (math.sin(t * math.pi * 2 / 4.7) + 1.2) / .7

        self.bars[1].setDirection((math.sin(r) * n / 2 , math.cos(r) * n))

        r = math.sin(t/17) * math.pi * 2 * 7 
        n = (math.sin(t * math.pi * 2 / 6.7) + 1.2) / 1.1

        self.bars[2].setDirection((math.sin(r) * n , math.cos(r) * n))

        for bar in self.bars:
            bar.render()
