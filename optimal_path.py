from dataclasses import dataclass
from typing import List, Tuple, Dict
import matplotlib.pyplot as plt
import random
import numpy as np

random.seed(2000)

from lib import * 


class Node(object):
    def __init__(self, position, is_null=False):
        self.position = position
        self.children = []
        self.total_scores = {0: 0}
        self.covered_targets = []
        self.current_scores = {}
        self.is_null = is_null

    def clear(self):
        if not self.is_null:
            self.total_scores = {0: 0}

    def total_score(self, turn, problem, max_turn):

        try:
            return self.total_scores[max_turn-turn]
        
        except KeyError:
            if self.is_null:
                return -1000
            score = self.current_scores[turn] 
            score += max(
                [child.total_score(turn+1, problem, max_turn) for child in self.children]
            )
            self.total_scores[max_turn - turn] = score
            return score


class TargetCell(object):
    def __init__(self, turns):
        self.not_covered = [1]*turns
        self.covering_nodes = []

    def covered(self, turn):
        if self.not_covered[turn]:
            self.not_covered[turn] = 0
            for node in self.covering_nodes:
                node.current_scores[turn] -= 1


def next_position(x, y, z, problem):
    if z < 1: # either currently on the ground or outside the box
        return x, y, z
    wind_vec = problem.wind_vectors[(x, y, z)]
    new_x, new_y = (x + wind_vec[0]) % problem.C, y + wind_vec[1]
    # next step is outside the graph
    if not 0 <= new_y < problem.R:
        return -1, -1, -1
    return new_x, new_y, z


def covered_target_cells(x, y, z, problem, target_cells_set):
    if z < 0:
        return []
    covered_squares = problem.covered_squares[(x, y)]
    return list(set(covered_squares).intersection(target_cells_set))


def construct_graph(problem):
    target_cells_set = set(problem.target_cells)

    # Initialise one node for each position
    graph = {}
    for x in range(problem.C):
        for y in range(problem.R):
            for z in range(1, problem.A+1):
                graph[(x, y, z)] = Node((x, y, z))
    # Only a single node at altitude 0
    graph[(*problem.starting_cell, 0)] = Node((*problem.starting_cell, 0))
    # represents outside the grid
    graph[(-1, -1, -1)] = Node(None, is_null=True)

    # Connect the graph
    for (x, y, z), node in graph.items():
        if node.is_null:
            for turn in range(problem.T):
                node.current_scores[turn] = -1000
        else:
            node.covered_targets = covered_target_cells(x, y, z, problem, target_cells_set)
            for turn in range(problem.T):
                node.current_scores[turn] = len(node.covered_targets)
            node.children.append(graph[next_position(x, y, z, problem)])
            if z > 1:
                node.children.append(graph[next_position(x, y, z-1, problem)])
            if 0 <= z < problem.A:
                node.children.append(graph[next_position(x, y, z+1, problem)])

    return graph


def construct_target_cells(problem, graph):
    cells = {(x, y): TargetCell(problem.T) for (x, y) in problem.target_cells}
    for node in graph.values():
        for cell in node.covered_targets:
            cells[cell].covering_nodes.append(node)
    return cells


def update_coverage(path, graph, target_cells):
    for turn, position in enumerate(path):
        for target_cell_pos in graph[position].covered_targets:
            target_cells[target_cell_pos].covered(turn)


def construct_optimal_path(graph, problem, depth, max_start_turn):

    current_position = (*problem.starting_cell, 0)
    turn = 0
    path = []
    instructions = []
    died = False

    while turn < problem.T:
        print(f"\t turn {turn} ", end="")
        
        if turn == max_start_turn and current_position[2] == 0:
            turn += 1
            instructions.append(1)
            current_position = next_position(*current_position[:2], 1, problem)
            path.append(current_position)
            continue

        children = graph[current_position].children
        scores = [
            child.total_score(turn + 1, problem, max_turn=min(turn+depth, problem.T))
            for child in children
        ]
        max_score = max(scores)
        choices = [
            child.position for child, score in zip(children, scores)
            if score == max_score
        ]
        new_position = random.choice(choices)
        print(current_position, end=" ")
        if new_position is None:
            died = True
            break

        instructions.append(new_position[2] - current_position[2])
        print(instructions[-1], end=" ")
        current_position = new_position
        print(current_position)
        turn += 1
        path.append(current_position)

    if died:
        print("Died")
        path += [(-1, -1, -1)] * (problem.T - len(path))
        instructions += [0] * (problem.T - len(instructions))

    return path, instructions
        

def optimal_paths(problem):
    depth = 50
    batch_size = 5
    interval = 10
    graph = construct_graph(problem)
    target_cells = construct_target_cells(problem, graph)
    
    solution = []

    # First balloon always stays at base
    path = [(*problem.starting_cell, 0)]*problem.T
    instructions = [0]*problem.T
    solution.append(instructions)

    update_coverage(path, graph, target_cells)
    for node in graph.values():
        node.clear()

    for b in range(1, problem.B):
        print(f"Optimising balloon {b}")
        max_start_turn = (b // batch_size) * interval
        path, instructions = construct_optimal_path(graph, problem, depth, max_start_turn)
        
        solution.append(instructions)
        
        update_coverage(path, graph, target_cells)
        for node in graph.values():
            node.clear()

    # transpose
    solution = list(zip(*solution))
    return solution

if __name__ == "__main__":
    problem = Problem("hashcode_2015_final_round.in")
    solution = optimal_paths(problem)
    save_solution(solution, "optimal_iterative_greedy_deep.txt")
    print(score(problem, solution))


