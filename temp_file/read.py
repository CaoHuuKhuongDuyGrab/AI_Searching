# first init, divide file later 

from collections import deque
import heapq

def read_input(file_name):
    with open(file_name, 'r') as file:
        # Read the first line
        first_line = file.readline().strip()
        n, m, t, f = map(int, first_line.split())

        # Read the next n lines for the map
        map_data = []
        for _ in range(n):
            line = file.readline().strip().split()
            map_row = line[:]
            map_data.append(map_row)

    return n, m, t, f, map_data 

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
                # Calculate the new time if moving to the next cell
                if map_data[next_x][next_y] == '0' or map_data[next_x][next_y] == 'S' or map_data[next_x][next_y] == 'G':
                    move_time = 1  # Normal road
                elif map_data[next_x][next_y].isdigit():
                    move_time = int(map_data[next_x][next_y])  # Toll booth delay time
                else:
                    continue  # Barrier or invalid cell
                
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

if __name__ == "__main__":
    file_name = "I://AI_Searching/temp_file/input_lv2.txt"
    n, m, t, f, map_data = read_input(file_name)
    print("n:", n)
    print("m:", m)
    print("t:", t)
    print("f:", f)
    # Find start and goal positions
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
        # Find the shortest path using BFS
        shortest_path = bfs_shortest_path_with_time_constraint(map_data, start, goal, t)
        
        if shortest_path == "No path found":
            print("No path found from S to G")
        else:
            print("Shortest path from S to G:", shortest_path)
