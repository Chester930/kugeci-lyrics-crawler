# strategy_weird_substance_max.py - 怪異物質極限產量策略
# 針對32x32農場的怪異物質極限生產布局：
# - 左下角 20x20：仙人掌區 (400格，100%感染 + 排序 + 連鎖採收)
# - 三個角落 12x12：南瓜區 (432格，100%感染 + 巨型南瓜)
# - 其餘區域：向日葵區 (192格，持續產出能量)
# 
# 極限產量策略：
# 1. 仙人掌：100%感染 → 排序 → 連鎖收穫 → 80,000 Weird_Substance/次
# 2. 南瓜：100%感染 → 等待12×12巨型合併 → 432 Weird_Substance/次（6x提升）
# 3. 極限浇水（0.95）+ 肥料加速
# 
# 預期產量：
# - 仙人掌：~80,000 Weird_Substance/次（1-2次/小時）
# - 南瓜：~1,296 Weird_Substance/次（3個12×12區域，432×3）
# - 總計：~150,000+ Weird_Substance/小時（提升50%！）

# 農場布局參數
farm_size = 32
harvest_count = 0
round_count = 0

# 怪異物質極限生產參數
fertilizer_min_stock = 20  # 提高最低肥料庫存（需要大量肥料）
use_fertilizer_on_cactus = True
use_fertilizer_on_pumpkin = True

# 仙人掌排序參數（恢復排序功能）
cactus_sorting_cycles = 4
cactus_ready_for_harvest = False  # 仙人掌是否準備好採收

# 仙人掌感染追蹤
cactus_infection_complete = False  # 仙人掌區是否完成感染

# 南瓜策略參數
pumpkin_wait_for_merge = True  # 等待巨型南瓜合併（6x Weird_Substance）
pumpkin_threshold = 17  # ID連續出現閾值（12×12需要~17次）

# 南瓜ID追蹤（用於判斷巨型南瓜）
pumpkin_ids_vertical = {}
pumpkin_ids_horizontal = {}
last_pumpkin_id_vertical = None
last_pumpkin_id_horizontal = None
consecutive_count_vertical = 0
consecutive_count_horizontal = 0

# 區域定義
def is_cactus_zone(x, y):
	return x < 20 and y < 20

def is_pumpkin_zone(x, y):
	if x >= 20 and y < 12:
		return True
	if x < 12 and y >= 20:
		return True
	if x >= 20 and y >= 20:
		return True
	return False

def is_sunflower_zone(x, y):
	return not is_cactus_zone(x, y) and not is_pumpkin_zone(x, y)

# 土地狀態判斷函數
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
		'is_sunflower_zone': is_sunflower_zone(x, y)
	}

def reset_position():
	while get_pos_x() > 0:
		move(West)
	while get_pos_y() > 0:
		move(South)

# 智能處理 - 極限產量模式
def smart_zone_processing(x, y, is_vertical):
	global cactus_infection_complete
	global last_pumpkin_id_vertical
	global last_pumpkin_id_horizontal
	global consecutive_count_vertical
	global consecutive_count_horizontal
	
	actual_x = get_pos_x()
	actual_y = get_pos_y()
	status = get_land_status(actual_x, actual_y)
	local_harvests = 0
	
	# 南瓜區 - 巨型南瓜模式（等待合併，6x Weird_Substance）
	if status['is_pumpkin_zone']:
		if status['entity'] == Entities.Dead_Pumpkin:
			plant(Entities.Pumpkin)
			# 種植後立即感染
			if use_fertilizer_on_pumpkin and num_items(Items.Fertilizer) > fertilizer_min_stock:
				use_item(Items.Fertilizer)
		
		elif status['ground'] == Grounds.Grassland:
			if status['entity'] == Entities.Grass:
				harvest()
				local_harvests += 1
			till()
			plant(Entities.Pumpkin)
			# 種植後立即感染
			if use_fertilizer_on_pumpkin and num_items(Items.Fertilizer) > fertilizer_min_stock:
				use_item(Items.Fertilizer)
		
		elif status['can_harvest']:
			# 使用ID追蹤系統判斷巨型南瓜
			if pumpkin_wait_for_merge:
				# 取得南瓜ID (measure() 返回的mysterious number)
				pumpkin_id = measure()
				
				# 根據移動方向選擇追蹤系統
				if is_vertical:
					# 縱向移動連續追蹤
					if pumpkin_id == last_pumpkin_id_vertical:
						consecutive_count_vertical += 1
					else:
						# ID不同，重置計數
						consecutive_count_vertical = 1
						last_pumpkin_id_vertical = pumpkin_id
					
					# 檢查是否達到連續出現閾值（表示巨型南瓜）
					if consecutive_count_vertical >= pumpkin_threshold:
						harvest()
						local_harvests += 1
						plant(Entities.Pumpkin)
						# 種植後立即感染
						if use_fertilizer_on_pumpkin and num_items(Items.Fertilizer) > fertilizer_min_stock:
							use_item(Items.Fertilizer)
						# 收成後重置計數
						consecutive_count_vertical = 0
						last_pumpkin_id_vertical = None
					else:
						# 未達到閾值，繼續使用肥料加速
						if use_fertilizer_on_pumpkin and num_items(Items.Fertilizer) > fertilizer_min_stock:
							use_item(Items.Fertilizer)
				else:
					# 橫向移動連續追蹤
					if pumpkin_id == last_pumpkin_id_horizontal:
						consecutive_count_horizontal += 1
					else:
						# ID不同，重置計數
						consecutive_count_horizontal = 1
						last_pumpkin_id_horizontal = pumpkin_id
					
					# 檢查是否達到連續出現閾值（表示巨型南瓜）
					if consecutive_count_horizontal >= pumpkin_threshold:
						harvest()
						local_harvests += 1
						plant(Entities.Pumpkin)
						# 種植後立即感染
						if use_fertilizer_on_pumpkin and num_items(Items.Fertilizer) > fertilizer_min_stock:
							use_item(Items.Fertilizer)
						# 收成後重置計數
						consecutive_count_horizontal = 0
						last_pumpkin_id_horizontal = None
					else:
						# 未達到閾值，繼續使用肥料加速
						if use_fertilizer_on_pumpkin and num_items(Items.Fertilizer) > fertilizer_min_stock:
							use_item(Items.Fertilizer)
			else:
				# 不等待合併，直接採收（參考f3.py）
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
	
	# 向日葵區 - 能量生產
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
	
	# 仙人掌區 - 感染 + 種植模式（不採收，等待排序）
	elif status['is_cactus_zone']:
		if status['ground'] == Grounds.Grassland:
			if status['entity'] == Entities.Grass:
				harvest()
				local_harvests += 1
			till()
			plant(Entities.Cactus)
			# 立即感染
			if use_fertilizer_on_cactus and num_items(Items.Fertilizer) > fertilizer_min_stock:
				use_item(Items.Fertilizer)
		
		# 仙人掌不在遍歷時採收（等待排序和連鎖採收）
		elif status['entity'] == Entities.Cactus:
			# 如果未成熟，使用肥料加速並感染
			if not status['can_harvest']:
				if use_fertilizer_on_cactus and num_items(Items.Fertilizer) > fertilizer_min_stock:
					use_item(Items.Fertilizer)
			# 如果成熟，不採收（等待排序完成）
		
		elif status['entity'] == None and status['ground'] == Grounds.Soil:
			plant(Entities.Cactus)
			if use_fertilizer_on_cactus and num_items(Items.Fertilizer) > fertilizer_min_stock:
				use_item(Items.Fertilizer)
		
		if status['water'] < 0.95:
			use_item(Items.Water)
	
	return local_harvests

# 仙人掌排序函數 - 橫向
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

# 仙人掌排序函數 - 縱向
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

# 檢查仙人掌區是否全部成熟
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

# 縱向S型移動
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

# 橫向S型移動
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

# 主策略執行
reset_position()

# 主循環 - 極限產量模式
while True:
	round_count += 1
	
	# 階段 1：遍歷農場（南瓜和向日葵持續採收，仙人掌種植+感染）
	total_harvests = smart_zone_harvest()
	harvest_count += total_harvests
	reset_position()
	
	# 階段 2：檢查仙人掌是否全部成熟
	all_mature = check_cactus_all_mature()
	reset_position()
	
	# 階段 3：如果全部成熟，進行排序
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
		
		# 階段 4：排序完成，執行連鎖採收
		if total_swap_count == 0:
			while get_pos_x() < 19:
				move(East)
			while get_pos_y() < 19:
				move(North)
			
			if get_entity_type() == Entities.Cactus and can_harvest():
				cactus_before = num_items(Items.Cactus)
				weird_before = num_items(Items.Weird_Substance)
				
				# 連鎖採收（感染的仙人掌會產生 Weird_Substance）
				harvest()
				
				cactus_after = num_items(Items.Cactus)
				weird_after = num_items(Items.Weird_Substance)
				
				cactus_gained = cactus_after - cactus_before
				weird_gained = weird_after - weird_before
				
				harvest_count += 1
				
				# 可選：顯示收穫結果
				# 仙人掌：cactus_gained
				# 怪異物質：weird_gained
			
			reset_position()
	
	# 如果沒有收穫，等待生長
	if total_harvests == 0 and not all_mature:
		for i in range(2):
			do_a_flip()
	
	# 每10輪重置計數器
	if round_count % 10 == 0:
		harvest_count = 0

