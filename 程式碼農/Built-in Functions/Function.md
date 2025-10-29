abs(number)
Computes the absolute value of a number.

returns number if number is positive, -number otherwise.

takes 1 tick to execute.

example:
abs(-69)



can_harvest()
Used to find out if plants are fully grown.

returns True if there is an entity under the drone that is ready to be harvested, False otherwise.

takes 1 tick to execute.

example:
if can_harvest():
    harvest()

For more related information see: <u><link="docs/unlocks/speed.md">Speed


can_move(direction)
Checks if the drone can move in the specified direction.

returns True if the drone can move, False otherwise.

takes 1 tick to execute.

example:
if can_move(North):
    move(North)

For more related information see: <u><link="docs/unlocks/mazes.md">Mazes



change_hat(hat)
Changes the hat of the drone to hat.

returns None

takes 200 ticks to execute.

example:
change_hat(Hats.Dinosaur_Hat)



clear() 
Removes everything from the farm, moves the drone back to position (0,0) and changes the hat back to the straw hat.

returns None

takes 200 ticks to execute.

example:
clear()

For more related information see: <u><link="docs/unlocks/plant.md">Plant



dict(dictionary = None)
Creates a new dictionary.
If dictionary is None, it creates an empty dictionary.
If dictionary is a dictionary, it creates a copy of it.

returns a dictionary.

takes 1 + len(dictionary) ticks to execute.

example:
new_dict = dict()

For more related information see: <u><link="docs/scripting/dicts.md">Dicts



do_a_flip() 
Makes the drone do a flip! This action is not affected by speed upgrades.

returns None

takes 1s to execute.

example:
while True:
    do_a_flip()



get_companion() 
Get the preferred companion of the plant under the drone.

returns a tuple of the form (companion_type, (companion_x_position, companion_y_position))

takes 1 tick to execute.

example:
companion = get_companion()
if companion != None:
	print(companion)

For more related information see: <u><link="docs/unlocks/polyculture.md">Polyculture



get_cost(thing) 
Gets the cost of a thing

If thing is an entity get the cost of planting it.
If thing is an unlock get the cost of unlocking it.

returns a dictionary with items as keys and numbers as values. Each item is mapped to how much of it is needed.
returns {} when used on an upgradeable unlock that is already at the max level.

takes 1 tick to execute.

example:
cost = get_cost(Unlocks.Carrots)
for item in cost:
    if num_items(item) < cost[item]:
        print("not enough items to unlock carrots")

For more related information see: <u><link="docs/unlocks/costs.md">Costs



get_entity_type() 
Find out what kind of entity is under the drone.

returns None if the tile is empty, otherwise returns the type of the entity under the drone.

takes 1 tick to execute.

example:
if get_entity_type() == Entities.Grass:
    harvest()

For more related information see: <u><link="docs/unlocks/senses.md">Senses



get_ground_type() 
Find out what kind of ground is under the drone.

returns the type of the ground under the drone.

takes 1 tick to execute.

example:
if get_ground_type() != Grounds.Soil:
    till()

For more related information see: <u><link="docs/unlocks/senses.md">Senses



get_pos_x() 
Gets the current x position of the drone.
The x position starts at 0 in the west and increases in the east direction.

returns a number representing the current x coordinate of the drone.

takes 1 tick to execute.

example:
x, y = get_pos_x(), get_pos_y()

For more related information see: <u><link="docs/unlocks/senses.md">Senses



get_pos_y() 
Gets the current y position of the drone.
The y position starts at 0 in the south and increases in the north direction.

returns a number representing the current y coordinate of the drone.

takes 1 tick to execute.

example:
x, y = get_pos_x(), get_pos_y()

For more related information see: <u><link="docs/unlocks/senses.md">Senses




get_tick_count()
Used to measure the number of ticks performed.

returns the number of ticks performed since the start of execution.

takes 0 tick to execute.

example:
do_something()

print(get_tick_count())

For more related information see: <u><link="docs/unlocks/timing.md">Timing



get_time() 
Get the current game time.

returns the time in seconds since the start of the game.

takes 1 tick to execute.

example:
start = get_time()

do_something()

time_passed = get_time() - start

For more related information see: <u><link="docs/unlocks/timing.md">Timing




get_water() 
Get the current water level under the drone.

returns the water level under the drone as a number between 0 and 1.

takes 1 tick to execute.

example:
if get_water() < 0.5:
    use_item(Items.Water)

For more related information see: <u><link="docs/unlocks/watering.md">Watering





get_world_size() 
Get the current size of the farm.

returns the side length of the grid in the north to south direction.

takes 1 tick to execute.

example:
for i in range(get_world_size()):
    move(North)




harvest()
Harvests the entity under the drone. 
If you harvest an entity that can't be harvested, it will be destroyed.

returns True if an entity was removed, False otherwise.

takes 200 ticks to execute if an entity was removed, 1 tick otherwise.

example:
harvest()





len(collection) 
Get the number of elements in a list, set, dict or tuple.

returns the length of the collection.

takes 1 tick to execute.

example:
for i in range(len(list)):
    list[i] += 1

For more related information see: <u><link="docs/scripting/lists.md">Lists





list(collection = None)
Creates a new list. 
If collection is None, it creates an empty list.
If collection is any sequence, it creates a new list with the element of the sequence.

returns a list.

takes 1 + len(collection) ticks to execute.

example:
new_list = list((1,2,3))

For more related information see: <u><link="docs/scripting/lists.md">Lists




max(*args)
Gets the maximum of a sequence of elements or several passed arguments.
Can be used on numbers and strings.

max(a,b,c): Returns the maximum of a, b and c.
max(sequence): Returns the maximum of all values in a sequence.

takes #comparisons ticks to execute.

example:
max([3,6,34,16])





measure(direction = None) 
Can measure some values on some entities. The effect of this depends on the entity.

If direction is not None it measures the neighboring entity in the given direction.

returns the number of petals of a sunflower.
returns the next position for a treasure or apple.
returns the size of a cactus.
returns a mysterious number for a pumpkin.
returns None for all other entities.

takes 1 tick to execute.

example:
num_petals = measure()

For more related information see: <u><link="docs/unlocks/sunflowers.md">Sunflowers





min(*args)
Gets the minimum of a sequence of elements or several passed arguments.
Can be used on numbers and strings.

min(a,b,c): Returns the minimum of a, b and c.
min(sequence): Returns the minimum of all values in a sequence.

takes #comparisons ticks to execute.

example:
min([3,6,34,16])




move(direction)
Moves the drone into the specified direction by one tile.
If the drone moves over the edge of the farm it wraps back to the other side of the farm.

East   =  right
West   =  left
North  =  up
South  =  down

returns True if the drone has moved, False otherwise.

takes 200 ticks to execute if the drone has moved, 1 tick otherwise.

example:
move(North)

For more related information see: <u><link="docs/unlocks/expand_1.md">Expand_1





num_items(item) 
Find out how much of item you currently have.

returns the number of item currently in your inventory.

takes 1 tick to execute.

example:
if num_items(Items.Fertilizer) > 0:
    use_item(Items.Fertilizer)

For more related information see: <u><link="docs/unlocks/senses.md">Senses





num_unlocked(thing)
Used to check if an unlock, entity, ground, item or hat is already unlocked.

returns 1 plus the number of times thing has been upgraded if thing is upgradable. Otherwise returns 1 if thing is unlocked, 0 otherwise.

takes 1 tick to execute.

example:
plant(Entities.Bush)
n_substance = get_world_size() * num_unlocked(Unlocks.Mazes)
use_item(Items.Weird_Substance, n_substance)

For more related information see: <u><link="docs/unlocks/senses.md">Senses






pet_the_piggy() 
Pets the piggy! This action is not affected by speed upgrades.

returns None

takes 1s to execute.

example:
while True:
    pet_the_piggy()




    plant(entity) 
Spends the cost of the specified entity and plants it under the drone.
It fails if you can't afford the plant, the ground type is wrong or there's already a plant there.

returns True if it succeeded, False otherwise.

takes 200 ticks to execute if it succeeded, 1 tick otherwise.

example:
plant(Entities.Bush)




print(*args) 
Prints all args into the air above the drone using smoke. This action is not affected by speed upgrades.
Multiple values can be printed at once.

returns None

takes 1s to execute.

example:
print("ground:", get_ground_type())

For more related information see: <u><link="docs/scripting/debug.md">Debug




quick_print(*args)
Prints a value just like print(*args) but it doesn't stop to write it into the air so it can only be found on the output page.

returns None

takes 0 ticks to execute.

example:
quick_print("hi mom")

For more related information see: <u><link="docs/scripting/debug.md">Debug





random()
Samples a random number between 0 (inclusive) and 1 (exclusive).

returns the random number.

takes 1 ticks to execute.

example:
def random_elem(list):
	index = random() * len(list) // 1
	return list[index]





range(start = 0, end, step = 1)
Generates a sequence of numbers starting at start, ending right before reaching end (so end is excluded) using steps of size step.

Note that start is set to 0 by default, and if only one argument is given, it will bind to end. This isn't normally possible.
In Python, range is a class constructor that allows this strange behavior.

takes 1 tick to execute.

example:
for i in range(10):
    print(i)

for i in range(2,6):
    print(i)

for i in range(10, 0, -1):
    print(i)





set(collection = None)
Creates a new set.
If collection is None, it creates an empty set.
If collection is a collection of values, it creates a new set with those values in it.

returns a set.

takes 1 + len(collection) ticks to execute.

example:
new_set = set((1,2,3))

For more related information see: <u><link="docs/scripting/dicts.md">Dicts




str(object)

returns a string representation of object.

takes 1 ticks to execute.

example:
string = str(1000)

For more related information see: <u><link="docs/scripting/debug.md">Debug




swap(direction)
Swaps the entity under the drone with the entity next to the drone in the specified direction.
Doesn't work on all entities.
Also works if one (or both) of the entities are None.

returns True if it succeeded, False otherwise.

takes 200 ticks to execute on success, 1 tick otherwise.

example:
swap(North)

For more related information see: <u><link="docs/unlocks/cactus.md">Cactus





till() 
Tills the ground under the drone into Grounds.Soil. If it's already soil it will change the ground back to Grounds.Grassland.

returns None

takes 200 ticks to execute.

example:
till()

For more related information see: <u><link="docs/unlocks/carrots.md">Carrots





unlock(unlock) 
Has exactly the same effect as clicking the button corresponding to unlock in the research tree.

returns True if the unlock was successful, False otherwise.

takes 200 ticks to execute if it succeeded, 1 tick otherwise.

example:
unlock(Unlocks.Carrots)

For more related information see: <u><link="docs/unlocks/auto_unlock.md">Auto_Unlock




use_item(item, n=1) 
Attempts to use the specified item n times. Can only be used with some items including Items.Water, Items.Fertilizer.

returns True if an item was used, False otherwise.

takes 200 ticks to execute if it succeeded, 1 tick otherwise.

example:
use_item(Items.Fertilizer)

For more related information see: <u><link="docs/unlocks/watering.md">Watering