# strategy_zone_harvest.py - 智能分區採收策略
# 針對22x22農場的分區採收：南瓜區、仙人掌區、混合區
# 基於作物習性的土地狀態判斷

# 農場布局參數
farm_size = 22
harvest_count = 0
round_count = 0

# 仙人掌排序參數
cactus_sorting_cycles = 7  # 每輪進行的排序循環次數（可調整：1-10）

# 恐龍模式參數（可選功能）
enable_dinosaur_mode = True  # 設為 True 啟用恐龍模式
dinosaur_mode_trigger_cactus = 10000  # 仙人掌數量達到此值時觸發恐龍模式
dinosaur_target_tail_length = 200  # 目標尾巴長度（50-200推薦）

# 南瓜ID追蹤系統
pumpkin_ids_vertical = {}  # 縱向移動的南瓜ID追蹤
pumpkin_ids_horizontal = {}  # 橫向移動的南瓜ID追蹤
pumpkin_threshold = 9 # 連續出現9就收成 (S型移動需要更多次數)

# 連續出現追蹤
last_pumpkin_id_vertical = None  # 上一個縱向移動的南瓜ID
last_pumpkin_id_horizontal = None  # 上一個橫向移動的南瓜ID
consecutive_count_vertical = 0  # 縱向連續出現次數
consecutive_count_horizontal = 0  # 橫向連續出現次數

# 區域定義 - 左下角改為向日葵區
def is_pumpkin_zone(x, y):
	# 右上、右下、左上角落的6x6區域 - 南瓜專用（不包含左下角）
	return (x >= 16 and (y < 6 or y >= 16)) or (x < 6 and y >= 16)

def is_sunflower_zone(x, y):
	# 左下角6x6區域 - 向日葵專用
	return x < 6 and y < 6

def is_cactus_zone(x, y):
	# 中間10x10區域 - 仙人掌專用
	return x >= 6 and x < 16 and y >= 6 and y < 16

def is_mixed_zone(x, y):
	# 上下混合區 - 6x10範圍，伴生種植
	return x >= 6 and x < 16 and (y < 6 or y >= 16)

def is_carrot_zone(x, y):
	# 左右混合區 - 6x10範圍，伴生種植
	return (x < 6 or x >= 16) and y >= 6 and y < 16

# 四區塊伴生混合種植函數
def get_companion_plant_type(x, y):
	# 根據 x, y 的奇偶性決定植物類型
	x_odd = x % 2 == 1
	y_odd = y % 2 == 1
	
	if x_odd and y_odd:
		# 奇奇：雜草
		return Entities.Grass
	elif x_odd and not y_odd:
		# 奇偶：灌木
		return Entities.Bush
	elif not x_odd and y_odd:
		# 偶奇：樹木
		return Entities.Tree
	else:  # not x_odd and not y_odd
		# 偶偶：胡蘿蔔
		return Entities.Carrot

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
		'is_pumpkin_zone': is_pumpkin_zone(x, y),
		'is_sunflower_zone': is_sunflower_zone(x, y),
		'is_cactus_zone': is_cactus_zone(x, y),
		'is_mixed_zone': is_mixed_zone(x, y),
		'is_carrot_zone': is_carrot_zone(x, y)
	}

# 回到起始位置
def reset_position():
	while get_pos_x() > 0:
		move(West)
	while get_pos_y() > 0:
		move(South)

# 智能種植函數 - 結合伴生種植和網狀交錯
def get_smart_plant_type(x, y, is_sunflower_zone):
	# 優先檢查伴生種植需求
	companion_info = get_companion()
	if companion_info:
		# 如果有伴生需求，優先種植主植物
		# 但這裡我們先種植基礎植物，收穫時再處理伴生
		pass
	
	# 網狀交錯排列：使用棋盤模式確保相鄰植物不同
	pattern = (x + y) % 2
	
	if is_sunflower_zone:
		# 上下混合區：樹木、向日葵網狀交錯
		if pattern == 0:
			return Entities.Tree
		else:
			return Entities.Sunflower
	else:
		# 左右混合區：樹木、胡蘿蔔網狀交錯
		if pattern == 0:
			return Entities.Tree
		else:
			return Entities.Carrot

# 移動到指定位置的輔助函數（已移除，伴生區改為放養模式）

# 基於作物習性的智能處理
def smart_zone_processing(x, y, is_vertical):
	# 宣告全域變數（必須在函數最開始）
	global last_pumpkin_id_vertical
	global last_pumpkin_id_horizontal
	global consecutive_count_vertical
	global consecutive_count_horizontal
	# 使用實際座標位置，而不是循環變量
	actual_x = get_pos_x()
	actual_y = get_pos_y()
	status = get_land_status(actual_x, actual_y)
	local_harvests = 0
	
	# 南瓜區處理 - 保持原有邏輯
	if status['is_pumpkin_zone']:
		# 1. 優先處理壞瓜 (死南瓜) - 最高優先級
		if status['entity'] == Entities.Dead_Pumpkin:
			plant(Entities.Pumpkin)  # 移除死南瓜並種新瓜
		
		# 2. 處理草地 - 清理並準備種植
		elif status['ground'] == Grounds.Grassland:
			if status['entity'] == Entities.Grass:
				harvest()
				local_harvests += 1
			till()
			plant(Entities.Pumpkin)
		
		# 3. 處理可收成的南瓜 - 使用連續出現追蹤系統
		elif status['can_harvest']:
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
				
				# 檢查是否達到連續出現閾值
				if consecutive_count_vertical >= pumpkin_threshold:
					harvest()
					local_harvests += 1
					plant(Entities.Pumpkin)
					# 收成後重置計數
					consecutive_count_vertical = 0
					last_pumpkin_id_vertical = None
			else:
				# 橫向移動連續追蹤
				if pumpkin_id == last_pumpkin_id_horizontal:
					consecutive_count_horizontal += 1
				else:
					# ID不同，重置計數
					consecutive_count_horizontal = 1
					last_pumpkin_id_horizontal = pumpkin_id
				
				# 檢查是否達到連續出現閾值
				if consecutive_count_horizontal >= pumpkin_threshold:
					harvest()
					local_harvests += 1
					plant(Entities.Pumpkin)
					# 收成後重置計數
					consecutive_count_horizontal = 0
					last_pumpkin_id_horizontal = None
		
		# 4. 處理空地 - 補種南瓜
		elif status['entity'] == None and status['ground'] == Grounds.Soil:
			plant(Entities.Pumpkin)
		
		# 5. 南瓜區高水分需求 - 保持最佳生長條件
		if status['water'] < 0.75:
			use_item(Items.Water)
	
	# 向日葵區處理 - 左下角6x6專用
	elif status['is_sunflower_zone']:
		# 1. 優先處理壞瓜 (死南瓜) - 最高優先級
		if status['entity'] == Entities.Dead_Pumpkin:
			plant(Entities.Sunflower)  # 移除死南瓜並種向日葵
		
		# 2. 處理草地 - 清理並準備種植
		elif status['ground'] == Grounds.Grassland:
			if status['entity'] == Entities.Grass:
				harvest()
				local_harvests += 1
			till()
			plant(Entities.Sunflower)
		
		# 3. 處理可收成的向日葵 - 直接收穫
		elif status['can_harvest']:
			harvest()
			local_harvests += 1
			plant(Entities.Sunflower)
		
		# 4. 處理空地 - 補種向日葵
		elif status['entity'] == None and status['ground'] == Grounds.Soil:
			plant(Entities.Sunflower)
		
		# 5. 向日葵區中等水分需求
		if status['water'] < 0.5:
			use_item(Items.Water)
	
	# 仙人掌區處理 - 只種植和維護，不採收
	elif status['is_cactus_zone']:
		# 1. 處理草地 - 清理並準備種植
		if status['ground'] == Grounds.Grassland:
			if status['entity'] == Entities.Grass:
				harvest()
				local_harvests += 1
			till()
			plant(Entities.Cactus)
		
		# 2. 仙人掌不在經過時採收
		# 仙人掌需要完全排序後才手動採收，以獲得 n^2 收益
		# 如果在經過時採收，會破壞排序且只得到單個仙人掌
		elif status['entity'] == Entities.Cactus:
			# 不處理仙人掌（無論成熟與否）
			# 排序邏輯在專門的排序階段執行
			# 採收需要手動或等待完全排序後再進行
			pass
		
		# 3. 處理空地 - 補種仙人掌
		elif status['entity'] == None and status['ground'] == Grounds.Soil:
			plant(Entities.Cactus)
		
		# 4. 仙人掌區高水分需求
		if status['water'] < 0.75:
			use_item(Items.Water)
	
	# 混合區處理 - 放養模式，保留除草功能
	elif status['is_mixed_zone'] or status['is_carrot_zone']:
		# 1. 處理草地 - 除草才能種蘿蔔
		if status['ground'] == Grounds.Grassland:
			if status['entity'] == Entities.Grass:
				harvest()
				local_harvests += 1
			till()
			# 種植對應植物
			plant_type = get_companion_plant_type(actual_x, actual_y)
			plant(plant_type)
		
		# 2. 放養模式：只做最基本的收穫和種植，不進行任何移動或複雜檢查
		elif status['can_harvest']:
			harvest()
			local_harvests += 1
			# 簡單補種
			plant_type = get_companion_plant_type(actual_x, actual_y)
			plant(plant_type)
		
		# 3. 處理空地 - 補種
		elif status['entity'] == None and status['ground'] == Grounds.Soil:
			plant_type = get_companion_plant_type(actual_x, actual_y)
			plant(plant_type)
	
	return local_harvests

# 安全的仙人掌排序函數 - 橫向移動檢查北方
def safe_cactus_sorting_horizontal():
	reset_position()
	swap_count = 0
	
	# 橫向遍歷仙人掌區 (先x後y)
	for x in range(6, 16):  # 仙人掌區 x 範圍
		for y in range(6, 16):  # 仙人掌區 y 範圍
			# 移動到指定位置
			while get_pos_x() < x:
				move(East)
			while get_pos_x() > x:
				move(West)
			while get_pos_y() < y:
				move(North)
			while get_pos_y() > y:
				move(South)
			
			# 檢查當前位置是否有仙人掌
			if get_entity_type() == Entities.Cactus:
				current_size = measure()
				
				# 橫向移動：檢查北方仙人掌
				if y < 15:  # 不在最上邊
					north_size = measure(North)
					# 若本體比較大，則交換位置
					if north_size != None and current_size > north_size:
						swap(North)
						swap_count += 1
	
	return swap_count

# 安全的仙人掌排序函數 - 縱向移動檢查東方
def safe_cactus_sorting_vertical():
	reset_position()
	swap_count = 0
	
	# 縱向遍歷仙人掌區 (先y後x)
	for y in range(6, 16):  # 仙人掌區 y 範圍
		for x in range(6, 16):  # 仙人掌區 x 範圍
			# 移動到指定位置
			while get_pos_x() < x:
				move(East)
			while get_pos_x() > x:
				move(West)
			while get_pos_y() < y:
				move(North)
			while get_pos_y() > y:
				move(South)
			
			# 檢查當前位置是否有仙人掌
			if get_entity_type() == Entities.Cactus:
				current_size = measure()
				
				# 縱向移動：檢查東方仙人掌
				if x < 15:  # 不在最右邊
					east_size = measure(East)
					# 若本體比較大，則交換位置（把大的往東推）
					if east_size != None and current_size > east_size:
						swap(East)
						swap_count += 1
	
	return swap_count

# 檢查特定區域是否有可收穫的植物
def check_zone_harvestable(zone_func):
	reset_position()
	for x in range(farm_size):
		for y in range(farm_size):
			if zone_func(x, y) and can_harvest():
				return True
			if y < farm_size - 1:
				move(North)
		if x < farm_size - 1:
			move(East)
			while get_pos_y() > 0:
				move(South)
	return False

# 縱向S型移動 (垂直S型)
def harvest_vertical_s():
	local_harvests = 0
	reset_position()
	
	for x in range(farm_size):
		for y in range(farm_size):
			# 使用智能處理函數 (縱向移動)
			harvests = smart_zone_processing(x, y, True)
			local_harvests += harvests
			
			if y < farm_size - 1:
				if x % 2 == 0:
					move(North)  # 偶數列：從下到上
				else:
					move(South)  # 奇數列：從上到下
		if x < farm_size - 1:
			move(East)
			if (x + 1) % 2 == 0:
				while get_pos_y() > 0:
					move(South)
			else:
				while get_pos_y() < farm_size - 1:
					move(North)
	
	return local_harvests

# 橫向S型移動 (水平S型)
def harvest_horizontal_s():
	local_harvests = 0
	reset_position()
	
	for y in range(farm_size):
		for x in range(farm_size):
			# 使用智能處理函數 (橫向移動)
			harvests = smart_zone_processing(x, y, False)
			local_harvests += harvests
			
			if x < farm_size - 1:
				if y % 2 == 0:
					move(East)  # 偶數行：從左到右
				else:
					move(West)  # 奇數行：從右到左
		if y < farm_size - 1:
			move(North)
			if (y + 1) % 2 == 0:
				while get_pos_x() > 0:
					move(West)
			else:
				while get_pos_x() < farm_size - 1:
					move(East)
	
	return local_harvests

# 智能分區處理 (基於土地狀態判斷) - 交替使用縱向和橫向S型
def smart_zone_harvest():
	# 交替使用縱向和橫向S型移動
	if round_count % 2 == 0:
		return harvest_vertical_s()
	else:
		return harvest_horizontal_s()

# 智能澆水 (根據區域需求)
def smart_watering():
	reset_position()
	water_used = 0
	
	for x in range(farm_size):
		for y in range(farm_size):
			current_water = get_water()
			
			# 根據區域設定不同的水分需求
			if is_pumpkin_zone(x, y) and current_water < 0.75:
				if use_item(Items.Water):
					water_used += 1
			elif is_cactus_zone(x, y) and current_water < 0.75:
				if use_item(Items.Water):
					water_used += 1
			elif (is_mixed_zone(x, y) or is_carrot_zone(x, y)) and current_water < 0.5:
				if use_item(Items.Water):
					water_used += 1
			
			if y < farm_size - 1:
				if x % 2 == 0:
					move(North)
				else:
					move(South)
		if x < farm_size - 1:
			move(East)
			if (x + 1) % 2 == 0:
				while get_pos_y() > 0:
					move(South)
			else:
				while get_pos_y() < farm_size - 1:
					move(North)
	
	return water_used

# 主策略執行
reset_position()

# 主採收循環
while True:
	round_count += 1
	
	# 智能分區處理 (基於土地狀態判斷)
	total_harvests = smart_zone_harvest()
	harvest_count += total_harvests
	reset_position()
	
	# 仙人掌排序階段 - 每輪進行多次排序循環
	# 整理模式：連續執行多次排序，讓仙人掌快速排序到位
	total_swap_count = 0
	
	for cycle in range(cactus_sorting_cycles):
		# 交替使用橫向和縱向排序
		if (round_count + cycle) % 2 == 0:
			swap_count = safe_cactus_sorting_horizontal()
		else:
			swap_count = safe_cactus_sorting_vertical()
		total_swap_count += swap_count
		reset_position()
		
		# 如果這次循環沒有交換，表示已經排序完成，提前結束
		if swap_count == 0:
			break
	
	# total_swap_count 是交換次數，不是收穫次數
	
	# 仙人掌採收階段 - 當排序完成（沒有交換）時採收
	if total_swap_count == 0:
		# 排序完成，所有仙人掌已變綠色，可以採收
		# 移動到右上角 (15, 15) 觸發連鎖採收
		while get_pos_x() < 15:
			move(East)
		while get_pos_y() < 15:
			move(North)
		
		# 檢查是否有成熟的仙人掌
		if get_entity_type() == Entities.Cactus and can_harvest():
			# 記錄採收前數量
			cactus_before = num_items(Items.Cactus)
			
			# 執行連鎖採收
			harvest()
			
			# 計算獲得數量
			cactus_after = num_items(Items.Cactus)
			cactus_gained = cactus_after - cactus_before
			
			# 採收成功，記錄到收穫計數（雖然這是特殊採收）
			harvest_count += 1
		
		reset_position()
	
	# 恐龍模式觸發檢查（可隨時執行，不限於採收後）
	if enable_dinosaur_mode:
		cactus_count = num_items(Items.Cactus)
		if cactus_count >= dinosaur_mode_trigger_cactus:
			# 執行恐龍模式：將仙人掌轉換為骨頭
			reset_position()
			
			# 前置作業：清除草地，確保蘋果能生成
			# 遍歷農場，除草並翻地
			for pre_x in range(farm_size):
				for pre_y in range(farm_size):
					# 移動到位置
					while get_pos_x() < pre_x:
						move(East)
					while get_pos_x() > pre_x:
						move(West)
					while get_pos_y() < pre_y:
						move(North)
					while get_pos_y() > pre_y:
						move(South)
					
					# 檢查並處理草地
					if get_ground_type() == Grounds.Grassland:
						# 如果有草，收割
						if get_entity_type() == Entities.Grass:
							harvest()
						# 翻土，防止草再長
						till()
				
				# 移動到下一行
				if pre_x < farm_size - 1:
					move(East)
					while get_pos_y() > 0:
						move(South)
			
			reset_position()
			
			# 裝備恐龍帽
			change_hat(Hats.Dinosaur_Hat)
			
			# S型移動收集蘋果
			apple_eaten = 0
			for dino_x in range(farm_size):
				for dino_y in range(farm_size):
					if dino_y < farm_size - 1:
						if dino_x % 2 == 0:
							result = move(North)
						else:
							result = move(South)
						
						# 如果移動失敗（被尾巴擋住），停止
						if not result:
							break
					
					apple_eaten += 1
					
					# 達到目標長度，停止
					if apple_eaten >= dinosaur_target_tail_length:
						break
				
				if apple_eaten >= dinosaur_target_tail_length:
					break
				
				# 移動到下一列
				if dino_x < farm_size - 1:
					move(East)
					if (dino_x + 1) % 2 == 0:
						while get_pos_y() > 0:
							result = move(South)
							if not result:
								break
					else:
						while get_pos_y() < farm_size - 1:
							result = move(North)
							if not result:
								break
			
			# 卸下恐龍帽，收穫骨頭（n^2 收益）
			change_hat(Hats.Brown_Hat)
			
			reset_position()
	
	# 如果沒有收穫，等待生長
	if total_harvests == 0:
		for i in range(5):
			do_a_flip()
	
	# 每10輪重置計數器
	if round_count % 10 == 0:
		harvest_count = 0