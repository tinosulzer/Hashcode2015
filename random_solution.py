from dataclasses import dataclass
from typing import List, Tuple, Dict
import matplotlib.pyplot as plt
import random
random.seed(1993)

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
                    wind_vectors[(x, y, z+1)] = (pairs[2*x+1], pairs[2*x])
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
        self.is_live = True

    def move(self, instruction, update=True):
        if not self.is_live:
            if update:
                self.instructions.append(instruction)
            return self.position, self.altitude

        assert -1 <= instruction <= 1
        if self.altitude < 2:
            assert instruction > -1
        if self.altitude == self.A:
            assert instruction < 1
        new_altitude = self.altitude + instruction
        if new_altitude > 0:
            wind_vec = self.wind_vectors[(*self.position, new_altitude)]
        else:
            wind_vec = (0, 0)

        new_position = ((self.position[0] + wind_vec[0]) % self.C, (self.position[1] + wind_vec[1]))
        if update:
            self.position = new_position
            self.altitude = new_altitude
            self.instructions.append(instruction)

            if self.is_live and not 0 <= self.position[1] < self.R:
                self.is_live = False

        return new_position, new_altitude

def random_solution(problem):
    balloons = [
        Balloon(problem.starting_cell, problem.wind_vectors, problem.R, problem.C, problem.A)
        for _ in range(problem.B)
    ]
    for turn in range(problem.T):
        for balloon in balloons:
            if balloon.altitude < 2:
                possible = [0, 1]
            elif balloon.altitude == problem.A:
                possible = [-1, 0]
            else:
                possible = [-1, 0, 1]
            instruction = random.choice(possible)
            balloon.move(instruction)

    instructions = []
    for turn in range(problem.T):
        instructions += [b.instructions[turn] for b in balloons]
    return instructions


def save_solution(instructions, filename):
    with open(filename, "w") as f:
        for instruction in instructions:
            print(instruction, file=f)


def coldist(x, bx, C):
    return min(abs(x - bx), C - abs(x - bx))


def distance_sq(x, y, bx, by, C):
    return (y - by)**2 + coldist(x, bx, C)**2


def covered_squares(x, y, radius, C):
    cells = []
    for i in range(-radius, radius+1):
        for j in range(-radius, radius+1):
            if i**2 + j**2 < radius**2:
                cells.append(((x + i) % C, y + j))
    return cells


def current_score(balloons, target_cells, problem):
    radius = problem.V
    score = 0
    target_cell_is_covered = {
        cell: 0 for cell in target_cells
    }
    for b in balloons:
        bx, by = b.position
        for square in covered_squares(bx, by, radius, problem.C):
            if square in target_cell_is_covered:
                target_cell_is_covered[square] = 1

    return sum(target_cell_is_covered.values())


def score(problem, instructions):
    target_cells = problem.target_cells
    turns = problem.T

    score = 0

    balloons = [
        Balloon(problem.starting_cell, problem.wind_vectors, problem.R, problem.C, problem.A)
        for _ in range(problem.B)
    ]

    for turn in range(turns):
        for i, balloon in enumerate(balloons):
            balloon.move(instructions[problem.B*turn+i])
        score += current_score(balloons, target_cells, problem)

    return score

    

def test(problem):
    balloon = Balloon(problem.starting_cell, problem.wind_vectors, problem.R, problem.C, problem.A)
    balloon.move(1)
    for i in range(problem.T-1):
        print(balloon.position, balloon.altitude, balloon.is_live)
        balloon.move(0)


if __name__ == "__main__":
    problem = parse_input("hashcode_2015_final_round.in")
    solution = random_solution(problem)
    save_solution(solution, "random.txt")
    print(score(problem, solution))

if False:
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
