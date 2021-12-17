import sys
from typing import TextIO
from collections import namedtuple, defaultdict

Point = namedtuple("Point", ['x', 'y'])

class Everything:
    @classmethod
    def read_input(cls, textio: TextIO):
        line = textio.readline().strip()
        xs, ys = [[int(loc) for loc in dim[2:].split('..')] for dim in line[13:].split(', ')]
        return Everything(Point(x=xs[0],y=ys[0]), Point(x=xs[1],y=ys[1]))
    
    def __init__(self, trench_from: Point, trench_to: Point):
        min_trench_x = min(trench_from.x, trench_to.x)
        max_trench_x = max(trench_from.x, trench_to.x)
        min_trench_y = min(trench_from.y, trench_to.y)
        max_trench_y = max(trench_from.y, trench_to.y)

        self.trench_from = Point(min_trench_x, min_trench_y)
        self.trench_to = Point(max_trench_x, max_trench_y)
        self.probe_loc = Point(x=0,y=0)

    def __str__(self):
        min_bound_x = min(0, self.trench_from.x, self.trench_to.x, self.probe_loc.x)
        max_bound_x = max(0, self.trench_from.x, self.trench_to.x, self.probe_loc.x)
        min_bound_y = min(0, self.trench_from.y, self.trench_to.y, self.probe_loc.y)
        max_bound_y = max(0, self.trench_from.y, self.trench_to.y, self.probe_loc.y)

        out = ''
        for y in range(max_bound_y, min_bound_y-1, -1):
            for x in range(min_bound_x, max_bound_x+1):
                if x==0 and y==0:
                    out += 'S'
                elif x==self.probe_loc.x and y== self.probe_loc.y:
                    out += '#'
                elif self.trench_from.x <= x <= self.trench_to.x and self.trench_from.y <= y <= self.trench_to.y:
                    out += 'T'
                else:
                    out += '.'
            out += '\n'
        return out
    
    @staticmethod
    def _drag(velocity: int):
        if velocity == 0:
            return 0
        if velocity < 0:
            return velocity+1
        if velocity > 0:
            return velocity-1
        
    def in_trench(self):
        return self.trench_from.x <= self.probe_loc.x <= self.trench_to.x and self.trench_from.y <= self.probe_loc.y <= self.trench_to.y

    def simulate(self, probe_velocity: Point):
        self.probe_loc = Point(x=0, y=0)
        velocity = probe_velocity
        max_height = self.probe_loc.y
        
        while not self.in_trench() and self.probe_loc.x <= max(self.trench_from.x,self.trench_to.x) and self.probe_loc.y >= max(self.trench_from.y,self.trench_to.y):
            self.probe_loc = Point(x=self.probe_loc.x + velocity.x, y=self.probe_loc.y + velocity.y)
            max_height = max(max_height, self.probe_loc.y)
            velocity = Point(x=Everything._drag(velocity.x), y=velocity.y-1)
            # print(self)
            # print(velocity)
        
        return self.in_trench(), max_height

ev = Everything.read_input(sys.stdin)
# hit, max_height = ev.simulate(probe_velocity=Point(x=6,y=3))
# print(hit, max_height)

max_hit=0
for x in range(-2*abs(ev.trench_to.x), 2*abs(ev.trench_to.x)):
    for y in range(-2*abs(ev.trench_to.y), 2*abs(ev.trench_to.y)):
        hit, max_height = ev.simulate(probe_velocity=Point(x=x,y=y))
        if hit:
            max_hit=max(max_hit, max_height)
print(max_hit)