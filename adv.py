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

"""
1. Translate the problem into graph terminology:
Travel to random unvisited rooms until I reach a dead end, 
then, find the shortest path to the next unvisited room,
each step as I go.
"""
# 2. Build your graph
 
# Create an empty stack
s = Stack()
# Create an empty dictionary to store visited nodes and their directions
visited = {}
# Push starting node onto the stack
s.push( [player.current_room.id] )

# While there is more than one room to visit (not a dead end)
while len(player.current_room.get_exits()) is not 1:
    # Pop room from top of stack
    r = s.pop()
    print('~~~~~~~~~~', r)
    r1 = r[-1]
    print('*************', r1)
    # Check if it's visited. If not...
    if r1 not in visited:
        # Mark it as visited
        visited[r1] = {} # visited = { 0: {} }
        # Store all possible directions in room key value ex: visited = { 0: { 'n': '?', 's': '?', 'w': '?', 'e': '?'} }
        for direction in player.current_room.get_exits():
            visited[r1][direction] = '?' # 'n' : '?'
        d = random.choice(list(visited[player.current_room.id].keys()))# Generate a random available direction from room directions dictionary
        player.travel(d) # Move player in that direction
        traversal_path.append(d) # Add move to traversal path
        # TODO: HELPER FUNCTION TO UPDATE VISITED ROOMS IN ADJACENCY DICTIONARIES FROM '?' TO DIRECTION
        # Push current room onto stack
        s.push([player.current_room.id])
    else:
        d = random.choice(list(visited[player.current_room.id].keys()))# Generate a random available direction from room directions dictionary
        player.travel(d) # Move player in that direction
        traversal_path.append(d) # Add move to traversal path
        # TODO: HELPER FUNCTION TO UPDATE VISITED ROOMS IN ADJACENCY DICTIONARIES FROM '?' TO DIRECTION
        # Push current room onto stack
        s.push([player.current_room.id])
print(player.current_room.id)
print('TRAVERSAL PATH: ',traversal_path)
# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
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
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
