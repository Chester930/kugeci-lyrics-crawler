# f1.py - 遊戲探索程式參考
# 詳細的探索表單請參考：探索表單.md

# 這是一個簡化版的探索程式，可以一次性執行所有檢查
# 建議使用探索表單.md 中的逐個問題進行探索

print("=== 程式碼農遊戲探索開始 ===")

# 基本狀態檢查
print("1. 基本狀態:")
print("   無人機位置: (" + str(get_pos_x()) + ", " + str(get_pos_y()) + ")")
print("   農場大小: " + str(get_world_size()))
print("   當前帽子: " + str(get_hat()))

# 地面狀態檢查
print("\n2. 地面狀態:")
print("   地面類型: " + str(get_ground()))
print("   水分等級: " + str(get_water()))

# 實體狀態檢查
print("\n3. 實體狀態:")
print("   實體類型: " + str(get_entity()))
print("   可以收穫: " + str(can_harvest()))

# 物品庫存檢查
print("\n4. 物品庫存:")
print("   乾草數量: " + str(num_items(Items.Hay)))
print("   木材數量: " + str(num_items(Items.Wood)))
print("   水桶數量: " + str(num_items(Items.Water)))

# 解鎖狀態檢查
print("\n5. 解鎖狀態:")
print("   變數解鎖: " + str(num_unlocked(Unlocks.Variables)))
print("   迴圈解鎖: " + str(num_unlocked(Unlocks.Loops)))
print("   函數解鎖: " + str(num_unlocked(Unlocks.Functions)))

print("\n=== 探索完成 ===")
print("請將結果回報給我，或使用探索表單.md 進行更詳細的探索")
