# test_apple_ring_perfect.py - 完美環形策略

def reset_position():
    while get_pos_x() > 0:
        move(West)
    while get_pos_y() > 0:
        move(South)

def walk_one_ring():
    # 走一圈環形路徑
    farm_size = get_world_size()
    
    # S型遍歷所有行
    for row in range(farm_size):
        for col in range(farm_size - 1):
            if row % 2 == 0:
                move(East)
            else:
                move(West)
        
        if row < farm_size - 1:
            move(North)
    
    # 回到起點（形成環）
    for i in range(farm_size - 1):
        move(South)

farm_size = get_world_size()
total_tiles = farm_size * farm_size
min_cactus = 1000

# 無限循環
while True:
    # 檢查仙人掌
    if num_items(Items.Cactus) < min_cactus:
        for i in range(50):
            do_a_flip()
        continue
    
    reset_position()
    
    # 裝備恐龍帽
    change_hat(Hats.Dinosaur_Hat)
    
    # 關鍵策略：持續繞環，讓尾巴填滿整個地圖
    # 目標：收集接近 484 個蘋果（整個地圖）
    
    apples_collected = 0
    target_apples = total_tiles - 10  # 留些緩衝
    
    # 持續繞環，直到達到目標
    while apples_collected < target_apples:
        # 走一圈環
        farm_size_local = get_world_size()
        
        # S型遍歷
        for row in range(farm_size_local):
            for col in range(farm_size_local - 1):
                if row % 2 == 0:
                    result = move(East)
                else:
                    result = move(West)
                
                if result:
                    apples_collected += 1
                
                # 達到目標，停止
                if apples_collected >= target_apples:
                    break
            
            if apples_collected >= target_apples:
                break
            
            if row < farm_size_local - 1:
                result = move(North)
                if result:
                    apples_collected += 1
        
        if apples_collected >= target_apples:
            break
        
        # 回到起點（完成一圈）
        for i in range(farm_size_local - 1):
            result = move(South)
            if result:
                apples_collected += 1
    
    # 現在尾巴已經填滿整個地圖
    # 卸下恐龍帽，收穫骨頭
    change_hat(Hats.Brown_Hat)
    
    # 獲得 484² = 234,256 骨頭！
    
    # 短暫等待後繼續下一輪
    do_a_flip()

# 這個策略：
# 1. 環形路徑確保不會卡住
# 2. 多圈繞行確保填滿整個地圖
# 3. 最大化尾巴長度（接近地圖極限）
# 4. 收穫最大骨頭數量
