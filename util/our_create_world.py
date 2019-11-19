from adventure.models import Player, Room

Room.objects.all().delete()

class World:
    def __init__(self):
        self.grid = None
        self.width = 0
        self.height = 0

    def generate_rooms(self, size_x, size_y, num_rooms):
        if num_rooms > size_x * size_y:
            return 'Grid size is not big enough to accommodate all rooms'
        self.grid = [None] * size_y
        self.width = size_x
        self.height = size_y
        for i in range(len(self.grid)):
            self.grid[i] = [None] * size_x
        room_count = 0
        while room_count < num_rooms:
            x = room_count % size_x
            y = room_count // size_x
            if y % 2 == 1:
                room = Room(id=room_count, title='Some room',
                            description = 'Just some room', x_coord =size_x - 1
                                                                  - x,
                            y_coord=y)
                self.grid[y][size_x - 1 - x] = room
            else:
                room = Room(id=room_count, title='Some room',
                            descirption='Just some room', x_coord = x,
                            y_coord =y)
                self.grid[y][x] = room
            room_count += 1
        room_count = 0
        while room_count < num_rooms:
            x = room_count % size_x
            y = room_count // size_x
            if x < size_x - 1:
                if y % 2 == 1:
                    curr_room = self.grid[y][size_x - 1 - x]
                    next_room = self.grid[y][size_x - 1 - x - 1]
                    if next_room is not None:
                        curr_room.connect_rooms(next_room, 'w')
                else:
                    curr_room = self.grid[y][x]
                    next_room = self.grid[y][x + 1]
                    if next_room is not None:
                        curr_room.connect_rooms(next_room, 'e')
            room_count += 1
        room_count = 0
        while room_count < num_rooms:
            x = room_count % size_x
            y = room_count // size_x
            if y < size_y - 1:
                curr_room = self.grid[y][x]
                next_room = self.grid[y + 1][x]
                if next_room is not None:
                    curr_room.connect_rooms(next_room, 's')
            room_count += 1

w = World()
num_rooms = 21
width = 7
height = 3
w.generate_rooms(width, height, num_rooms)

players=Player.objects.all()
for p in players:
    p.currentRoom=w.grid[0][0]
    p.save()
