# hybrid_farming.py - 智能混合策略
# 自动在迷宫模式和 Weird_Substance 生产模式之间切换
# 
# 核心策略：
# 1. 当 Weird_Substance >= 50,000 时 → 迷宫模式（消耗 Weird_Substance，获得金币）
# 2. 当 Weird_Substance < 100 时 → 生产模式（f4.py 策略，积累 Weird_Substance）
# 3. 自动切换，持续循环
# 
# 预期效果：
# - 持续获得金币
# - 持续生产 Weird_Substance
# - 完全自动化，无需手动干预

# ==================== 全局参数 ====================

# 地图参数
farm_size = get_world_size()

# 模式切换阈值
weird_substance_maze_threshold = 50000  # 达到此值时切换到迷宫模式
weird_substance_farm_threshold = 100    # 低于此值时切换到生产模式

# 迷宫参数
maze_position_x = 0
maze_position_y = 0

# 生产模式参数（来自 f4.py）
fertilizer_min_stock = 20
use_fertilizer_on_cactus = True
use_fertilizer_on_pumpkin = True
cactus_sorting_cycles = 4
pumpkin_wait_for_merge = True
pumpkin_threshold = 17

# 统计数据
total_mazes_solved = 0
total_gold_earned = 0
total_weird_used = 0
total_harvests = 0
round_count = 0
harvest_count = 0

# 南瓜ID追踪
last_pumpkin_id_vertical = None
last_pumpkin_id_horizontal = None
consecutive_count_vertical = 0
consecutive_count_horizontal = 0

# 当前模式
current_mode = "FARM"  # "FARM" 或 "MAZE"

# ==================== 通用函数 ====================

def reset_position():
	while get_pos_x() > 0:
		move(West)
	while get_pos_y() > 0:
		move(South)

# ==================== 迷宫模式函数 ====================

def move_to_position(target_x, target_y):
	reset_position()
	while get_pos_x() < target_x:
		move(East)
	while get_pos_y() < target_y:
		move(North)

def create_maze():
	move_to_position(maze_position_x, maze_position_y)
	
	current_entity = get_entity_type()
	current_ground = get_ground_type()
	
	if current_entity == Entities.Grass:
		harvest()
	
	if current_ground == Grounds.Grassland:
		till()
	
	plant(Entities.Bush)
	
	maze_level = num_unlocked(Unlocks.Mazes)
	if maze_level == 0:
		substance_needed = farm_size
	else:
		substance_needed = farm_size * 2**(maze_level - 1)
	
	weird_count = num_items(Items.Weird_Substance)
	if weird_count < substance_needed:
		return False, 0
	
	use_item(Items.Weird_Substance, substance_needed)
	return True, substance_needed

def solve_maze_smart():
	directions = [North, East, South, West]
	current_direction = 0
	steps = 0
	max_steps = farm_size * farm_size * 4
	
	while steps < max_steps:
		if get_entity_type() == Entities.Treasure:
			harvest()
			return True
		
		right_direction = (current_direction + 1) % 4
		
		if can_move(directions[right_direction]):
			current_direction = right_direction
			move(directions[current_direction])
		elif can_move(directions[current_direction]):
			move(directions[current_direction])
		else:
			current_direction = (current_direction - 1) % 4
		
		steps += 1
	
	return False

def maze_mode():
	global total_mazes_solved
	global total_gold_earned
	global total_weird_used
	global current_mode
	
	weird_count = num_items(Items.Weird_Substance)
	
	# 检查是否应该切换到生产模式
	if weird_count < weird_substance_farm_threshold:
		current_mode = "FARM"
		return
	
	# 创建迷宫
	success, substance_used = create_maze()
	
	if not success:
		current_mode = "FARM"
		return
	
	# 求解迷宫
	solved = solve_maze_smart()
	
	if solved:
		maze_level = num_unlocked(Unlocks.Mazes)
		if maze_level == 0:
			gold_earned = farm_size * farm_size
		else:
			gold_earned = farm_size * farm_size * 2**maze_level
		
		total_mazes_solved += 1
		total_gold_earned += gold_earned
		total_weird_used += substance_used
	
	reset_position()

# ==================== 生产模式函数（来自 f4.py）====================

def is_cactus_zone(x, y):
	return x < 20 and y < 20

def is_pumpkin_zone(x, y):
	# 右下角 (20-31, 0-11)
	if x >= 20 and y < 12:
		return True
	# 左上角 (0-11, 20-31)
	if x < 12 and y >= 20:
		return True
	# 右上角改为混合区，不再是南瓜区
	return False

def is_mixed_zone(x, y):
	# 右上角混合区 (20-31, 20-31)
	return x >= 20 and y >= 20

def is_sunflower_zone(x, y):
	return not is_cactus_zone(x, y) and not is_pumpkin_zone(x, y) and not is_mixed_zone(x, y)

def get_land_status(x, y):
	current_ground = get_ground_type()
	current_entity = get_entity_type()
	current_water = get_water()
	
	return {
		'ground': current_ground,
		'entity': current_entity,
		'water': current_water,
		'can_harvest': can_harvest(),
		'is_cactus_zone': is_cactus_zone(x, y),
		'is_pumpkin_zone': is_pumpkin_zone(x, y),
		'is_mixed_zone': is_mixed_zone(x, y),
		'is_sunflower_zone': is_sunflower_zone(x, y)
	}

# 混合区植物类型（参考 f2.py）
def get_companion_plant_type(x, y):
	x_odd = x % 2 == 1
	y_odd = y % 2 == 1
	
	if x_odd and y_odd:
		return Entities.Grass
	elif x_odd and not y_odd:
		return Entities.Bush
	elif not x_odd and y_odd:
		return Entities.Tree
	else:
		return Entities.Carrot

def smart_zone_processing(x, y, is_vertical):
	global last_pumpkin_id_vertical
	global last_pumpkin_id_horizontal
	global consecutive_count_vertical
	global consecutive_count_horizontal
	
	actual_x = get_pos_x()
	actual_y = get_pos_y()
	status = get_land_status(actual_x, actual_y)
	local_harvests = 0
	
	# 南瓜区
	if status['is_pumpkin_zone']:
		if status['entity'] == Entities.Dead_Pumpkin:
			plant(Entities.Pumpkin)
			if use_fertilizer_on_pumpkin and num_items(Items.Fertilizer) > fertilizer_min_stock:
				use_item(Items.Fertilizer)
		
		elif status['ground'] == Grounds.Grassland:
			if status['entity'] == Entities.Grass:
				harvest()
				local_harvests += 1
			till()
			plant(Entities.Pumpkin)
			if use_fertilizer_on_pumpkin and num_items(Items.Fertilizer) > fertilizer_min_stock:
				use_item(Items.Fertilizer)
		
		elif status['can_harvest']:
			if pumpkin_wait_for_merge:
				pumpkin_id = measure()
				
				if is_vertical:
					if pumpkin_id == last_pumpkin_id_vertical:
						consecutive_count_vertical += 1
					else:
						consecutive_count_vertical = 1
						last_pumpkin_id_vertical = pumpkin_id
					
					if consecutive_count_vertical >= pumpkin_threshold:
						harvest()
						local_harvests += 1
						plant(Entities.Pumpkin)
						if use_fertilizer_on_pumpkin and num_items(Items.Fertilizer) > fertilizer_min_stock:
							use_item(Items.Fertilizer)
						consecutive_count_vertical = 0
						last_pumpkin_id_vertical = None
					else:
						if use_fertilizer_on_pumpkin and num_items(Items.Fertilizer) > fertilizer_min_stock:
							use_item(Items.Fertilizer)
				else:
					if pumpkin_id == last_pumpkin_id_horizontal:
						consecutive_count_horizontal += 1
					else:
						consecutive_count_horizontal = 1
						last_pumpkin_id_horizontal = pumpkin_id
					
					if consecutive_count_horizontal >= pumpkin_threshold:
						harvest()
						local_harvests += 1
						plant(Entities.Pumpkin)
						if use_fertilizer_on_pumpkin and num_items(Items.Fertilizer) > fertilizer_min_stock:
							use_item(Items.Fertilizer)
						consecutive_count_horizontal = 0
						last_pumpkin_id_horizontal = None
					else:
						if use_fertilizer_on_pumpkin and num_items(Items.Fertilizer) > fertilizer_min_stock:
							use_item(Items.Fertilizer)
			else:
				harvest()
				local_harvests += 1
				plant(Entities.Pumpkin)
				if use_fertilizer_on_pumpkin and num_items(Items.Fertilizer) > fertilizer_min_stock:
					use_item(Items.Fertilizer)
		
		elif status['entity'] == None and status['ground'] == Grounds.Soil:
			plant(Entities.Pumpkin)
			if use_fertilizer_on_pumpkin and num_items(Items.Fertilizer) > fertilizer_min_stock:
				use_item(Items.Fertilizer)
		
		elif status['entity'] == Entities.Pumpkin and not status['can_harvest']:
			if use_fertilizer_on_pumpkin and num_items(Items.Fertilizer) > fertilizer_min_stock:
				use_item(Items.Fertilizer)
		
		if status['water'] < 0.95:
			use_item(Items.Water)
	
	# 向日葵区
	elif status['is_sunflower_zone']:
		if status['entity'] == Entities.Dead_Pumpkin:
			plant(Entities.Sunflower)
		
		elif status['ground'] == Grounds.Grassland:
			if status['entity'] == Entities.Grass:
				harvest()
				local_harvests += 1
			till()
			plant(Entities.Sunflower)
		
		elif status['can_harvest']:
			if status['entity'] == Entities.Sunflower:
				petals = measure()
				if petals >= 13:
					harvest()
					local_harvests += 1
					plant(Entities.Sunflower)
				elif petals >= 7:
					harvest()
					local_harvests += 1
					plant(Entities.Sunflower)
			else:
				harvest()
				local_harvests += 1
				plant(Entities.Sunflower)
		
		elif status['entity'] == None and status['ground'] == Grounds.Soil:
			plant(Entities.Sunflower)
		
		if status['water'] < 0.95:
			use_item(Items.Water)
	
	# 仙人掌区
	elif status['is_cactus_zone']:
		if status['ground'] == Grounds.Grassland:
			if status['entity'] == Entities.Grass:
				harvest()
				local_harvests += 1
			till()
			plant(Entities.Cactus)
			if use_fertilizer_on_cactus and num_items(Items.Fertilizer) > fertilizer_min_stock:
				use_item(Items.Fertilizer)
		
		elif status['entity'] == Entities.Cactus:
			if not status['can_harvest']:
				if use_fertilizer_on_cactus and num_items(Items.Fertilizer) > fertilizer_min_stock:
					use_item(Items.Fertilizer)
		
		elif status['entity'] == None and status['ground'] == Grounds.Soil:
			plant(Entities.Cactus)
			if use_fertilizer_on_cactus and num_items(Items.Fertilizer) > fertilizer_min_stock:
				use_item(Items.Fertilizer)
		
		if status['water'] < 0.95:
			use_item(Items.Water)
	
	# 混合区处理（参考 f2.py 的放养模式）
	elif status['is_mixed_zone']:
		# 1. 处理草地 - 除草才能种萝卜
		if status['ground'] == Grounds.Grassland:
			if status['entity'] == Entities.Grass:
				harvest()
				local_harvests += 1
			till()
			plant_type = get_companion_plant_type(actual_x, actual_y)
			plant(plant_type)
		
		# 2. 放养模式：只做最基本的收获和种植
		elif status['can_harvest']:
			harvest()
			local_harvests += 1
			plant_type = get_companion_plant_type(actual_x, actual_y)
			plant(plant_type)
		
		# 3. 处理空地 - 补种
		elif status['entity'] == None and status['ground'] == Grounds.Soil:
			plant_type = get_companion_plant_type(actual_x, actual_y)
			plant(plant_type)
		
		# 4. 混合区水分需求
		if status['water'] < 0.5:
			use_item(Items.Water)
	
	return local_harvests

def harvest_vertical_s():
	local_harvests = 0
	reset_position()
	
	harvests = smart_zone_processing(0, 0, True)
	local_harvests += harvests
	
	for x in range(farm_size):
		for y in range(farm_size):
			if y < farm_size - 1:
				if x % 2 == 0:
					move(North)
				else:
					move(South)
				
				harvests = smart_zone_processing(x, y, True)
				local_harvests += harvests
		
		if x < farm_size - 1:
			move(East)
			actual_x = get_pos_x()
			actual_y = get_pos_y()
			harvests = smart_zone_processing(actual_x, actual_y, True)
			local_harvests += harvests
			
			if (x + 1) % 2 == 0:
				while get_pos_y() > 0:
					move(South)
					actual_x = get_pos_x()
					actual_y = get_pos_y()
					harvests = smart_zone_processing(actual_x, actual_y, True)
					local_harvests += harvests
			else:
				while get_pos_y() < farm_size - 1:
					move(North)
					actual_x = get_pos_x()
					actual_y = get_pos_y()
					harvests = smart_zone_processing(actual_x, actual_y, True)
					local_harvests += harvests
	
	return local_harvests

def harvest_horizontal_s():
	local_harvests = 0
	reset_position()
	
	harvests = smart_zone_processing(0, 0, False)
	local_harvests += harvests
	
	for y in range(farm_size):
		for x in range(farm_size):
			if x < farm_size - 1:
				if y % 2 == 0:
					move(East)
				else:
					move(West)
				
				harvests = smart_zone_processing(x, y, False)
				local_harvests += harvests
		
		if y < farm_size - 1:
			move(North)
			actual_x = get_pos_x()
			actual_y = get_pos_y()
			harvests = smart_zone_processing(actual_x, actual_y, False)
			local_harvests += harvests
			
			if (y + 1) % 2 == 0:
				while get_pos_x() > 0:
					move(West)
					actual_x = get_pos_x()
					actual_y = get_pos_y()
					harvests = smart_zone_processing(actual_x, actual_y, False)
					local_harvests += harvests
			else:
				while get_pos_x() < farm_size - 1:
					move(East)
					actual_x = get_pos_x()
					actual_y = get_pos_y()
					harvests = smart_zone_processing(actual_x, actual_y, False)
					local_harvests += harvests
	
	return local_harvests

def smart_zone_harvest():
	if round_count % 2 == 0:
		return harvest_vertical_s()
	else:
		return harvest_horizontal_s()

def safe_cactus_sorting_horizontal():
	reset_position()
	swap_count = 0
	
	for x in range(0, 20):
		for y in range(0, 20):
			while get_pos_x() < x:
				move(East)
			while get_pos_x() > x:
				move(West)
			while get_pos_y() < y:
				move(North)
			while get_pos_y() > y:
				move(South)
			
			if get_entity_type() == Entities.Cactus:
				current_size = measure()
				
				if y < 19:
					north_size = measure(North)
					if north_size != None and current_size > north_size:
						swap(North)
						swap_count += 1
	
	return swap_count

def safe_cactus_sorting_vertical():
	reset_position()
	swap_count = 0
	
	for y in range(0, 20):
		for x in range(0, 20):
			while get_pos_x() < x:
				move(East)
			while get_pos_x() > x:
				move(West)
			while get_pos_y() < y:
				move(North)
			while get_pos_y() > y:
				move(South)
			
			if get_entity_type() == Entities.Cactus:
				current_size = measure()
				
				if x < 19:
					east_size = measure(East)
					if east_size != None and current_size > east_size:
						swap(East)
						swap_count += 1
	
	return swap_count

def check_cactus_all_mature():
	reset_position()
	for x in range(0, 20):
		for y in range(0, 20):
			while get_pos_x() < x:
				move(East)
			while get_pos_x() > x:
				move(West)
			while get_pos_y() < y:
				move(North)
			while get_pos_y() > y:
				move(South)
			
			if get_entity_type() == Entities.Cactus:
				if not can_harvest():
					return False
	return True

def farm_mode():
	global round_count
	global harvest_count
	global current_mode
	
	# 检查是否应该切换到迷宫模式
	weird_count = num_items(Items.Weird_Substance)
	if weird_count >= weird_substance_maze_threshold:
		current_mode = "MAZE"
		return
	
	round_count += 1
	
	# 采收
	total_harvests = smart_zone_harvest()
	harvest_count += total_harvests
	reset_position()
	
	# 仙人掌排序
	all_mature = check_cactus_all_mature()
	reset_position()
	
	if all_mature:
		total_swap_count = 0
		
		for cycle in range(cactus_sorting_cycles):
			if (round_count + cycle) % 2 == 0:
				swap_count = safe_cactus_sorting_horizontal()
			else:
				swap_count = safe_cactus_sorting_vertical()
			total_swap_count += swap_count
			reset_position()
			
			if swap_count == 0:
				break
		
		if total_swap_count == 0:
			while get_pos_x() < 19:
				move(East)
			while get_pos_y() < 19:
				move(North)
			
			if get_entity_type() == Entities.Cactus and can_harvest():
				harvest()
				harvest_count += 1
			
			reset_position()
	
	if total_harvests == 0 and not all_mature:
		for i in range(2):
			do_a_flip()
	
	if round_count % 10 == 0:
		harvest_count = 0

# ==================== 主循环 ====================

reset_position()

# 主循环：自动切换模式
while True:
	weird_count = num_items(Items.Weird_Substance)
	
	if current_mode == "MAZE":
		# 迷宫模式：消耗 Weird_Substance，获得金币
		maze_mode()
	else:
		# 生产模式：积累 Weird_Substance
		farm_mode()