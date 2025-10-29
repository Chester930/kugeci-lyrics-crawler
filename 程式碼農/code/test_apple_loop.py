# test_apple_ring_400_cycles.py - 400圈哈密頓迴路策略（32×32地圖配置）
# 針對32×32地圖優化：
# - 總格數：1024 格
# - 哈密頓路徑長度：1024 步/圈
# - 400 圈 = 409,600 步
# - 預期尾巴長度：接近 1024（滿地圖）

def reset_position():
	while get_pos_x() > 0:
		move(West)
	while get_pos_y() > 0:
		move(South)

def generate_hamiltonian_path():
	farm_size = get_world_size()
	path = []
	
	# 先從 (0,0) 移動到 (1,0)
	path.append(East)
	
	# S 型路徑（之字形），從第二列開始
	for row in range(farm_size):
		if row % 2 == 0:
			# 偶數行：向東走（從 x=1 到 x=farm_size-1）
			for col in range(farm_size - 2):
				path.append(East)
		else:
			# 奇數行：向西走（從 x=farm_size-1 到 x=1）
			for col in range(farm_size - 2):
				path.append(West)
		
		# 除了最後一行，都要向北移動
		if row < farm_size - 1:
			path.append(North)
	
	# 從 (1, farm_size-1) 回到 (0, farm_size-1)
	path.append(West)
	
	# 從 (0, farm_size-1) 向南走回 (0, 0)
	for i in range(farm_size - 1):
		path.append(South)
	
	return path

def walk_cycles(num_cycles):
	path = generate_hamiltonian_path()
	total_apples = 0
	
	for cycle in range(num_cycles):
		for direction in path:
			result = move(direction)
			if result:
				total_apples += 1
	
	return total_apples

# ===== 主程式 =====

farm_size = get_world_size()  # 應該是 32
total_tiles = farm_size * farm_size  # 32×32 = 1024 格
min_cactus = 2000  # 32×32 地圖需要更多仙人掌（原 1000 → 2000）
CYCLES_TO_WALK = 1000  # 增加循環次數以填滿更大的地圖（原 400 → 600）

# 無限循環
while True:
	# 檢查仙人掌庫存
	if num_items(Items.Cactus) < min_cactus:
		for i in range(50):
			do_a_flip()
		continue
	
	# 回到起點
	reset_position()
	
	# 裝備恐龍帽開始收集
	change_hat(Hats.Dinosaur_Hat)
	
	# 持續繞行400圈
	apples_collected = walk_cycles(CYCLES_TO_WALK)
	
	# 換回普通帽子，收穫骨頭
	change_hat(Hats.Brown_Hat)
	
	# 短暫等待後繼續下一輪
	do_a_flip()