from room import Room
from player import Player
from world import World
from util import Stack, Queue

import random
from ast import literal_eval

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
# traversal_path = ['n', 'n']
traversal_path = []
visited = {}
last_room = 0

def return_opposites(direction):
    if direction == "n":
        return "s"
    if direction == "s":
        return "n"
    if direction == "e":
        return "w"
    if direction == "w":
        return "e"
def mark_as_visited(current_room_id):
    if current_room_id not in visited:
        # Mark it as visited
        visited[current_room_id] = {} # visited = { 0: {} }
        # Store all possible directions in room key value ex: visited = { 0: { 'n': '?', 's': '?', 'w': '?', 'e': '?'} }
        for direction in player.current_room.get_exits():
            visited[current_room_id][direction] = '?' # 'n' : '?'
def update_visited_rooms(current_room_id):
    if current_room_id not in visited:
        # Mark it as visited
        mark_as_visited(current_room_id)
    d = random.choice(list(visited[current_room_id].keys()))# Generate a random available direction from room directions dictionary
    visited[current_room_id][d] = player.current_room.get_room_in_direction(d).id
    print('ROOM', visited[current_room_id][d])

    old_room_id = current_room_id
    player.travel(d) # Move player in that direction
    traversal_path.append(d) # Add move to traversal path
    visited[current_room_id][return_opposites(d)] = old_room_id

def dft_to_dead_ends(starting_room_id):
    """
    1. Translate the problem into graph terminology:
    Travel to random unvisited rooms until I reach a dead end, 
    then, find the shortest path to the next unvisited room,
    each step as I go.
    """
    # 2. Build your graph

    # Create an empty stack
    s = Stack()
    # Create an empty dictionary to store visited nodes and their directions: SEE VISITED ABOVE^^^
    # Push starting node onto the stack
    s.push( [player.current_room.id] )
    # 3. Traverse your graph
    # While there is more than one room to visit (not a dead end)
    while len(player.current_room.get_exits()) != 1:
        # Pop room from top of stack
        r = s.pop()
        r1 = r[-1]
        # Check if it's visited. If not...
        mark_as_visited(r1)
        # HELPER FUNCTION TO UPDATE VISITED ROOMS IN ADJACENCY DICTIONARIES FROM '?' TO DIRECTION
        update_visited_rooms(player.current_room.id)
        # Push current room onto stack
        s.push([player.current_room.id])            
    
        road_not_taken = []
        for i in list(visited[player.current_room.id].keys()):
            if visited[player.current_room.id][i] == '?':
                road_not_taken.append(i)
        # print('ROAD NOT TAKEN', road_not_taken)
        # TODO: ONLY ALLOW PLAYER TO WALK IN DIRECTIONS NOT TAKEN            
        
        # HELPER FUNCTION TO UPDATE VISITED ROOMS IN ADJACENCY DICTIONARIES FROM '?' TO DIRECTION
        update_visited_rooms(player.current_room.id)
        # Push current room onto stack
        s.push([player.current_room.id])
        print('DFT STACK', s.stack)
        print('VISITED ROOMS', visited)

            
    # find_nearest_unvisited_rm(player.current_room.id, last_room=0)
    
# def find_nearest_unvisited_rm(starting_room_id, last_room=0, target_value='?'):
#     '''
#     1b.Find the shortest path to the next unvisited room or the nearest '?'
#     '''
#     # Create an empty queue to hold paths
#     q = Queue()
#     # Enqueue an empty list
#     starter_queue = list()
#     q.enqueue(starter_queue) # len(q) = 1
#     # Create an empty set to store visited rooms
#     bfs_visited = set()
#     # While queue is not empty...
#     while q.size() > 0:
#     # while player.current_room.id in visited:
#         # Dequeue first set of possible directions ex: ['n', 's', 'e', 'w'] or []
#         path = q.dequeue()
#         print('P FROM THE TOP: ', path)
#         # Grab last direction ex: 'w'
#         if len(path) == 0:
#             direction = 'z'
#         else:
#             direction = path[-1]
#             print('VISITED ROOMS SO FAR: ', bfs_visited)
#             print('direction FROM THE TOP: ', direction)
#         # Check it's the target: '?'
#         if direction == target_value:
#             print('FOUND TARGET, FOLLOW THIS PATH: ', traversal_path)
#             traversal_path.append(path[:-1])
#             # Move player along this path
#             for d in path:
#                 player.travel(d)
#             dft_to_dead_ends(player.current_room.id)
#             return path
#         else:
#             # if player.current_room.id not in bfs_visited:
#             # # Mark it as visited
#             # bfs_visited.add(player.current_room.id)
#             if player.current_room.id not in visited:
#                 visited[player.current_room.id] = {}
#                 for direction in player.current_room.get_exits():
#                     visited[player.current_room.id][direction] = '?' # 'n' : '?'
#             road_not_taken = []
#             for i in list(visited[player.current_room.id].keys()):
#                 if visited[player.current_room.id][i] == '?':
#                     road_not_taken.append(i)
#             # print('ROAD NOT TAKEN', road_not_taken)
#             for d in road_not_taken:
#                 # Make a copy of the path before adding next step
#                 p_copy = path.copy()
#                 p_copy.append(d)
#                 q.enqueue(p_copy)
#                 # Move player into next room
#                 for i in p_copy:
#                     player.travel(i)
#                 # Reverse directions
#                 reverse_d = []
#                 for i in p_copy:
#                     if i == "n":
#                         reverse_d.append("s")
#                     if i == "s":
#                         reverse_d.append("n")
#                     if i == "e":
#                         reverse_d.append("w")
#                     if i == "w":
#                         reverse_d.append("e")
#                 print('REVERSED DIRECTIONS', reverse_d.reverse())
                
#                 for i in reverse_d:
#                     player.travel(i)
#                 print('D1: ', direction)
#                 print('Q: ', q.queue)
#                 print('P COPY: ', p_copy)
#                 print('STARTED FROM THE TOP NOW WE ARE HERE: ', player.current_room.id)
                
#         # Get directions from room in each direction ex: n: ['s', 'w' ] until we find '?'
#         # Add to master visited adjacency dictionary list

#     # dft_to_dead_ends(player.current_room.id)




# dft_to_dead_ends(player.current_room.id)


# print('TRAVERSAL PATH: ',traversal_path)
# # TRAVERSAL TEST
# visited_rooms = set()
# player.current_room = world.starting_room
# visited_rooms.add(player.current_room)

# for move in traversal_path:
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
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")