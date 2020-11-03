from room import Room
from player import Player
from world import World
from util import Queue
from random import choice, sample
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
#map_file = "maps/test_line.txt"
#map_file = "maps/test_cross.txt"
#map_file = "maps/test_loop.txt"

map_file = "maps/test_loop_fork.txt"
#map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

def merge(d1, d2):
    return {**d1,**d2}
# Fill this out with directions to walk
def reverse_direction(last_direction):
    reverse_dirs = {"n": "s", "s": "n", "e": "w", "w": "e"}
    return reverse_dirs[last_direction]

def valid_direction(new_direction,player):
    '''
    returns true if the new direction is a valid direction
    otherwise returns false
    '''
    
    directions = player.current_room.get_exits()
    delete = reverse_direction(new_direction)
    directions.remove(delete)
    return directions

def available_exits(roomnumber, graph):
    roomdata = graph[roomnumber]
    exits = []
    old = {}
    for key, value in roomdata.items():
        if value == "?":
            exits.append(key)
        else:
            old[key] = value

    return exits,old

def graph_update(graph, player,prev_direction,visited_rooms):
    default = '?'
    possible_exits = {}
    exits = player.current_room.get_exits()
    nsew = ['n','s','e','w']
    room = player.current_room.id
    copy_graph = graph.copy()
    #print(f"graph before update {graph}")
    mix = False
    # for each direction
    if player.current_room.id in graph.keys():
        #print("This room is in the graph")
        exits, old = available_exits(player.current_room.id, graph)
        #print("old g",old)
        mix = True

    for ex in exits:
        #print(f"Exit {ex}")
        

        if prev_direction is None :
            possible_exits[ex] = default
                
        else:
             
            # in a new room so get the room before it
            reverse = reverse_direction(prev_direction)
            #print(f"reverse of previous move ({prev_direction}) is {reverse}")
            roombefore = player.current_room.get_room_in_direction(reverse)
            #print(f"Room before {room} was {roombefore.id}")
            # make the room before point to the current room
            graph[roombefore.id][prev_direction] = player.current_room.id
                
                
            if ex == reverse:
                possible_exits[ex] = roombefore.id
                #print(f"possible exits are {possible_exits}")
                

            else:
                possible_exits[ex] = default
                #print(f"possible exits are {possible_exits}")


    #print()
    if mix:
        possible_exits = merge(possible_exits, old)
        #print(f"Merged {possible_exits} with {old}")
        copy_graph[room] = possible_exits
    else:
        copy_graph[room] = possible_exits
    

    
    print(possible_exits)
    return copy_graph

def choose(player, graph):
    room = player.current_room.id
    roomdata = graph[room]
    places = []

    for key, value in roomdata.items():
        if value == "?":
            places.append(key)

    return choice(places)
    
def is_deadend(player, prev_direction,graph):
    if prev_direction is not None:
        exits = player.current_room.get_exits()
        backwards = reverse_direction(prev_direction)
        length = len(exits)
        ext = exits[0]
        room = player.current_room.id
        g = graph[room]
        values = g.values()
        if "?" not in values:
            return True

        elif (length == 1) and (ext == backwards):
            return True
        else:
            return False
    else:
        return False

def backtrack(player, graph, traversal_path):
    found = False
    # reverse the traversal path to walk back to the next unexplored room
    travelback = traversal_path.copy()
       
    
    while not found:
        # travel back to the most recent room
        direction = reverse_direction(travelback.pop())
        player.travel(direction)
        
        room = player.current_room.id
        traversal_path.append(direction)
        
        # find that room in the graph
        roomdata = graph[room]
        # search to see if there is an unexplored path in the room
        if "?" in roomdata.values():
            found = True
            #print(roomdata)
        
    return direction

def get_direction(player, graph):
    room = player.current_room.id
    roomdata = graph[room]
    for key, value in roomdata.items():
        if value == "?":
            return key

# traversal_path = ['n', 'n']
traversal_path = []
# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)
graph = {}
roomsleft = len(room_graph) - len(visited_rooms)
moving = None
previous = None


# while roomsleft > 0:
#     print(f"The player is in room {player.current_room.id}")
#     ## update the graph
    
#     graph = graph_update(graph, player,previous,visited_rooms)
#     #update_graph(graph, player, moving, previous)
#     #print(graph)
    
    
#     # is the room a dead end?
#     if is_deadend(player, previous,graph) is False:
#         # if not get the first unexplored path and move in that direction
#         moving = get_direction(player, graph)
#         print(f"Moving the player {moving}")
#         # if moving is None:
#         #     moving = backtrack(player, graph, traversal_path)
            
#         player.travel(moving)
#         traversal_path.append(moving)
#         visited_rooms.add(player.current_room)
#         roomsleft = len(room_graph) - len(visited_rooms)
#         previous = moving
#         #print()
#     elif is_deadend(player, previous,graph) or player.current_room in visited_rooms:
#         # if it is a dead end, go back to the first room with an unexplored path
#         previous = backtrack(player, graph, traversal_path)
        
#         # print(f"Moving the player {moving}")
#         # player.travel(moving)
#         # traversal_path.append(moving)

    




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
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")

