# test_apple_cost.py - 測試蘋果的仙人掌成本

def reset_position():
    while get_pos_x() > 0:
        move(West)
    while get_pos_y() > 0:
        move(South)

reset_position()

# 記錄初始仙人掌數量
cactus_before = num_items(Items.Cactus)

# 裝備恐龍帽
change_hat(Hats.Dinosaur_Hat)

# 等待第一個蘋果生成（在無人機下方）
# 蘋果會自動生成，無需手動操作

# 檢查仙人掌數量變化
cactus_after = num_items(Items.Cactus)
cactus_used = cactus_before - cactus_after

# 移動一步，吃掉蘋果
move(East)

# 等待第二個蘋果生成（隨機位置）
# 檢查仙人掌數量變化
cactus_after_2 = num_items(Items.Cactus)
cactus_used_2 = cactus_after - cactus_after_2

# 卸下恐龍帽
change_hat(Hats.Brown_Hat)

# 結果會顯示在背包的仙人掌和骨頭數量變化中
# 第一個蘋果成本 = cactus_used
# 第二個蘋果成本 = cactus_used_2
# 收穫骨頭 = 1² = 1 個骨頭
