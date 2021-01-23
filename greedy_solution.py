from dataclasses import dataclass
from typing import List, Tuple, Dict
import matplotlib.pyplot as plt
import random

random.seed(2000)

from lib import * 


def heuristic_score(balloon, move, problem, target_cells_set):
    (bx, by), _ = balloon.move(move, update=False)

    score = 0
    radius = problem.V
    for square in covered_squares(bx, by, radius, problem.C):
        if square in target_cells_set:
            score += 1
    
    return score



def greedy_solution(problem):
    target_cells_set = set(problem.target_cells)
    balloons = [
        Balloon(
            problem.starting_cell, problem.wind_vectors, problem.R, problem.C, problem.A
        )
        for _ in range(problem.B)
    ]
    for turn in range(problem.T):
        print(f"Solving turn {turn}")
        for balloon in balloons:
            if balloon.altitude < 2:
                possible = [0, 1]
            elif balloon.altitude == problem.A:
                possible = [-1, 0]
            else:
                possible = [-1, 0, 1]

            scores = []
            for choice in possible:
                scores.append(heuristic_score(balloon, choice, problem, target_cells_set))
            max_score = max(scores)
            choices = []
            for choice, score in zip(possible, scores):
                if score == max_score:
                    choices.append(choice)

            balloon.move(random.choice(choices))

    instructions = []
    for turn in range(problem.T):
        instructions.append([b.instructions[turn] for b in balloons])
    return instructions


if __name__ == "__main__":
    problem = parse_input("hashcode_2015_final_round.in")
    solution = greedy_solution(problem)
    save_solution(solution, "greedy.txt")
    print(score(problem, solution))


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
