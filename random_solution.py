from dataclasses import dataclass
from typing import List, Tuple, Dict
import matplotlib.pyplot as plt
import random

random.seed(2000)

from lib import * 


def random_solution(problem):
    balloons = [
        Balloon(
            problem.starting_cell, problem.wind_vectors, problem.R, problem.C, problem.A
        )
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
        instructions.append([b.instructions[turn] for b in balloons])
    return instructions

def randPerm(problem,solution):
    balloons = [
        Balloon(
            problem.starting_cell, problem.wind_vectors, problem.R, problem.C, problem.A
        )
        for _ in range(problem.B)
    ]
    for turn in range(problem.T):
        i=0
        for balloon in balloons:
            currentChoice = solution[turn][i]
            i+=1
            if balloon.altitude < 2:
                possible = [0, 1]
            elif balloon.altitude == problem.A:
                possible = [-1, 0]
            else:
                possible = [-1, 0, 1]
            if currentChoice==possible[0]:
                weights = [99]+[0.5]*(len(possible)-1)
            elif currentChoice==possible[1]:
                weights = [0.5,99]+[0.5]*(len(possible)-2)
            elif currentChoice not in possible:
                possible = [0]
                weights = [1]
            else:
                weights = [0.5,0.5,99]
            instruction = random.choices(possible,weights=weights)[0]
            balloon.move(instruction)

    instructions = []
    for turn in range(problem.T):
        instructions.append([b.instructions[turn] for b in balloons])
    return instructions

if __name__ == "__main__":
    problem = Problem("hashcode_2015_final_round.in")
    solution = random_solution(problem)
    save_solution(solution, "random.txt")
    bestScore = score(problem,solution)
    nextSolution = solution
    for epoch in range(100):
        solution = nextSolution
        for child in range(10):
            solNew = randPerm(problem,solution)
            score2 = score(problem,solNew)
            print(epoch,child,score2,bestScore)
            if score2>bestScore:
                bestScore = score2
                nextSolution = solNew

                

def visualise(problem):
    plt.scatter(
        [p[0] for p in problem.target_cells], [p[1] for p in problem.target_cells]
    )
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
