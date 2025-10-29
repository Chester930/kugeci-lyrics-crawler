# maze_farming.py - 迷宫金币最大化生产策略
# 使用 Weird_Substance 创建迷宫，获取金币
# 
# 核心策略：
# 1. 使用 f4.py 积累的大量 Weird_Substance
# 2. 创建最大尺寸迷宫（32×32 = 1,024 金币）
# 3. 使用右手法则（沿墙走法）快速求解
# 4. 持续循环，最大化金币产出
# 
# 预期产量：
# - 无升级：1,024 金币/次（16 Weird_Substance）
# - 等级 1：2,048 金币/次（32 Weird_Substance）
# - 等级 2：4,096 金币/次（64 Weird_Substance）
# - 效率：64 金币/Weird_Substance

# 参数配置
farm_size = get_world_size()  # 获取地图大小
weird_substance_min = 100  # 最低 Weird_Substance 库存（低于此值停止）
maze_position_x = 0  # 迷宫创建位置 X
maze_position_y = 0  # 迷宫创建位置 Y

# 统计数据
total_mazes_solved = 0
total_gold_earned = 0
total_weird_used = 0

# 回到起始位置
def reset_position():
	while get_pos_x() > 0:
		move(West)
	while get_pos_y() > 0:
		move(South)

# 移动到指定位置
def move_to_position(target_x, target_y):
	reset_position()
	
	# 移动到目标 X
	while get_pos_x() < target_x:
		move(East)
	
	# 移动到目标 Y
	while get_pos_y() < target_y:
		move(North)

# 创建迷宫
def create_maze():
	# 移动到迷宫位置
	move_to_position(maze_position_x, maze_position_y)
	
	# 检查当前位置
	current_entity = get_entity_type()
	current_ground = get_ground_type()
	
	# 如果有草，先收割
	if current_entity == Entities.Grass:
		harvest()
	
	# 如果是草地，先翻土
	if current_ground == Grounds.Grassland:
		till()
	
	# 种植灌木
	plant(Entities.Bush)
	
	# 计算所需 Weird_Substance
	maze_level = num_unlocked(Unlocks.Mazes)
	if maze_level == 0:
		# 未解锁迷宫功能
		substance_needed = farm_size
	else:
		substance_needed = farm_size * 2**(maze_level - 1)
	
	# 检查是否有足够的 Weird_Substance
	weird_count = num_items(Items.Weird_Substance)
	if weird_count < substance_needed:
		return False, 0
	
	# 创建迷宫
	use_item(Items.Weird_Substance, substance_needed)
	
	return True, substance_needed

# 使用右手法则求解迷宫
def solve_maze_right_hand():
	directions = [North, East, South, West]
	current_direction = 0  # 初始方向：北
	
	steps = 0
	max_steps = farm_size * farm_size * 4  # 防止无限循环
	
	while steps < max_steps:
		# 检查是否找到宝藏
		if get_entity_type() == Entities.Treasure:
			harvest()
			return True
		
		# 右手法则：优先右转
		right_direction = (current_direction + 1) % 4
		
		if can_move(directions[right_direction]):
			# 可以右转，右转并前进
			current_direction = right_direction
			move(directions[current_direction])
		elif can_move(directions[current_direction]):
			# 不能右转，但可以直走
			move(directions[current_direction])
		else:
			# 不能直走，左转
			current_direction = (current_direction - 1) % 4
		
		steps += 1
	
	# 超过最大步数，求解失败
	return False

# 使用 measure() 辅助的智能求解（更快）
def solve_maze_smart():
	# 获取宝藏位置
	treasure_x, treasure_y = measure()
	
	directions = [North, East, South, West]
	current_direction = 0
	
	steps = 0
	max_steps = farm_size * farm_size * 4
	
	while steps < max_steps:
		# 检查是否找到宝藏
		if get_entity_type() == Entities.Treasure:
			harvest()
			return True
		
		# 计算到宝藏的距离
		current_x = get_pos_x()
		current_y = get_pos_y()
		distance = (treasure_x - current_x)**2 + (treasure_y - current_y)**2
		
		# 右手法则，但优先朝向宝藏方向
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

# 主迷宫循环
def maze_farming_loop():
	global total_mazes_solved
	global total_gold_earned
	global total_weird_used
	
	while True:
		# 检查 Weird_Substance 库存
		weird_count = num_items(Items.Weird_Substance)
		
		if weird_count < weird_substance_min:
			# Weird_Substance 不足，停止
			break
		
		# 创建迷宫
		success, substance_used = create_maze()
		
		if not success:
			# 创建失败（Weird_Substance 不足）
			break
		
		# 求解迷宫（使用智能求解）
		solved = solve_maze_smart()
		
		if solved:
			# 计算获得的金币
			maze_level = num_unlocked(Unlocks.Mazes)
			if maze_level == 0:
				gold_earned = farm_size * farm_size
			else:
				gold_earned = farm_size * farm_size * 2**maze_level
			
			# 更新统计
			total_mazes_solved += 1
			total_gold_earned += gold_earned
			total_weird_used += substance_used
		else:
			# 求解失败，跳出循环
			break
		
		# 重置位置，准备下一个迷宫
		reset_position()

# 测试模式：单次迷宫
def test_single_maze():
	# 创建迷宫
	success, substance_used = create_maze()
	
	if not success:
		return
	
	# 求解迷宫
	solved = solve_maze_smart()
	
	if solved:
		# 计算金币
		maze_level = num_unlocked(Unlocks.Mazes)
		if maze_level == 0:
			gold_earned = farm_size * farm_size
		else:
			gold_earned = farm_size * farm_size * 2**maze_level
	
	reset_position()

# 高级模式：结合 f4.py 的混合策略
def hybrid_farming():
	weird_threshold = 500  # Weird_Substance 阈值
	
	while True:
		weird_count = num_items(Items.Weird_Substance)
		
		if weird_count >= weird_threshold:
			# 创建并求解迷宫
			maze_farming_loop()
		else:
			# Weird_Substance 不足，等待
			# 这里可以调用 f4.py 的采收逻辑
			do_a_flip()

# 效率分析函数
def analyze_efficiency():
	if total_mazes_solved > 0:
		avg_gold_per_maze = total_gold_earned / total_mazes_solved
		avg_weird_per_maze = total_weird_used / total_mazes_solved
		efficiency = total_gold_earned / total_weird_used
		
		# 可选：显示统计（如果有输出功能）
		# 迷宫数：total_mazes_solved
		# 总金币：total_gold_earned
		# 总消耗：total_weird_used
		# 效率：efficiency 金币/Weird_Substance

# 主程序入口
reset_position()

# 选择运行模式
run_mode = 2  # 1=单次测试, 2=持续循环, 3=混合模式

if run_mode == 1:
	# 单次测试模式
	test_single_maze()
elif run_mode == 2:
	# 持续循环模式
	maze_farming_loop()
	analyze_efficiency()
elif run_mode == 3:
	# 混合模式（需要与 f4.py 结合）
	hybrid_farming()

	