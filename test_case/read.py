# first init, divide file later 

from collections import deque
import heapq

def read_input(file_name):
    with open(file_name, 'r') as file:
        # Read the first line
        number_agents = 0
        first_line = file.readline().strip()
        n, m, t, f = map(int, first_line.split())

        # Read the next n lines for the map
        map_data = []
        for _ in range(n):
            line = file.readline().strip().split()
            map_row = []
            for cell in line:
                if cell.startswith('F') or cell.startswith('S') or cell.startswith('G') or cell == -1:
                    map_row.append(cell)
                    if (cell.startswith('S')):
                        number_agents += 1
                else:
                    map_row.append(int(cell))
            map_data.append(map_row)

    return n, m, t, f, map_data, number_agents











def bfs_shortest_path(map_data, start, goal):
    # Directions for moving in 4 possible directions: up, down, left, right
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    rows = len(map_data)
    cols = len(map_data[0])
    
    # Initialize queue for BFS, starting with the start position
    queue = deque([start])

    # Visited array to keep track of visited nodes
    visited = [[False]*cols for _ in range(rows)]
    visited[start[0]][start[1]] = True

    # Parent dictionary to reconstruct the path if needed
    parent = {}
    
    while queue:
        current_x, current_y = queue.popleft()
        
        # Check if we reached the goal
        if (current_x, current_y) == goal:
            break
        
        # Explore neighbors
        for direction in directions:
            next_x = current_x + direction[0]
            next_y = current_y + direction[1]
            
            # Check if the next position is within bounds and is a valid move
            if 0 <= next_x < rows and 0 <= next_y < cols and not visited[next_x][next_y] and map_data[next_x][next_y] != '-1':
                visited[next_x][next_y] = True
                queue.append((next_x, next_y))
                parent[(next_x, next_y)] = (current_x, current_y)
    
    # If we reached here, reconstruct the path from start to goal
    if (goal[0], goal[1]) not in parent:
        return "No path found"
    
    # Reconstruct path
    path = []
    current = (goal[0], goal[1])
    while current != start:
        path.append(current)
        current = parent[current]
    path.append(start)
    path.reverse()
    
    return path

def bfs_shortest_path_with_time_constraint(map_data, start, goal, t):
    # Directions for moving in 4 possible directions: up, down, left, right
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    rows = len(map_data)
    cols = len(map_data[0])
    
    # Priority queue (min-heap) to explore nodes with the minimum time taken
    pq = [(0, start[0], start[1])]  # (time_taken, x, y)
    heapq.heapify(pq)
    
    # Time taken array to keep track of the minimum time to reach each cell
    time_taken = [[float('inf')] * cols for _ in range(rows)]
    time_taken[start[0]][start[1]] = 0
    
    # Parent dictionary to reconstruct the path if needed
    parent = {}
    
    while pq:
        current_time, current_x, current_y = heapq.heappop(pq)
        
        # If we reach the goal within the committed time, return the path
        if (current_x, current_y) == goal and current_time <= t:
            break
        
        # Explore neighbors
        for direction in directions:
            next_x = current_x + direction[0]
            next_y = current_y + direction[1]
            
            # Check if the next position is within bounds
            if 0 <= next_x < rows and 0 <= next_y < cols:
                next_cell = map_data[next_x][next_y]
                
                # Calculate the new time if moving to the next cell
                if next_cell == 0 or next_cell == 'S' or next_cell == 'G':
                    move_time = 1  # Normal road
                elif next_cell == '-1':
                    continue  # Barrier or invalid cell
                else:
                    move_time = int(next_cell)  # Toll booth delay time
                
                new_time = current_time + move_time
                
                # Only proceed if the new time is less than the previously recorded time
                if new_time < time_taken[next_x][next_y] and new_time <= t:
                    time_taken[next_x][next_y] = new_time
                    heapq.heappush(pq, (new_time, next_x, next_y))
                    parent[(next_x, next_y)] = (current_x, current_y)
    
    # If we reached here, reconstruct the path from start to goal
    if (goal[0], goal[1]) not in parent or time_taken[goal[0]][goal[1]] > t:
        return "No path found within the committed time"
    
    # Reconstruct path
    path = []
    current = (goal[0], goal[1])
    while current != start:
        path.append(current)
        current = parent[current]
    path.append(start)
    path.reverse()
    
    return path

def bfs_shortest_path_with_fuel(map_data, start, goal, t, f):
    # Directions for moving in 4 possible directions: up, down, left, right
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    rows = len(map_data)
    cols = len(map_data[0])
    
    # Priority queue (min-heap) to explore nodes with the minimum time taken
    pq = [(0, start[0], start[1], f)]  # (time_taken, x, y, remaining_fuel)
    heapq.heapify(pq)
    
    # Time taken array to keep track of the minimum time to reach each cell with remaining fuel
    time_taken = [[[float('inf')] * (f + 1) for _ in range(cols)] for _ in range(rows)]
    time_taken[start[0]][start[1]][f] = 0
    
    # Parent dictionary to reconstruct the path if needed
    parent = {}
    
    while pq:
        current_time, current_x, current_y, current_fuel = heapq.heappop(pq)
        
        # If we reach the goal within the committed time, return the path
        if (current_x, current_y) == goal and current_time <= t:
            break
        
        # Explore neighbors
        for direction in directions:
            next_x = current_x + direction[0]
            next_y = current_y + direction[1]
            
            # Check if the next position is within bounds
            if 0 <= next_x < rows and 0 <= next_y < cols:
                next_cell = map_data[next_x][next_y]
                
                # Calculate the new time and fuel if moving to the next cell
                if next_cell == 0 or next_cell == 'S' or next_cell == 'G':
                    move_time = 1  # Normal road
                    new_fuel = current_fuel - 1
                elif next_cell == '-1':
                    continue  # Barrier or invalid cell
                elif isinstance(next_cell, str) and next_cell.startswith('F'):
                    move_time = 1  # Refueling at gas station
                    new_fuel = f  # Refuel to full capacity
                else:
                    move_time = int(next_cell)  # Toll booth delay time
                    new_fuel = current_fuel - 1

                # If the vehicle runs out of fuel, skip this path
                if new_fuel < 0:
                    continue
                
                new_time = current_time + move_time
                
                # Only proceed if the new time is less than the previously recorded time
                if new_time < time_taken[next_x][next_y][new_fuel] and new_time <= t:
                    time_taken[next_x][next_y][new_fuel] = new_time
                    heapq.heappush(pq, (new_time, next_x, next_y, new_fuel))
                    parent[(next_x, next_y, new_fuel)] = (current_x, current_y, current_fuel)
    
    # If we reached here, reconstruct the path from start to goal
    goal_reached = False
    for fuel in range(f + 1):
        if (goal[0], goal[1], fuel) in parent:
            goal_reached = True
            break
    
    if not goal_reached:
        return "No path found"
    
    # Reconstruct path
    path = []
    current = (goal[0], goal[1], fuel)
    while current != (start[0], start[1], f):
        path.append((current[0], current[1]))
        current = parent[current]
    path.append((start[0], start[1]))
    path.reverse()
    
    return path

if __name__ == "__main__":
    file_name = "D://AI_Searching/temp_file/my_input.txt"
    n, m, t, f, map_data, number_agents = read_input(file_name)
    print("n:", n)
    print("m:", m)
    print("t:", t)
    print("f:", f)
    # Find start and goal positions
    # print(map_data)
    start = None
    goal = None
    for i in range(len(map_data)):
       for j in range(len(map_data[0])):
            if map_data[i][j] == 'S':
                start = (i, j)
            elif map_data[i][j] == 'G':
                goal = (i, j)
    
    if start is None or goal is None:
        print("Start or goal not found in the map!")
    else:
        # Find the shortest path using BFS with fuel constraints
        shortest_path = bfs_shortest_path_with_fuel(map_data, start, goal, t, f)
        # shortest_path = bfs_shortest_path_with_time_constraint(map_data, start, goal, t)
        if shortest_path == "No path found within the committed time":
            print("No path found from S to G within the committed time")
        else:
            print("Shortest path from S to G:", shortest_path)
