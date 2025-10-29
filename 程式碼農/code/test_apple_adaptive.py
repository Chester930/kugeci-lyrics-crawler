# test_apple_adaptive.py - 自適應長度，根據地圖大小動態調整

def reset_position():
    while get_pos_x() > 0:
        move(West)
    while get_pos_y() > 0:
        move(South)

# 無限循環配置
farm_size = get_world_size()
total_tiles = farm_size * farm_size

# 動態計算最佳長度
# 公式：使用 70% 的地圖空間
# 22×22 = 484 格 → 70% = 338 格
optimal_length = (total_tiles * 7) // 10

# 最小/最大限制
if optimal_length < 200:
    optimal_length = 200
if optimal_length > 450:
    optimal_length = 450

target_tail_length = optimal_length
min_cactus_threshold = 100

# 無限循環
while True:
    # 檢查仙人掌數量
    cactus_available = num_items(Items.Cactus)
    
    # 如果仙人掌不足，等待
    if cactus_available < min_cactus_threshold:
        for wait in range(50):
            do_a_flip()
        continue
    
    # 調整目標長度
    current_target = target_tail_length
    if cactus_available < current_target:
        current_target = cactus_available
    
    # 回到原點
    reset_position()
    
    # 裝備恐龍帽
    change_hat(Hats.Dinosaur_Hat)
    
    # S型移動收集蘋果
    apples_eaten = 0
    stuck_count = 0
    max_stuck = 200
    
    for x in range(farm_size):
        for y in range(farm_size - 1):
            if x % 2 == 0:
                result = move(North)
            else:
                result = move(South)
            
            if result:
                apples_eaten += 1
                stuck_count = 0
            else:
                stuck_count += 1
                if stuck_count >= max_stuck:
                    break
            
            if apples_eaten >= current_target:
                break
        
        if apples_eaten >= current_target or stuck_count >= max_stuck:
            break
        
        if x < farm_size - 1:
            result = move(East)
            if result:
                stuck_count = 0
            else:
                stuck_count += 1
                if stuck_count >= max_stuck:
                    break
    
    # 卸下恐龍帽
    change_hat(Hats.Brown_Hat)
    
    # 等待後繼續
    do_a_flip()

# 自動適應不同地圖大小：
# 10×10 (100 格) → 70 格 → 限制為 200 → 使用 200
# 22×22 (484 格) → 338 格 → 使用 338 ✅
# 30×30 (900 格) → 630 格 → 限制為 450 → 使用 450
