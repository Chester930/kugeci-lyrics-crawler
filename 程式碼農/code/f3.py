# strategy_weird_substance.py - 怪異物質最大化生產策略
# 針對32x32農場的怪異物質生產布局：
# - 左下角 20x20：仙人掌區 (400格，感染+採收 → Weird_Substance)
# - 三個角落 12x12：南瓜區 (432格，感染+採收 → Weird_Substance)
# - 其餘區域：向日葵區 (192格，持續產出能量)
# 
# 怪異物質生產策略：
# 1. 使用肥料感染植物（use_item(Items.Fertilizer)）
# 2. 收獲感染植物獲得 50% Weird_Substance
# 3. 不使用 Weird_Substance 治療（保持感染狀態）
# 4. 極限浇水加速生長（0.95 水分 = 4.75x 速度）
# 5. 肥料加速生長（-2秒生長時間）
# 
# 預期產量：
# - 南瓜：432 格 × 50% = 216 Weird_Substance/輪
# - 仙人掌：400 格 × 50% = 200 Weird_Substance/輪
# - 總計：~416 Weird_Substance/輪

# 農場布局參數
farm_size = 32  # 升級為 32x32
harvest_count = 0
round_count = 0

# 怪異物質生產參數
fertilizer_min_stock = 10  # 最低肥料庫存（低於此值不使用肥料）
use_fertilizer_on_cactus = True  # 對仙人掌使用肥料
use_fertilizer_on_pumpkin = True  # 對南瓜使用肥料

# 仙人掌不再排序，直接採收（不需要連鎖收穫）
# 南瓜不再追蹤ID，直接採收（不需要巨型南瓜）

# 區域定義 - 32x32 升級布局
def is_cactus_zone(x, y):
	# 左下角 20x20 區域 - 仙人掌專用
	return x < 20 and y < 20

def is_pumpkin_zone(x, y):
	# 三個角落的 12x12 區域 - 南瓜專用
	# 右下角 (20-31, 0-11)
	if x >= 20 and y < 12:
		return True
	# 左上角 (0-11, 20-31)
	if x < 12 and y >= 20:
		return True
	# 右上角 (20-31, 20-31)
	if x >= 20 and y >= 20:
		return True
	return False

def is_sunflower_zone(x, y):
	# 其他所有區域 - 向日葵專用
	return not is_cactus_zone(x, y) and not is_pumpkin_zone(x, y)

# 廢棄的區域定義（保留以防需要）
def is_mixed_zone(x, y):
	return False

def is_carrot_zone(x, y):
	return False

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
		'is_cactus_zone': is_cactus_zone(x, y),
		'is_pumpkin_zone': is_pumpkin_zone(x, y),
		'is_sunflower_zone': is_sunflower_zone(x, y)
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

# 基於作物習性的智能處理 - 怪異物質生產模式
def smart_zone_processing(x, y, is_vertical):
	# 使用實際座標位置
	actual_x = get_pos_x()
	actual_y = get_pos_y()
	status = get_land_status(actual_x, actual_y)
	local_harvests = 0
	
	# 南瓜區處理 - 怪異物質生產模式
	if status['is_pumpkin_zone']:
		# 1. 優先處理壞瓜 (死南瓜)
		if status['entity'] == Entities.Dead_Pumpkin:
			plant(Entities.Pumpkin)
		
		# 2. 處理草地
		elif status['ground'] == Grounds.Grassland:
			if status['entity'] == Entities.Grass:
				harvest()
				local_harvests += 1
			till()
			plant(Entities.Pumpkin)
		
		# 3. 處理可收成的南瓜 - 直接採收（不追蹤ID）
		elif status['can_harvest']:
			# 直接採收，獲得 50% 南瓜 + 50% Weird_Substance（如果感染）
			harvest()
			local_harvests += 1
			plant(Entities.Pumpkin)
			
			# 種植後立即使用肥料感染（如果有足夠肥料）
			if use_fertilizer_on_pumpkin and num_items(Items.Fertilizer) > fertilizer_min_stock:
				use_item(Items.Fertilizer)
		
		# 4. 處理空地
		elif status['entity'] == None and status['ground'] == Grounds.Soil:
			plant(Entities.Pumpkin)
			# 種植後立即使用肥料感染
			if use_fertilizer_on_pumpkin and num_items(Items.Fertilizer) > fertilizer_min_stock:
				use_item(Items.Fertilizer)
		
		# 5. 處理未成熟的南瓜 - 使用肥料加速並感染
		elif status['entity'] == Entities.Pumpkin and not status['can_harvest']:
			if use_fertilizer_on_pumpkin and num_items(Items.Fertilizer) > fertilizer_min_stock:
				use_item(Items.Fertilizer)
		
		# 6. 南瓜區極限水分需求（優化：水分=1.0時生長速度5x）
		if status['water'] < 0.95:
			use_item(Items.Water)
	
	# 向日葵區處理
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
		
		# 3. 處理可收成的向日葵 - 優先收穫高花瓣數（5x能量）
		elif status['can_harvest']:
			# 優化：檢查花瓣數，優先收穫高花瓣數向日葵
			if status['entity'] == Entities.Sunflower:
				petals = measure()
				# 花瓣數 ≥13 時優先收穫（獲得5x能量）
				if petals >= 13:
					harvest()
					local_harvests += 1
					plant(Entities.Sunflower)
				# 花瓣數較低時也收穫（保持產出）
				elif petals >= 7:
					harvest()
					local_harvests += 1
					plant(Entities.Sunflower)
			else:
				harvest()
				local_harvests += 1
				plant(Entities.Sunflower)
		
		# 4. 處理空地 - 補種向日葵
		elif status['entity'] == None and status['ground'] == Grounds.Soil:
			plant(Entities.Sunflower)
		
		# 5. 向日葵區極限水分需求（優化：水分=1.0時生長速度5x）
		if status['water'] < 0.95:
			use_item(Items.Water)
	
	# 仙人掌區處理 - 怪異物質生產模式
	elif status['is_cactus_zone']:
		# 1. 處理草地 - 清理並準備種植
		if status['ground'] == Grounds.Grassland:
			if status['entity'] == Entities.Grass:
				harvest()
				local_harvests += 1
			till()
			plant(Entities.Cactus)
			# 種植後立即使用肥料感染
			if use_fertilizer_on_cactus and num_items(Items.Fertilizer) > fertilizer_min_stock:
				use_item(Items.Fertilizer)
		
		# 2. 處理可收成的仙人掌 - 直接採收（不排序，不連鎖）
		elif status['can_harvest']:
			# 直接採收，獲得 50% 仙人掌 + 50% Weird_Substance（如果感染）
			harvest()
			local_harvests += 1
			plant(Entities.Cactus)
			# 種植後立即使用肥料感染
			if use_fertilizer_on_cactus and num_items(Items.Fertilizer) > fertilizer_min_stock:
				use_item(Items.Fertilizer)
		
		# 3. 處理空地 - 補種仙人掌
		elif status['entity'] == None and status['ground'] == Grounds.Soil:
			plant(Entities.Cactus)
			# 種植後立即使用肥料感染
			if use_fertilizer_on_cactus and num_items(Items.Fertilizer) > fertilizer_min_stock:
				use_item(Items.Fertilizer)
		
		# 4. 處理未成熟的仙人掌 - 使用肥料加速並感染
		elif status['entity'] == Entities.Cactus and not status['can_harvest']:
			if use_fertilizer_on_cactus and num_items(Items.Fertilizer) > fertilizer_min_stock:
				use_item(Items.Fertilizer)
		
		# 5. 仙人掌區極限水分需求（優化：水分=1.0時生長速度5x）
		if status['water'] < 0.95:
			use_item(Items.Water)
	
	return local_harvests

# 仙人掌排序函數已移除 - 怪異物質模式不需要排序

# 縱向S型移動 (垂直S型) - 積極採收模式
def harvest_vertical_s():
	local_harvests = 0
	reset_position()
	
	# 處理起始位置
	harvests = smart_zone_processing(0, 0, True)
	local_harvests += harvests
	
	for x in range(farm_size):
		for y in range(farm_size):
			# 移動到下一個位置
			if y < farm_size - 1:
				if x % 2 == 0:
					move(North)  # 偶數列：從下到上
				else:
					move(South)  # 奇數列：從上到下
				
				# 移動後立即處理
				harvests = smart_zone_processing(x, y, True)
				local_harvests += harvests
		
		# 移動到下一列
		if x < farm_size - 1:
			move(East)
			# 移動後立即處理
			actual_x = get_pos_x()
			actual_y = get_pos_y()
			harvests = smart_zone_processing(actual_x, actual_y, True)
			local_harvests += harvests
			
			if (x + 1) % 2 == 0:
				while get_pos_y() > 0:
					move(South)
					# 移動後立即處理
					actual_x = get_pos_x()
					actual_y = get_pos_y()
					harvests = smart_zone_processing(actual_x, actual_y, True)
					local_harvests += harvests
			else:
				while get_pos_y() < farm_size - 1:
					move(North)
					# 移動後立即處理
					actual_x = get_pos_x()
					actual_y = get_pos_y()
					harvests = smart_zone_processing(actual_x, actual_y, True)
					local_harvests += harvests
	
	return local_harvests

# 橫向S型移動 (水平S型) - 積極採收模式
def harvest_horizontal_s():
	local_harvests = 0
	reset_position()
	
	# 處理起始位置
	harvests = smart_zone_processing(0, 0, False)
	local_harvests += harvests
	
	for y in range(farm_size):
		for x in range(farm_size):
			# 移動到下一個位置
			if x < farm_size - 1:
				if y % 2 == 0:
					move(East)  # 偶數行：從左到右
				else:
					move(West)  # 奇數行：從右到左
				
				# 移動後立即處理
				harvests = smart_zone_processing(x, y, False)
				local_harvests += harvests
		
		# 移動到下一行
		if y < farm_size - 1:
			move(North)
			# 移動後立即處理
			actual_x = get_pos_x()
			actual_y = get_pos_y()
			harvests = smart_zone_processing(actual_x, actual_y, False)
			local_harvests += harvests
			
			if (y + 1) % 2 == 0:
				while get_pos_x() > 0:
					move(West)
					# 移動後立即處理
					actual_x = get_pos_x()
					actual_y = get_pos_y()
					harvests = smart_zone_processing(actual_x, actual_y, False)
					local_harvests += harvests
			else:
				while get_pos_x() < farm_size - 1:
					move(East)
					# 移動後立即處理
					actual_x = get_pos_x()
					actual_y = get_pos_y()
					harvests = smart_zone_processing(actual_x, actual_y, False)
					local_harvests += harvests
	
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
			elif is_sunflower_zone(x, y) and current_water < 0.5:
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

# 主採收循環 - 怪異物質生產模式
while True:
	round_count += 1
	
	# 智能分區處理 (基於土地狀態判斷)
	# 遍歷所有區域，使用肥料感染植物，直接採收獲得 Weird_Substance
	total_harvests = smart_zone_harvest()
	harvest_count += total_harvests
	reset_position()
	
	# 不再需要仙人掌排序和連鎖採收
	# 直接在遍歷時採收感染的植物
	
	# 如果沒有收穫，等待生長（優化：減少等待時間）
	if total_harvests == 0:
		for i in range(2):
			do_a_flip()
	
	# 每10輪重置計數器並顯示 Weird_Substance 庫存
	if round_count % 10 == 0:
		harvest_count = 0
		# 可選：檢查 Weird_Substance 庫存
		# weird_count = num_items(Items.Weird_Substance)