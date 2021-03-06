from dataclasses import dataclass
from typing import List, Tuple, Dict
import matplotlib.pyplot as plt
import random

random.seed(2000)

from lib import * 


def heuristic_score(balloon, move, problem, target_cells_set):
    (bx, by), _ = balloon.move(move, update=False)

    if 0 <= by <= problem.R:
        score = 0
        radius = problem.V
        for square in problem.covered_squares[(bx,by)]:
            if square in target_cells_set:
                score += 1
    else:
        score = -10
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


def visualise(problem, solution):
    plt.scatter(
        [p[0] for p in problem.target_cells], [p[1] for p in problem.target_cells]
    )

    balloons = [
        Balloon(
            problem.starting_cell, problem.wind_vectors, problem.R, problem.C, problem.A
        )
        for _ in range(problem.B)
    ]

    paths = [list() for _ in range(problem.B)]
    for turn, instructions in enumerate(solution):
        for i, balloon in enumerate(balloons):
            pos, _ = balloon.move(instructions[i])
            paths[i].append(pos)

    for path in paths:
        plt.plot([p[0] for p in path], [p[1] for p in path])
    plt.show()



if __name__ == "__main__":
    problem = Problem("hashcode_2015_final_round.in")
    solution = greedy_solution(problem)
    save_solution(solution, "greedy.txt")
    visualise(problem, solution)
    print(score(problem, solution))
