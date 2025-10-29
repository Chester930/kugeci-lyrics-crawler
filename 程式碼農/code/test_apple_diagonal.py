# test_apple_diagonal.py - 對角線填充路徑

def reset_position():
    while get_pos_x() > 0:
        move(West)
    while get_pos_y() > 0:
        move(South)

farm_size = get_world_size()
min_cactus_threshold = 100
target_tail_length = (farm_size * farm_size) - 10

while True:
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
    
    apples_eaten = 0
    stuck_count = 0
    
    # 對角線填充：從左下角開始
    # 每條對角線從下到上
    
    for diagonal in range(farm_size * 2 - 1):
        # 確定這條對角線的起點
        if diagonal < farm_size:
            start_x = 0
            start_y = diagonal
        else:
            start_x = diagonal - farm_size + 1
            start_y = farm_size - 1
        
        # 沿對角線移動
        x = start_x
        y = start_y
        
        while x < farm_size and y >= 0:
            if apples_eaten >= current_target or stuck_count >= 200:
                break
            
            # 移動到目標位置
            current_x = get_pos_x()
            current_y = get_pos_y()
            
            # 先調整 x
            while current_x < x and stuck_count < 200:
                result = move(East)
                if result:
                    apples_eaten += 1
                    stuck_count = 0
                    current_x = get_pos_x()
                else:
                    stuck_count += 1
            
            # 再調整 y
            while current_y < y and stuck_count < 200:
                result = move(North)
                if result:
                    apples_eaten += 1
                    stuck_count = 0
                    current_y = get_pos_y()
                else:
                    stuck_count += 1
            
            while current_y > y and stuck_count < 200:
                result = move(South)
                if result:
                    apples_eaten += 1
                    stuck_count = 0
                    current_y = get_pos_y()
                else:
                    stuck_count += 1
            
            # 移動到下一個對角線位置
            x += 1
            y -= 1
        
        if apples_eaten >= current_target or stuck_count >= 200:
            break
    
    change_hat(Hats.Brown_Hat)
    do_a_flip()

# 對角線路徑：
# - 尾巴在後方對角線
# - 不會阻擋前方移動
# - 可以覆蓋整個地圖
