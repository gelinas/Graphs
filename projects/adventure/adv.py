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
                    'w': None
                    # 'x': current_room.x,
                    # 'y': current_room.y
                }
                for direction in ['n', 's', 'e', 'w']:
                    # get neighboring room object
                    neighbor = current_room.get_room_in_direction(direction)
                    if neighbor is not None:
                        # add neighboring room id to map
                        self.map[current_room.id][direction] = neighbor.id
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
# adv_map = WorldGraph()
# adv_map.map_world(world.starting_room)
# print(adv_map.map)


# 3. Traverse your graph
'''
1. Possibility of using quadrants or connected components to prioritize traversals
2. need to log "moves" including backtracking
3. First pass
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
        while len(self.visited) < len(world.rooms):
            # check if current_room has been visited and map if not
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
            # do the other thing: move to a "?"
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
                
            else:
                # do the other thing: no "?"s, BFS to a room with a "?"
                # use self.find_nearest_unvisited_room() to find room id
                # use go_to_mapped_room
                # repeat loop
                print("Ran out of ?s")
                break
        else:
            print("You traversed the entire world!")
            print(f"Path Length: {len(self.traversal_path)} \n Traveral Path: {self.traversal_path}")
        print("loop terminated by break")
        print(f"Path Length: {len(self.traversal_path)} \n Traversal Path: {self.traversal_path}")

    def travel(self, direction):
        '''
        go in a direction
        log to self.traversal_path
        '''
        if direction in ['n', 's', 'e', 'w']:
            print(f"Moving {direction}")
            self.traversal_path.append(direction)
            player.travel(direction)
        else:
            print("ERROR: invalid direction")

    def find_nearest_unvisited_room(self):
        """
        Breadth first search for room with "?"s
        """
        pass

    def go_to_mapped_room(self, player, target_room):
        """
        Breadth first search for shortest path to target_room
        travel there and log path
        """
        pass
        # print("FINAL:")
        # print(self.visited)
        # print(self.map)
        # print(f"Length visited: {len(self.visited)}, Length mapped: {len(self.map)}")


test = DepthFirstRoute()
test.traverse_world(player)
    



# traversal_path = ['n', 'n']
# traversal_path = ['n', 'n']



# TRAVERSAL TEST
# visited_rooms = set()
# player.current_room = world.starting_room
# visited_rooms.add(player.current_room)

# for move in traversal_path:
#     print(player.current_room.__str__())
#     player.travel(move)
#     visited_rooms.add(player.current_room)

# if len(visited_rooms) == len(room_graph):
#     print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
# else:
#     print("TESTS FAILED: INCOMPLETE TRAVERSAL")
#     print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



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
