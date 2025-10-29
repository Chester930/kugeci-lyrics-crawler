# test_cactus_harvest.py - 測試仙人掌採收狀態

def reset_position():
    while get_pos_x() > 0:
        move(West)
    while get_pos_y() > 0:
        move(South)

print("=== 仙人掌採收狀態測試 ===")
print("")

reset_position()

# 統計數據
total_cactus = 0
mature_cactus = 0
harvestable_cactus = 0
sorted_cactus = 0  # 綠色的（已排序）
unsorted_cactus = 0  # 棕色的（未排序）

# 大小分布
size_distribution = {}

print("掃描仙人掌區...")
print("")

# 遍歷仙人掌區
for x in range(6, 16):
    for y in range(6, 16):
        # 移動到指定位置
        while get_pos_x() < x:
            move(East)
        while get_pos_x() > x:
            move(West)
        while get_pos_y() < y:
            move(North)
        while get_pos_y() > y:
            move(South)
        
        # 檢查當前位置
        entity = get_entity_type()
        
        if entity == Entities.Cactus:
            total_cactus += 1
            
            # 檢查是否可收成
            if can_harvest():
                harvestable_cactus += 1
                mature_cactus += 1
                
                # 測量大小
                size = measure()
                if size in size_distribution:
                    size_distribution[size] += 1
                else:
                    size_distribution[size] = 1

print("=== 掃描結果 ===")
print("仙人掌總數:", total_cactus)
print("成熟仙人掌:", mature_cactus)
print("可採收仙人掌:", harvestable_cactus)
print("")

if len(size_distribution) > 0:
    print("大小分布:")
    for size in range(10):
        if size in size_distribution:
            count = size_distribution[size]
            print("  大小", size, ":", count, "個")
    print("")

# 檢查排序狀態
print("--- 排序狀態檢查 ---")
if total_cactus == 0:
    print("仙人掌區沒有仙人掌！請先種植。")
elif mature_cactus == 0:
    print("所有仙人掌都還在生長中，等待成熟...")
elif harvestable_cactus > 0:
    print("發現", harvestable_cactus, "個可採收的仙人掌！")
    print("")
    print("採收說明:")
    print("- 仙人掌需要完全排序才能連鎖採收")
    print("- 連鎖採收收益: n^2 個仙人掌")
    print("- 綠色 = 已排序，棕色 = 未排序")
    print("")
    print("建議：繼續執行排序直到所有仙人掌變綠色")
else:
    print("沒有可採收的仙人掌")

print("")
print("測試完成！")
