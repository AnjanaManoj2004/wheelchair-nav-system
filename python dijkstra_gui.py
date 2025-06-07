import tkinter as tk
from tkinter import ttk, messagebox
import heapq

# -------------------- Dijkstra with terrain costs --------------------
def dijkstra(adj_matrix, start, goal, terrain_costs):
    num_nodes = len(adj_matrix)
    open_list = []
    heapq.heappush(open_list, (0, start))
    distances = {node: float('inf') for node in range(num_nodes)}
    distances[start] = 0
    parent_node = {node: None for node in range(num_nodes)}

    while open_list:
        current_distance, current_node = heapq.heappop(open_list)
        if current_node == goal:
            return reconstruct_path(parent_node, goal), distances[goal]

        for neighbor, cost in enumerate(adj_matrix[current_node]):
            if cost != float('inf'):
                if (current_node, neighbor) in terrain_costs:
                    cost += terrain_costs[(current_node, neighbor)]
                tentative_distance = current_distance + cost
                if tentative_distance < distances[neighbor]:
                    parent_node[neighbor] = current_node
                    distances[neighbor] = tentative_distance
                    heapq.heappush(open_list, (tentative_distance, neighbor))
    return None, float('inf')

def reconstruct_path(parent_node, goal):
    path = []
    current_node = goal
    while current_node is not None:
        path.append(current_node)
        current_node = parent_node[current_node]
    return path[::-1]

# -------------------- Data --------------------
locations = {
    0: ("Golden Leaf", (250, 120)),
    1: ("Residential Area", (400, 120)),
    2: ("Strip Mall", (120, 60)),
    3: ("Parking Lot", (40, 60)),
    4: ("Teppanyaki House", (130, 120)),
    5: ("Petrol Pump", (490, 220)),
    6: ("Burwood One", (440, 240))
}

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
# -------------------- GUI --------------------
root = tk.Tk()
root.title("Wheelchair-Friendly Pathfinder")
root.geometry("700x500")
root.configure(bg="#f0f0f0")

canvas = tk.Canvas(root, width=650, height=300, bg="white")
canvas.pack(pady=10)

# Draw static edges and nodes
node_coords = {}
for i in range(len(adj_matrix)):
    for j in range(i + 1, len(adj_matrix[i])):
        if adj_matrix[i][j] != float('inf'):
            x1, y1 = locations[i][1]
            x2, y2 = locations[j][1]
            canvas.create_line(x1, y1, x2, y2, fill="gray")

for idx, (name, pos) in locations.items():
    x, y = pos
    node_coords[idx] = (x, y)
    canvas.create_oval(x - 10, y - 10, x + 10, y + 10, fill="#90caf9", outline="black")
    canvas.create_text(x, y - 15, text=f"{idx}: {name}", font=("Arial", 9))

# Dropdown menus
frame = tk.Frame(root, bg="#f0f0f0")
frame.pack(pady=10)

tk.Label(frame, text="Start:", bg="#f0f0f0").grid(row=0, column=0)
start_var = tk.StringVar()
start_menu = ttk.Combobox(frame, textvariable=start_var, values=[f"{i}: {name}" for i, (name, _) in locations.items()], state="readonly", width=25)
start_menu.grid(row=0, column=1)
start_menu.current(0)

tk.Label(frame, text="Goal:", bg="#f0f0f0").grid(row=1, column=0)
goal_var = tk.StringVar()
goal_menu = ttk.Combobox(frame, textvariable=goal_var, values=[f"{i}: {name}" for i, (name, _) in locations.items()], state="readonly", width=25)
goal_menu.grid(row=1, column=1)
goal_menu.current(1)

# Result label
result_label = tk.Label(root, text="", font=("Arial", 11), bg="#f0f0f0", fg="black")
result_label.pack(pady=5)

# Pathfinding logic
def find_path():
    canvas.delete("path")  # Clear previous path lines

    try:
        start_id = int(start_var.get().split(":")[0])
        goal_id = int(goal_var.get().split(":")[0])
    except:
        messagebox.showerror("Error", "Please select valid start and goal nodes.")
        return

    path, total_cost = dijkstra(adj_matrix, start_id, goal_id, terrain_costs)

    if path:
        # Draw path in red
        for i in range(len(path) - 1):
            x1, y1 = node_coords[path[i]]
            x2, y2 = node_coords[path[i + 1]]
            canvas.create_line(x1, y1, x2, y2, fill="red", width=3, tags="path")
        readable_path = " → ".join(locations[i][0] for i in path)
        result_label.config(text=f"Path: {readable_path}\n Cost: {round(total_cost, 2)}")
    else:
        result_label.config(text=" No path found.")

# Button
tk.Button(root, text="Find Optimal Path", command=find_path, bg="#1976d2", fg="white", font=("Arial", 10, "bold")).pack(pady=10)

root.mainloop()
