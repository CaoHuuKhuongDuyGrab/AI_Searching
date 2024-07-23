def extend_paths(paths):
    parsed_paths = [list(map(lambda s: tuple(map(int, s.strip('()').split(','))), path.split(') ('))) for path in paths]
    max_length = max(len(path) for path in parsed_paths)
    extended_paths = []
    for path in parsed_paths:
        if len(path) < max_length:
            last_coord = path[-1]
            path.extend([last_coord] * (max_length - len(path)))
        extended_paths.append(path)
    extended_paths_str = [' '.join(f'({x},{y})' for (x, y) in path) for path in extended_paths]
    return extended_paths_str

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


def read_output(coordinates):
    coord_list = coordinates.strip().split(') ')
    lines = []
    for i in range(len(coord_list) - 1):
        start = tuple(map(int, coord_list[i].strip('(').split(',')))
        end = tuple(map(int, coord_list[i + 1].strip('()').split(',')))
        lines.append([start, end])
    number_of_steps = len(coord_list) - 1
    return lines, number_of_steps

