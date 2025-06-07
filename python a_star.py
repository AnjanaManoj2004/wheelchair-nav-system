import heapq

def manhattan_distance(a, b):
    """Calculate Manhattan distance between two points a and b."""
    x1, y1 = a
    x2, y2 = b
    return abs(x1 - x2) + abs(y1 - y2)

def reconstruct_path(parent, goal):
    """Reconstruct path from start to goal using parent map."""
    path = []
    current = goal
    while current is not None:
        path.append(current)
        current = parent[current]
    return path[::-1]

def a_star(adj_matrix, heuristics, start, goal):
    """Perform A* pathfinding given adjacency matrix and heuristics."""
    num_nodes = len(adj_matrix)
    open_list = []
    heapq.heappush(open_list, (heuristics[start][goal], 0, start))  # f, g, node

    g_score = {node: float('inf') for node in range(num_nodes)}
    g_score[start] = 0
    parent = {node: None for node in range(num_nodes)}

    while open_list:
        _, curr_g, curr = heapq.heappop(open_list)

        if curr == goal:
            return reconstruct_path(parent, goal)

        for neighbor, cost in enumerate(adj_matrix[curr]):
            if cost != float('inf'):
                tentative_g = curr_g + cost
                if tentative_g < g_score[neighbor]:
                    parent[neighbor] = curr
                    g_score[neighbor] = tentative_g
                    f = tentative_g + heuristics[neighbor][goal]
                    heapq.heappush(open_list, (f, tentative_g, neighbor))

    return None  # No valid path found

# --- Environment Setup ---

locations = {
    0: (-37.8135, 145.1120),  # Golden Leaf Restaurant
    1: (-37.8128, 145.1142),  # Residential Area
    2: (-37.8101, 145.1069),  # Strip Mall
    3: (-37.8108, 145.1072)   # Parking Lot
}


location_names = {
    0: "Golden Leaf Restaurant",
    1: "Residential Area",
    2: "Strip Mall",
    3: "Parking Lot"
}

adj_matrix = [
    [0, 2, float('inf'), 6],      # Restaurant
    [2, 0, float('inf'), 5],      # Residential Area
    [float('inf'), float('inf'), 0, 1],  # Strip Mall
    [6, 5, 1, 0]                  # Parking Lot
]



# Precompute heuristics (Manhattan)
heuristics = {
    i: {j: manhattan_distance(locations[i], locations[j]) for j in locations}
    for i in locations
}

# --- User Interaction ---
print("\nChoose your start and goal location:")
for idx, name in location_names.items():
    print(f"{idx}: {name}")

try:
    start = int(input("\nEnter start location (0-3): "))
    goal = int(input("Enter goal location (0-3): "))

    if start in locations and goal in locations:
        path = a_star(adj_matrix, heuristics, start, goal)
        if path:
            print("\nOptimal path:")
            for step in path:
                print(f" -> {location_names[step]}", end="")
            print(f"\nTotal cost: {sum(adj_matrix[path[i]][path[i+1]] for i in range(len(path)-1))}")
        else:
            print("No path found.")
    else:
        print("Invalid node selection. Choose between 0–3.")

except ValueError:
    print("Invalid input. Please enter integers only.")
