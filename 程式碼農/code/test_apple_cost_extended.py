# test_apple_cost_extended.py - 測試蘋果成本並獲得更多骨頭

def reset_position():
    while get_pos_x() > 0:
        move(West)
    while get_pos_y() > 0:
        move(South)

reset_position()

# 記錄初始數量
cactus_before = num_items(Items.Cactus)
bones_before = num_items(Items.Bone)

# 裝備恐龍帽
change_hat(Hats.Dinosaur_Hat)

# 目標：收集 10 個蘋果（獲得 10² = 100 個骨頭）
target_apples = 10
apples_eaten = 0

# S型移動收集蘋果
farm_size = get_world_size()

for x in range(farm_size):
    for y in range(farm_size - 1):
        # 根據列數決定移動方向
        if x % 2 == 0:
            result = move(North)
        else:
            result = move(South)
        
        # 如果移動失敗（被尾巴擋住），停止
        if not result:
            break
        
        apples_eaten += 1
        
        # 達到目標，停止
        if apples_eaten >= target_apples:
            break
    
    if apples_eaten >= target_apples:
        break
    
    # 移動到下一列
    if x < farm_size - 1:
        move(East)

# 卸下恐龍帽，收穫骨頭
change_hat(Hats.Brown_Hat)

# 計算結果
cactus_after = num_items(Items.Cactus)
bones_after = num_items(Items.Bone)

cactus_used = cactus_before - cactus_after
bones_gained = bones_after - bones_before

# 結果分析：
# 吃了多少蘋果 = apples_eaten
# 消耗仙人掌 = cactus_used
# 獲得骨頭 = bones_gained (應該是 apples_eaten²)
# 每個蘋果成本 = cactus_used / apples_eaten
