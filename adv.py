from room import Room
from player import Player
from world import World

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

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []
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

def update_graph(graph, player, new_direction, prev_direction):
    default = '?'
    possible_exits = {}
    exits = player.current_room.get_exits()
    nsew = ['n','s','e','w']
    room = player.current_room.id
    
    for ex in exits:
        if prev_direction is None:
            if new_direction == ex:
                possible_exits[ex] = player.current_room.get_room_in_direction(new_direction).id
            else:
                possible_exits[ex] = default
        else:
            reverse = reverse_direction(prev_direction)
            if new_direction == ex:
                possible_exits[ex] = player.current_room.get_room_in_direction(new_direction).id
            elif reverse == ex:
                #reverse = reverse_direction(prev_direction)
                possible_exits[ex] = player.current_room.get_room_in_direction(reverse).id
            else:
                possible_exits[ex] = default
        



    # for e in exits:
    #     # the starting room
    #     if room == 0:
    #         # add the room in the new direction
    #         if new_direction == e:

    #             possible_exits[e] = player.current_room.get_room_in_direction(new_direction).id
    #         else:
    #             possible_exits[e] = default
    #     elif room > 0:
    #         # get the reverse direction of the previous direction
    #         reverse = reverse_direction(prev_direction)
    #         if new_direction == e:
    #             possible_exits[e] = player.current_room.get_room_in_direction(new_direction).id
    #         elif prev_direction == e:
    #             possible_exits[e] = player.current_room.get_room_in_direction(reverse).id
    #         else:
    #             possible_exits = default

    graph[room] = possible_exits
    return graph


    
         

# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)
graph = {}
rooms_left = len(room_graph) - len(visited_rooms)
prev_direction = None
prev_room = None
rooms_path = []

while rooms_left > 0:

    
    # say where the player is
    print(f"the player is in room {player.current_room.id}")
    if player.current_room.id not in rooms_path:
        rooms_path.append(player.current_room.id)
    # get the next available exits
    exits = player.current_room.get_exits()
    print(f"Available exits {exits}")
    # choose a new direction for the player to move in 
    new_direction = choice(exits)
    updated = False
    
    # make sure the player is not moving backwards
    if prev_direction is not None:
        # returns a list of the directions the player can move in
        valid = valid_direction(prev_direction,player)
        # if the new direction is not a valid direction, choose a new direction from the valid options
        if new_direction not in valid and len(valid) > 0:
            new_direction = choice(valid)
            traversal_path.append(new_direction)
            updated = True
            print(f"The previous move was {prev_direction} which is invalid to the new direction \nchanging the new direction to {new_direction}")
        
    
    # generate graph    
    print(update_graph(graph, player, new_direction, prev_direction))
    
    # if the player has been to a room do a search to find the next room to travel to
    if player.current_room.get_room_in_direction(new_direction) in visited_rooms:
        print(f"been to this room")
        found = False
        copy_path = rooms_path.copy()
        while not found:
            print(f"rooms path {copy_path}")
            last = copy_path.pop()
            search = graph[last]
            room_number = last
            if "?" in search.values():
                print(search)
                found = True
        
        for key, value in reversed(list(search.items())):
            if value == "?":
                new_direction = key
                print(new_direction)
                print(room_number)
                break
            
        for room in visited_rooms:
            if room.id == room_number:
                player.current_room = room
         
        print(f"new room {player.current_room.id}")
        update_graph(graph, player, new_direction, prev_direction)
            
        



    # move the player
    print(f"moving the player {new_direction}")
    player.travel(new_direction)

    # connect the rooms
    #player.current_room.connect_rooms(new_direction, player.current_room)
    

    #update the traversal path
    if updated is False:
        traversal_path.append(new_direction)

    print(f"Updated the traversal path to {traversal_path}")

    # update the rooms visited set, how many rooms are left, and the previous direction before the loop
    visited_rooms.add(player.current_room)
    #rooms_left = len(room_graph) - len(visited_rooms)
    rooms_left -= 1
    prev_direction = new_direction
    
    print()
    


    


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



