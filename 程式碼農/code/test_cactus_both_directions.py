# test_cactus_both_directions.py - 測試兩種S型移動的仙人掌交換

def reset_position():
    while get_pos_x() > 0:
        move(West)
    while get_pos_y() > 0:
        move(South)

print("=== 測試兩種S型移動的仙人掌交換 ===")
print("")

# 測試1: 橫向移動 - 檢查北方仙人掌
print("--- 測試1: 橫向移動 (先x後y) 檢查北方 ---")
reset_position()
horizontal_swap_count = 0

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
        
        # 檢查當前位置是否有仙人掌
        if get_entity_type() == Entities.Cactus:
            current_size = measure()
            
            # 橫向移動：檢查北方仙人掌
            if y < 15:
                north_size = measure(North)
                # 若本體比較大，則交換位置
                if north_size != None and current_size > north_size:
                    print("橫向交換: (", x, ",", y, ") 當前:", current_size, " <-> 北方:", north_size)
                    swap(North)
                    horizontal_swap_count += 1

print("橫向交換次數:", horizontal_swap_count)
print("")

# 等待一下，讓用戶看清楚
for i in range(3):
    do_a_flip()

# 測試2: 縱向移動 - 檢查東方仙人掌
print("--- 測試2: 縱向移動 (先y後x) 檢查東方 ---")
reset_position()
vertical_swap_count = 0

for y in range(6, 16):
    for x in range(6, 16):
        # 移動到指定位置
        while get_pos_x() < x:
            move(East)
        while get_pos_x() > x:
            move(West)
        while get_pos_y() < y:
            move(North)
        while get_pos_y() > y:
            move(South)
        
        # 檢查當前位置是否有仙人掌
        if get_entity_type() == Entities.Cactus:
            current_size = measure()
            
            # 縱向移動：檢查東方仙人掌
            if x < 15:
                east_size = measure(East)
                # 若本體比較大，則交換位置
                if east_size != None and current_size > east_size:
                    print("縱向交換: (", x, ",", y, ") 當前:", current_size, " <-> 東方:", east_size)
                    swap(East)
                    vertical_swap_count += 1

print("縱向交換次數:", vertical_swap_count)
print("")

# 總結
print("=== 測試結果總結 ===")
print("橫向移動交換次數:", horizontal_swap_count)
print("縱向移動交換次數:", vertical_swap_count)
print("總交換次數:", horizontal_swap_count + vertical_swap_count)
print("")

if horizontal_swap_count > 0 or vertical_swap_count > 0:
    print("兩種S型移動都能正確執行交換！")
    print("")
    print("排序邏輯:")
    print("- 橫向移動: 檢查北方，若本體>北方則交換 (大的往北推)")
    print("- 縱向移動: 檢查東方，若本體>東方則交換 (大的往東推)")
    print("- 目標: 右上角最大，左下角最小")
else:
    print("目前沒有需要交換的仙人掌")
    print("可能已經排序完成或仙人掌未成熟")

print("")
print("測試完成！")
