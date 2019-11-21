# Sample Python code that can be used to generate rooms in
# a zig-zag pattern.
#
# You can modify generate_rooms() to create your own
# procedural generation algorithm and use print_rooms()
# to see the world.

from room_descriptions import rooms
import random

class Room:
    def __init__(self, id, name, description, x, y):
        self.id = id
        self.name = name
        self.description = description
        self.n_to = None
        self.s_to = None
        self.e_to = None
        self.w_to = None
        self.x = x
        self.y = y
    def __repr__(self):
        if self.e_to is not None:
            return f"({self.x}, {self.y}) -> ({self.e_to.x}, {self.e_to.y})"
        return f"({self.x}, {self.y})"
    def connect_rooms(self, connecting_room, direction):
        '''
        Connect two rooms in the given n/s/e/w direction
        '''
        reverse_dirs = {"n": "s", "s": "n", "e": "w", "w": "e"}
        reverse_dir = reverse_dirs[direction]
        setattr(self, f"{direction}_to", connecting_room)
        setattr(connecting_room, f"{reverse_dir}_to", self)
    def get_room_in_direction(self, direction):
        '''
        Connect two rooms in the given n/s/e/w direction
        '''
        return getattr(self, f"{direction}_to")


class World:
    def __init__(self):
        self.grid = None
        self.width = 0
        self.height = 0
    def generate_rooms(self, size_x, size_y, num_rooms):
        '''
        Fill up the grid, bottom to top, in a zig-zag pattern
        '''
        if num_rooms > size_x * size_y:
            return 'Grid size is not big enough to accommodate all rooms' 

        # Initialize the grid
        self.grid = [None] * size_y
        self.width = size_x
        self.height = size_y
        for i in range( len(self.grid) ):
            self.grid[i] = [None] * size_x

        # Filling grid with rooms (in zig-zag pattern)
        room_count = 0
        while room_count < num_rooms:
            x = room_count % size_x
            y = room_count // size_x
            num = random.randrange(101)    
            x_coord = size_x - 1 - x if y % 2 == 1 else x
            if x_coord == 0 and y == 0:
                room = rooms[1] 
            elif num % 10 == 0:
                room = rooms[2]
            else:
                room = rooms[1]
            room = Room(room_count, room['name'], room['description'], x_coord, y)
            self.grid[y][x_coord] = room
            room_count += 1

        #Making east + west connection between adjacent rooms
        room_count = 0
        while room_count < num_rooms:
            x = room_count % size_x
            y = room_count // size_x
            if x < size_x - 1:
                if y % 2 == 1:
                    curr_room =  self.grid[y][size_x - 1 - x]
                    next_room = self.grid[y][size_x - 1 - x - 1]
                    if next_room is not None:
                        if curr_room.name != 'Empty' and next_room.name != 'Empty':
                            curr_room.connect_rooms(next_room, 'w') 
                else: 
                    curr_room = self.grid[y][x]
                    next_room = self.grid[y][x + 1]
                    if next_room is not None: 
                        if curr_room.name != 'Empty' and next_room.name != 'Empty':
                            curr_room.connect_rooms(next_room, 'e') 
            room_count += 1

        #Making north + south connection between adjacent rooms
        room_count = 0
        while room_count < num_rooms:
            x = room_count % size_x
            y = room_count // size_x
            if y < size_y - 1:
                curr_room = self.grid[y][x]
                next_room = self.grid[y + 1][x]
                if next_room is not None:
                    if curr_room.name != 'Empty' and next_room.name != 'Empty':
                        curr_room.connect_rooms(next_room, 's') 
            room_count += 1
        
        #Update rooms based on connections
        room_count = 0
        while room_count < num_rooms:
            x = room_count % size_x
            y = room_count // size_x
            curr_room = self.grid[y][x]
            num = random.randrange(625) 
            if not (x == 0 and y == 0) and curr_room.name != 'Empty':
                conn = 0
                if curr_room.n_to is not None:
                    conn += 1
                if curr_room.w_to is not None:
                    conn += 1
                if curr_room.e_to is not None:
                    conn += 1
                if curr_room.s_to is not None:
                    conn += 1
                if conn == 1:
                    room = rooms[num % 5 + 18]
                elif conn == 2:
                    if ((curr_room.n_to is not None and curr_room.s_to is not None) or (curr_room.w_to is not None and curr_room.e_to is not None)): 
                        room = rooms[3]
                    else:
                        room = rooms[num % 9 + 10]
                else:
                    if num % 2 == 0:
                        room = rooms[1]
                    else:
                        room = rooms[num % 18 + 4]
                curr_room.name = room['name']
                curr_room.description = room['description']
            room_count += 1

    def print_rooms(self):
        str = "# " * ((3 + self.width * 5) // 2) + "\n"
        reverse_grid = list(self.grid) 
        for row in reverse_grid:
            str += "#"
            for room in row:
                if room is not None and room.n_to is not None:
                    str += "  |  "
                else:
                    str += "     "
            str += "#\n"
            str += "#"
            for room in row:
                if room is not None and room.w_to is not None:
                    str += "-"
                else:
                    str += " "
                if room is not None:
                    str += f"{room.name}"[-3:]
                else:
                    str += "   "
                if room is not None and room.e_to is not None:
                    str += "-"
                else:
                    str += " "
            str += "#\n"
            str += "#"
            for room in row:
                if room is not None and room.s_to is not None:
                    str += "  |  "
                else:
                    str += "     "
            str += "#\n"
        str += "# " * ((3 + self.width * 5) // 2) + "\n"
        print(str)

w = World()
num_rooms = 625
width = 25
height = 25
w.generate_rooms(width, height, num_rooms)
w.print_rooms()
print(f"\n\nWorld\n  height: {height}\n  width: {width},\n  num_rooms: {num_rooms}\n")
