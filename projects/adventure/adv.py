from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

from util import Stack, Queue  # These may come in handy

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk

# 1. Translate the problem into graph terminology
'''
Cyclic undirected graph. Goal is to visit every node in smallest number of edge traversals
'''

# 2. Build your graph
'''
Use depth first traversal to create a graph of the map
'''

class WorldGraph:
    def __init__(self):
        # add key value 'room_id': RoomObject
        self.visited = {}
        # map room exits, id, coordinates
        self.map = {}
        # dictionary entires of the form:
        # 0 : {'n': None, 's': int, 'w': int, 'e': None, 'x': int, 'y': int}
        # Or:
        # 0 : {'n': None, 's': int, 'w': int, 'e': None}

        # 0 for nothing, ? for unknown, int for id for next room. Plus x / y coord

    def map_world(self, starting_room):
        """
        Depth first traversal to map all rooms
        Map each room in depth-first order
        beginning from starting_room.
        """
        # create a STACK, otherwise same as above
        s = Stack()
        # push the starting vertex
        s.push(starting_room)
        # use self.visited dictionary to store visited rooms
        # while the stack is not empty...
        while s.size() > 0:
            # pop the first room
            current_room = s.pop()
            # do the thing:
            # check if it's been visited and map if not
            if current_room.id not in self.visited.keys():
                # visit it
                self.visited[current_room.id] = current_room
                # Map it
                self.map[current_room.id] = {
                    'n': None,
                    's': None,
                    'e': None,
                    'w': None,
                    "connections": 0
                }
                for direction in ['n', 's', 'e', 'w']:
                    # get neighboring room object
                    neighbor = current_room.get_room_in_direction(direction)
                    if neighbor is not None:
                        # add neighboring room id to map
                        self.map[current_room.id][direction] = neighbor.id
                        self.map[current_room.id]['connections'] += 1
                        # add room to stack
                        s.push(neighbor)
        # print("FINAL:")
        # print(self.visited)
        # print(self.map)
        # print(f"Length visited: {len(self.visited)}, Length mapped: {len(self.map)}")

'''
create world graph glass
Depth first traversal to map the world into an adjaceny list
Print the adjaceny list
'''
adv_map = WorldGraph()
adv_map.map_world(world.starting_room)
# print(adv_map.map)


# 3. Traverse your graph
'''
1. Possibility of using quadrants or connected components to prioritize traversals
2. need to log "moves" including backtracking
3. First pass just use depth first traversing plus BFS for '?'s when reaching a dead end
'''
class DepthFirstRoute:
    def __init__(self):
        # add key value 'room_id': RoomObject
        self.visited = {}
        # map room exits, id, coordinates
        # dictionary entires of the form:
        # 0 : {'n': None, 's': int, 'w': int, 'e': None}
        self.map = {}
        # traversal path
        self.traversal_path = []
        

    def traverse_world(self, player):
        """
        Depth first traversal to map all rooms
        Map each room in depth-first order
        beginning from starting_room.
        """
        # reset values
        self.visited = {}
        self.map = {}
        self.traversal_path = []

        # victory condition: every room visited
        while len(self.visited) < len(world.rooms):

            # Step 1: check if current_room has been visited and map if not
            if player.current_room.id not in self.visited.keys():
                # visit it
                self.visited[player.current_room.id] = player.current_room
                # Map it
                self.map[player.current_room.id] = {
                    'n': None,
                    's': None,
                    'e': None,
                    'w': None
                    # 'x': current_room.x,
                    # 'y': current_room.y
                }
                for direction in ['n', 's', 'e', 'w']:
                    # get neighboring room object
                    neighbor = player.current_room.get_room_in_direction(direction)
                    if neighbor is not None:
                        if neighbor.id not in self.visited:
                            # add '?' to indicate need to travel there
                            self.map[player.current_room.id][direction] = '?'
                        else:
                            # add id reference to indicate it has been explored
                            self.map[player.current_room.id][direction] = neighbor.id
                # print new map
                # print(f"updated map: {self.map}")

            # Step 2: check for neighboring unexplored rooms and randomly travel to one, restart loop
            if "?" in self.map[player.current_room.id].values():
                # get a list of unexplored directions
                options = []
                for key in self.map[player.current_room.id]:
                    if self.map[player.current_room.id][key] == "?":
                        options.append(key)
                # randomly pick an unexplored direction and get that room id
                rand_num = random.randrange(len(options))
                rand_direction = options[rand_num]
                next_room = player.current_room.get_room_in_direction(rand_direction)
                # replace the "?" with the correct id
                self.map[player.current_room.id][rand_direction] = next_room.id
                # move to that direction
                self.travel(rand_direction)
            
            # Step 3: If no neighboring unexplored rooms, move to the closest known unexplored room
            else:
                # use self.find_nearest_unvisited_room() to find path
                shortest_path = self.find_nearest_unvisited_room(player.current_room.id)
                # use follow_path
                if shortest_path is not None:
                    # print("UPDATE: Ran out of ?s, found closest unexplored path and starting again")
                    self.follow_path(shortest_path)
                # repeat loop
                else:
                    # print(f"BREAK: find_nearest_unvisited_room returned None.")
                    pass
                # print(f"LOOP END: Current Path Length: {len(self.traversal_path)} \nCurrent Visited Length: {len(self.visited)}")
        else:
            # print("You traversed the entire world!")
            # print(f"Path Length: {len(self.traversal_path)} \nTraversal Path: {self.traversal_path}")
            return self.traversal_path

    def travel(self, direction):
        '''
        go in a direction
        log to self.traversal_path
        '''
        if direction in ['n', 's', 'e', 'w']:
            # print(f"Moving {direction}")
            self.traversal_path.append(direction)
            player.travel(direction)
        else:
            print("ERROR: invalid direction")

    def find_nearest_unvisited_room(self, current_room):
        """
        Breadth first search for path to room with "?"s
        pass in current_room as int 'id'
        return path as sequential list of tuples
        tuple format (room_id, direction_to_room)
        """
        q = Queue()
        # equeue path to current room
        # tuple of (room_id, direction_to_room)
        q.enqueue([(current_room, None)])
        # visited just tracks room.id ints
        visited = set()
        while q.size() > 0:
            path = q.dequeue()
            end = path[-1][0]
            if end not in visited:
                visited.add(end)
                # check if there's a "?" in the map for that room
                if "?" in self.map[end].values():
                    return path
                for direction in self.map[end]:
                    neighbor = self.map[end][direction]
                    if neighbor not in visited and neighbor is not None:
                        new_path = path.copy()
                        new_step = (neighbor, direction)
                        new_path.append(new_step)
                        q.enqueue(new_path)
        else:
            # print("No '?'s found on graph")
            return None
        

    def follow_path(self, path):
        """
        Take path in (room_id, direction_to_room) and travel to the end
        """
        for step in path:
            if step[1] is not None:
                self.travel(step[1])
        # print(f"Travel complete. Current location: {player.current_room.id}")
        # print(f"Adjacent rooms: {self.map[player.current_room.id]}")


test = DepthFirstRoute()

'''
MVP solution
run with random succesful path
'''
# player.current_room = world.starting_room
# traversal_path = test.traverse_world(player)

'''
Stretch attempt #1
continuously run function and look for shortest path (random)
'''
# def find_shortest_path(attempts):
#     count = 0
#     best_path = test.traverse_world(player)
#     while count < attempts and len(best_path) > 959:
#         player.current_room = world.starting_room
#         new_path = test.traverse_world(player)
#         if len(new_path) < len(best_path):
#             best_path = new_path.copy()
#             print(best_path)
#             print(f"New shortest: {len(best_path)}")
#         count +=1
#     print(f"best_path:{best_path}")
#     return best_path

# best_path = find_shortest_path(50000)

# 963 path shortest so far
saved_path = ['s', 'w', 'e', 'n', 'w', 'w', 's', 'w', 's', 's', 'n', 'n', 'e', 'n', 'e', 'n', 'w', 'w', 's', 'n', 'w', 's', 's', 's', 'w', 'w', 'w', 's', 'w', 'n', 's', 'e', 'n', 'e', 'e', 'n', 'w', 'w', 'w', 'e', 'e', 'e', 's', 'e', 's', 'w', 's', 'w', 'e', 'n', 'w', 'e', 'e', 's', 's', 's', 's', 'w', 's', 'w', 's', 'w', 'e', 's', 'w', 'e', 'n', 'n', 'e', 's', 's', 'n', 'n', 'n', 'e', 's', 's', 's', 'e', 'e', 's', 's', 'e', 'w', 's', 'w', 'e', 'n', 'n', 'n', 'w', 's', 'n', 'w', 's', 'w', 'e', 'n', 'n', 'n', 'n', 'n', 'n', 'w', 's', 'w', 'w', 'w', 'w', 'e', 's', 'w', 'w', 'e', 'e', 's', 's', 's', 's', 'e', 'w', 's', 'e', 'w', 'n', 'n', 'n', 'n', 'w', 's', 's', 's', 's', 'n', 'w', 'w', 'e', 'e', 'n', 'w', 'e', 'n', 'w', 'e', 'n', 'w', 'w', 'w', 'e', 'e', 'e', 'e', 'n', 'n', 'e', 'e', 's', 'w', 's', 'n', 'e', 'n', 'e', 'n', 'w', 'w', 'n', 's', 'w', 'w', 'w', 's', 'w', 's', 'n', 'e', 'n', 'e', 'e', 'n', 'w', 'w', 'n', 'w', 'e', 's', 'e', 'n', 'n', 'w', 'n', 'w', 'e', 'e', 'n', 'w', 'n', 's', 'w', 'e', 'e', 'n', 's', 'e', 'e', 'e', 'n', 'e', 'n', 'w', 'w', 'w', 'n', 'w', 'w', 'w', 'e', 's', 'n', 'e', 'n', 'n', 's', 'w', 'w', 'w', 'e', 'e', 'e', 's', 'e', 'n', 's', 's', 'w', 'e', 'e', 'e', 'e', 'e', 'e', 'e', 'n', 's', 'e', 'e', 'e', 's', 'e', 'n', 'n', 'n', 'e', 'n', 'n', 's', 's', 'w', 'n', 'n', 's', 's', 's', 's', 'e', 'n', 'e', 'n', 'n', 'n', 'n', 's', 's', 's', 'e', 'n', 'n', 'e', 'n', 'n', 'e', 'n', 's', 'e', 'e', 'e', 'w', 'n', 's', 'w', 'n', 's', 'w', 'w', 's', 's', 'w', 'n', 's', 's', 's', 'w', 's', 'w', 's', 'w', 's', 'e', 'e', 'e', 'e', 'e', 'e', 'w', 'w', 's', 'e', 'e', 'e', 'n', 's', 'e', 'w', 'w', 'w', 'w', 'n', 'w', 's', 'n', 'w', 'n', 'e', 'e', 'e', 'e', 'e', 'e', 's', 'n', 'w', 'w', 'w', 'w', 'w', 'n', 'e', 'n', 'e', 'e', 's', 'e', 'e', 'e', 's', 'n', 'w', 'w', 'w', 'n', 'e', 'e', 'w', 'n', 'e', 'w', 's', 'w', 'w', 's', 'n', 'w', 'n', 'e', 'e', 'n', 'e', 'w', 's', 'w', 'n', 'n', 'e', 'e', 'e', 's', 'n', 'w', 'w', 'w', 's', 's', 'w', 's', 's', 'w', 's', 'w', 's', 'w', 's', 'e', 's', 's', 'e', 'w', 'n', 'e', 'e', 'e', 'e', 'e', 'w', 'w', 'w', 's', 's', 's', 's', 'e', 'e', 'w', 'w', 's', 'e', 'e', 'w', 'w', 'n', 'n', 'e', 'n', 's', 'e', 'w', 'w', 'n', 'n', 'e', 'e', 'e', 'w', 's', 'n', 'w', 'w', 'n', 'w', 'w', 'n', 'w', 's', 's', 'n', 'n', 'n', 'w', 'w', 's', 'e', 'w', 's', 's', 'w', 's', 's', 's', 's', 's', 's', 's', 's', 's', 's', 'n', 'n', 'n', 'n', 'n', 'w', 'w', 'w', 'n', 's', 'e', 's', 'e', 's', 's', 's', 'n', 'n', 'n', 'w', 's', 'n', 'w', 's', 'n', 'e', 'n', 'e', 'n', 'w', 'e', 'n', 'w', 'e', 'n', 'w', 'w', 's', 'n', 'e', 'e', 'n', 'w', 'e', 'n', 'w', 'e', 'e', 'w', 'e', 'e', 's', 's', 's', 's', 's', 'n', 'e', 's', 's', 'w', 's', 's', 'n', 'n', 'e', 's', 'e', 'e', 'e', 'n', 'e', 's', 's', 'n', 'n', 'e', 's', 's', 's', 's', 'n', 'n', 'e', 'w', 'n', 'n', 'e', 'w', 'w', 'w', 's', 'w', 'w', 's', 's', 's', 'n', 'n', 'e', 's', 's', 'n', 'n', 'e', 's', 's', 'n', 'n', 'w', 'w', 'n', 'w', 's', 's', 'w', 's', 'n', 'e', 's', 's', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'w', 'n', 'n', 'n', 'e', 's', 's', 'n', 'n', 'e', 's', 's', 's', 's', 's', 'e', 'w', 'n', 'n', 'n', 'e', 's', 's', 'e', 'e', 'e', 'e', 'w', 'w', 'w', 'w', 'n', 'e', 'w', 'n', 'w', 'n', 'e', 'n', 'e', 's', 's', 'n', 'n', 'w', 's', 'w', 'n', 'w', 'w', 'n', 'n', 'e', 's', 'n', 'w', 'n', 'w', 'n', 's', 'e', 'n', 'n', 'w', 'n', 'w', 'e', 'n', 'e', 's', 'n', 'n', 'n', 'w', 'n', 'n', 'w', 'n', 'e', 'w', 'w', 'e', 's', 'e', 's', 's', 'e', 'n', 'e', 'e', 'w', 'w', 'n', 'n', 'e', 'w', 'n', 'e', 'n', 'n', 's', 's', 'w', 'n', 'n', 'n', 'e', 'n', 'w', 'w', 'e', 'e', 's', 'e', 'n', 'e', 'e', 'w', 'w', 's', 's', 's', 's', 'e', 's', 'e', 'n', 'e', 'e', 'e', 'w', 'n', 's', 'w', 'n', 's', 'w', 's', 'e', 'w', 'w', 's', 'w', 'n', 's', 'w', 'w', 'e', 'e', 'e', 'e', 'w', 'n', 'n', 'n', 'e', 'n', 'e', 'n', 'n', 's', 'e', 'e', 'w', 's', 'n', 'w', 's', 'w', 'n', 's', 's', 'w', 'n', 'n', 's', 's', 's', 's', 's', 'w', 'w', 'w', 'n', 'n', 'w', 'w', 'w', 'n', 'n', 'n', 'n', 's', 's', 's', 'w', 'n', 'n', 'w', 'e', 's', 's', 'e', 's', 'w', 'w', 'w', 'n', 's', 'e', 'n', 's', 'e', 's', 'w', 'e', 'n', 'e', 'e', 'e', 'n', 'w', 'n', 's', 'e', 'n', 's', 's', 'e', 's', 's', 's', 's', 's', 's', 'w', 'w', 'n', 'w', 'n', 's', 'e', 'n', 'n', 'w', 'w', 'n', 'w', 'e', 's', 'e', 'n', 's', 'e', 's', 's', 's', 'w', 'w', 'w', 'n', 's', 'w', 'n', 'w', 'n', 'n', 'n', 'n', 'n', 'n', 's', 's', 'w', 'e', 's', 's', 's', 'w', 'w', 'w', 'w', 'w', 'e', 's', 'w', 'e', 'n', 'e', 'e', 'n', 'n', 'n', 's', 's', 'w', 'e', 's', 'e', 'n', 'n', 's', 's', 'e', 's', 'w', 'w', 'e', 'e', 'e', 'n', 'n', 'n', 'n', 's', 's', 's', 's', 's', 'e', 'e', 'n', 'n', 'w', 'n', 's', 'e', 's', 's', 'e', 'e', 'e', 'n', 's', 's', 's', 'w', 'w', 'w', 'n', 's', 'w', 'n', 's', 'w', 'n', 'w', 'n', 'w', 'e', 's', 'w', 'e', 'e', 's', 's', 's', 'n', 'w', 'w', 'w']


# run with 960 step saved path
traversal_path = saved_path.copy()

# run with random succesful path
# player.current_room = world.starting_room
# traversal_path = test.traverse_world(player)



# # TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    print(player.current_room.__str__())
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
