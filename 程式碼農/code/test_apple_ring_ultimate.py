# test_apple_ring_ultimate.py - 終極環形策略

def reset_position():
    while get_pos_x() > 0:
        move(West)
    while get_pos_y() > 0:
        move(South)

farm_size = get_world_size()
total_tiles = farm_size * farm_size
min_cactus = 100

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
    
    # 關鍵策略：
    # 環形路徑的優勢是不會被尾巴卡住
    # 可以一直繞環，直到收集足夠多的蘋果
    
    apples_collected = 0
    target_apples = total_tiles - 10  # 目標：接近地圖大小
    stuck_count = 0
    max_stuck = 200
    
    # 持續繞環移動
    # 不管蘋果在哪裡，只要持續移動就會吃到
    while apples_collected < target_apples and stuck_count < max_stuck:
        # 走一圈完整的環
        # S型路徑
        for row in range(farm_size):
            # 橫向移動
            for col in range(farm_size - 1):
                if row % 2 == 0:
                    result = move(East)
                else:
                    result = move(West)
                
                if result:
                    apples_collected += 1
                    stuck_count = 0
                else:
                    stuck_count += 1
                
                if apples_collected >= target_apples or stuck_count >= max_stuck:
                    break
            
            if apples_collected >= target_apples or stuck_count >= max_stuck:
                break
            
            # 縱向移動
            if row < farm_size - 1:
                result = move(North)
                if result:
                    apples_collected += 1
                    stuck_count = 0
                else:
                    stuck_count += 1
        
        if apples_collected >= target_apples or stuck_count >= max_stuck:
            break
        
        # 回到起點（形成環）
        for i in range(farm_size - 1):
            result = move(South)
            if result:
                apples_collected += 1
                stuck_count = 0
            else:
                stuck_count += 1
            
            if apples_collected >= target_apples or stuck_count >= max_stuck:
                break
        
        # 完成一圈，繼續下一圈（不卸帽！）
    
    # 收集完成，卸下恐龍帽
    change_hat(Hats.Brown_Hat)
    
    # 收穫 apples_collected² 骨頭
    # 理想情況：474² ≈ 224,676 骨頭
    
    do_a_flip()

# 環形路徑的核心優勢：
# 1. 永遠不會被尾巴完全卡住
# 2. 可以持續繞環，增加遇到蘋果的機會
# 3. 即使某些位置暫時被尾巴擋住，繼續繞環就能繞過
# 4. 最終能收集接近地圖大小的蘋果數量
