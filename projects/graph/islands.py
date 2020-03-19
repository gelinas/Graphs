from util import Stack, Queue  # These may come in handy

'''
Write a function that takes a 2D binary array and returns the number of 1 islands. An island consists of 1s that are connected to the north, south, east or west. For example:
islands = [[0, 1, 0, 1, 0],
           [1, 1, 0, 1, 1],
           [0, 0, 1, 0, 0],
           [1, 0, 1, 0, 0],
           [1, 1, 0, 0, 0]]
island_counter(islands) # returns 4
'''
islands = [[0, 1, 0, 1, 0],
           [1, 1, 0, 1, 1],
           [0, 0, 1, 0, 0],
           [1, 0, 1, 0, 0],
           [1, 1, 0, 0, 0]]

def island_counter(matrix):
    # create a visited matrix
    visited = []
    for i in range(len(matrix)):
        visited.append([False] * len(matrix[0]))
    island_count = 0
    # for all nodes
    for col in range(len(matrix[0])):
        for row in range(len(matrix)):
            #if node is not visited
            if not visited [row][col]:
                # If we hit a 1 that has not been visited
                if matrix[row][col] == 1:
                    # mark visited
                    # traverse all connected nodes, marking as visited
                    visited = dft(row, col, matrix, visited)
                    island_count += 1
    return island_count

def dft(start_row, start_col, matrix, visited):
    # create a STACK, otherwise same as above
    s = Stack()
    # push the starting vertex
    s.push((start_row, start_col))
    # while the stack is not empty...
    while s.size() > 0:
        # pop the first vertex
        temp = s.pop()
        row = temp[0]
        col = temp[1]
        # do the thing:
        # check if it's been visited and print if not
        if not visited[row][col]:
            # Mark it as visited
            visited[row][col] = True
            # push all it's neighbors
            for neighbor in get_neighbors(row, col, matrix):
                s.push(neighbor)
    return visited

def get_neighbors(row, col, matrix):
    '''
    return a list of neighboring 1 tuples in the form [(row, col)]
    '''
    neighbors = []
    # check north
    if row > 0 and matrix[row-1][col]:
        neighbors.append((row-1, col))
    # check south
    if row < len(matrix) - 1 and matrix[row+1][col]:
        neighbors.append((row+1, col))
    # check east
    if col < len(matrix[0]) - 1 and matrix[row][col+1]:
        neighbors.append((row, col+1))
    # check west
    if col > 0 and matrix[row][col-1]:
        neighbors.append((row, col-1))
    return neighbors

print(island_counter(islands))