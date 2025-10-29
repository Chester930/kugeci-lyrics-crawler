# test_apple_gradual.py - 漸進式測試最大長度

def reset_position():
    while get_pos_x() > 0:
        move(West)
    while get_pos_y() > 0:
        move(South)

# 漸進式測試：從小到大找出最大可行長度
test_lengths = [50, 100, 150, 200, 250, 300]
farm_size = get_world_size()

for test_length in test_lengths:
    # 檢查仙人掌是否足夠
    if num_items(Items.Cactus) < test_length:
        break  # 仙人掌不足，停止測試
    
    # 記錄初始骨頭數量
    bones_before = num_items(Items.Bone)
    
    reset_position()
    
    # 裝備恐龍帽
    change_hat(Hats.Dinosaur_Hat)
    
    # 嘗試收集指定長度
    apples_eaten = 0
    move_failed_count = 0
    success = True
    
    for x in range(farm_size):
        for y in range(farm_size - 1):
            if x % 2 == 0:
                result = move(North)
            else:
                result = move(South)
            
            if not result:
                move_failed_count += 1
                if move_failed_count >= 5:
                    # 失敗，被尾巴困住
                    success = False
                    break
            else:
                move_failed_count = 0
                apples_eaten += 1
            
            if apples_eaten >= test_length:
                break
        
        if apples_eaten >= test_length or not success:
            break
        
        if x < farm_size - 1:
            result = move(East)
            if not result:
                move_failed_count += 1
                if move_failed_count >= 5:
                    success = False
                    break
            else:
                move_failed_count = 0
    
    # 卸下恐龍帽
    change_hat(Hats.Brown_Hat)
    
    # 檢查結果
    bones_after = num_items(Items.Bone)
    bones_gained = bones_after - bones_before
    
    # 如果這次失敗，不再嘗試更長的
    if not success or apples_eaten < test_length * 0.8:
        # 失敗或只完成不到 80%
        break
    
    # 這個長度成功！繼續測試更長的

# 測試完成
# 最後成功的 test_length 就是最大可行長度
# 查看背包中的骨頭數量，計算實際收益
