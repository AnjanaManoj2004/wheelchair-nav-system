# Wheelchair Navigation System
Wheelchair-friendly pathfinding application that uses Dijkstra’s and A* algorithms to find optimal accessible routes across urban locations. Incorporates terrain-based costs and graphical visualization with a user-friendly interface.


## Features

- **Dijkstra’s Algorithm** with terrain slope penalties (uphill/downhill cost added).
- **A* Algorithm** using Manhattan distance as a heuristic.
- **Tkinter GUI** to visualize the map and show optimal wheelchair-accessible paths.
- **Interactive map** connecting seven real-world locations.
- Custom cost system to simulate real accessibility challenges.

---

## Locations Covered

1. Golden Leaf Chinese Restaurant  
2. Residential Area  
3. Strip Mall  
4. Parking Lot  
5. Burwood Teppanyaki House  
6. Petrol Pump  
7. Burwood One Shopping Centre  

These points were selected from a real-world map of Burwood East, Melbourne, and manually encoded to simulate a realistic environment for testing accessible navigation.

---

## Algorithms

### Dijkstra’s Algorithm

Used to compute the shortest accessible path from a start to destination node, factoring in terrain difficulty (e.g., uphill/downhill slopes).

### A* Algorithm

A more efficient version of Dijkstra that uses **Manhattan distance** as a heuristic to estimate path costs, improving performance.

---

## 🖥️ How to Use

### ▶️ Run Terminal Version

```bash
python dijkstra_terminal.py
```
This will prompt you to enter a starting location and destination. It will output the optimal path and total cost based on slope considerations.

```bash
python dijkstra_gui.py
```
A Tkinter window will launch, displaying the nodes on a simple grid. You can select start and end points using dropdowns and click "Find Path" to see the accessible route.

```bash
python a_star.py
```
## Requirements

Python 3.x
Tkinter (usually pre-installed with Python)
No external libraries required (only standard Python libraries like heapq)

## Author
Anjana Manoj

