import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from lib import *


def load_solution(filename):
    solution = []
    with open(filename) as f:
        for line in f.readlines():
            solution.append([int(x) for x in line.split()])
    return solution


def calculate_paths(problem, solution):
    paths = []

    current_altitudes = [0]
             
    for b in range(problem.B):
        path = []
        balloon = Balloon(
            problem.starting_cell,
            problem.wind_vectors,
            problem.R,
            problem.C,
            problem.A
        )
        turn = 0
        while turn < problem.T:
            path.append(balloon.position)
            balloon.move(solution[turn][b])
            turn += 1
        paths.append(path)
    return paths


def main(args):
    filename, output = args[1:]
    solution = load_solution(filename)
    problem = Problem("hashcode_2015_final_round.in")

    target_cells = problem.target_cells
    grid = np.zeros((problem.C, problem.R))
    for x in range(problem.C):
        for y in range(problem.R):
            if (x, y) in target_cells:
                grid[x, y] = 0.5

    paths = calculate_paths(problem, solution)

    fig, ax = plt.subplots(figsize=(12, 5))
    ax.set_aspect("equal")
    ax.set_xlim((0, problem.C))
    ax.set_ylim((0, problem.R))
    points = ax.scatter([], [], c="k")
    img = ax.imshow(grid.T, origin="lower", cmap="binary", vmax=1)

    def init():
        return points, img

    def animate(i):
        pos = []
        for path in paths:
            pos.append(path[i])
        points.set_offsets(pos)
        return points, img
    
    anim = FuncAnimation(
        fig, animate, frames=problem.T, interval=10, blit=False, init_func=init
    )
    anim.save(output, fps=30)
    plt.show()


if __name__ == "__main__":
    main(sys.argv)
