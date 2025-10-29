# dinosaur_max_bones.py - 最大化骨頭收集策略

def reset_position():
    while get_pos_x() > 0:
        move(West)
    while get_pos_y() > 0:
        move(South)

# 計算農場可用空間
farm_size = get_world_size()
total_tiles = farm_size * farm_size

# 統計當前空地數量（已翻土的區域）
reset_position()
empty_tiles = 0
for x in range(farm_size):
    for y in range(farm_size):
        while get_pos_x() < x:
            move(East)
        while get_pos_x() > x:
            move(West)
        while get_pos_y() < y:
            move(North)
        while get_pos_y() > y:
            move(South)
        
        if get_entity_type() == None:
            empty_tiles += 1

# 計算最佳尾巴長度
# 保守估計：使用 70% 的空地（避免被自己尾巴卡住）
max_safe_length = (empty_tiles * 7) // 10  # 等同於 70%

# 如果農場很大，限制在合理範圍
if max_safe_length > 400:
    max_safe_length = 400  # 避免太長導致時間過久

# 計算可以執行幾輪
cactus_available = num_items(Items.Cactus)
rounds_possible = cactus_available // max_safe_length

# 如果仙人掌不足一輪，降低長度
if rounds_possible == 0:
    max_safe_length = cactus_available
    rounds_possible = 1

# 設定參數
target_tail_length = max_safe_length
total_rounds = rounds_possible

# 開始執行
reset_position()

for round_num in range(total_rounds):
    reset_position()
    
    # 檢查仙人掌是否足夠
    if num_items(Items.Cactus) < target_tail_length:
        break
    
    # 裝備恐龍帽
    change_hat(Hats.Dinosaur_Hat)
    
    # S型移動收集蘋果
    apples_eaten = 0
    
    for x in range(farm_size):
        for y in range(farm_size - 1):
            # 根據列數決定移動方向
            if x % 2 == 0:
                result = move(North)
            else:
                result = move(South)
            
            # 如果移動失敗（被尾巴擋住），說明已經達到極限
            if not result:
                # 提前結束這輪
                break
            
            apples_eaten += 1
            
            # 達到目標長度
            if apples_eaten >= target_tail_length:
                break
        
        # 完成目標或被擋住，跳出外層循環
        if apples_eaten >= target_tail_length or not result:
            break
        
        # 移動到下一列
        if x < farm_size - 1:
            result = move(East)
            if not result:
                break

    # 卸下恐龍帽，收穫骨頭
    change_hat(Hats.Brown_Hat)
    
    # 這一輪結束
    # 實際獲得：apples_eaten² 個骨頭

# 執行完畢
# 預期總骨頭：rounds × target_tail_length²
# 實際骨頭：查看背包中的 Items.Bone
