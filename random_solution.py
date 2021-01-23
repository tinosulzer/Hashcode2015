from dataclasses import dataclass
from typing import List, Tuple, Dict
import matplotlib.pyplot as plt

@dataclass
class Problem:
    R: int
    C: int
    A: int
    L: int
    V: int
    B: int
    T: int
    starting_cell: None
    target_cells: None
    wind_vectors: None


def parse_input(filename):
    with open(filename) as f:
        R, C, A = [int(i) for i in f.readline().split()]
        L, V, B, T = [int(i) for i in f.readline().split()]
        starting_cell = tuple([int(i) for i in f.readline().split()][::-1])
        target_cells = []
        for _ in range(L):
            target_cells.append(tuple([int(i) for i in f.readline().split()][::-1]))
        wind_vectors = dict()
        for z in range(A):
            for y in range(R):
                pairs = [int(i) for i in f.readline().split()]
                for x in range(C):
                    wind_vectors[(x, y, z)] = (pairs[2*x+1], pairs[2*x])
        return Problem(
            R,
            C, 
            A,
            L,
            V,
            B,
            T,
            starting_cell,
            target_cells,
            wind_vectors,
        )

class Balloon(object):
    def __init__(self, starting_cell, wind_vectors, R, C, A):
        self.position = starting_cell
        self.altitude = 0
        self.instructions = []
        self.wind_vectors = wind_vectors
        self.R = R
        self.C = C
        self.A = A

    def move(self, instruction):
        assert -1 <= instruction <= 1
        if self.altitude < 2:
            assert instruction > -1
        if self.altitude == self.A - 1:
            assert instruction < 1
        self.altitude += instruction
        self.instructions.append(instruction)
        wind_vec = self.wind_vectors[(self.altitude, *self.position)]
        self.position = (self.position[0] + wind_vec[0], (self.position[1] + wind_vec[1]))


if __name__ == "__main__":
    problem = parse_input("hashcode_2015_final_round.in")
    plt.scatter([p[0] for p in problem.target_cells], [p[1] for p in problem.target_cells])
    altitude = 7
    x, y, u, v = [], [], [], []
    for xi in range(problem.C):
        for yi in range(problem.R):
            x.append(xi)
            y.append(yi)
            u.append(problem.wind_vectors[(xi, yi, altitude)][0])
            v.append(problem.wind_vectors[(xi, yi, altitude)][1])
    plt.quiver(x, y, u, v)
    plt.show()
    print(problem)
