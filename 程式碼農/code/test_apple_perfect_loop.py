# test_apple_perfect_loop.py - 完美封閉迴路，永不卡住

def reset_position():
    while get_pos_x() > 0:
        move(West)
    while get_pos_y() > 0:
        move(South)

farm_size = get_world_size()
min_cactus_threshold = 100

# 目標：整個地圖（484格）
# 但實際上我們會一直移動，讓程式自然達到極限
target_tail_length = farm_size * farm_size

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
    
    # 回到起點 (0,0)
    reset_position()
    
    # 裝備恐龍帽
    change_hat(Hats.Dinosaur_Hat)
    
    # 完美封閉迴路：遍歷所有格子，最後回到起點
    apples_eaten = 0
    stuck_count = 0
    
    # 第一階段：S型走完所有行（除了最後回程）
    for y in range(farm_size):
        # 最後一行特殊處理
        if y == farm_size - 1:
            # 最後一行：向東走到 (21, 21)
            for x in range(farm_size - 1):
                result = move(East)
                if result:
                    apples_eaten += 1
                    stuck_count = 0
                else:
                    stuck_count += 1
                    if stuck_count >= 200:
                        break
                
                if apples_eaten >= current_target:
                    break
        else:
            # 普通行
            if y % 2 == 0:
                # 偶數行：向東走到底
                for x in range(farm_size - 1):
                    result = move(East)
                    if result:
                        apples_eaten += 1
                        stuck_count = 0
                    else:
                        stuck_count += 1
                        if stuck_count >= 200:
                            break
                    
                    if apples_eaten >= current_target:
                        break
                
                # 向北移動到下一行
                if apples_eaten < current_target and stuck_count < 200:
                    result = move(North)
                    if result:
                        apples_eaten += 1
                        stuck_count = 0
                    else:
                        stuck_count += 1
            else:
                # 奇數行：向西走到底
                for x in range(farm_size - 1):
                    result = move(West)
                    if result:
                        apples_eaten += 1
                        stuck_count = 0
                    else:
                        stuck_count += 1
                        if stuck_count >= 200:
                            break
                    
                    if apples_eaten >= current_target:
                        break
                
                # 向北移動到下一行
                if apples_eaten < current_target and stuck_count < 200:
                    result = move(North)
                    if result:
                        apples_eaten += 1
                        stuck_count = 0
                    else:
                        stuck_count += 1
        
        if apples_eaten >= current_target or stuck_count >= 200:
            break
    
    # 第二階段：從 (21, 21) 回到 (0, 0)
    # 沿著右邊緣向下，再沿著底邊向左
    if apples_eaten < current_target and stuck_count < 200:
        # 向南走到底
        while get_pos_y() > 0 and apples_eaten < current_target and stuck_count < 200:
            result = move(South)
            if result:
                apples_eaten += 1
                stuck_count = 0
            else:
                stuck_count += 1
                if stuck_count >= 200:
                    break
        
        # 向西走回起點
        while get_pos_x() > 0 and apples_eaten < current_target and stuck_count < 200:
            result = move(West)
            if result:
                apples_eaten += 1
                stuck_count = 0
            else:
                stuck_count += 1
                if stuck_count >= 200:
                    break
    
    # 現在回到起點 (0,0)，形成完美迴圈！
    # 卸下恐龍帽，收穫骨頭
    change_hat(Hats.Brown_Hat)
    
    # 短暫等待後繼續下一輪
    do_a_flip()

# 完美封閉迴路：
# - 走遍所有 484 格
# - 回到起點
# - 尾巴形成封閉迴圈
# - 理論收益：484² = 234,256 骨頭/輪！
# - 實際上，尾巴會在路徑上，所以收集到的會稍少
# - 但比 S 型的 350 好很多！
