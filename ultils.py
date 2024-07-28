from object.map import Map
from level.level_1 import Level1
from level.level_2 import Level2
from level.level_3 import Level3
from level.level_4 import Level4



def extend_paths(paths):
    extended_paths = []
    for path in paths:
        if path == '-1':
            extended_paths.append('-1')
            continue
        
        parsed_path = list(map(lambda s: tuple(map(int, s.strip('()').split(','))), path.split(') (')))
        max_length = max(len(parsed_path) for parsed_path in [parsed_path])
        
        if len(parsed_path) < max_length:
            last_coord = parsed_path[-1]
            parsed_path.extend([last_coord] * (max_length - len(parsed_path)))
        
        extended_paths.append(' '.join(f'({x},{y})' for (x, y) in parsed_path))
    
    return extended_paths

def read_input(file_name, current_level):
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
                if cell.startswith('F'):
                    if current_level >= 3:
                        map_row.append(cell)
                    else:
                        map_row.append(0)
                elif cell.startswith('S'):
                    if current_level == 4:
                        map_row.append(cell)
                        number_agents += 1
                    else:
                        number_agents = 1
                        if cell == 'S':
                            map_row.append(cell)
                        else:
                            map_row.append(0)
                elif cell.startswith('G'):
                    if current_level == 4:
                        map_row.append(cell)
                    else:
                        if cell == 'G':
                            map_row.append(cell)
                        else:
                            map_row.append(0)
                else:
                    if int(cell) != -1 and int(cell) != 0:
                        if current_level >= 2:
                            map_row.append(int(cell))
                        else:
                            map_row.append(0)
                    else:
                        map_row.append(int(cell))
            map_data.append(map_row)
    if current_level == 2:
        f = 0
    if current_level == 1:
        t = 0
        f = 0
    return n,m,t, f, map_data, number_agents


def read_output(coordinates):
    if str(coordinates) == '-1':
        return ['-1'], 1
    coord_list = coordinates.strip().split(') ')
    lines = []
    for i in range(len(coord_list) - 1):
        start = tuple(map(int, coord_list[i].strip('(').split(',')))
        end = tuple(map(int, coord_list[i + 1].strip('()').split(',')))
        lines.append([start, end])
    number_of_steps = len(coord_list) - 1
    return lines, number_of_steps




def generate_inputfile_path(currentLevel, currentMap):
    return f'./test_case/level{currentLevel}/test{currentMap}.txt'

def parse_path(inputfile_path, current_level, algorithm):
    pathReturned = None
    _map = Map(inputfile_path)
    # print(inputfile_path)
    level = None
    if current_level == 1:
        level = Level1(_map)
        path1, path2, path3, path4, path5 = level.run()
        if algorithm == 1:            # BFS 
            pathReturned = path1
        elif algorithm == 2:          # DFS 
            pathReturned = path2
        elif algorithm == 3:          # UCS
            pathReturned = path3
        elif algorithm == 4:          # GBFS
            pathReturned = path4
        else:                         # AStar
            pathReturned = path5

    elif current_level == 2:
        level = Level2(_map)
        pathReturned = level.run()
    elif current_level == 3:
        level = Level3(_map)
        pathReturned = level.run()
        # print("Level 3")
        # pathReturned = [[(1, 1), (1, 2), (1, 3)], [(3, 2), (3, 3), (3, 4), (3, 5)]]
        # pathReturned = [(1, 1), (1, 2), (1, 3)]
    else:
        level = Level4(_map)
        pathReturned = level.run()
        # pass
    # print(_map.matrix)
    # print(current_level, algorithm, pathReturned)

    # print(pathReturned)
    # print(pathReturned)
    pathReturned = convert_tuples_to_strings(pathReturned)
    pathReturned = extend_paths(pathReturned)
    return pathReturned


def convert_tuples_to_strings(tuples_list):
    if tuples_list == -1:
        return ['-1']
    converted_path = []
    if type(tuples_list[0]) == list:
        for path in tuples_list:
            converted_path.append(" ".join(str(t) for t in path))
        return converted_path
    string_representation = " ".join(str(t) for t in tuples_list)
    return [string_representation]