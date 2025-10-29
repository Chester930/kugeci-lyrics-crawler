# test_apple_spiral.py - 螺旋路徑，最大化蘋果收集

def reset_position():
    while get_pos_x() > 0:
        move(West)
    while get_pos_y() > 0:
        move(South)

farm_size = get_world_size()
min_cactus_threshold = 100

# 目標：吃滿整個地圖
target_tail_length = (farm_size * farm_size) - 10  # 留 10 格緩衝

# 無限循環
while True:
    # 檢查仙人掌
    cactus_available = num_items(Items.Cactus)
    if cactus_available < min_cactus_threshold:
        for wait in range(50):
            do_a_flip()
        continue
    
    current_target = target_tail_length
    if cactus_available < current_target:
        current_target = cactus_available
    
    reset_position()
    change_hat(Hats.Dinosaur_Hat)
    
    # 螺旋路徑移動
    apples_eaten = 0
    stuck_count = 0
    
    # 定義邊界
    min_x = 0
    max_x = farm_size - 1
    min_y = 0
    max_y = farm_size - 1
    
    # 當前方向：0=東, 1=北, 2=西, 3=南
    direction = 0
    
    while apples_eaten < current_target and stuck_count < 200:
        # 根據方向移動
        if direction == 0:
            # 向東移動
            result = move(East)
            if result:
                apples_eaten += 1
                stuck_count = 0
                # 如果到達右邊界，轉向北，縮小下邊界
                if get_pos_x() >= max_x:
                    direction = 1
                    min_y += 1
            else:
                stuck_count += 1
        
        elif direction == 1:
            # 向北移動
            result = move(North)
            if result:
                apples_eaten += 1
                stuck_count = 0
                # 如果到達上邊界，轉向西，縮小右邊界
                if get_pos_y() >= max_y:
                    direction = 2
                    max_x -= 1
            else:
                stuck_count += 1
        
        elif direction == 2:
            # 向西移動
            result = move(West)
            if result:
                apples_eaten += 1
                stuck_count = 0
                # 如果到達左邊界，轉向南，縮小上邊界
                if get_pos_x() <= min_x:
                    direction = 3
                    max_y -= 1
            else:
                stuck_count += 1
        
        elif direction == 3:
            # 向南移動
            result = move(South)
            if result:
                apples_eaten += 1
                stuck_count = 0
                # 如果到達下邊界，轉向東，縮小左邊界
                if get_pos_y() <= min_y:
                    direction = 0
                    min_x += 1
            else:
                stuck_count += 1
    
    change_hat(Hats.Brown_Hat)
    do_a_flip()

# 螺旋路徑優勢：
# - 尾巴在外圍，不阻擋內部
# - 理論上可以吃滿整個地圖
# - 22×22 = 484 個蘋果 → 484² = 234,256 骨頭！
