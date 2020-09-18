# Vijendra, Megha
# 1001736938

import sys
from queue import PriorityQueue


def readInput(inputfile):
    graph = dict()
    try:
        inpFile = open(inputfile, 'r')
        for line in inpFile:
            line = line.rstrip('\n')
            line = line.rstrip('\r')
            if line == 'END OF INPUT':
                inpFile.close()
                return graph
            else:
                data = line.split(' ')
                start = data[0]
                end = data[1]
                dist = float(data[2])
                # creating a nested dictionary to store the structure of the graph
                graph.setdefault(start, {})[end] = dist
                graph.setdefault(end, {})[start] = dist
    except:
        print("No Input file found")


def readHeuristic(heuristicfile):
    heuristics = dict()
    try:
        heurFile = open(heuristicfile, 'r')
        for line in heurFile:
            line = line.rstrip('\n')
            line = line.rstrip('\r')
            if line == 'END OF INPUT':
                heurFile.close()
                return heuristics
            else:
                data = line.split(' ')
                city = data[0]
                hvalue = float(data[1])
                heuristics[city] = hvalue
    except:
        print("No Input file found")


def uninformed_ucs(start, goal, graph):
    nodes_exp = 0
    nodes_gen = 0
    # Initialise a set to store all the visited nodes
    visited_nodes = set()
    # Initialise a queue to store and sort the fringe
    queue = PriorityQueue()
    queue.put((0, [start]))
    nodes_gen += 1
    # Initialise a dictionary to store the resulting path
    final_path = dict()

    while queue:
        cost, path = queue.get()
        current = path[len(path)-1]
        nodes_exp += 1

        # If the current node is not in the visited set
        if current not in visited_nodes:
            visited_nodes.add(current)
            if current == goal:
                final_path['cost'] = cost
                final_path['path'] = path
                return generatedPath(nodes_exp, nodes_gen, graph, final_path)
            for child in graph[current]:
                temp = path[:]
                temp.append(child)
                nodes_gen += 1
                queue.put((float(cost) + float(graph[current][child]), temp))

        # If there is no route between the start node and goal node
        if queue.empty():
            return generatedPath(nodes_exp, nodes_gen, graph, None)


def informed_a_star(start, goal, graph, heuristic):
    nodes_exp = 0
    nodes_gen = 0
    # Initialise a dictionary to store the resulting path
    final_path = {}
    # Initialise a set to store all the visited nodes
    openSet = [start]
    cameFrom = {}
    
    gScore = {}
    fScore = {}

    for h in heuristic.keys():
        gScore[h] = float('inf')
        fScore[h] = float('inf')

    gScore[start] = 0
    fScore[start] = heuristic[start]
    fScore.values()
    while len(openSet) != 0:
        minim = float('inf')
        nodes_exp += 1
        for node in openSet:
            if minim > fScore[node]:
                current = node
                minim = fScore[node]
        if current == goal:
            final_path['cost'] = 0
            final_path['path'] = []
            while current != "":
                if current == start:
                    final_path['path'].append(start)
                    final_path['path'].reverse()
                    return generatedPath(nodes_exp, nodes_gen + 1, graph, final_path)
                final_path['path'].append(current)
                final_path['cost'] += graph[current][cameFrom[current]]
                current = cameFrom[current]
        openSet.remove(current)
        for neighbor in graph[current].keys():
            nodes_gen += 1
            tentative_gScore = gScore[current] + graph[current][neighbor]
            if tentative_gScore < gScore[neighbor]:
                cameFrom[neighbor] = current
                gScore[neighbor] = tentative_gScore
                fScore[neighbor] = gScore[neighbor] + heuristic[neighbor]
                if neighbor not in openSet:
                    openSet.append(neighbor)

    # If there is no route between the start node and goal node
    return generatedPath(nodes_exp, nodes_gen, graph, None)


def generatedPath(expanded, generated, graph, final_path):
    if final_path:
        print("Nodes Expanded:", expanded)
        print("Nodes Generated:", generated)
        print('Distance: ', final_path['cost'])
        print('Route: ')
        for i in range(len(final_path['path']) - 1):
            start = final_path['path'][i]
            end = final_path['path'][i + 1]
            cost = graph[final_path['path'][i]][final_path['path'][i + 1]]
            print(f'{start} to {end} : {cost} kms')
    else:
        print("Nodes Expanded:", expanded)
        print("Nodes Generated:", generated)
        print("Distance: infinity \nRoute: None")


def main():

    # Check if the number of arguments are correct
    arg_l = len(sys.argv)
    if arg_l < 4 or arg_l > 5:
        print('Incorrect number of arguments\n')
        sys.exit()

    # Read the command line arguments
    input_file = sys.argv[1]
    start = sys.argv[2]
    goal = sys.argv[3]

    # Creating the graph from the input file
    graph = readInput(input_file)

    # Check if the given start and the goal state is present in the graph
    if start not in graph.keys():
        print('Start node is not present')
        sys.exit()
    if goal not in graph.keys():
        print('Destination node is not present')
        sys.exit()

    if arg_l == 4:
        uninformed_ucs(start, goal, graph)
    elif arg_l == 5:
        heuristic_file = sys.argv[4]
        heuristic = readHeuristic(heuristic_file)
        informed_a_star(start, goal, graph, heuristic)


if __name__ == '__main__':
    main()

