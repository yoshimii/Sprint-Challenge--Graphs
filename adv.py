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
traversal_path = []
visited = {}

def return_opposites(direction):
    if direction == "n":
        return "s"
    if direction == "s":
        return "n"
    if direction == "e":
        return "w"
    if direction == "w":
        return "e"
def move(direction):
    player.travel(direction)
    traversal_path.append(direction)
    
def add_to_visited(current_room_id, exits):
    visited[current_room_id] = {}
    for e in exits:
        visited[current_room_id][e] = None        
    

def dft_maze_traversal(current_room):
    current_room = player.current_room.id
    current_exits = player.current_room.get_exits()
    prev_room = None
    s = Stack()

    s.push([None, current_room, prev_room, current_exits])
    while len(visited) < 499:
        curr_node = s.pop()
        direction = curr_node[0]
        current_room = curr_node[1]
        prev_room = curr_node[2]
        curr_exits = curr_node[3]
        if current_room not in visited:
            add_to_visited(current_room, curr_exits)
        if direction is not None:
            visited[current_room][return_opposites(direction)] = prev_room
        if prev_room is not None:
            visited[prev_room][direction] = current_room
        for d in visited[current_room].keys():
           
            if visited[current_room][d] is None:
                s.push(curr_node)
                prev = player.current_room.id                
                move(d)
                s.push([d, player.current_room.id, prev, player.current_room.get_exits()])
                break
        if current_room == player.current_room.id:
            move(return_opposites(direction))
                      
dft_maze_traversal(player.current_room.id)
                
                # Get id
                # Get exits, previous room, current room, 
                # Update visited
                # 
                

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