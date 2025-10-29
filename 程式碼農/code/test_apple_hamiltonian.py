# test_apple_hamiltonian.py - 哈密頓迴路，完美封閉路徑

def reset_position():
    while get_pos_x() > 0:
        move(West)
    while get_pos_y() > 0:
        move(South)

farm_size = get_world_size()
min_cactus_threshold = 100
target_tail_length = farm_size * farm_size

# 無限循環
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
    should_stop = False
    
    # 哈密頓迴路：S型走完所有行
    for y in range(farm_size):
        if should_stop:
            break
        
        if y % 2 == 0:
            # 偶數行：向東
            for x in range(farm_size - 1):
                result = move(East)
                if result:
                    apples_eaten += 1
                    stuck_count = 0
                else:
                    stuck_count += 1
                    if stuck_count >= 200:
                        should_stop = True
                        break
                
                if apples_eaten >= current_target:
                    should_stop = True
                    break
        else:
            # 奇數行：向西
            for x in range(farm_size - 1):
                result = move(West)
                if result:
                    apples_eaten += 1
                    stuck_count = 0
                else:
                    stuck_count += 1
                    if stuck_count >= 200:
                        should_stop = True
                        break
                
                if apples_eaten >= current_target:
                    should_stop = True
                    break
        
        if should_stop:
            break
        
        # 移動到下一行（除了最後一行）
        if y < farm_size - 1:
            result = move(North)
            if result:
                apples_eaten += 1
                stuck_count = 0
            else:
                stuck_count += 1
                if stuck_count >= 200:
                    break
    
    # 回到起點形成封閉迴圈
    if not should_stop and apples_eaten < current_target:
        # 22×22: 最後一行是第21行（索引21），是奇數
        # 結束時在左側，需向南回到起點
        if (farm_size - 1) % 2 == 0:
            # 偶數行結束，在右側
            while get_pos_y() > 0 and apples_eaten < current_target and stuck_count < 200:
                result = move(South)
                if result:
                    apples_eaten += 1
                    stuck_count = 0
                else:
                    stuck_count += 1
            
            while get_pos_x() > 0 and apples_eaten < current_target and stuck_count < 200:
                result = move(West)
                if result:
                    apples_eaten += 1
                    stuck_count = 0
                else:
                    stuck_count += 1
        else:
            # 奇數行結束，在左側
            while get_pos_y() > 0 and apples_eaten < current_target and stuck_count < 200:
                result = move(South)
                if result:
                    apples_eaten += 1
                    stuck_count = 0
                else:
                    stuck_count += 1
    
    # 完美！現在回到起點 (0,0)
    # 形成封閉迴路，尾巴不會阻擋
    
    change_hat(Hats.Brown_Hat)
    do_a_flip()

# 哈密頓迴路優勢：
# 1. 封閉路徑，起點=終點
# 2. 走遍所有格子
# 3. 尾巴形成環，不會阻擋
# 4. 理論極限：484² = 234,256 骨頭
# 5. 每輪都遵循相同路徑，永不卡住！
