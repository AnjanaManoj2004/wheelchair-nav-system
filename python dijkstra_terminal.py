import heapq

# Implementation of Dijkstra's Algorithm considering terrain-based adjustments (e.g., slope and obstacles)
def dijkstra(adj_matrix, start, goal, terrain_costs):
    num_nodes = len(adj_matrix)

    # Priority queue to prioritize exploration of nodes with the shortest known distance
    open_list = []
    heapq.heappush(open_list, (0, start))  # Push the starting node with initial cost of 0

    # Initialize dictionaries to track the shortest distances and parent nodes
    distances = {node: float('inf') for node in range(num_nodes)}
    distances[start] = 0
    parent_node = {node: None for node in range(num_nodes)}

    while open_list:
        current_distance, current_node = heapq.heappop(open_list)

        # If the destination node is reached, reconstruct and return the path
        if current_node == goal:
            return reconstruct_path(parent_node, goal)

        # Explore neighboring nodes (adjacent locations)
        for neighbor, cost in enumerate(adj_matrix[current_node]):
            if cost != float('inf'):  # Check if there's a valid path
                # Apply terrain adjustments (like slope penalties) where applicable
                if (current_node, neighbor) in terrain_costs:
                    cost += terrain_costs[(current_node, neighbor)]
                
                tentative_distance = current_distance + cost
                if tentative_distance < distances[neighbor]:
                    parent_node[neighbor] = current_node
                    distances[neighbor] = tentative_distance
                    heapq.heappush(open_list, (tentative_distance, neighbor))

    return None  # Return None if no valid path exists

# Helper function to reconstruct the shortest path from start to goal node
def reconstruct_path(parent_node, goal):
    path = []
    current_node = goal
    while current_node is not None:
        path.append(current_node)
        current_node = parent_node[current_node]
    return path[::-1]  # Reverse the path to get it from start to goal

# 0 = Golden Leaf, 1 = Residential Area, 2 = Strip Mall, 3 = Parking Lot, 4 = Burwood Teppanyaki House, 5 = Petrol Pump, 6 = Burwood One Shopping Centre
adj_matrix = [
    [0, 1, float('inf'), float('inf'), 1, float('inf'), float('inf')],  # Golden Leaf
    [1, 0, float('inf'), 8, float('inf'), 10, 7],            # Residential Area
    [float('inf'), float('inf'), 0, 1, float('inf'), float('inf'), float('inf')],  # Strip Mall
    [float('inf'), 8, 1, 0, 3, float('inf'), float('inf')],             # Parking Lot
    [1, float('inf'), float('inf'), 3, 0, float('inf'), float('inf')],  # Teppanyaki
    [float('inf'), 10, float('inf'), float('inf'), float('inf'), 0, float('inf')],  # Petrol Pump
    [float('inf'), 7, float('inf'), float('inf'), float('inf'), float('inf'), 0]   # Burwood One Shopping Centre
]

# Asymmetric terrain penalties: uphill = higher penalty, downhill = lower
terrain_costs = {
    (1, 0): 3,  # Residential Area -> Golden Leaf (uphill)
    (3, 0): 1,  # Parking Lot -> Golden Leaf (downhill)
    (0, 3): 1,  # Golden Leaf -> Parking Lot (downhill)
    (1, 6): 3,  # Residential Area -> Burwood One (uphill)
    (6, 1): 1,  # Burwood One -> Residential Area (downhill)
    (1, 5): 3,  # Residential Area -> Petrol Pump (uphill)
    (5, 1): 1,  # Petrol Pump -> Residential Area (downhill)
    (4, 3): 2,  # Teppanyaki -> Parking Lot (uphill)
    (3, 4): 1,  # Parking Lot -> Teppanyaki (downhill)
    (2, 3): 1,  # Strip Mall -> Parking Lot (uphill)
    (3, 2): 1   # Parking Lot -> Strip Mall (slight uphill/downhill)
}

# Locations (for easy reference when displaying results)
locations = {
    0: "Golden Leaf Chinese Restaurant",
    1: "Residential Area",
    2: "Strip Mall",
    3: "Parking Lot",
    4: "Burwood Teppanyaki House",
    5: "Petrol Pump",
    6: "Burwood One Shopping Centre"
}

# Display available locations for user input
print("Locations: ")
for loc, name in locations.items():
    print(f"{loc} = {name}")
try:
    start = int(input("\nEnter the start location (0–6): "))
    goal = int(input("Enter the goal location (0–6): "))

    if start in locations and goal in locations:
        path = dijkstra(adj_matrix, start, goal, terrain_costs)
        if path:
            print("\nOptimal path found:")
            for step in path:
                print(f" -> {locations[step]}", end="")
            # Calculate the total cost including terrain adjustments
            total_cost = 0
            for i in range(len(path) - 1):
                base_cost = adj_matrix[path[i]][path[i + 1]]
                terrain_penalty = terrain_costs.get((path[i], path[i + 1]), 0)
                total_cost += base_cost + terrain_penalty
            print(f"\nTotal cost (with terrain penalties): {total_cost}")
        else:
            print("No path found.")
    else:
        print("Invalid node selection. Please choose values between 0–6.")

except ValueError:
    print("Invalid input. Please enter **integers only**.")
