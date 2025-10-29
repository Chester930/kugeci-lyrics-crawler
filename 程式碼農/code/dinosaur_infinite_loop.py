# dinosaur_infinite_loop.py - 無限循環恐龍模式，最大化骨頭收集

def reset_position():
    while get_pos_x() > 0:
        move(West)
    while get_pos_y() > 0:
        move(South)

farm_size = get_world_size()

# 每次嘗試的目標長度
target_tail_length = 400

# 最小仙人掌門檻（低於此數量不執行）
min_cactus_threshold = 100

# 無限循環
while True:
    # 檢查仙人掌數量
    cactus_available = num_items(Items.Cactus)
    
    # 如果仙人掌不足，跳過這次
    if cactus_available < min_cactus_threshold:
        # 等待一段時間，讓主程式採收更多仙人掌
        for wait in range(100):
            do_a_flip()
        continue  # 繼續下一輪檢查
    
    # 調整目標長度（不超過可用仙人掌）
    current_target = target_tail_length
    if cactus_available < current_target:
        current_target = cactus_available
    
    # 回到原點
    reset_position()
    
    # 裝備恐龍帽
    change_hat(Hats.Dinosaur_Hat)
    
    # 開始收集蘋果
    apples_eaten = 0
    stuck_count = 0
    max_stuck = 200  # 非常寬容的失敗容忍
    
    # S型移動
    for x in range(farm_size):
        for y in range(farm_size - 1):
            # 根據列數決定移動方向
            if x % 2 == 0:
                result = move(North)
            else:
                result = move(South)
            
            if result:
                # 移動成功
                apples_eaten += 1
                stuck_count = 0
            else:
                # 移動失敗
                stuck_count += 1
                if stuck_count >= max_stuck:
                    break
            
            # 達到目標
            if apples_eaten >= current_target:
                break
        
        # 檢查是否結束
        if apples_eaten >= current_target or stuck_count >= max_stuck:
            break
        
        # 移動到下一列
        if x < farm_size - 1:
            result = move(East)
            if result:
                stuck_count = 0
            else:
                stuck_count += 1
                if stuck_count >= max_stuck:
                    break
    
    # 卸下恐龍帽，收穫骨頭
    change_hat(Hats.Brown_Hat)
    
    # 這一輪完成
    # 獲得 apples_eaten² 個骨頭
    # 無論成功或失敗，都會重新開始下一輪
    
    # 短暫等待後繼續（避免太快重複）
    do_a_flip()

# 這個程式永遠不會結束
# 會持續：檢查仙人掌 → 收集蘋果 → 收穫骨頭 → 重複
