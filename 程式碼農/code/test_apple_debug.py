# test_apple_debug.py - 診斷恐龍模式停止原因

def reset_position():
    while get_pos_x() > 0:
        move(West)
    while get_pos_y() > 0:
        move(South)

# 記錄初始狀態
farm_size = get_world_size()
cactus_before = num_items(Items.Cactus)
bones_before = num_items(Items.Bone)

# 目標長度（較小，用於測試）
target_tail_length = 50  # 先測試小長度

reset_position()

# 裝備恐龍帽
change_hat(Hats.Dinosaur_Hat)

# 開始收集
apples_eaten = 0
move_failed_count = 0
last_successful_pos = (0, 0)

for x in range(farm_size):
    for y in range(farm_size - 1):
        # 記錄當前位置
        current_x = get_pos_x()
        current_y = get_pos_y()
        
        # 嘗試移動
        if x % 2 == 0:
            result = move(North)
        else:
            result = move(South)
        
        # 檢查移動結果
        if not result:
            # 移動失敗
            move_failed_count += 1
            
            # 如果連續失敗 3 次，可能被困住
            if move_failed_count >= 3:
                # 記錄停止位置
                stop_x = get_pos_x()
                stop_y = get_pos_y()
                
                # 卸下帽子
                change_hat(Hats.Brown_Hat)
                
                # 檢查最終狀態
                cactus_after = num_items(Items.Cactus)
                bones_after = num_items(Items.Bone)
                
                # 結果分析：
                # apples_eaten = 實際吃到的蘋果數
                # stop_x, stop_y = 停止位置
                # cactus_before - cactus_after = 消耗的仙人掌
                # bones_after - bones_before = 獲得的骨頭（應該是 apples_eaten²）
                # move_failed_count = 移動失敗次數
                
                # 停止執行
                break
        else:
            # 移動成功
            move_failed_count = 0
            apples_eaten += 1
            last_successful_pos = (current_x, current_y)
        
        # 達到目標
        if apples_eaten >= target_tail_length:
            # 正常完成
            change_hat(Hats.Brown_Hat)
            
            cactus_after = num_items(Items.Cactus)
            bones_after = num_items(Items.Bone)
            
            # 成功完成
            break
    
    # 檢查是否已結束
    if apples_eaten >= target_tail_length or move_failed_count >= 3:
        break
    
    # 移動到下一列
    if x < farm_size - 1:
        result = move(East)
        if not result:
            # 向東移動失敗
            move_failed_count += 1
            if move_failed_count >= 3:
                change_hat(Hats.Brown_Hat)
                break

# 如果還沒卸下帽子，現在卸下
if get_hat() == Hats.Dinosaur_Hat:
    change_hat(Hats.Brown_Hat)

# 最終結果會顯示在背包中
# 檢查：
# - 骨頭數量變化 = 實際收益
# - 仙人掌數量變化 = 實際消耗
# - 如果 apples_eaten < target_tail_length，說明提前停止了
