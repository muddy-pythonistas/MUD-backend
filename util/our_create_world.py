from adventure.models import Player, Room
import random

Room.objects.all().delete()

rooms = {
    1: {"name": "Corridor",
        "description": "In-between rooms"},
    2: {"name": "Empty",
        "description": "Nothing here"},
    3: {"name": "The Windy Tunnels",
        "description": "A chill wind blows against you as you open the door. Beyond it, you see that the floor and ceiling are nothing but iron grates. Above and below the grates the walls extend up and down with no true ceiling or floor within your range of vision."},
    4: {"name": "The Shadowy Chambers",
        "description": "Thick cobwebs fill the corners of the room, and wisps of webbing hang from the ceiling and waver in a wind you can barely feel."},
    5: {"name": "The Tranquil Haunt",
        "description": "Rats inside the room shriek when they hear the door open, then they run in all directions from a putrid corpse lying in the center of the floor."},
    6: {"name": "The Living Vault",
        "description": "You open the door, and the room comes alive with light and music. A sourceless, warm glow suffuses the chamber, and a harp you cannot see plays soothing sounds."},
    7: {"name": "The Desolated Caverns", 
        "description": "A pungent, earthy odor greets you as you pull open the door and peer into this room. Mushrooms grow in clusters of hundreds all over the floor. Looking into the room is like looking down on a forest."},
    8: {"name": "The Melancholy Delves",
        "description": "A flurry of bats suddenly flaps through the doorway, their screeching barely audible as they careen past your heads. They flap past you into the rooms and halls beyond."},
    9: {"name": "The Delusional Vault",
        "description": "You are confronted by a thousand reflections of yourself looking back. Mirrored walls set at different angles fill the room. A path seems to wind through the mirrors, although you cannot tell where it leads."},
    10: {"name": "The Dreadful Quarters",
        "description": "Neither light nor darkvision can penetrate the gloom in this chamber. An unnatural shade fills it, and the room's farthest reaches are barely visible."},
    11: {"name": "The Scorching Maze",
        "description": "You open the door and a gout of flame rushes at your face. An inferno engulfs the place, clinging to bare rock and burning without fuel"},
    12: {"name": "The Roaring Lair",
        "description": "A huge iron cage lies on its side in this room, and its gate rests open on the floor. A broken chain lies under the door. The cage is on a rotting corpse and another headless corpse lies next to the cage."},
    13: {"name": "The Southern Labyrinth",
        "description": "The room is hung with hundreds of dusty tapestries, blocking your view of the rest of the room. All show signs of wear: moth holes, scorch marks, dark stains, and the damage of years of neglect."},
    14: {"name": "Delves of the Whispering Priest",
        "description": "Before you is a room about which alchemists dream. Three tables bend beneath a clutter of bottles of liquid and connected glass piping. Several bookshelves stand nearby overfilled with a jumble of books, jars, bottles, bags, and boxes."},
    15: {"name": "Grotto of the Chaotic Raven",
        "description": "A dozen statues stand or kneel in this room, and each one lacks a head and stands in a posture of action or defense. All are garbed for battle. It's difficult to tell for sure without their heads, but two appear to be dwarves."},
    16: {"name": "The Lion Tooth Burrows",
        "description": "You catch a whiff of the unmistakable metallic tang of blood as you open the door. The floor is covered with it, and splashes of blood spatter the walls. It looks fresh."},
    17: {"name": "Fountain of the Stormed Queen",
        "description": "You inhale a briny smell as you enter, and quickly identify the source of the scent: a dark and still pool of brackish water within a low circular wall. Above it stands a statue of a lobster-headed and clawed woman."},
    18: {"name": "Cells of the Savage Goblin",
        "description": "Rusting spikes line the walls and ceiling of this chamber. You can see the skeleton of some humanoid impaled on some wall spikes nearby"},
    19: {"name": "Maze of the Vanishing Elf",
        "description": "Many doors fill the room ahead. Doors of varied shape, size, and design are set in every wall and even the ceiling and floor. Barely a hand's width lies between one door and the next."},
    20: {"name": "Dungeon of the Uncanny Orc",
        "description": "This hall stinks with the wet, pungent scent of mildew. Black mold grows in tangled veins across the walls and parts of the floor. "},
    21: {"name": "The Rejected Catacombs",
        "description": "You gaze into the room and hundreds of skulls gaze coldly back at you. They're set in niches in the walls in a checkerboard pattern, each skull bearing a half-melted candle on its head."},
    22: {"name": "Tombs of the Cursed Army",
         "description": "You open the door to a scene of carnage. It seems that they might once have been wearing armor. Clearly they lost some battle and victors stripped them of their valuables."},
}

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
            num = random.randrange(101)    
            if x == 0 and y == 0:
                room = rooms[1] 
            elif num % 10 == 0:
                room = rooms[2]
            else:
                room = rooms[1]
            room = Room(id=room_count + 1, title=room['name'], description=room['description'], x_coord=x, y_coord=y)
            room.save()
            self.grid[y][x] = room
            room_count += 1
        room_count = 0
        while room_count < num_rooms:
            x = room_count % size_x
            y = room_count // size_x
            if x < size_x - 1:
                curr_room = self.grid[y][x]
                next_room = self.grid[y][x + 1]
                if next_room is not None:
                    if curr_room.title != 'Empty' and next_room.title != 'Empty':
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
                    if curr_room.title != 'Empty' and next_room.title != 'Empty':
                        curr_room.connect_rooms(next_room, 's')
            room_count += 1
        room_count = 0
        while room_count < num_rooms:
            x = room_count % size_x
            y = room_count // size_y
            curr_room = self.grid[y][x]
            num = random.randrange(625)
            if not (x == 0 and y == 0) and curr_room.title != 'Empty':
                conn = 0
                if curr_room.n_to is not None:
                    conn += 1
                if curr_room.w_to is not None:
                    conn += 1 
                if curr_room.s_to is not None:
                    conn += 1
                if curr_room.e_to is not None:
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
                curr_room.title = room['name']
                curr_room.description = room['description']
                curr_room.save()
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

players=Player.objects.all()
for p in players:
    p.currentRoom=w.grid[0][0].id
    p.save()
